from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class SpanAugmentedMention(BaseModel):
    is_present: Optional[bool]  # True, False, or None
    spans: List[str]

###############################################################################
# Donor Characteristics
###############################################################################

# Dates are treated as strings - no enum needed
class DonorTransplantDateMention(SpanAugmentedMention):
    transplant_date: str = Field(
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
    donor_hla_quality: DonorHlaMatchQuality = Field(
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
    donor_hla_mismatch: DonorHlaMismatchCount = Field(
        DonorHlaMismatchCount.NotMentioned,
        description='What was the renal donor-recipient HLA mismatch count?'
    )

###############################################################################
# Medication Compliance
###############################################################################
# TO DISCUSS: Why is this a mention with 3-different fields and not just an enum
# then modelled as a mention. 
# Assuming this is a mistake and fixing
class RxTherapeutic(str, Enum):
    therapeutic = 'Immunosuppression levels are documented as therapeutic or adequate.'
    subtherapeutic = 'Immunosuppression levels are documented as subtherapeutic or insufficient.'
    supratherapeutic = 'Immunosuppression levels are documented as supratherapeutic or above therapeutic level.'
    NotMentioned = 'Immunosuppression levels are not documented or mentioned at a therapeutic level.'


class RxTherapeuticMention(SpanAugmentedMention):
    therapeutic_status : Optional[RxTherapeutic]= Field(
        None, 
        description='What type of therapeutic-level immunosuppression levels are documented for the patient?'
    ) 

class RxCompliance(str, Enum):
    compliant ='The patient is compliant with immunosuppressive medications.'
    partial ='The patient is only partially compliant with immunosuppressive medications.'
    noncompliant ='The patient is noncompliant with immunosuppressive medications.'
    NotMentioned = 'Immunosuppressive medication compliance was not documented or mentioned.'

class RxComplianceMention(SpanAugmentedMention):
    compliance_status : RxCompliance= Field(
        None, 
        description='What type of immunosuppressive medication compliance is mentioned?'
    ) 

###############################################################################
# DSA Donor Specific Antibody
###############################################################################
class DSAPresent(str, Enum):
    Confirmed = "DSA diagnostic test positive, DSA diagnosis 'confirmed' or 'positive', or increase in immunosuppression due to DSA"
    Treatment = "DSA Treatment prescribed or DSA treatment administered"
    Suspected = "DSA suspected, DSA likely, DSA cannot be ruled out, DSA test result pending or DSA is a differential diagnosis"
    NoneOfTheAbove = "None of the above"

class DSAMention(SpanAugmentedMention):
    dsa_history: bool = Field(False, description="Has the patient ever had donor specific antibodies (DSA)?")
    dsa_present: DSAPresent = Field(
        DSAPresent.NoneOfTheAbove, 
        description="Is there documented evidence of donor specific antibodies (DSA) in the present encounter?"
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
    infection_history: bool = Field(False, description="Has the patient ever had an infection?")
    infection_present: InfectionPresent = Field(
        InfectionPresent.NoneOfTheAbove, description="Is there documented evidence of infection in the present encounter?")

###############################################################################
# Infection (Viral)
###############################################################################
class ViralInfectionPresent(str, Enum):
    Confirmed = "Viral infection confirmed by laboratory test or imaging, viral infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to viral infection"
    Treatment = "Antiviral treatment prescribed/administered for viral infection (not including prophylaxis)"
    Suspected = "Viral infection is suspected, likely, cannot be ruled out, viral infection is a differential diagnosis or viral test result is pending"
    NoneOfTheAbove = "None of the above"

class ViralInfectionMention(SpanAugmentedMention):
    viral_history: bool = Field(False, description="Has the patient ever had a viral infection?")
    viral_present: ViralInfectionPresent = Field(
        ViralInfectionPresent.NoneOfTheAbove, description="Is there documented evidence of viral infection in the present encounter?")

###############################################################################
# Infection (Bacterial)
###############################################################################
class BacterialInfectionPresent(str, Enum):
    Confirmed = "Bacterial infection confirmed by laboratory test or imaging, bacterial infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to bacterial infection"
    Treatment = "Antibacterial treatment prescribed/administered for bacterial infection (not including prophylaxis)"
    Suspected = "Bacterial infection is suspected, likely, cannot be ruled out, bacterial infection is a differential diagnosis or bacterial test result is pending"
    NoneOfTheAbove = "None of the above"

class BacterialInfectionMention(SpanAugmentedMention):
    bacterial_history: bool = Field(False, description="Has the patient ever had a bacterial infection?")
    bacterial_present: BacterialInfectionPresent = Field(
        BacterialInfectionPresent.NoneOfTheAbove, description="Is there documented evidence of bacterial infection in the present encounter?")

###############################################################################
# Infection (Fungal)
###############################################################################
class FungalInfectionPresent(str, Enum):
    Confirmed = "Fungal infection confirmed by laboratory test or imaging, fungal infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to fungal infection"
    Treatment = "Antifungal treatment prescribed/administered for fungal infection (not including prophylaxis)"
    Suspected = "Fungal infection is suspected, likely, cannot be ruled out, fungal infection is a differential diagnosis or fungal test result is pending"
    NoneOfTheAbove = "None of the above"

class FungalInfectionMention(SpanAugmentedMention):
    fungal_history: bool = Field(False, description="Has the patient ever had a fungal infection?")
    fungal_present: FungalInfectionPresent = Field(
        FungalInfectionPresent.NoneOfTheAbove, description="Is there documented evidence of fungal infection in the present encounter?")

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
    rejection_history: bool = Field(False, description="Has the patient ever had kidney graft rejection?")
    rejection_present: GraftRejectionPresent = Field(
        GraftRejectionPresent.NoneOfTheAbove, description="Is there documented evidence of kidney graft rejection in the present encounter?")

###############################################################################
# Graft Failure
###############################################################################
class GraftFailurePresent(str, Enum):
    Confirmed = "Kidney graft has failed or kidney graft loss"
    Suspected = "Kidney graft failure presumed, suspected, likely, or cannot be ruled out"
    NoneOfTheAbove = "None of the above"

class GraftFailureMention(SpanAugmentedMention):
    failure_history: bool = Field(False, description="Has the patient ever had kidney graft failure?")
    failure_present: GraftFailurePresent = Field(
        GraftFailurePresent.NoneOfTheAbove, description="Is there documented evidence of kidney graft failure in the present encounter?")

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
    ptld_history: bool = Field(False, description="Has the patient ever had post transplant lymphoproliferative disorder (PTLD)?")
    ptld_present: PTLDPresent = Field(
        PTLDPresent.NoneOfTheAbove, description="Is there documented evidence of post transplant lymphoproliferative disorder (PTLD) in the present encounter?")

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
    cancer_history: bool = Field(False, description="Has the patient ever had cancer?")
    cancer_present: CancerPresent = Field(
        CancerPresent.NoneOfTheAbove, description="Is there documented evidence of cancer in the present encounter?")



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
    donor_transplant_date: DonorTransplantDateMention
    donor_type: DonorTypeMention
    donor_relationship: DonorRelationshipMention
    donor_hla_match_quality: DonorHlaMatchQualityMention
    donor_hla_mismatch_count: DonorHlaMismatchCountMention
    rx_therapeutic: RxTherapeuticMention
    rx_compliance: RxComplianceMention
    dsa: DSAMention
    infection: InfectionMention
    viral_infection: ViralInfectionMention
    bacterial_infection: BacterialInfectionMention
    fungal_infection: FungalInfectionMention
    graft_rejection: GraftRejectionMention
    graft_failure: GraftFailureMention
    ptld: PTLDMention
    cancer: CancerMention

# Enum describing all the relevant mention types' display labels
# Keys should be 1 to 1 with the KidneyTransplantAnnotation
class KidneyTransplantMentionLabels(Enum):
    donor_transplant_date: "Donor Transplate Date"
    donor_type: "Donor Type"
    donor_relationship: "Donor Relationship"
    donor_hla_match_quality: "Donor Hla Match Quality"
    donor_hla_mismatch_count: "Donor Hla Mismatch Count"
    rx_therapeutic: "Immunosuppresion levels - therapeutic"
    rx_compliance: "Immunosuppresion medication compliance"
    dsa: "Donor Specific Antibodies"
    infection: "Infection"
    viral_infection: "Viral Infection"
    bacterial_infection: "Bacterial Infection"
    fungal_infection: "Fungal Infection"
    graft_rejection: "Graft Rejection"
    graft_failure: "Graft Failure"
    ptld: "Post-transplant lymphoproliferative disorder"
    cancer: "Cancer"
