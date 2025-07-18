create table irae__gpt4_compliance as
select
    distinct
    documentreference_ref               ,
    subject_ref                         ,
    encounter_ref                       ,
    enc_start_date                      ,
    enc_end_date                        ,    
    rx_therapeutic_is_present	        ,
    rx_therapeutic_therapeutic	        ,
    rx_therapeutic_subtherapeutic	    ,
    rx_therapeutic_supratherapeutic	    ,
    rx_compliance_is_present	        ,
    rx_compliance_compliant	            ,
    rx_compliance_partial	            ,
    rx_compliance_noncompliant          ,
    error
from irae__gpt4_fhir;

