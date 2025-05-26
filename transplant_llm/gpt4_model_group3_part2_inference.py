import os
import json
import openai
import signal
import csv
import time
from tenacity import retry, wait_fixed, stop_after_attempt
from tqdm import tqdm
from pydantic import BaseModel
from typing import Optional, List
from openai.error import RateLimitError, Timeout, APIError, APIConnectionError, ServiceUnavailableError

# Azure OpenAI setup
openai.api_type = "azure"
openai.api_version = "2024-08-01-preview"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = "gpt-4o"
TIME_LIMIT = 300

class SpanAugmentedMention(BaseModel):
    is_present: Optional[bool]
    spans: List[str]

class ComplicationGroup1(BaseModel):
    filename: str
    biopsy_proven_graft_failure: Optional[SpanAugmentedMention] = None
    graft_failure_ckd5_esrd: Optional[SpanAugmentedMention] = None
    return_to_dialysis: Optional[SpanAugmentedMention] = None
    transplant_nephrectomy: Optional[SpanAugmentedMention] = None
    ptld_clinical: Optional[SpanAugmentedMention] = None
    ptld_biopsy: Optional[SpanAugmentedMention] = None
    graft_failure: Optional[SpanAugmentedMention] = None
    error: Optional[str] = None

def timeout_handler(signum, frame):
    raise TimeoutError("Processing timed out")

@retry(wait=wait_fixed(5), stop=stop_after_attempt(10),
       retry_error_callback=lambda r: ComplicationGroup1(filename=r.args[1], error=str(r.outcome.exception())))
def process_file(file_path, filename):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIME_LIMIT)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        questions = (
            "Whether there is clinical biopsy proven graft failure?\n"
            "Whether there is graft failure with return to CKD stage 5 or ESRD?\n"
            "Whether there is clinically documented return to dialysis?\n"
            "Whether there is documented 'transplant nephrectomy'?\n"
            "Whether there is definitive clinical diagnosis of post-transplant lymphoproliferative disorder (PTLD)?\n"
            "Whether there is clinical biopsy proven or pathology proven PTLD?\n"
            "Whether there is definitive clinical diagnosis of graft failure?"
        )

        instruction = (
            "For each question:\n"
            "- Provide a boolean or null to indicate presence\n"
            "- Provide supporting text span(s)\n"
            "Return JSON in this format:\n"
            "{\n"
            '  "biopsy_proven_graft_failure": {"boolean": true/false/null, "spans": []},\n'
            '  "graft_failure_ckd5_esrd": {...},\n'
            '  "return_to_dialysis": {...},\n'
            '  "transplant_nephrectomy": {...},\n'
            '  "ptld_clinical": {...},\n'
            '  "ptld_biopsy": {...},\n'
            '  "graft_failure": {...}\n'
            "}"
        )

        messages = [
            {"role": "system", "content": "You are a clinical assistant reviewing transplant complications."},
            {"role": "user", "content": f"{questions}\n\n{instruction}\n\nMedical note:\n{content}"}
        ]

        total_wait = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                    engine=deployment_name,
                    messages=messages,
                    response_format={"type": "json_object"}
                )
                break
            except RateLimitError:
                if total_wait >= 30:
                    return ComplicationGroup1(filename=filename, error="Skipped due to 30s rate limit delay")
                time.sleep(10)
                total_wait += 10
            except (Timeout, APIError, APIConnectionError, ServiceUnavailableError) as e:
                raise e

        result = json.loads(response['choices'][0]['message']['content'].strip().strip("```json").strip("```"))
        def extract(name):
            return SpanAugmentedMention(is_present=result.get(name, {}).get("boolean"),
                                        spans=result.get(name, {}).get("spans", [])) if name in result else None

        return ComplicationGroup1(
            filename=filename,
            biopsy_proven_graft_failure=extract("biopsy_proven_graft_failure"),
            graft_failure_ckd5_esrd=extract("graft_failure_ckd5_esrd"),
            return_to_dialysis=extract("return_to_dialysis"),
            transplant_nephrectomy=extract("transplant_nephrectomy"),
            ptld_clinical=extract("ptld_clinical"),
            ptld_biopsy=extract("ptld_biopsy"),
            graft_failure=extract("graft_failure")
        )
    except Exception as e:
        return ComplicationGroup1(filename=filename, error=str(e))
    finally:
        signal.alarm(0)

def process_txt_files(input_folder, output_json, output_tsv):
    files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    results = []

    with open(output_tsv, 'w', newline='', encoding='utf-8') as tsv:
        writer = csv.writer(tsv, delimiter='\t')
        writer.writerow([
            "Filename",
            "Biopsy Graft Failure", "Biopsy Spans",
            "CKD5/ESRD", "CKD5 Spans",
            "Return to Dialysis", "Dialysis Spans",
            "Nephrectomy", "Nephrectomy Spans",
            "PTLD Clinical", "PTLD Clinical Spans",
            "PTLD Biopsy", "PTLD Biopsy Spans",
            "Graft Failure", "Graft Failure Spans",
            "Error"
        ])
        with tqdm(total=len(files), desc="Group 1", unit="file") as pbar:
            for f in files:
                path = os.path.join(input_folder, f)
                print(f"\n>>> Processing: {f}")
                result = process_file(path, f)
                results.append(result.dict())

                def val(x): return x.is_present if x else None
                def span(x): return "; ".join(x.spans) if x else ""

                writer.writerow([
                    f,
                    val(result.biopsy_proven_graft_failure), span(result.biopsy_proven_graft_failure),
                    val(result.graft_failure_ckd5_esrd), span(result.graft_failure_ckd5_esrd),
                    val(result.return_to_dialysis), span(result.return_to_dialysis),
                    val(result.transplant_nephrectomy), span(result.transplant_nephrectomy),
                    val(result.ptld_clinical), span(result.ptld_clinical),
                    val(result.ptld_biopsy), span(result.ptld_biopsy),
                    val(result.graft_failure), span(result.graft_failure),
                    result.error or ""
                ])
                time.sleep(1.5)
                pbar.update(1)

    with open(output_json, 'w', encoding='utf-8') as jf:
        json.dump(results, jf, indent=4)

# Set paths and run
#input_folder = './test'
output_json = "./result.json"
output_tsv = "./result.tsv"

process_txt_files(input_folder, output_json, output_tsv)