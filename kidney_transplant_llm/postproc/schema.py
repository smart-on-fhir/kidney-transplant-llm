###############################################################################
# SAMPLES
###############################################################################
SAMPLE_PRE = 'irae__sample_casedef_pre'
SAMPLE_INDEX = 'irae__sample_casedef_index'
SAMPLE_POST = 'irae__sample_casedef_post'

###############################################################################
# ORIGIN
###############################################################################
NLP_GPT_OSS_120B= 'irae__nlp_gpt_oss_120b'
NLP_DONOR_GPT_OSS_120B = 'irae__nlp_donor_gpt_oss_120b'
NLP_DONOR_GPT_4o = 'irae__nlp_donor_gpt4o'

###############################################################################
# COLUMNS
###############################################################################
SUBJECT_REF = 'subject_ref'
ENCOUNTER_REF = 'encounter_ref'
DOCUMENT_REF = 'documentreference_ref'
NOTE_REF = 'note_ref'
SORT_BY_DATE = 'sort_by_date'
ENC_ORDINAL = 'enc_period_ordinal'
DOC_ORDINAL = 'doc_ordinal'

SAMPLE_COLS = [SUBJECT_REF, ENCOUNTER_REF, DOCUMENT_REF,
               SORT_BY_DATE, ENC_ORDINAL, DOC_ORDINAL]

HIGHLIGHT_COLS = ['sublabel_name', 'sublabel_value', 'span']

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

def name_view(highlights:str, sample:str) -> str:
    """
    :return: str view name like 'irae__highlights_donor_index'
    """
    sample_period = sample.replace('irae__sample_casedef_', '')
    return highlights + '_' + sample_period


