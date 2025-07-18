create or replace view irae__gpt4_summary as
select
    distinct
    documentreference_ref               ,
    subject_ref                         ,
    encounter_ref                       ,
    enc_start_date                      ,
    enc_end_date                        ,
    donor_type	                        ,
    donor_relationship	                ,
    donor_hla_match_quality	            ,
    donor_hla_mismatch_count	        ,
    rx_therapeutic_therapeutic	        ,
    rx_therapeutic_subtherapeutic	    ,
    rx_therapeutic_supratherapeutic	    ,
    rx_compliance_compliant	            ,
    rx_compliance_partial	            ,
    rx_compliance_noncompliant	        ,
    dsa_present                         ,
    viral_infection_present	            ,
    infection_present	                ,
    bacterial_infection_present	        ,
    fungal_infection_present	        ,
    graft_rejection_present	            ,
    graft_failure_present	            ,
    cancer_present	                    ,
    ptld_present                        ,
    error
from irae__gpt4_fhir;

