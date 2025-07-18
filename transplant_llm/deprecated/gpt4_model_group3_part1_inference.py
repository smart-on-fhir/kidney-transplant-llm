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

class ComplicationGroup2(BaseModel):
    filename: str
    infection_encounter: Optional[SpanAugmentedMention] = None
    bacterial_infection: Optional[SpanAugmentedMention] = None
    viral_infection: Optional[SpanAugmentedMention] = None
    fungal_infection: Optional[SpanAugmentedMention] = None
    cancer_encounter: Optional[SpanAugmentedMention] = None
    dsa: Optional[SpanAugmentedMention] = None
    rejection: Optional[SpanAugmentedMention] = None
    rejection_biopsy: Optional[SpanAugmentedMention] = None
    rejection_treatment: Optional[SpanAugmentedMention] = None
    tcmr: Optional[SpanAugmentedMention] = None
    amr: Optional[SpanAugmentedMention] = None
    error: Optional[str] = None

def timeout_handler(signum, frame):
    raise TimeoutError("Processing timed out")

@retry(wait=wait_fixed(5), stop=stop_after_attempt(10),
       retry_error_callback=lambda r: ComplicationGroup2(filename=r.args[1], error=str(r.outcome.exception())))
def process_file(file_path, filename):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIME_LIMIT)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        questions = (
            "Whether there is definitive clinical diagnosis of infection in the present encounter?\n"
            "Whether there is definitive clinical diagnosis of bacterial infection?\n"
            "Whether there is definitive clinical diagnosis of viral infection?\n"
            "Whether there is definitive clinical diagnosis of fungal infection?\n"
            "Whether there is definitive clinical diagnosis of cancer in the present encounter?\n"
            "Whether there is definitive clinical diagnosis of donor specific antibody (DSA)?\n"
            "Whether there is definitive clinical diagnosis of transplant rejection?\n"
            "Whether there is clinical biopsy proven allograft rejection?\n"
            "Whether there is documented medication treatment of transplant rejection?\n"
            "Whether there is definitive clinical diagnosis of t-cell mediated rejection (TCR)?\n"
            "Whether there is definitive clinical diagnosis of antibody mediated rejection (AMR)?"
        )

        instruction = (
            "For each question:\n"
            "- Provide a boolean or null to indicate presence\n"
            "- Provide supporting text span(s)\n"
            "Return JSON in this format:\n"
            "{\n"
            '  "infection_encounter": {"boolean": true/false/null, "spans": []},\n'
            '  "bacterial_infection": {...},\n'
            '  "viral_infection": {...},\n'
            '  "fungal_infection": {...},\n'
            '  "cancer_encounter": {...},\n'
            '  "dsa": {...},\n'
            '  "rejection": {...},\n'
            '  "rejection_biopsy": {...},\n'
            '  "rejection_treatment": {...},\n'
            '  "tcmr": {...},\n'
            '  "amr": {...}\n'
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
                    return ComplicationGroup2(filename=filename, error="Skipped due to 30s rate limit delay")
                time.sleep(10)
                total_wait += 10
            except (Timeout, APIError, APIConnectionError, ServiceUnavailableError) as e:
                raise e

        result = json.loads(response['choices'][0]['message']['content'].strip().strip("```json").strip("```"))
        def extract(name):
            return SpanAugmentedMention(is_present=result.get(name, {}).get("boolean"),
                                        spans=result.get(name, {}).get("spans", [])) if name in result else None

        return ComplicationGroup2(
            filename=filename,
            infection_encounter=extract("infection_encounter"),
            bacterial_infection=extract("bacterial_infection"),
            viral_infection=extract("viral_infection"),
            fungal_infection=extract("fungal_infection"),
            cancer_encounter=extract("cancer_encounter"),
            dsa=extract("dsa"),
            rejection=extract("rejection"),
            rejection_biopsy=extract("rejection_biopsy"),
            rejection_treatment=extract("rejection_treatment"),
            tcmr=extract("tcmr"),
            amr=extract("amr")
        )
    except Exception as e:
        return ComplicationGroup2(filename=filename, error=str(e))
    finally:
        signal.alarm(0)

def process_txt_files(input_folder, output_json, output_tsv):
    files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    results = []

    with open(output_tsv, 'w', newline='', encoding='utf-8') as tsv:
        writer = csv.writer(tsv, delimiter='\t')
        writer.writerow([
            "Filename",
            "Infection", "Infection Spans",
            "Bacterial", "Bacterial Spans",
            "Viral", "Viral Spans",
            "Fungal", "Fungal Spans",
            "Cancer", "Cancer Spans",
            "DSA", "DSA Spans",
            "Rejection", "Rejection Spans",
            "Rejection Biopsy", "Rejection Biopsy Spans",
            "Rejection Treated", "Rejection Treatment Spans",
            "TCMR", "TCMR Spans",
            "AMR", "AMR Spans",
            "Error"
        ])
        with tqdm(total=len(files), desc="Group 2", unit="file") as pbar:
            for f in files:
                path = os.path.join(input_folder, f)
                print(f"\n>>> Processing: {f}")
                result = process_file(path, f)
                results.append(result.dict())

                def val(x): return x.is_present if x else None
                def span(x): return "; ".join(x.spans) if x else ""

                writer.writerow([
                    f,
                    val(result.infection_encounter), span(result.infection_encounter),
                    val(result.bacterial_infection), span(result.bacterial_infection),
                    val(result.viral_infection), span(result.viral_infection),
                    val(result.fungal_infection), span(result.fungal_infection),
                    val(result.cancer_encounter), span(result.cancer_encounter),
                    val(result.dsa), span(result.dsa),
                    val(result.rejection), span(result.rejection),
                    val(result.rejection_biopsy), span(result.rejection_biopsy),
                    val(result.rejection_treatment), span(result.rejection_treatment),
                    val(result.tcmr), span(result.tcmr),
                    val(result.amr), span(result.amr),
                    result.error or ""
                ])
                time.sleep(1.5)
                pbar.update(1)

    with open(output_json, 'w', encoding='utf-8') as jf:
        json.dump(results, jf, indent=4)

# Set paths and run
input_folder = './test'
output_json = "./result.json"
output_tsv = "./result.tsv"

process_txt_files(input_folder, output_json, output_tsv)