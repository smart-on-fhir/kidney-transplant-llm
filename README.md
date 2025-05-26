# kidney-transplant-llm
Kidney Transplant LLM Prompts

## Donor characteristics 
| Variable           | Description                                               | Data Type (or none) | 
|--------------------|-----------------------------------------------------------|---------------------|
| transplant_date    | Date of surgical procedure                                | Date                |
| donor_type         | Was the kidney donor living at the time of transplant?    | True, False, None |
| donor_relationship | Was the kidney donor related to the transplant recipient? | True, False, None |
| hla_match_quality  | What was the HLA match quality?                           | Multiple choice | 
| hla_mismatch_count | What was the HLA mismatch count?                          | Integer 0-6 or None|

## Medication Compliance 
| Variable         | Description                                           | Data Type (or none) | 
|------------------|-------------------------------------------------------|---------------------|
| therapeutic      | Documented immunosuppression levels are adequate      | Date                |
| subtherapeutic   | Documented subtherapeutic immunosuppression levels    | True, False, None |
| supratherapeutic | Documented supratherapeutic immunosuppression levels  | True, False, None |
| compliant        | Patient is compliant with immunosuppression           | True, False, None |
| partial          | Patient is partially compliant with immunosuppression | True, False, None |
| noncompliant     | Patient is noncompliant with immunosuppression           | True, False, None |


