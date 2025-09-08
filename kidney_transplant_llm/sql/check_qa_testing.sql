-- ###########################################################################
-- Raw VS FHIR linked data matches

select  count(distinct filename) as cnt_documents,
        count(*) as cnt_rows
from    irae__gpt4_raw;

--     cnt_documents	cnt_rows
--     33117	        33117

select  count(distinct subject_ref)             as cnt_patients,
        count(distinct documentreference_ref)   as cnt_documents,
        count(distinct encounter_ref)           as cnt_encounters
from    irae__gpt4_fhir;

--     cnt_patients cnt_documents   cnt_encounters
--     218	        33116	        10506


select count(*) from irae__gpt4_fhir where dsa_is_present!=dsa_mentioned;
--     75 (0.2% compared to 32406)


with patient_variable as
(
    select  distinct subject_ref,
            donor_type as variable
    from irae__gpt4_parsed
)
select  count(distinct subject_ref) as cnt_patients,
        variable
from    patient_variable
group by variable
order by cnt_patients desc;


select  count(*) as cnt, donor_date
from    irae__gpt4_donor
where   subject_ref =
'Patient/806dda1fd7979681eeee1e88d703b69e47c10370663584e380919b9f4e6088b4'
and     donor_date is not null
and     donor_date > date('2000-01-01')
group by donor_date
order by cnt desc