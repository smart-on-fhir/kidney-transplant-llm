select      count(distinct subject_ref)     as  cnt_patients,
            count(distinct encounter_ref)   as  cnt_encounters,
            rx_compliance_compliant,
            rx_compliance_partial,
            rx_compliance_noncompliant,
            rx_therapeutic_therapeutic,
            rx_therapeutic_subtherapeutic,
            rx_therapeutic_supratherapeutic
from        irae__gpt4_compliance
group by    rx_compliance_compliant,
            rx_compliance_partial,
            rx_compliance_noncompliant,
            rx_therapeutic_therapeutic,
            rx_therapeutic_subtherapeutic,
            rx_therapeutic_supratherapeutic
order by    rx_compliance_compliant,
            rx_compliance_partial,
            rx_compliance_noncompliant,
            rx_therapeutic_therapeutic,
            rx_therapeutic_subtherapeutic,
            rx_therapeutic_supratherapeutic;

