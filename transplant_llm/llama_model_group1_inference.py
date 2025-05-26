import os
import json
import signal
import csv
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import logging

from tenacity import retry, wait_random_exponential, stop_after_attempt
from tqdm import tqdm
from pydantic import BaseModel, Field
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TIME_LIMIT = 300  # 5 minutes
BATCH_SIZE = 1  # Adjust based on GPU memory
MODEL_NAME = "meta-llama/Llama-3.3-70B-Instruct"

# Quantization config for 4-bit
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# Model setup with 4-bit quantization
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    quantization_config=quantization_config
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    batch_size=BATCH_SIZE
)

class ReasoningElement(BaseModel):
    boolean: Optional[bool]
    value: Optional[str]
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
        {"role": "system", "content": "You are a helpful assistant tasked with chart review of kidney transplant patients. You will be asked questions about the kidney transplant."},
        {"role": "user", "content":
            "Please answer the following questions based on the medical note provided.\n\n"
            f"Medical note: {file_content}"
            "1. What is the date of the kidney transplant (if documented)?\n"
            "2. What is the donor type? (Living, Deceased, or Not mentioned)\n"
            "3. What is the relatedness of the donor? (Related, Unrelated, or Not mentioned)\n"
            "4. What is the quality of HLA match? (Zero mismatch, Good match, Poor match, or Not mentioned)\n\n"
            "Provide supporting evidence by citing exact phrases from the medical note for each question.\n\n"
            "Return the result strictly in the following JSON format:\n"
            "{\n"
            "  \"transplant_date\": { \"boolean\": true/false/null, \"value\": \"\", \"spans\": [] },\n"
            "  \"donor_type\": { \"boolean\": true/false/null, \"value\": \"\", \"spans\": [] },\n"
            "  \"donor_relatedness\": { \"boolean\": true/false/null, \"value\": \"\", \"spans\": [] },\n"
            "  \"hla_match\": { \"boolean\": true/false/null, \"value\": \"\", \"spans\": [] }\n"
            "}\n\n"
            
        }
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

def extract_json_from_response(response: str) -> Optional[str]:
    try:
        json_match = re.search(r"```(?:json)?\s*({.*?})\s*```", response, re.DOTALL)
        if json_match:
            return json_match.group(1).strip()

        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1:
            return response[start:end+1].strip()
    except Exception:
        pass
    return None

def process_output(raw_result: str, filename: str) -> TransplantAnalysis:
    try:
        json_str = extract_json_from_response(raw_result)
        if not json_str:
            return TransplantAnalysis(filename=filename, error="No JSON found in response")

        json_str = json_str.replace("'", '"')
        json_str = re.sub(r'\bTrue\b', 'true', json_str)
        json_str = re.sub(r'\bFalse\b', 'false', json_str)
        json_str = re.sub(r'\bNone\b', 'null', json_str)

        data = json.loads(json_str)
        
        return TransplantAnalysis(
            filename=filename,
            transplant_date=ReasoningElement(**data.get("transplant_date", {})),
            donor_type=ReasoningElement(**data.get("donor_type", {})),
            donor_relatedness=ReasoningElement(**data.get("donor_relatedness", {})),
            hla_match=ReasoningElement(**data.get("hla_match", {}))
        )
    except Exception as e:
        return TransplantAnalysis(filename=filename, error=str(e))

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
            max_new_tokens=128,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.eos_token_id
        )

        results = []
        for i, output in enumerate(outputs):
            filename = file_batch[i].name
            generated_text = output[0]['generated_text'] if isinstance(output, list) else output['generated_text']
            if generated_text.startswith(prompts[i]):
                generated_text = generated_text[len(prompts[i]):].strip()
            results.append(process_output(generated_text, filename))

        return results
    except Exception as e:
        logger.error(f"Batch processing failed: {str(e)}")
        return [TransplantAnalysis(filename=f.name, error=str(e)) for f in file_batch]
    finally:
        signal.alarm(0)

def process_txt_files(input_folder: str, output_json: str, output_tsv: str):
    input_path = Path(input_folder)
    output_json_path = Path(output_json)
    output_tsv_path = Path(output_tsv)

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_tsv_path.parent.mkdir(parents=True, exist_ok=True)

    txt_files = list(input_path.glob('*.txt'))
    if not txt_files:
        logger.warning(f"No .txt files found in {input_folder}")
        return

    all_results = []

    with open(output_tsv_path, 'w', newline='', encoding='utf-8') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t')
        writer.writerow([
            "Filename", 
            "Transplant Date Present", "Transplant Date Value", "Transplant Date Spans",
            "Donor Type Present", "Donor Type Value", "Donor Type Spans",
            "Donor Relatedness Present", "Donor Relatedness Value", "Donor Relatedness Spans",
            "HLA Match Present", "HLA Match Value", "HLA Match Spans",
            "Error"])

        for i in tqdm(range(0, len(txt_files), BATCH_SIZE), desc="Processing batches"):
            batch = txt_files[i:i+BATCH_SIZE]
            batch_results = process_batch(batch)
            all_results.extend(batch_results)

            for result in batch_results:
                td = result.transplant_date
                dt = result.donor_type
                dr = result.donor_relatedness
                hl = result.hla_match
                writer.writerow([
                    result.filename,
                    td.boolean if td else None, td.value if td else None, " | ".join(td.spans) if td and td.spans else "",
                    dt.boolean if dt else None, dt.value if dt else None, " | ".join(dt.spans) if dt and dt.spans else "",
                    dr.boolean if dr else None, dr.value if dr else None, " | ".join(dr.spans) if dr and dr.spans else "",
                    hl.boolean if hl else None, hl.value if hl else None, " | ".join(hl.spans) if hl and hl.spans else "",
                    result.error or ""
                ])

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump([r.dict() for r in all_results], json_file, indent=2)

if __name__ == "__main__":
    #input_folder = './test'
    #output_json = "./result.json"
    #output_tsv = "./result.tsv"

    # process_txt_files(input_folder, output_json, output_tsv)



    