create TABLE irae__gpt4_compliance as
with comparable as
(
    SELECT  distinct
            documentreference_ref               ,
            subject_ref                         ,
            encounter_ref                       ,
            enc_start_date                      ,
            enc_end_date                        ,
            doc_date                            ,
            rank_rx_therapy.ranking             as rx_therapeutic_level,
            rank_rx_therapy_sub.ranking         as rx_therapeutic_sub,
            rank_rx_therapy_supra.ranking       as rx_therapeutic_supra,
            rank_rx_compliance.ranking          as rx_compliance_level,
            rank_rx_compliance_partial.ranking  as rx_compliance_partial,
            rank_rx_compliance_non.ranking      as rx_compliance_non
    FROM    irae__gpt4_fhir     as LLM,
            irae__ranking       as rank_rx_therapy,
            irae__ranking       as rank_rx_therapy_sub,
            irae__ranking       as rank_rx_therapy_supra,
            irae__ranking       as rank_rx_compliance,
            irae__ranking       as rank_rx_compliance_partial,
            irae__ranking       as rank_rx_compliance_non
    WHERE   rank_rx_therapy.code = LLM.rx_therapeutic_level
    and     rank_rx_therapy_sub.code = LLM.rx_therapeutic_sub
    and     rank_rx_therapy_supra.code = LLM.rx_therapeutic_supra
    and     rank_rx_compliance.code = LLM.rx_compliance_level
    and     rank_rx_compliance_partial.code = LLM.rx_compliance_partial
    and     rank_rx_compliance_non.code = LLM.rx_compliance_non
),
note_score as
(
    select  distinct
            (rx_therapeutic_level + rx_compliance_level)    as compliant,
            (rx_therapeutic_sub + rx_compliance_partial)    as compliant_partial,
            (rx_therapeutic_sub + rx_compliance_non)        as compliant_non,
            comparable.*
    from    comparable
)
select * from note_score;

with visit as
(
    select  encounter_ref,
            sum(compliant)          as compliant,
            sum(compliant_partial)  as compliant_partial,
            sum(compliant_non)      as compliant_non
    from irae__gpt4_compliance
    group by encounter_ref
)
SELECT  case    when    compliant=0 and compliant_partial=0 and compliant_non=0 then 'NotMentioned'
                when    compliant > compliant_partial and compliant > compliant_non then 'level'
                else    'todo'
                end as  compliant
FROM    visit
limit 50;


