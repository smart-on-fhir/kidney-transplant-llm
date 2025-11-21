###############################################################################
# SAMPLES
###############################################################################
SAMPLE_PRE_CSV = 'irae__sample_casedef_pre.csv'
SAMPLE_INDEX_CSV = 'irae__sample_casedef_index.csv'
SAMPLE_POST_CSV = 'irae__sample_casedef_post.csv'

###############################################################################
# ORIGIN
###############################################################################
GPT_OSS_120B = 'irae__nlp_donor_gpt_oss_120b'
GPT_4o = 'irae__nlp_donor_gpt4o'
###############################################################################
# COLUMNS
###############################################################################
SUBJECT_REF = 'subject_ref'
# PATIENT_ID = 'patient_id'

ENCOUNTER_REF = 'encounter_ref'
# ENCOUNTER_ID = 'encounter_id'

DOCUMENT_REF = 'documentreference_ref'
# DOCUMENT_ID = 'docref_dxr_id'
# NOTE_REF = 'note_ref'

SORT_BY_DATE = 'sort_by_date'
ENC_ORDINAL = 'enc_period_ordinal'
DOC_ORDINAL = 'doc_ordinal'

SAMPLE_COLS = [SUBJECT_REF, ENCOUNTER_REF, DOCUMENT_REF,
               SORT_BY_DATE, ENC_ORDINAL, DOC_ORDINAL]

HIGHLIGHT_COLS = ['sublabel_name', 'sublabel_value']

###############################################################################
# TASKS
###############################################################################
HIGHLIGHTS_DONOR_INDEX_100 = 'highlights_donor_index_100'




###############################################################################
# LLM Schema constants
###############################################################################
NOT_MENTIONED = 'NOT_MENTIONED'
NONE_OF_THE_ABOVE = 'NONE_OF_THE_ABOVE'

###############################################################################
# irae__highlights
###############################################################################
# note_ref      (documentreference_ref)
# subject_ref   Patient/UUID
# origin        irae__nlp_donor_gpt4o (raw annotation source table)
# label         `Transplant Date`, `Donor Relationship` , `Donor Type`, `Hla Mismatch Count`, `Hla Match Quality`
# span          character positions
# sublabel_name (see label above)
# sublabel_value Enum for all types except `Transplant Date`

###############################################################################
# desc irae__sample_casedef_****
###############################################################################
# group_name          	string
# subject_ref         	Patient/UUID
# encounter_ref       	Encounter/UUID
# documentreference_ref	DocumentReference/UUID
# enc_period_ordinal  	int: sequence of visit
# enc_period_start_day	date
# doc_author_day      	date
# doc_date            	date
# sort_by_date        	SORT by this date (best)
# doc_ordinal         	int: sequence of visit documents
# doc_type_code       	doc_type
# doc_type_display    	doc_type
# doc_type_system     	doc_type



###############################################################################
# Deprecated, from prior tabular outputs of "aggregate results" from Dylan
###############################################################################
# BOTH_INDEX = '2025-10-21-donor-and-non-donor-index'
# DONOR_INDEX = '2025-10-16-donor-characteristics-index'
# DONOR_INDEX_10 = '2025-10-16-donor-characteristics-index-10'
# LONGITUDINAL_INDEX_10 = '2025-10-16-non-donor-characteristics-index-10'
# LONGITUDINAL_POST_10 = '2025-10-16-non-donor-characteristics-post-10'
# GPT_OSS_CSV = 'gpt-oss-120b-azure_aggregate-results.csv'
# E3_IRAE_DIR = 'e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/'


###############################################################################
# E3 paths
###############################################################################
# export IRAE_DIR='/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/'
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-21-donor-and-non-donor-index/output/*.csv" .
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-16-donor-characteristics/output/*.csv" .
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-16-non-donor-characteristics/output/*.csv" .
# scp "e3:/lab-share/CHIP-Mandl-e2/Public/dp-llm/llm-structured-data-extraction/data/irae/2025-10-16-non-donor-characteristics-post-10/output/*.csv" .