# Goals
1. Obtain high quality medication data from EHR  
  * FHIR MedicationRequest [STU4](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest.html) coded data  
  * LLM chart review   
    * [medicationrequest.py](medicationrequest.py) is a generic PyDantic class for this task
      * Allow specific drug class/ingredients to use a base funtionality with specific rules as needed
        * [immunosuppression.py](ingredients/immunosuppression.py)
        * [infection.py](ingredients/infection.py)
        * [cancer.py](ingredients/cancer.py)
        * [kidney.py](ingredients/kidney.py)
        
2. Calculate "**Drug Eras**" to define when the patient was "actively" on a medication.

# Drug Eras
_METHODS_ : "Medication exposure was derived from FHIR MedicationRequest. 
For each immunosuppressant drug ingredient, the drug era start and end dates were derived from the FHIR medication request. 
The preferred source of start date and end date was the “validity period” when available. 
If the validity period start date was empty, the “authored on” date was used. 
If the end date was empty, the end date was calculated using “dosage instructions” containing drug quantity and frequency: 
the expected number of medicated days was derived from the number of doses requested and the usage frequency. 

If the stop date could not be calculated, a fallback convention was used: set expected duration 30 days for outpatient medications, and length of stay (days) for inpatient medications. 
If the status changed to “stopped” or status changed with an explicit stop date, the end date was set accordingly." 

# Table of Contents
- [status](#status)
- [intent](#intent)
- [category](#category)
- [dispenseRequest](#dispenserequest)
  - [validityPeriod](#dispenserequestvalidityperiod)
  - [expectedSupplyDuration](#dispenserequestexpectedsupplyduration)
  - [quantity](#dispenserequestquantity)
  - [numberOfRepeatsAllowed](#dispenserequestnumberofrepeatsallowed)
- [dosageInstruction](#dosageinstruction)
  - [doseQuantity](#dosageinstructiondosequantity)
  - [timing](#dosageinstructiontiming)
  - [rateQuantity](#dosageinstructionratequantity)
  - [route](#dosageinstructionroute)
- [Epic-Cerner differences](#epic-cerner-differences)


## [status](https://build.fhir.org/valueset-medicationrequest-status.html)

Status: 
* completed
* active 
* stopped
* canceled
* on-hold

```
select  count(distinct subject_ref)   as cnt_pat,
        count(distinct encounter_ref) as cnt_enc,
        count(medicationrequest_ref)  as cnt_med,
        status 
from    core__medicationrequest
group   by status 
order   by cnt_pat desc, cnt_enc desc
```
--------------------------------------------------------------------------
## [intent](https://build.fhir.org/valueset-medicationrequest-intent.html)
 
Intent:  
* plan 
* order 

```
select  count(distinct subject_ref)   as cnt_pat,
        count(distinct encounter_ref) as cnt_enc,
        count(medicationrequest_ref)  as cnt_med,
        intent 
from    core__medicationrequest
group   by intent 
order   by cnt_pat desc, cnt_enc desc
```

--------------------------------------------------------------------------
## [category](https://build.fhir.org/valueset-medicationrequest-admin-location.html)

**Epic** 
* community
* discharge
* inpatient
* outpatient

**Cerner** 
* charge-only --> _Other or None_  
* community
* discharge
* inpatient
* outpatient
* patientspecified --> _community_

```
select  count(distinct subject_ref)   as cnt_pat,
        count(distinct encounter_ref) as cnt_enc,
        count(medicationrequest_ref)  as cnt_med,
        category_code 
from    core__medicationrequest
group   by category_code 
order   by cnt_pat desc, cnt_enc desc
```

--------------------------------------------------------------------------
## [dispenseRequest](https://build.fhir.org/medicationrequest-definitions.html#MedicationRequest.dispenseRequest) 

### dispenseRequest.[validityPeriod](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.validityPeriod)

_Example_
```json
{ "start": "2024-12-19",
  "end": "2024-12-19"}
```


```
select  count(distinct subject)     as cnt_pat,
        count(distinct encounter)   as cnt_enc,
        count(id)                   as cnt_med,
        dispenseRequest.validityPeriod 
from    medicationrequest
group   by dispenseRequest.validityPeriod
order   by cnt_pat desc, cnt_enc desc
```

### dispenseRequest.[expectedSupplyDuration](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.expectedSupplyDuration)

Example 
```json
{
  "code": "d",
  "system": "http://unitsofmeasure.org",
  "unit": "Day",
  "value": 30.0
}
```

```
select  count(distinct subject)     as cnt_pat,
        count(distinct encounter)   as cnt_enc,
        count(id)                   as cnt_med,
        dispenseRequest.expectedSupplyDuration 
from    medicationrequest
group   by dispenseRequest.expectedSupplyDuration
order   by cnt_pat desc, cnt_enc desc
```

### dispenseRequest.[quantity](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.quantity)

Example 
```json
{ "unit" : "tablet", 
  "value" : "30.0"}
```

```
select  count(distinct subject)     as cnt_pat,
        count(distinct encounter)   as cnt_enc,
        count(id)                   as cnt_med,
        dispenseRequest.quantity 
from    medicationrequest
group   by dispenseRequest.quantity
order   by cnt_pat desc, cnt_enc desc
```

### dispenseRequest.[numberOfRepeatsAllowed](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dispenseRequest.numberOfRepeatsAllowed)

Example 
```json
{ "numberOfRepeatsAllowed" : "3"}
```

```
select  count(distinct subject)     as cnt_pat,
        count(distinct encounter)   as cnt_enc,
        count(id)                   as cnt_med,
        dispenseRequest.numberOfRepeatsAllowed
from    medicationrequest
group   by dispenseRequest.numberOfRepeatsAllowed
order   by cnt_pat desc, cnt_enc desc
```

--------------------------------------------------------------------------
## [dosageInstruction](https://build.fhir.org/medicationrequest-definitions.html#MedicationRequest.dosageInstruction)

* [GPT5 suggested units](https://chatgpt.com/share/68b73db3-38e0-800f-9341-6c3ebc2f0e8e)

 ### dosageInstruction.[doseQuantity](http://hl7.org/fhir/R4/dosage.html#Dosage)

_example:_ 
```json 
{"code" : "mg", 
"system" : "http://unitsofmeasure.org", 
"unit" : "mg", 
"value" : "2.0"}
```

```
select  count(distinct subject)     as cnt_pat, 
        count(distinct id)          as cnt_med, 
        DAR.doseQuantity 
from    medicationRequest           as MR, 
        UNNEST(dosageInstruction)   as t(DI), 
        UNNEST(DI.doseAndRate)      as t(DAR)
where   dosageInstruction is not NULL  
group   by DAR.doseQuantity      
order   by cnt_pat desc, cnt_med desc 
```

 ### dosageInstruction.[timing](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest-definitions.html#MedicationRequest.dosageInstruction.timing)

**Notice** 
* Timing codes [DataType](http://hl7.org/fhir/R4/datatypes.html#Timing) is usually NULL.
* Timing text (and display) are more reliable
Typical immunosuppression dosage frequency (timing) 

| Drug Class            | Common Frequency | FHIR `timing` Representation                    |
| --------------------- | ---------------- | ----------------------------------------------- |
| Calcineurin Inhibitor | q12h (BID)       | `repeat.frequency=1, period=12, periodUnit="h"` |
| Antimetabolite        | q12h (BID)       | Same as above                                   |
| Prednisone            | q24h (QD)        | `repeat.frequency=1, period=1, periodUnit="d"`  |
| mTOR Inhibitors       | QD / BID         | QD: `period=1d`; BID: `period=12h`              |
| Belatacept            | q2w → q4w        | `period=2wk` then `period=4wk`                  |
| ATG / Basiliximab     | Discrete dates   | `timing.event` list                             |


_Example:_ Ideally populated but non-existent in real world BCH data (Neither Cerner nor Epic)  
```json 
{
  "repeat": {
    "frequency": 2,
    "period": 1,
    "periodUnit": "d"
  },
  "code": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v3-GTSAbbreviation",
        "code": "BID",
        "display": "2 times a day"
      }
    ]
  }
}
```

Example: Rare and also can't be assumed to exist 
```json 
{
  "code": "229799001",
  "display": "Twice a day (qualifier value)",
  "system": "http://snomed.info/sct",
}
```

_Example_: sometimes TEXT/display is available  

```json
{
  "id": null,
  "coding": null,
  "text": "Once a week"
}
```


```
select  count(distinct subject)     as cnt_pat, 
        count(distinct id)          as cnt_med, 
        DI.timing
from    medicationRequest           as MR, 
        UNNEST(dosageInstruction)   AS t(DI)
where   dosageInstruction is not NULL  
group   by DI.timing 
order   by cnt_pat desc, cnt_med desc 
```

### dosageInstruction.[rateQuantity](http://hl7.org/fhir/R4/dosage.html#Dosage)

_example:_ 
```json
{
  "unit": "mL/hr",
  "value": 100.0,
  "code": "mL/h",
  "system": "http://unitsofmeasure.org"
}
```

```
select  count(distinct subject)  as cnt_pat, 
        count(distinct id)  as cnt_med, 
        DAR.rateQuantity 
from    medicationRequest           as MR, 
        UNNEST(dosageInstruction)   as t(DI), 
        UNNEST(DI.doseAndRate)      as t(DAR)
where   dosageInstruction is not NULL  
group   by DAR.rateQuantity      
order   by cnt_pat desc, cnt_med desc 
```


### dosageInstruction.[route](http://hl7.org/fhir/R4/dosage.html#Dosage)
_example:_ 
```json
{
  "code": "47625008",
  "display": "Intravenous route (qualifier value)",
  "system": "http://snomed.info/sct"
}
```

```
select  count(distinct subject)     as cnt_pat, 
        count(distinct id)          as cnt_med, 
        RouteCoding.display
from    medicationRequest           as MR, 
        UNNEST(dosageInstruction)   as t(DI), 
        UNNEST(DI.route.coding)     AS t(RouteCoding)
where   dosageInstruction is not NULL  
group   by RouteCoding.display
order   by cnt_pat desc, cnt_med desc 
```

## Epic-Cerner differences
NULL is common, Epic vs Cerner have different "inline" strategies for the FHIR MedicationRequest object.  
```
select distinct form, ingredient from medication
```
"[MedicationRequest](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-medicationrequest.html) resources can represent a medication using either a code, or reference"
Each MedicationRequest must have
* a `status`
* an `intent` code
* a medication (see guidance below)
* a patient
* a prescriber"

"MedicationRequest resources can represent a medication using either a `code`, or reference a `Medication` resource." 



