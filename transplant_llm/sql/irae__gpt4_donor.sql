create table irae__gpt4_donor as
select
    distinct
    documentreference_ref,
    subject_ref,
    encounter_ref,
    enc_start_date,
    enc_end_date,
    donor_transplant_date_mentioned,
    donor_transplant_date,
    donor_type_is_present,
    donor_type,
    donor_relationship_mentioned,
    donor_relationship,
    donor_hla_match_quality_mentioned,
    donor_hla_match_quality,
    donor_hla_mismatch_count_mentioned,
    donor_hla_mismatch_count,
    error
from irae__gpt4_fhir;

