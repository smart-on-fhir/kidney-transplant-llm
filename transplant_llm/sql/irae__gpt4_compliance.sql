create or replace view irae__gpt4_compliance as
select
    distinct
    documentreference_ref               ,
    subject_ref                         ,
    encounter_ref                       ,
    enc_start_date                      ,
    doc_date                            ,
    rx_therapeutic_therapeutic	        ,
    rx_therapeutic_subtherapeutic	    ,
    rx_therapeutic_supratherapeutic	    ,
    rx_compliance_compliant	            ,
    rx_compliance_partial	            ,
    rx_compliance_noncompliant
from irae__gpt4_fhir;

create or replace view irae__gpt4_compliance_score as
SELECT  subject_ref,
        count(*) as cnt,
        rx_therapeutic_therapeutic	        ,
        rx_therapeutic_subtherapeutic	    ,
        rx_therapeutic_supratherapeutic	    ,
        rx_compliance_compliant	            ,
        rx_compliance_partial	            ,
        rx_compliance_noncompliant
FROM    irae__gpt4_fhir
WHERE   NOT (
        rx_therapeutic_therapeutic	    = 'NotMentioned' AND
        rx_therapeutic_subtherapeutic	= 'NotMentioned' AND
        rx_therapeutic_supratherapeutic	= 'NotMentioned')
AND     NOT (
        rx_compliance_compliant	        = 'NotMentioned' AND
        rx_compliance_partial	        = 'NotMentioned' AND
        rx_compliance_noncompliant	    = 'NotMentioned')
group by subject_ref,
        rx_therapeutic_therapeutic	        ,
        rx_therapeutic_subtherapeutic	    ,
        rx_therapeutic_supratherapeutic	    ,
        rx_compliance_compliant	            ,
        rx_compliance_partial	            ,
        rx_compliance_noncompliant
order by subject_ref, cnt desc;
