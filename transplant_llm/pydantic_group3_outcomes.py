from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class SpanAugmentedMention(BaseModel):
    is_present: Optional[bool]  # True, False, or None
    spans: List[str]

###############################################################################
# DSA Donor Specific Antibody
###############################################################################
class DSAPresent(str, Enum):
    Confirmed = "DSA diagnostic test positive, DSA diagnosis 'confirmed' or 'positive', or increase in immunosuppression due to DSA"
    Treatment = "DSA Treatment prescribed or DSA treatment administered"
    Suspected = "DSA suspected, DSA likely, DSA cannot be ruled out, DSA test result pending or DSA is a differential diagnosis"
    NoneOfTheAbove = "None of the above"

class DSAMention(SpanAugmentedMention):
    dsa_mentioned: bool = Field(False, description="Are donor specific antibodies (DSA) mentioned?")
    dsa_history: bool = Field(False, description="Has the patient ever had donor specific antibodies (DSA)?")
    dsa_present: DSAPresent = Field(
        DSAPresent.NoneOfTheAbove, description="Is there documented evidence of donor specific antibodies (DSA) in the present encounter?")

############################################################################################################
# Infection (** Any **)
#   * necessary for PNA and UTI infections that often do not have a confirmed infection type!
#   * useful as a secondary check to ensure more specific infection types are not missed
############################################################################################################
class InfectionPresent(str, Enum):
    Confirmed = "Infection confirmed by laboratory test or imaging, infection diagnosed 'confirmed' or 'positive', or reduced immunosuppression due to infection"
    Treatment = "Treatment prescribed/administered for infection (not including prophylaxis)"
    Suspected = "Infection is suspected, likely, cannot be ruled out, infection is a differential diagnosis or viral test result is pending"
    NoneOfTheAbove = "None of the above"

class InfectionMention(SpanAugmentedMention):
    infection_mentioned: bool = Field(False, description="Is infection mentioned?")
    infection_history: bool = Field(False, description="Has the patient ever had an infection?")
    infection_present: InfectionPresent = Field(
        InfectionPresent.NoneOfTheAbove, description="Is there documented evidence of infection in the present encounter?")

###############################################################################
# Infection (Viral)
###############################################################################
class ViralInfectionPresent(str, Enum):
    Confirmed = "Viral infection confirmed by laboratory test or imaging, viral infection diagnosed 'confirmed' or 'positive', or reduced immunosuppression due to viral infection"
    Treatment = "Antiviral treatment prescribed/administered for viral infection (not including prophylaxis)"
    Suspected = "Viral infection is suspected, likely, cannot be ruled out, viral infection is a differential diagnosis or viral test result is pending"
    NoneOfTheAbove = "None of the above"

class ViralInfectionMention(SpanAugmentedMention):
    viral_infection_mentioned: bool = Field(False, description="Is viral infection mentioned?")
    viral_infection_history: bool = Field(False, description="Has the patient ever had a viral infection?")
    viral_infection_present: ViralInfectionPresent = Field(
        ViralInfectionPresent.NoneOfTheAbove, description="Is there documented evidence of viral infection in the present encounter?")

###############################################################################
# Infection (Bacterial)
###############################################################################
class BacterialInfectionPresent(str, Enum):
    Confirmed = "Bacterial infection confirmed by laboratory test or imaging, bacterial infection diagnosed 'confirmed' or 'positive', or reduced immunosuppression due to bacterial infection"
    Treatment = "Antibacterial treatment prescribed/administered for bacterial infection (not including prophylaxis)"
    Suspected = "Bacterial infection is suspected, likely, cannot be ruled out, bacterial infection is a differential diagnosis or bacterial test result is pending"
    NoneOfTheAbove = "None of the above"

class BacterialInfectionMention(SpanAugmentedMention):
    bacterial_infection_mentioned: bool = Field(False, description="Is bacterial infection mentioned?")
    bacterial_infection_history: bool = Field(False, description="Has the patient ever had a bacterial infection?")
    bacterial_infection_present: BacterialInfectionPresent = Field(
        BacterialInfectionPresent.NoneOfTheAbove, description="Is there documented evidence of bacterial infection in the present encounter?")

###############################################################################
# Infection (Fungal)
###############################################################################
class FungalInfectionPresent(str, Enum):
    Confirmed = "Fungal infection confirmed by laboratory test or imaging, fungal infection diagnosed 'confirmed' or 'positive', or reduced immunosuppression due to fungal infection"
    Treatment = "Antifungal treatment prescribed/administered for fungal infection (not including prophylaxis)"
    Suspected = "Fungal infection is suspected, likely, cannot be ruled out, fungal infection is a differential diagnosis or fungal test result is pending"
    NoneOfTheAbove = "None of the above"

class FungalInfectionMention(SpanAugmentedMention):
    fungal_infection_mentioned: bool = Field(False, description="Is fungal infection mentioned?")
    fungal_infection_history: bool = Field(False, description="Has the patient ever had a fungal infection?")
    fungal_infection_present: FungalInfectionPresent = Field(
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
    graft_rejection_mentioned: bool = Field(False, description="Is kidney graft rejection mentioned?")
    graft_rejection_history: bool = Field(False, description="Has the patient ever had kidney graft rejection?")
    graft_rejection_present: GraftRejectionPresent = Field(
        GraftRejectionPresent.NoneOfTheAbove, description="Is there documented evidence of kidney graft rejection in the present encounter?")

###############################################################################
# Graft Failure
###############################################################################
class GraftFailurePresent(str, Enum):
    Confirmed = "Kidney graft has failed or kidney graft loss"
    Suspected = "Kidney graft failure presumed, suspected, likely, or cannot be ruled out"
    NoneOfTheAbove = "None of the above"

class GraftFailureMention(SpanAugmentedMention):
    graft_failure_mentioned: bool = Field(False, description="Is kidney graft failure mentioned?")
    graft_failure_history: bool = Field(False, description="Has the patient ever had kidney graft failure?")
    graft_failure_present: GraftFailurePresent = Field(
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
    ptld_mentioned: bool = Field(False, description="Is post transplant lymphoproliferative disorder (PTLD) mentioned?")
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
    cancer_mentioned: bool = Field(False, description="Is cancer mentioned?")
    cancer_history: bool = Field(False, description="Has the patient ever had cancer?")
    cancer_present: CancerPresent = Field(
        CancerPresent.NoneOfTheAbove, description="Is there documented evidence of cancer in the present encounter?")
