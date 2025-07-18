create or replace view irae__gpt4_ranked as
select  distinct
        encounter_ref                       ,
        documentreference_ref               ,
        subject_ref                         ,
        enc_start_date                      ,
        enc_end_date                        ,
        doc_date                            ,
        rank_dt.ranking                     as donor_type,
        rank_dr.ranking                     as donor_relationship,
        donor_hla_match_quality	            ,
        donor_hla_mismatch_count	        ,
        rank_rx_therapy.ranking             as rx_therapeutic_therapeutic,
        rank_rx_therapy_sub.ranking         as rx_therapeutic_subtherapeutic,
        rank_rx_therapy_supra.ranking       as rx_therapeutic_supratherapeutic,
        rank_rx_compliance.ranking          as rx_compliance_compliant,
        rank_rx_compliance_partial.ranking  as rx_compliance_partial,
        rank_rx_compliance_non.ranking      as rx_compliance_noncompliant,
        rank_dsa.ranking                    as dsa_present,
        rank_viral.ranking                  as viral_infection_present,
        rank_infection.ranking              as infection_present,
        rank_bacterial.ranking              as bacterial_infection_present,
        rank_fungal.ranking                 as fungal_infection_present,
        rank_rejection.ranking              as graft_rejection_present,
        rank_failure.ranking                as graft_failure_present,
        rank_cancer.ranking                 as cancer_present,
        rank_ptld.ranking                   as ptld_present,
        error_found
from    irae__gpt4_fhir     as LLM,
        irae__ranking       as rank_dt,
        irae__ranking       as rank_dr,
        irae__ranking       as rank_rx_therapy,
        irae__ranking       as rank_rx_therapy_sub,
        irae__ranking       as rank_rx_therapy_supra,
        irae__ranking       as rank_rx_compliance,
        irae__ranking       as rank_rx_compliance_partial,
        irae__ranking       as rank_rx_compliance_non,
        irae__ranking       as rank_dsa,
        irae__ranking       as rank_infection,
        irae__ranking       as rank_viral,
        irae__ranking       as rank_bacterial,
        irae__ranking       as rank_fungal,
        irae__ranking       as rank_rejection,
        irae__ranking       as rank_failure,
        irae__ranking       as rank_ptld,
        irae__ranking       as rank_cancer
where   rank_dt.code = LLM.donor_type
and     rank_dr.code = LLM.donor_relationship
and     rank_rx_therapy.code = LLM.rx_therapeutic_therapeutic
and     rank_rx_therapy_sub.code = LLM.rx_therapeutic_subtherapeutic
and     rank_rx_therapy_supra.code = LLM.rx_therapeutic_supratherapeutic
and     rank_rx_compliance.code = LLM.rx_compliance_compliant
and     rank_rx_compliance_partial.code = LLM.rx_compliance_partial
and     rank_rx_compliance_non.code = LLM.rx_compliance_noncompliant
and     rank_dsa.code = LLM.dsa_present
and     rank_viral.code = LLM.viral_infection_present
and     rank_infection.code = LLM.infection_present
and     rank_bacterial.code = LLM.bacterial_infection_present
and     rank_fungal.code = LLM.fungal_infection_present
and     rank_rejection.code = LLM.graft_rejection_present
and     rank_failure.code = LLM.graft_failure_present
and     rank_cancer.code = LLM.cancer_present
and     rank_ptld.code = LLM.ptld_present
;