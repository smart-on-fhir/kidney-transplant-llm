from enum import StrEnum
from pydantic import BaseModel, Field

class SpanAugmentedMention(BaseModel):
    has_mention: bool | None  # True, False, or None
    spans: list[str]

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

class DonorType(StrEnum):
    LIVING = 'Donor was alive at time of renal transplant'
    DECEASED = 'Donor was deceased at time of renal transplant'
    NOT_MENTIONED = "Donor was not mentioned as living or deceased"

class DonorTypeMention(SpanAugmentedMention):
    donor_type: DonorType = Field(
        DonorType.NOT_MENTIONED,
        description='Was the renal donor living at the time of transplant?'
    )

class DonorRelationship(StrEnum):
    RELATED = 'Donor was related to the renal transplant recipient'
    UNRELATED = 'Donor was unrelated to the renal transplant recipient'
    NOT_MENTIONED = "Donor relationship status was not mentioned"

class DonorRelationshipMention(SpanAugmentedMention):
    donor_relationship: DonorRelationship = Field(
        DonorRelationship.NOT_MENTIONED,
        description='Was the renal donor related to the recipient?'
    )

class DonorHlaMatchQuality(StrEnum):
    WELL = 'Well matched (0-1 mismatches)'
    MODERATE = 'Moderately matched (2-4 mismatches)'
    POOR = 'Poorly matched (5-6 mismatches)'
    NOT_MENTIONED = "HLA match quality not mentioned"

class DonorHlaMatchQualityMention(SpanAugmentedMention):
    donor_hla_match_quality: DonorHlaMatchQuality = Field(
        DonorHlaMatchQuality.NOT_MENTIONED,
        description='What was the renal transplant HLA match quality?'
    )

class DonorHlaMismatchCount(StrEnum):
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    NOT_MENTIONED = 'HLA mismatch count not mentioned'

class DonorHlaMismatchCountMention(SpanAugmentedMention):
    donor_hla_mismatch_count: DonorHlaMismatchCount = Field(
        DonorHlaMismatchCount.NOT_MENTIONED,
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
    rx_compliance: bool | None = Field(
        None, 
        description='In the present encounter is the patient documented as compliant with immunosuppressive medications?'
    )

class RxPartialComplianceMention(SpanAugmentedMention):
    rx_partial_compliance: bool | None = Field(
        None, 
        description='In the present encounter is the patient documented as only partially compliant with immunosuppressive medications?'
    )

class RxNonComplianceMention(SpanAugmentedMention):
    rx_non_compliance: bool | None = Field(
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
class DSAPresent(StrEnum):
    CONFIRMED = "DSA diagnostic test positive, DSA diagnosis 'confirmed' or 'positive', or increase in immunosuppression due to DSA"
    TREATMENT = "DSA Treatment prescribed or DSA treatment administered"
    SUSPECTED = "DSA suspected, DSA likely, DSA cannot be ruled out, DSA test result pending or DSA is a differential diagnosis"
    NONE_OF_THE_ABOVE = "None of the above"

class DSAMention(SpanAugmentedMention):
    dsa_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of donor specific antibodies (DSA)?"
    )
    dsa: DSAPresent = Field(
        DSAPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of donor specific antibodies (DSA)?"
    )

############################################################################################################
# Infection (** Any **)
#   * necessary for PNA and UTI infections that often do not have a confirmed infection type!
#   * useful as a secondary check to ensure more specific infection types are not missed
############################################################################################################
class InfectionPresent(StrEnum):
    CONFIRMED = "Infection confirmed by laboratory test or imaging, infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to infection"
    TREATMENT = "Treatment prescribed/administered for infection (not including prophylaxis)"
    SUSPECTED = "Infection is suspected, likely, cannot be ruled out, infection is a differential diagnosis or infectious test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class InfectionMention(SpanAugmentedMention):
    infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of an infection?"
    )
    infection: InfectionPresent = Field(
        InfectionPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of infection?"
    )

###############################################################################
# Infection (Viral)
###############################################################################
class ViralInfectionPresent(StrEnum):
    CONFIRMED = "Viral infection confirmed by laboratory test or imaging, viral infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to viral infection"
    TREATMENT = "Antiviral treatment prescribed/administered for viral infection (not including prophylaxis)"
    SUSPECTED = "Viral infection is suspected, likely, cannot be ruled out, viral infection is a differential diagnosis or viral test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class ViralInfectionMention(SpanAugmentedMention):
    viral_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a viral infection?"
    )
    viral_infection: ViralInfectionPresent = Field(
        ViralInfectionPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of viral infection?"
    )

###############################################################################
# Infection (Bacterial)
###############################################################################
class BacterialInfectionPresent(StrEnum):
    CONFIRMED = "Bacterial infection confirmed by laboratory test or imaging, bacterial infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to bacterial infection"
    TREATMENT = "Antibacterial treatment prescribed/administered for bacterial infection (not including prophylaxis)"
    SUSPECTED = "Bacterial infection is suspected, likely, cannot be ruled out, bacterial infection is a differential diagnosis or bacterial test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class BacterialInfectionMention(SpanAugmentedMention):
    bacterial_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a bacterial infection?"
    )
    bacterial_infection: BacterialInfectionPresent = Field(
        BacterialInfectionPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of bacterial infection?"
    )

###############################################################################
# Infection (Fungal)
###############################################################################
class FungalInfectionPresent(StrEnum):
    CONFIRMED = "Fungal infection confirmed by laboratory test or imaging, fungal infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to fungal infection"
    TREATMENT = "Antifungal treatment prescribed/administered for fungal infection (not including prophylaxis)"
    SUSPECTED = "Fungal infection is suspected, likely, cannot be ruled out, fungal infection is a differential diagnosis or fungal test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class FungalInfectionMention(SpanAugmentedMention):
    fungal_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a fungal infection?"
    )
    fungal_infection: FungalInfectionPresent = Field(
        FungalInfectionPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of fungal infection?"
    )

###############################################################################
# Graft Rejection
###############################################################################
class GraftRejectionPresent(StrEnum):
    BIOPSY_PROVEN = "Biopsy proven kidney graft rejection or pathology proven kidney graft rejection"
    CONFIRMED = "Kidney graft rejection was 'diagnosed', 'confirmed' or 'positive'"
    TREATMENT = "Treatment prescribed/administered for kidney rejection (AMR or TCMR)"
    SUSPECTED = "Kidney graft rejection presumed, suspected, likely, cannot be ruled out, or biopsy result pending"
    NONE_OF_THE_ABOVE = "None of the above"

class GraftRejectionMention(SpanAugmentedMention):
    graft_rejection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of kidney graft rejection?"
    )
    graft_rejection: GraftRejectionPresent = Field(
        GraftRejectionPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of kidney graft rejection?"
    )

###############################################################################
# Graft Failure
###############################################################################
class GraftFailurePresent(StrEnum):
    CONFIRMED = "Kidney graft has failed or kidney graft loss"
    SUSPECTED = "Kidney graft failure presumed, suspected, likely, or cannot be ruled out"
    NONE_OF_THE_ABOVE = "None of the above"

class GraftFailureMention(SpanAugmentedMention):
    graft_failure_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of kidney graft failure?"
    )
    graft_failure: GraftFailurePresent = Field(
        GraftFailurePresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of kidney graft failure?"
    )

###############################################################################
# PTLD
###############################################################################
class PTLDPresent(StrEnum):
    BIOPSY_PROVEN = "Biopsy proven or pathology proven post transplant lymphoproliferative disorder (PTLD)"
    CONFIRMED = "Post transplant lymphoproliferative disorder (PTLD) was 'diagnosed', 'confirmed' or 'positive' or viral positive lymphoma"
    TREATMENT = "Treatment prescribed/administered for post transplant lymphoproliferative disorder (PTLD) or stopped immunosuppression due to PTLD"
    SUSPECTED = "Post transplant lymphoproliferative disorder (PTLD) presumed, suspected, likely, cannot be ruled out, or PTLD biopsy result pending"
    NONE_OF_THE_ABOVE = "None of the above"

class PTLDMention(SpanAugmentedMention):
    ptld_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of post transplant lymphoproliferative disorder (PTLD)?"
    )
    ptld: PTLDPresent = Field(
        PTLDPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of post transplant lymphoproliferative disorder (PTLD)?"
    )

###############################################################################
# Cancer
###############################################################################
class CancerPresent(StrEnum):
    BIOPSY_PROVEN = "Biopsy proven or pathology proven cancer"
    CONFIRMED = "Cancer was 'diagnosed', 'confirmed' or 'positive'"
    TREATMENT = "Treatment prescribed/administered for cancer"
    SUSPECTED = "Cancer is presumed, suspected, likely, cannot be ruled out, or biopsy of any lesion"
    NONE_OF_THE_ABOVE = "None of the above"

class CancerMention(SpanAugmentedMention):
    cancer_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of cancer?"
    )
    cancer: CancerPresent = Field(
        CancerPresent.NONE_OF_THE_ABOVE, 
        description="In the present encounter is there documented evidence of cancer?"
    )

###############################################################################
# Deceased
#  For tracking if the patient is noted to be deceased in any notes
###############################################################################
class DeceasedMention(SpanAugmentedMention):
    deceased: bool | None = Field(
        None, 
        description='In the present encounter, does the note state if the patient is deceased?'
    )
    deceased_datetime: str | None = Field(
        None, 
        description=(
            'If the patient is deceased, include the datetime of when the patient became deceased. '
            'Use None if there is no datetime recorded or if the patient is not observed as deceased.'
        )
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
    deceased_mention: DeceasedMention

# Enum describing all the relevant mention types' display labels
# Keys should be 1 to 1 with the KidneyTransplantAnnotation
# Labels aim to be as short as possible
class KidneyTransplantMentionLabels(StrEnum):
    donor_transplant_date_mention =     "Transplate Date"
    donor_type_mention =                "Donor Type"
    donor_relationship_mention =        "Donor Relationship"
    donor_hla_match_quality_mention =   "Hla Match Quality"
    donor_hla_mismatch_count_mention =  "Hla Mismatch Count"
    rx_therapeutic_mention =            "Therapeutic"
    rx_sub_therapeutic_mention =        "Sub therapeutic"
    rx_supra_therapeutic_mention =      "Supra therapeutic"
    rx_compliance_mention =             "Rx compliance"
    rx_partial_compliance_mention =     "Rx partial compliance"
    rx_non_compliance_mention =         "Rx non compliance"
    dsa_mention =                       "DSA"
    infection_mention =                 "Infection"
    viral_infection_mention =           "Viral"
    bacterial_infection_mention =       "Bacterial"
    fungal_infection_mention =          "Fungal"
    graft_rejection_mention =           "Graft Rejection"
    graft_failure_mention =             "Graft Failure"
    ptld_mention =                      "PTLD"
    cancer_mention =                    "Cancer"
    deceased_mention =                  "Deceased"
