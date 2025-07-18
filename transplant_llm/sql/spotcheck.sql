select      count(distinct subject_ref)     as  cnt_patients,
            count(distinct encounter_ref)   as  cnt_encounters,
            rx_compliance_level,
            rx_compliance_partial,
            rx_compliance_non,
            rx_therapeutic_level,
            rx_therapeutic_sub,
            rx_therapeutic_supra
from        irae__gpt4_compliance
group by    rx_compliance_level,
            rx_compliance_partial,
            rx_compliance_non,
            rx_therapeutic_level,
            rx_therapeutic_sub,
            rx_therapeutic_supra
order by    rx_compliance_level,
            rx_compliance_partial,
            rx_compliance_non,
            rx_therapeutic_level,
            rx_therapeutic_sub,
            rx_therapeutic_supra;

