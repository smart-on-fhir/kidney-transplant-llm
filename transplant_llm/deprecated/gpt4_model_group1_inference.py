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
TIME_LIMIT = 300  # seconds

class SpanAugmentedMention(BaseModel):
    is_present: Optional[bool]  # True, False, or None
    spans: List[str]

class DonorInformationMention(SpanAugmentedMention):
    donor_type: Optional[str]

class DonorRelatednessMention(SpanAugmentedMention):
    relatedness_type: Optional[str]

class DSAMention(SpanAugmentedMention):
    dsa_type: Optional[str]

class HLAMention(SpanAugmentedMention):
    hla_type: Optional[str]

class TransplantDateMention(SpanAugmentedMention):
    value: Optional[str]

class TransplantAnalysis(BaseModel):
    filename: str
    transplant_date: Optional[TransplantDateMention] = None
    donor_information: Optional[DonorInformationMention] = None
    donor_relatedness: Optional[DonorRelatednessMention] = None
    dsa: Optional[DSAMention] = None
    hla: Optional[HLAMention] = None
    error: Optional[str] = None

def timeout_handler(signum, frame):
    raise TimeoutError("Processing timed out")

@retry(
    wait=wait_fixed(5),
    stop=stop_after_attempt(10),
    retry_error_callback=lambda retry_state: TransplantAnalysis(
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
            {"role": "system", "content": "You are a helpful assistant tasked with chart review of kidney transplant patients. You will be asked questions about the kidney transplant donor."},
            {"role": "user", "content": (
                "What is the date of kidney transplant (if documented)?\n"
                "Was the donor a living donor? (true = living, false = deceased, null = not mentioned)\n"
                "Was the donor related to the recipient? (true = related, false = unrelated, null = not mentioned)\n"
                "What was the quality of HLA match? (Choose one: \"zero mismatch\", \"good match\", \"poor match\", null)\n\n"
                "For each question:\n"
                "- Provide a boolean or null indicating if the information is present\n"
                "- Provide exact supporting span(s)\n"
                "- Return the value when known (e.g., date, donor type, HLA quality)\n\n"
                "Respond in JSON format:\n"
                "```json\n"
                "{\n"
                '  "transplant_date": { "boolean": true/false/null, "value": string, "spans": string[] },\n'
                '  "donor_information": { "boolean": true/false/null, "donor_type": string, "spans": string[] },\n'
                '  "donor_relatedness": { "boolean": true/false/null, "relatedness_type": string, "spans": string[] },\n'
                '  "dsa": { "boolean": true/false/null, "dsa_type": string, "spans": string[] },\n'
                '  "hla": { "boolean": true/false/null, "hla_type": string, "spans": string[] }\n'
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
                    return TransplantAnalysis(filename=filename, error="Skipped due to repeated rate limit (30s total wait)")
                time.sleep(wait_interval)
            except (Timeout, APIError, APIConnectionError, ServiceUnavailableError) as e:
                raise e

        raw_result = response['choices'][0]['message']['content']
        cleaned_result = raw_result.strip().strip("```json").strip("```")
        data = json.loads(cleaned_result)

        return TransplantAnalysis(
            filename=filename,
            transplant_date=TransplantDateMention(
                is_present=data.get("transplant_date", {}).get("boolean"),
                value=data.get("transplant_date", {}).get("value"),
                spans=data.get("transplant_date", {}).get("spans", [])
            ) if "transplant_date" in data else None,
            donor_information=DonorInformationMention(
                is_present=data.get("donor_information", {}).get("boolean"),
                donor_type=data.get("donor_information", {}).get("donor_type"),
                spans=data.get("donor_information", {}).get("spans", [])
            ) if "donor_information" in data else None,
            donor_relatedness=DonorRelatednessMention(
                is_present=data.get("donor_relatedness", {}).get("boolean"),
                relatedness_type=data.get("donor_relatedness", {}).get("relatedness_type"),
                spans=data.get("donor_relatedness", {}).get("spans", [])
            ) if "donor_relatedness" in data else None,
            dsa=DSAMention(
                is_present=data.get("dsa", {}).get("boolean"),
                dsa_type=data.get("dsa", {}).get("dsa_type"),
                spans=data.get("dsa", {}).get("spans", [])
            ) if "dsa" in data else None,
            hla=HLAMention(
                is_present=data.get("hla", {}).get("boolean"),
                hla_type=data.get("hla", {}).get("hla_type"),
                spans=data.get("hla", {}).get("spans", [])
            ) if "hla" in data else None
        )

    except Exception as e:
        return TransplantAnalysis(filename=filename, error=str(e))
    finally:
        signal.alarm(0)

def process_txt_files(input_folder, output_json, output_tsv):
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    all_results = []

    with open(output_tsv, 'w', newline='', encoding='utf-8') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t')
        tsv_writer.writerow([
            "Filename",
            "Transplant Date Present", "Transplant Date", "Transplant Date Evidence",
            "Donor Info Present", "Donor Type", "Donor Info Evidence",
            "Donor Relatedness Present", "Relatedness Type", "Donor Relatedness Evidence",
            "DSA Present", "DSA Type", "DSA Evidence",
            "HLA Present", "HLA Type", "HLA Evidence",
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
                    result = TransplantAnalysis(filename=filename, error=error_msg)

                all_results.append(result.dict())

                tsv_writer.writerow([
                    filename,
                    result.transplant_date.is_present if result.transplant_date else None,
                    result.transplant_date.value if result.transplant_date else "",
                    "; ".join(result.transplant_date.spans) if result.transplant_date else "",
                    result.donor_information.is_present if result.donor_information else None,
                    result.donor_information.donor_type if result.donor_information else "None",
                    "; ".join(result.donor_information.spans) if result.donor_information else "",
                    result.donor_relatedness.is_present if result.donor_relatedness else None,
                    result.donor_relatedness.relatedness_type if result.donor_relatedness else "None",
                    "; ".join(result.donor_relatedness.spans) if result.donor_relatedness else "",
                    result.dsa.is_present if result.dsa else None,
                    result.dsa.dsa_type if result.dsa else "None",
                    "; ".join(result.dsa.spans) if result.dsa else "",
                    result.hla.is_present if result.hla else None,
                    result.hla.hla_type if result.hla else "None",
                    "; ".join(result.hla.spans) if result.hla else "",
                    result.error if result.error else ""
                ])

                time.sleep(1.5)
                pbar.update(1)

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(all_results, json_file, indent=4)

# Run

if __name__ == "__main__":
    #input_folder = './test'
    #output_json = './result.json'
    #output_tsv = "./result.tsv'



    #process_txt_files(input_folder, output_json, output_tsv)



