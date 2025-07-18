create or replace view irae__gpt4_parsed as
select distinct
    concat('Patient/', split_part(filename, '.', 1))            as subject_ref,
    concat('DocumentReference/', split_part(filename, '.', 2))  as documentreference_ref,

    coalesce(dsa_mentioned, False)	    as dsa_mentioned,
    coalesce(dsa_history, False)        as dsa_history,
    case    when    dsa_present = ''
            then    'NoneOfTheAbove'
            else    dsa_present
            end as  dsa_present,

    coalesce(infection_mentioned, False)    as infection_mentioned,
    coalesce(infection_history, False)      as infection_history,
    case    when    infection_present = ''
            then    'NoneOfTheAbove'
            else    infection_present
            end as  infection_present,

    coalesce(viral_infection_mentioned, False)  as viral_infection_mentioned,
    coalesce(viral_infection_history, False)    as viral_infection_history,
    case    when    viral_infection_present = ''
            then    'NoneOfTheAbove'
            else    viral_infection_present
            end as  viral_infection_present,

    coalesce(bacterial_infection_mentioned, False)      as bacterial_infection_mentioned,
    coalesce(bacterial_infection_history, False)        as bacterial_infection_history,
    case    when    bacterial_infection_present = ''
            then    'NoneOfTheAbove'
            else    bacterial_infection_present
            end as  bacterial_infection_present,

    coalesce(fungal_infection_mentioned, False)         as fungal_infection_mentioned,
    coalesce(fungal_infection_history, False)           as fungal_infection_history,
    case    when    fungal_infection_present = ''
            then    'NoneOfTheAbove'
            else    fungal_infection_present
            end as fungal_infection_present,

    coalesce(graft_rejection_mentioned, False)          as graft_rejection_mentioned,
    coalesce(graft_rejection_history, False)            as graft_rejection_history,
    case    when    graft_rejection_present = ''
            then    'NoneOfTheAbove'
            else    graft_rejection_present
            end as  graft_rejection_present,

    coalesce(graft_failure_mentioned, False)            as graft_failure_mentioned,
    coalesce(graft_failure_history, False)              as graft_failure_history,
    case    when    graft_failure_present = ''
            then    'NoneOfTheAbove'
            else    graft_failure_present
            end as  graft_failure_present,

    coalesce(ptld_mentioned, False)             as ptld_mentioned,
    coalesce(ptld_history, False)               as ptld_history,
    case    when    ptld_present = ''
            then    'NoneOfTheAbove'
            else    ptld_present
            end as  ptld_present,

    coalesce(cancer_mentioned, False)           as cancer_mentioned,
    coalesce(cancer_history, False)             as cancer_history,
    case    when    cancer_present = ''
            then    'NoneOfTheAbove'
            else    cancer_present
            end as  cancer_present,

    coalesce(donor_transplant_date_mentioned, False) as donor_transplant_date_mentioned,
    donor_transplant_date,

    coalesce(donor_type_mentioned, False)            as donor_type_mentioned,
    case    when    donor_type = ''
            then    'NotMentioned'
            else    donor_type
            end as  donor_type,

    coalesce(donor_relationship_mentioned, False)       as donor_relationship_mentioned,
    case    when    donor_relationship = ''
            then    'NotMentioned'
            else    donor_relationship
            end as  donor_relationship,

    coalesce(donor_hla_match_quality_mentioned, False)  as donor_hla_match_quality_mentioned,
    case    when    donor_hla_match_quality = ''
            then    'NotMentioned'
            else    donor_hla_match_quality
            end as  donor_hla_match_quality,

    coalesce(donor_hla_mismatch_count_mentioned, False) as donor_hla_mismatch_count_mentioned,
    case    when    donor_hla_mismatch_count = ''
            then    'NotMentioned'
            else    donor_hla_mismatch_count
            end as  donor_hla_mismatch_count,

    coalesce(rx_therapeutic_mentioned, False)               as rx_therapeutic_mentioned,

    case    when rx_therapeutic_therapeutic = ''
            then    'NotMentioned'
            else    rx_therapeutic_therapeutic
            end as  rx_therapeutic_therapeutic,

    case    when    rx_therapeutic_subtherapeutic = ''
            then    'NotMentioned'
            else    rx_therapeutic_subtherapeutic
            end as  rx_therapeutic_subtherapeutic,

    case    when    rx_therapeutic_supratherapeutic = ''
            then    'NotMentioned'
            else    rx_therapeutic_supratherapeutic
            end as  rx_therapeutic_supratherapeutic,

    coalesce(rx_compliance_mentioned, False)    as rx_compliance_mentioned,
    case    when    rx_compliance_compliant = ''
            then    'NotMentioned'
            else    rx_compliance_compliant
            end as  rx_compliance_compliant,

    case    when    rx_compliance_partial = ''
            then    'NotMentioned'
            else    rx_compliance_partial
            end as  rx_compliance_partial,

    case    when    rx_compliance_noncompliant = ''
            then    'NotMentioned'
            else    rx_compliance_noncompliant
            end as  rx_compliance_noncompliant,
    "filename",
    error_found
from    irae__gpt4_raw;