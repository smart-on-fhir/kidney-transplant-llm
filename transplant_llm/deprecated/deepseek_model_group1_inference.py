import os
import json
import signal
import csv
import re
from pathlib import Path
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import logging
from datetime import datetime

from tenacity import retry, wait_random_exponential, stop_after_attempt
from tqdm import tqdm
from pydantic import BaseModel, Field
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    pipeline,
    BitsAndBytesConfig
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TIME_LIMIT = 300
BATCH_SIZE = 1
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

# Model setup
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto"
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    batch_size=BATCH_SIZE
)

# Pydantic models
class ReasoningElement(BaseModel):
    boolean: Optional[bool] = None
    value: Optional[str] = None
    spans: List[str] = Field(default_factory=list)

class TransplantAnalysis(BaseModel):
    filename: str
    transplant_date: Optional[ReasoningElement] = None
    donor_type: Optional[ReasoningElement] = None
    donor_relatedness: Optional[ReasoningElement] = None
    hla_match: Optional[ReasoningElement] = None
    error: Optional[str] = None

def timeout_handler(signum, frame):
    raise TimeoutError(f"Processing timed out after {TIME_LIMIT} seconds")

@lru_cache(maxsize=100)
def build_mistral_prompt(file_content: str) -> str:
    messages = [
        {"role": "system", "content": (
            "You are a helpful assistant that extracts kidney transplant information from medical notes.\n"
            "Return ONLY a JSON object in the exact format:\n"
            "{\n"
            "  \"transplant_date\": {\"boolean\": true/false/null, \"value\": \"\", \"spans\": [] },\n"
            "  \"donor_type\": {\"boolean\": true/false/null, \"value\": \"\", \"spans\": [] },\n"
            "  \"donor_relatedness\": {\"boolean\": true/false/null, \"value\": \"\", \"spans\": [] },\n"
            "  \"hla_match\": {\"boolean\": true/false/null, \"value\": \"\", \"spans\": [] }\n"
            "}\n"
            "Do NOT include any explanation or extra text."
        )},
        {"role": "user", "content": (
            "Extract the following from the medical note:\n"
            "1. Kidney transplant date\n"
            "2. Donor type (Living/Deceased/Not mentioned)\n"
            "3. Donor relatedness (Related/Unrelated/Not mentioned)\n"
            "4. HLA match (Zero mismatch/Good match/Poor match/Not mentioned)\n\n"
            f"Medical note: {file_content}"
        )}
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

def extract_json_from_response(response: str) -> Optional[str]:
    json_match = re.search(r"```(?:json)?\s*({.*?})\s*```", response, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()
    try:
        stack = []
        start = -1
        for i, c in enumerate(response):
            if c == '{':
                if not stack:
                    start = i
                stack.append(c)
            elif c == '}':
                if stack:
                    stack.pop()
                    if not stack and start != -1:
                        candidate = response[start:i+1].strip()
                        if 'transplant_date' in candidate:
                            return candidate
    except Exception:
        pass
    return None

def clean_json_string(json_str: str) -> str:
    json_str = json_str.replace("'", '"')
    json_str = re.sub(r'\bTrue\b', 'true', json_str, flags=re.IGNORECASE)
    json_str = re.sub(r'\bFalse\b', 'false', json_str, flags=re.IGNORECASE)
    json_str = re.sub(r'\bNone\b', 'null', json_str, flags=re.IGNORECASE)
    json_str = re.sub(r'[-\x1f\x7f-\x9f]', '', json_str)
    return json_str.strip()

def process_output(raw_result: str, filename: str) -> TransplantAnalysis:
    try:
        json_str = extract_json_from_response(raw_result)
        if not json_str:
            return TransplantAnalysis(filename=filename, error="No valid JSON response found")
        
        json_str = clean_json_string(json_str)
        data = json.loads(json_str)
        
        return TransplantAnalysis(
            filename=filename,
            transplant_date=ReasoningElement(**data.get("transplant_date", {})),
            donor_type=ReasoningElement(**data.get("donor_type", {})),
            donor_relatedness=ReasoningElement(**data.get("donor_relatedness", {})),
            hla_match=ReasoningElement(**data.get("hla_match", {}))
        )
    except Exception as e:
        return TransplantAnalysis(filename=filename, error=f"Processing error: {str(e)}")

@retry(wait=wait_random_exponential(min=5, max=8), stop=stop_after_attempt(3))
def process_batch(file_batch: List[Path]) -> List[TransplantAnalysis]:
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIME_LIMIT)

    try:
        with ThreadPoolExecutor() as executor:
            contents = list(executor.map(lambda p: p.read_text(encoding='utf-8'), file_batch))

        prompts = [build_mistral_prompt(content) for content in contents]

        outputs = generator(
            prompts,
            max_new_tokens=512,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            return_full_text=False
        )

        results = []
        for i, output in enumerate(outputs):
            filename = file_batch[i].name
            generated_text = output[0]['generated_text'] if isinstance(output, list) else output['generated_text']
            print(f"\n=== Model output for {filename} ===\n{generated_text}")
            results.append(process_output(generated_text, filename))

        return results
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        return [TransplantAnalysis(filename=f.name, error=str(e)) for f in file_batch]
    finally:
        signal.alarm(0)

def process_txt_files(input_folder: str, output_json: str, output_tsv: Optional[str] = None):
    input_path = Path(input_folder)
    output_json_path = Path(output_json)
    output_json_path.parent.mkdir(parents=True, exist_ok=True)

    output_tsv_path = None
    if output_tsv:
        output_tsv_path = Path(output_tsv)
        output_tsv_path.parent.mkdir(parents=True, exist_ok=True)

    txt_files = list(input_path.glob('*.txt'))
    if not txt_files:
        logger.warning(f"No .txt files found in {input_folder}")
        return

    all_results = []

    if output_tsv:
        tsv_file = open(output_tsv_path, 'w', newline='', encoding='utf-8')
        tsv_writer = csv.writer(tsv_file, delimiter='\t')
        tsv_writer.writerow([
            "Filename",
            "Transplant Date Present", "Transplant Date Value", "Transplant Date Spans",
            "Donor Type Present", "Donor Type Value", "Donor Type Spans",
            "Donor Relatedness Present", "Donor Relatedness Value", "Donor Relatedness Spans",
            "HLA Match Present", "HLA Match Value", "HLA Match Spans",
            "Error"
        ])

    for i in tqdm(range(0, len(txt_files), BATCH_SIZE), desc="Processing batches"):
        batch = txt_files[i:i+BATCH_SIZE]
        batch_results = process_batch(batch)
        all_results.extend(batch_results)

        if output_tsv:
            for result in batch_results:
                td = result.transplant_date
                dt = result.donor_type
                dr = result.donor_relatedness
                hl = result.hla_match
                tsv_writer.writerow([
                    result.filename,
                    td.boolean if td else None, td.value if td else None, " | ".join(td.spans) if td and td.spans else "",
                    dt.boolean if dt else None, dt.value if dt else None, " | ".join(dt.spans) if dt and dt.spans else "",
                    dr.boolean if dr else None, dr.value if dr else None, " | ".join(dr.spans) if dr and dr.spans else "",
                    hl.boolean if hl else None, hl.value if hl else None, " | ".join(hl.spans) if hl and hl.spans else "",
                    result.error or ""
                ])

    if output_tsv:
        tsv_file.close()

    structured_results = {"results": [r.model_dump() for r in all_results]}
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(structured_results, json_file, indent=2)

if __name__ == "__main__":
    #input_folder = './test'
    # output_json = "./result.json"
    # output_tsv = "./result.tsv"

    # process_txt_files(input_folder, output_json, output_tsv)