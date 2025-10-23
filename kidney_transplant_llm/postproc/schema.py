###############################################################################
# Column names (REF)
###############################################################################
SUBJECT_REF = 'subject_ref'
PATIENT_ID = 'patient_id'

ENCOUNTER_REF = 'encounter_ref'
ENCOUNTER_ID = 'encounter_id'

DOCUMENT_REF = 'documentreference_ref'
DOCUMENT_ID = 'docref_dxr_id'

###############################################################################
# Environment (E3 paths)
###############################################################################
BOTH_INDEX = '2025-10-21-donor-and-non-donor-index'
DONOR_INDEX = '2025-10-16-donor-characteristics-index'
DONOR_INDEX_10 = '2025-10-16-donor-characteristics-index-10'
LONGITUDINAL_INDEX_10 = '2025-10-16-non-donor-characteristics-index-10'
LONGITUDINAL_POST_10 = '2025-10-16-non-donor-characteristics-post-10'
GPT_OSS_CSV = 'gpt-oss-120b-azure_aggregate-results.csv'
E3_IRAE_DIR = 'e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/'

###############################################################################
# casedef samples
###############################################################################
SAMPLE_PRE_CSV = 'irae__sample_casedef_pre.csv'
SAMPLE_INDEX_CSV = 'irae__sample_casedef_index.csv'
SAMPLE_POST_CSV = 'irae__sample_casedef_post.csv'

###############################################################################
# LLM Schema constants
###############################################################################
NOT_MENTIONED = 'NOT_MENTIONED'
NONE_OF_THE_ABOVE = 'NONE_OF_THE_ABOVE'


###############################################################################
# E3 paths
###############################################################################
# export IRAE_DIR='/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/'
#
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-21-donor-and-non-donor-index/output/*.csv" .
#
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-16-donor-characteristics/output/*.csv" .
#
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-16-non-donor-characteristics/output/*.csv" .
#
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-16-non-donor-characteristics-post-10/output/*.csv" .