create or replace view irae__gpt4_infection as
select  distinct
        documentreference_ref                   ,
        subject_ref                             ,
        encounter_ref                           ,
        enc_start_date                          ,
        doc_date                                ,
        dsa_mentioned	                        ,
        dsa_history	                            ,
        dsa_present	                            ,
        infection_mentioned	                    ,
        infection_history	                    ,
        infection_present	                    ,
        viral_mentioned	            ,
        viral_history	                ,
        viral_present	                ,
        bacterial_mentioned	        ,
        bacterial_history	            ,
        bacterial_present	            ,
        fungal_mentioned	            ,
        fungal_history	            ,
        fungal_present
from irae__gpt4_fhir;

create or replace view irae__gpt4_infection_present as
with union_note as
(
    select distinct documentreference_ref, infection_present        as present
    from    irae__gpt4_fhir    where infection_present!='NoneOfTheAbove'
    UNION
    select distinct documentreference_ref, viral_present  as present
    from    irae__gpt4_fhir    where viral_present!='NoneOfTheAbove'
    UNION
    select distinct documentreference_ref, bacterial_present as present
    from    irae__gpt4_fhir    where bacterial_present!='NoneOfTheAbove'
    UNION
    select distinct documentreference_ref, fungal_present as present
    from    irae__gpt4_fhir    where fungal_present!='NoneOfTheAbove'
),
ranked_note as
(
    select  count(*) as cnt, documentreference_ref, present
    from    union_note
    group by documentreference_ref, present
),
ranked_visit as
(
    select  count(*) as cnt, FHIR.encounter_ref, present
    from    union_note, irae__gpt4_fhir as FHIR
    where   union_note.documentreference_ref = FHIR.documentreference_ref
    group by FHIR.encounter_ref, present
),
ranked_patient as
(
    select  count(*) as cnt, FHIR.subject_ref, present
    from    union_note, irae__gpt4_fhir as FHIR
    where   union_note.documentreference_ref = FHIR.documentreference_ref
    group by FHIR.subject_ref, present
)




