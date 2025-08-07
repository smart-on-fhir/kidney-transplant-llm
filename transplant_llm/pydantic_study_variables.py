from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class SpanAugmentedMention(BaseModel):
    is_present: bool | None  # True, False, or None
    spans: List[str]

###############################################################################
# Donor Characteristics
# 
# For a given transplant, these should be static over time 
###############################################################################

# Dates are treated as strings - no enum needed
class DonorTransplantDateMention(SpanAugmentedMention):
    transplant_date: str | None = Field(
        None,
        description='Date of renal transplant'
    )

class DonorType(str, Enum):
    Living = 'Donor was alive at time of renal transplant'
    Deceased = 'Donor was deceased at time of renal transplant'
    NotMentioned = "Donor was not mentioned as living or deceased"

class DonorTypeMention(SpanAugmentedMention):
    donor_type: DonorType = Field(
        DonorType.NotMentioned,
        description='Was the renal donor living at the time of transplant?'
    )

class DonorRelationship(str, Enum):
    Related = 'Donor was related to the renal transplant recipient'
    Unrelated = 'Donor was unrelated to the renal transplant recipient'
    NotMentioned = "Donor relationship status was not mentioned"

class DonorRelationshipMention(SpanAugmentedMention):
    donor_relationship: DonorRelationship = Field(
        DonorRelationship.NotMentioned,
        description='Was the renal donor related to the recipient?'
    )

class DonorHlaMatchQuality(str, Enum):
    Well = 'Well matched (0-1 mismatches)'
    Moderate = 'Moderately matched (2-4 mismatches)'
    Poor = 'Poorly matched (5-6 mismatches)'
    NotMentioned = "HLA match quality not mentioned"

class DonorHlaMatchQualityMention(SpanAugmentedMention):
    donor_hla_match_quality: DonorHlaMatchQuality = Field(
        DonorHlaMatchQuality.NotMentioned,
        description='What was the renal transplant HLA match quality?'
    )

class DonorHlaMismatchCount(str, Enum):
    Zero = 0
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    NotMentioned = 'HLA mismatch count not mentioned'

class DonorHlaMismatchCountMention(SpanAugmentedMention):
    donor_hla_mismatch_count: DonorHlaMismatchCount = Field(
        DonorHlaMismatchCount.NotMentioned,
        description='What was the renal donor-recipient HLA mismatch count?'
    )

###############################################################################
# Medication Compliance
# NOTE: Therapeutic mentions and compliance values modeled below are 
#       technically mutually exclusive (Therapeutic|Subtherapeutic|Supra, and 
#       compliance|non-compliance|partial). That said, we model them separately 
#       allowing for inconsistent responses because of how complex these values are
###############################################################################
class RxTherapeuticMention(SpanAugmentedMention):
    rx_therapeutic: bool | None = Field(
        None, 
        description='In the present encounter are immunosuppression levels documented as therapeutic or adequate?'
    )

class RxSubTherapeuticMention(SpanAugmentedMention):
    rx_subtherapeutic: bool | None = Field(
        None, 
        description='In the present encounter are immunosuppression levels documented as subtherapeutic or insufficient?'
    )

class RxSupraTherapeuticMention(SpanAugmentedMention):
    rx_supratherapeutic: bool | None = Field(
        None, 
        description='In the present encounter are immunosuppression levels documented as supratherapeutic or above therapeutic level?'
    )

class RxComplianceMention(SpanAugmentedMention):
    compliant: bool | None = Field(
        None, 
        description='In the present encounter is the patient documented as compliant with immunosuppressive medications?'
    )

class RxPartialComplianceMention(SpanAugmentedMention):
    partial: bool | None = Field(
        None, 
        description='In the present encounter is the patient documented as only partially compliant with immunosuppressive medications?'
    )

class RxNonComplianceMention(SpanAugmentedMention):
    noncompliant: bool | None = Field(
        None, 
        description='In the present encounter is the patient documented as noncompliant with immunosuppressive medications?'
    )


###############################################################################
# THE FOLLOWING DATA ELEMENTS TRACK BOTH 
# THE HISTORY AND THE PRESENT STATUS OF VARIABLES
###############################################################################

###############################################################################
# DSA Donor Specific Antibody
###############################################################################
class DSAPresent(str, Enum):
    Confirmed = "DSA diagnostic test positive, DSA diagnosis 'confirmed' or 'positive', or increase in immunosuppression due to DSA"
    Treatment = "DSA Treatment prescribed or DSA treatment administered"
    Suspected = "DSA suspected, DSA likely, DSA cannot be ruled out, DSA test result pending or DSA is a differential diagnosis"
    NoneOfTheAbove = "None of the above"

class DSAMention(SpanAugmentedMention):
    dsa_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of donor specific antibodies (DSA)?"
    )
    dsa_present: DSAPresent = Field(
        DSAPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of donor specific antibodies (DSA)?"
    )

############################################################################################################
# Infection (** Any **)
#   * necessary for PNA and UTI infections that often do not have a confirmed infection type!
#   * useful as a secondary check to ensure more specific infection types are not missed
############################################################################################################
class InfectionPresent(str, Enum):
    Confirmed = "Infection confirmed by laboratory test or imaging, infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to infection"
    Treatment = "Treatment prescribed/administered for infection (not including prophylaxis)"
    Suspected = "Infection is suspected, likely, cannot be ruled out, infection is a differential diagnosis or infectious test result is pending"
    NoneOfTheAbove = "None of the above"

class InfectionMention(SpanAugmentedMention):
    infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of an infection?"
    )
    infection_present: InfectionPresent = Field(
        InfectionPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of infection?"
    )

###############################################################################
# Infection (Viral)
###############################################################################
class ViralInfectionPresent(str, Enum):
    Confirmed = "Viral infection confirmed by laboratory test or imaging, viral infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to viral infection"
    Treatment = "Antiviral treatment prescribed/administered for viral infection (not including prophylaxis)"
    Suspected = "Viral infection is suspected, likely, cannot be ruled out, viral infection is a differential diagnosis or viral test result is pending"
    NoneOfTheAbove = "None of the above"

class ViralInfectionMention(SpanAugmentedMention):
    viral_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a viral infection?"
    )
    viral_infection_present: ViralInfectionPresent = Field(
        ViralInfectionPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of viral infection?"
    )

###############################################################################
# Infection (Bacterial)
###############################################################################
class BacterialInfectionPresent(str, Enum):
    Confirmed = "Bacterial infection confirmed by laboratory test or imaging, bacterial infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to bacterial infection"
    Treatment = "Antibacterial treatment prescribed/administered for bacterial infection (not including prophylaxis)"
    Suspected = "Bacterial infection is suspected, likely, cannot be ruled out, bacterial infection is a differential diagnosis or bacterial test result is pending"
    NoneOfTheAbove = "None of the above"

class BacterialInfectionMention(SpanAugmentedMention):
    bacterial_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a bacterial infection?"
    )
    bacterial_infection_present: BacterialInfectionPresent = Field(
        BacterialInfectionPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of bacterial infection?"
    )

###############################################################################
# Infection (Fungal)
###############################################################################
class FungalInfectionPresent(str, Enum):
    Confirmed = "Fungal infection confirmed by laboratory test or imaging, fungal infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to fungal infection"
    Treatment = "Antifungal treatment prescribed/administered for fungal infection (not including prophylaxis)"
    Suspected = "Fungal infection is suspected, likely, cannot be ruled out, fungal infection is a differential diagnosis or fungal test result is pending"
    NoneOfTheAbove = "None of the above"

class FungalInfectionMention(SpanAugmentedMention):
    fungal_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a fungal infection?"
    )
    fungal_infection_present: FungalInfectionPresent = Field(
        FungalInfectionPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of fungal infection?"
    )

###############################################################################
# Graft Rejection
###############################################################################
class GraftRejectionPresent(str, Enum):
    BiopsyProven = "Biopsy proven kidney graft rejection or pathology proven kidney graft rejection"
    Confirmed = "Kidney graft rejection was 'diagnosed', 'confirmed' or 'positive'"
    Treatment = "Treatment prescribed/administered for kidney rejection (AMR or TCMR)"
    Suspected = "Kidney graft rejection presumed, suspected, likely, cannot be ruled out, or biopsy result pending"
    NoneOfTheAbove = "None of the above"

class GraftRejectionMention(SpanAugmentedMention):
    graft_rejection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of kidney graft rejection?"
    )
    graft_rejection_present: GraftRejectionPresent = Field(
        GraftRejectionPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of kidney graft rejection?"
    )

###############################################################################
# Graft Failure
###############################################################################
class GraftFailurePresent(str, Enum):
    Confirmed = "Kidney graft has failed or kidney graft loss"
    Suspected = "Kidney graft failure presumed, suspected, likely, or cannot be ruled out"
    NoneOfTheAbove = "None of the above"

class GraftFailureMention(SpanAugmentedMention):
    graft_failure_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of kidney graft failure?"
    )
    graft_failure_present: GraftFailurePresent = Field(
        GraftFailurePresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of kidney graft failure?"
    )

###############################################################################
# PTLD
###############################################################################
class PTLDPresent(str, Enum):
    BiopsyProven = "Biopsy proven or pathology proven post transplant lymphoproliferative disorder (PTLD)"
    Confirmed = "Post transplant lymphoproliferative disorder (PTLD) was 'diagnosed', 'confirmed' or 'positive' or viral positive lymphoma"
    Treatment = "Treatment prescribed/administered for post transplant lymphoproliferative disorder (PTLD) or stopped immunosuppression due to PTLD"
    Suspected = "Post transplant lymphoproliferative disorder (PTLD) presumed, suspected, likely, cannot be ruled out, or PTLD biopsy result pending"
    NoneOfTheAbove = "None of the above"

class PTLDMention(SpanAugmentedMention):
    ptld_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of post transplant lymphoproliferative disorder (PTLD)?"
    )
    ptld_present: PTLDPresent = Field(
        PTLDPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of post transplant lymphoproliferative disorder (PTLD)?"
    )

###############################################################################
# Cancer
###############################################################################
class CancerPresent(str, Enum):
    BiopsyProven = "Biopsy proven or pathology proven cancer"
    Confirmed = "Cancer was 'diagnosed', 'confirmed' or 'positive'"
    Treatment = "Treatment prescribed/administered for cancer"
    Suspected = "Cancer is presumed, suspected, likely, cannot be ruled out, or biopsy of any lesion"
    NoneOfTheAbove = "None of the above"

class CancerMention(SpanAugmentedMention):
    cancer_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of cancer?"
    )
    cancer_present: CancerPresent = Field(
        CancerPresent.NoneOfTheAbove, 
        description="In the present encounter is there documented evidence of cancer?"
    )



###############################################################################
# Aggregated Annotation and Mention Classes 
###############################################################################

class KidneyTransplantAnnotation(BaseModel): 
    """
    An object-model for annotations of immune related adverse event (IRAE) 
    observations found in a patient's chart, relating specifically to kidney 
    transplants.
    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate 
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """
    donor_transplant_date_mention: DonorTransplantDateMention
    donor_type_mention: DonorTypeMention
    donor_relationship_mention: DonorRelationshipMention
    donor_hla_match_quality_mention: DonorHlaMatchQualityMention
    donor_hla_mismatch_count_mention: DonorHlaMismatchCountMention
    rx_therapeutic_mention: RxTherapeuticMention
    rx_sub_therapeutic_mention: RxSubTherapeuticMention
    rx_supra_therapeutic_mention: RxSupraTherapeuticMention
    rx_compliance_mention: RxComplianceMention
    rx_partial_compliance_mention: RxPartialComplianceMention
    rx_non_compliance_mention: RxNonComplianceMention
    dsa_mention: DSAMention
    infection_mention: InfectionMention
    viral_infection_mention: ViralInfectionMention
    bacterial_infection_mention: BacterialInfectionMention
    fungal_infection_mention: FungalInfectionMention
    graft_rejection_mention: GraftRejectionMention
    graft_failure_mention: GraftFailureMention
    ptld_mention: PTLDMention
    cancer_mention: CancerMention

# Enum describing all the relevant mention types' display labels
# Keys should be 1 to 1 with the KidneyTransplantAnnotation
# Labels aim to be as short as possible
class KidneyTransplantMentionLabels(Enum):
    donor_transplant_date_mention:      "Transplate Date"
    donor_type_mention:                 "Donor Type"
    donor_relationship_mention:         "Donor Relationship"
    donor_hla_match_quality_mention:    "Hla Match Quality"
    donor_hla_mismatch_count_mention:   "Hla Mismatch Count"
    rx_therapeutic_mention:             "Therapeutic"
    rx_sub_therapeutic_mention:         "Sub therapeutic"
    rx_supra_therapeutic_mention:       "Supra therapeutic"
    rx_compliance_mention:              "Rx compliance"
    rx_partial_compliance_mention:      "Rx partial compliance"
    rx_non_compliance_mention:          "Rx non compliance"
    dsa_mention:                        "DSA"
    infection_mention:                  "Infection"
    viral_infection_mention:            "Viral"
    bacterial_infection_mention:        "Bacterial"
    fungal_infection_mention:           "Fungal"
    graft_rejection_mention:            "Graft Rejection"
    graft_failure_mention:              "Graft Failure"
    ptld_mention:                       "PTLD"
    cancer_mention:                     "Cancer"
