create or replace view irae__gpt4_donor as
select
    distinct
    encounter_ref,
    documentreference_ref,
    subject_ref,
    enc_start_date,
    doc_date,
    donor_transplant_date,
    donor_type,
    donor_relationship,
    donor_hla_match_quality,
    donor_hla_mismatch_count
from irae__gpt4_fhir;


create or replace view irae__gpt4_donor_transplant_date as
WITH date_counts AS (
    SELECT
        subject_ref,
        donor_transplant_date,
        COUNT(*) AS cnt
    from    irae__gpt4_donor
    where   donor_transplant_date is not null
    and     donor_transplant_date > date('2000-01-01')
    GROUP BY subject_ref, donor_transplant_date
),
ranked_dates AS (
    SELECT  cnt, subject_ref, donor_transplant_date,
        ROW_NUMBER() OVER (
            PARTITION BY subject_ref
            ORDER BY cnt DESC, donor_transplant_date ASC  -- break ties consistently
        ) AS rn
    FROM date_counts
)
SELECT cnt, subject_ref, donor_transplant_date
FROM ranked_dates
WHERE rn = 1
ORDER BY subject_ref;
