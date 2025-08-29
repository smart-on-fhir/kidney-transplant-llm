# MedicationRequest [STU4](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest.html)

## MedicationRequest.[status](https://build.fhir.org/valueset-medicationrequest-status.html)

>   select  count(distinct subject_ref)   as cnt_pat,
            count(distinct encounter_ref) as cnt_enc,
            count(medicationrequest_ref)  as cnt_med,
            status 
    from    core__medicationrequest
    group by status order by cnt_pat desc, cnt_enc desc

* completed
* active 
* stopped 
* canceled
* on-hold

## MedicationRequest.[intent](https://build.fhir.org/valueset-medicationrequest-intent.html)

>   select  count(distinct subject_ref)   as cnt_pat,
            count(distinct encounter_ref) as cnt_enc,
            count(medicationrequest_ref)  as cnt_med,
            intent 
    from    core__medicationrequest
    group by intent order by cnt_pat desc, cnt_enc desc

* plan 
* order 

## MedicationRequest.[category](https://build.fhir.org/valueset-medicationrequest-admin-location.html)

>   select  count(distinct subject_ref)   as cnt_pat,
            count(distinct encounter_ref) as cnt_enc,
            count(medicationrequest_ref)  as cnt_med,
            category_code 
    from    core__medicationrequest
    group by category_code order by cnt_pat desc, cnt_enc desc

Epic 
* community
* discharge
* inpatient
* outpatient

Cerner 
* charge-only (?)
* community
* discharge
* inpatient
* outpatient
* patientspecified (?)


## MedicationRequest.[dispenseRequest](https://build.fhir.org/medicationrequest-definitions.html#MedicationRequest.dispenseRequest) 

>   select  count(distinct subject)   as cnt_pat,
            count(distinct encounter) as cnt_enc,
            count(id)  as cnt_med,
            dispenseRequest 
    from    medicationrequest
    group by dispenseRequest order by cnt_pat desc, cnt_enc desc

## MedicationRequest.[dosageInstruction](https://build.fhir.org/medicationrequest-definitions.html#MedicationRequest.dosageInstruction)

>   select  count(distinct subject)   as cnt_pat,
            count(distinct encounter) as cnt_enc,
            count(id)  as cnt_med,
            dosageInstruction 
    from    medicationrequest
    group by dosageInstruction order by cnt_pat desc, cnt_enc desc
