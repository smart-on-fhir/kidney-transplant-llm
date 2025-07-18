import os
import json
import openai
import signal
import csv
import time
from tenacity import retry, wait_fixed, stop_after_attempt
from tqdm import tqdm
from pydantic import BaseModel, Field
from typing import Optional, List
from openai.error import RateLimitError, Timeout, APIError, APIConnectionError, ServiceUnavailableError

# Azure OpenAI configurations
openai.api_type = "azure"
openai.api_version = "2024-08-01-preview"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

deployment_name = "gpt-4o"
TIME_LIMIT = 300

class SpanAugmentedMention(BaseModel):
    is_present: Optional[bool]  # True, False, or None
    spans: List[str]

class ImmunosuppressionAnalysis(BaseModel):
    filename: str
    adequate_level: Optional[SpanAugmentedMention] = None
    subtherapeutic: Optional[SpanAugmentedMention] = None
    supratherapeutic: Optional[SpanAugmentedMention] = None
    compliant: Optional[SpanAugmentedMention] = None
    partially_compliant: Optional[SpanAugmentedMention] = None
    noncompliant: Optional[SpanAugmentedMention] = None
    error: Optional[str] = None

def timeout_handler(signum, frame):
    raise TimeoutError("Processing timed out")

@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(10),
    retry_error_callback=lambda retry_state: ImmunosuppressionAnalysis(
        filename=retry_state.args[1],
        error=f"Retry failed: {retry_state.outcome.exception()}"
    )
)
def process_file(file_path, filename):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(TIME_LIMIT)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        messages = [
            {"role": "system", "content": "You are a helpful assistant tasked with chart review of kidney transplant recipients. You will be asked questions about the transplant recipient medication compliance."},
            {"role": "user", "content": (
                "Answer the following questions based on the medical note:\n"
                "Whether the documented immunosuppression level is adequate? (True, False, not mentioned)\n"
                "Is there documented subtherapeutic immunosuppression? (True, False, not mentioned)\n"
                "Is there documented supratherapeutic immunosuppression? (True, False, not mentioned)\n"
                "Whether the patient is compliant with immunosuppressive medications? (True, False, not mentioned)\n"
                "Whether the patient is partially compliant with immunosuppressive medications? (True, False, not mentioned)\n"
                "Whether the patient is noncompliant with immunosuppressive medications? (True, False, not mentioned)\n\n"
                "For each:\n"
                "- Provide a boolean or null for whether the information is present\n"
                "- Include supporting text span(s)\n\n"
                "Return JSON in this format:\n"
                "```json\n"
                "{\n"
                '  "adequate_level": { "boolean": true/false/null, "spans": string[] },\n'
                '  "subtherapeutic": { "boolean": true/false/null, "spans": string[] },\n'
                '  "supratherapeutic": { "boolean": true/false/null, "spans": string[] },\n'
                '  "compliant": { "boolean": true/false/null, "spans": string[] },\n'
                '  "partially_compliant": { "boolean": true/false/null, "spans": string[] },\n'
                '  "noncompliant": { "boolean": true/false/null, "spans": string[] }\n'
                "}\n"
                "```\n\n"
                f"Medical note: {file_content}"
            )}
        ]

        total_wait = 0
        wait_interval = 10

        while True:
            try:
                response = openai.ChatCompletion.create(
                    engine=deployment_name,
                    messages=messages,
                    response_format={"type": "json_object"}
                )
                break
            except RateLimitError:
                print(f"⏳ Rate limit hit for {filename}. Waiting {wait_interval}s...")
                total_wait += wait_interval
                if total_wait > 30:
                    print(f"⚠️ Skipping {filename} after 30s wait due to rate limits.")
                    return ImmunosuppressionAnalysis(filename=filename, error="Skipped due to repeated rate limit (30s total wait)")
                time.sleep(wait_interval)
            except (Timeout, APIError, APIConnectionError, ServiceUnavailableError) as e:
                raise e

        raw_result = response['choices'][0]['message']['content']
        cleaned_result = raw_result.strip().strip("```json").strip("```")
        data = json.loads(cleaned_result)

        return ImmunosuppressionAnalysis(
            filename=filename,
            adequate_level=SpanAugmentedMention(
                is_present=data.get("adequate_level", {}).get("boolean"),
                spans=data.get("adequate_level", {}).get("spans", [])
            ) if "adequate_level" in data else None,
            subtherapeutic=SpanAugmentedMention(
                is_present=data.get("subtherapeutic", {}).get("boolean"),
                spans=data.get("subtherapeutic", {}).get("spans", [])
            ) if "subtherapeutic" in data else None,
            supratherapeutic=SpanAugmentedMention(
                is_present=data.get("supratherapeutic", {}).get("boolean"),
                spans=data.get("supratherapeutic", {}).get("spans", [])
            ) if "supratherapeutic" in data else None,
            compliant=SpanAugmentedMention(
                is_present=data.get("compliant", {}).get("boolean"),
                spans=data.get("compliant", {}).get("spans", [])
            ) if "compliant" in data else None,
            partially_compliant=SpanAugmentedMention(
                is_present=data.get("partially_compliant", {}).get("boolean"),
                spans=data.get("partially_compliant", {}).get("spans", [])
            ) if "partially_compliant" in data else None,
            noncompliant=SpanAugmentedMention(
                is_present=data.get("noncompliant", {}).get("boolean"),
                spans=data.get("noncompliant", {}).get("spans", [])
            ) if "noncompliant" in data else None
        )

    except Exception as e:
        return ImmunosuppressionAnalysis(filename=filename, error=str(e))
    finally:
        signal.alarm(0)

def process_txt_files(input_folder, output_json, output_tsv):
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    all_results = []

    with open(output_tsv, 'w', newline='', encoding='utf-8') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')
        tsv_writer.writerow([
            "Filename",
            "Adequate", "Adequate Evidence",
            "Subtherapeutic", "Subtherapeutic Evidence",
            "Supratherapeutic", "Supratherapeutic Evidence",
            "Compliant", "Compliant Evidence",
            "Partially Compliant", "Partial Compliance Evidence",
            "Noncompliant", "Noncompliance Evidence",
            "Error"
        ])

        with tqdm(total=len(txt_files), desc="Processing Files", unit="file") as pbar:
            for filename in txt_files:
                file_path = os.path.join(input_folder, filename)
                print(f"\n>>> Processing: {filename}")
                start_time = time.time()

                try:
                    result = process_file(file_path, filename)
                    print(f"✓ Done: {filename} (in {time.time() - start_time:.2f}s)")
                except Exception as e:
                    error_msg = f"Exception during processing: {str(e)}"
                    print(f"✗ Error: {filename} – {error_msg}")
                    result = ImmunosuppressionAnalysis(filename=filename, error=error_msg)

                all_results.append(result.dict())

                tsv_writer.writerow([
                    filename,
                    result.adequate_level.is_present if result.adequate_level else None,
                    "; ".join(result.adequate_level.spans) if result.adequate_level else "",
                    result.subtherapeutic.is_present if result.subtherapeutic else None,
                    "; ".join(result.subtherapeutic.spans) if result.subtherapeutic else "",
                    result.supratherapeutic.is_present if result.supratherapeutic else None,
                    "; ".join(result.supratherapeutic.spans) if result.supratherapeutic else "",
                    result.compliant.is_present if result.compliant else None,
                    "; ".join(result.compliant.spans) if result.compliant else "",
                    result.partially_compliant.is_present if result.partially_compliant else None,
                    "; ".join(result.partially_compliant.spans) if result.partially_compliant else "",
                    result.noncompliant.is_present if result.noncompliant else None,
                    "; ".join(result.noncompliant.spans) if result.noncompliant else "",
                    result.error if result.error else ""
                ])

                time.sleep(1.5)
                pbar.update(1)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(all_results, json_file, indent=4)

# Set paths and run
#input_folder = "./test"
output_json = "./result.json"
output_tsv = "./result.tsv"

process_txt_files(input_folder, output_json, output_tsv)