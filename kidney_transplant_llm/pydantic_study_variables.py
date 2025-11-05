from enum import StrEnum, auto
from pydantic import BaseModel, Field

class SpanAugmentedMention(BaseModel):
    has_mention: bool # True, False
    spans: list[str]

###############################################################################
# Donor Characteristics
# 
# For a given transplant, these should be static over time 
###############################################################################

# Dates are treated as strings - no enum needed
class DonorTransplantDateMention(SpanAugmentedMention):
    donor_transplant_date: str | None = Field(
        None,
        description='Exact date of renal transplant; use YYYY-MM-DD format in your response. Only highlight date mentions with an explicit day, month, and year (e.g. 2020-01-15). All other date mentions, or an absence of a date mention, should be indicated with None.'
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
    RELATED = 'Donor was biologically related to the renal transplant recipient'
    UNRELATED = 'Donor was biologically unrelated to the renal transplant recipient'
    NOT_MENTIONED = "Donor relationship status was not mentioned"

class DonorRelationshipMention(SpanAugmentedMention):
    donor_relationship: DonorRelationship = Field(
        DonorRelationship.NOT_MENTIONED,
        description='Was the renal donor related to the recipient?'
    )

class DonorHlaMatchQuality(StrEnum):
    WELL = "Well matched (0-1 mismatches) OR recipient explicitly documented as not sensitized"
    MODERATE = "Moderately matched (2-4 mismatches) OR recipient explicitly documented as sensitized"
    POOR = "Poorly matched (5-6 mismatches) OR recipient explicitly documented as highly sensitized"
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
# Therapeutic Status Compliance
###############################################################################
class RxTherapeuticStatus(StrEnum):
    THERAPEUTIC = "Immunosuppression levels are documented as therapeutic, adequate, or within target range."
    SUB_THERAPEUTIC = 'Immunosuppression levels are documented as subtherapeutic, insufficient, or below target range.'
    SUPRA_THERAPEUTIC = 'Immunosuppression levels are documented as supratherapeutic, above therapeutic level, or above target range.'
    NONE_OF_THE_ABOVE = "None of the above"

class RxTherapeuticStatusMention(SpanAugmentedMention):
    rx_therapeutic_status: RxTherapeuticStatus = Field(
        RxTherapeuticStatus.NONE_OF_THE_ABOVE, 
        description='In the present encounter, what is the documented immunosuppression level?'
    )

###############################################################################
# Medication Compliance
###############################################################################
class RxCompliance(StrEnum):
    COMPLIANT = 'Patient is documented as compliant with immunosuppressive medications.'
    PARTIALLY_COMPLIANT = "Patient is documented as only partially compliant with immunosuppressive medications."
    NON_COMPLIANT = "Patient is documented as noncompliant with immunosuppressive medications."
    NONE_OF_THE_ABOVE = "None of the above"

class RxComplianceMention(SpanAugmentedMention):
    rx_compliance: RxCompliance = Field(
        RxCompliance.NONE_OF_THE_ABOVE, 
        description='In the present encounter, is the patient documented as compliant with immunosuppressive medications? Note: If the physician documents patient-reported compliance information without contradicting it, this information should be used when evaluating compliance.'
    )


###############################################################################
# THE FOLLOWING DATA ELEMENTS TRACK BOTH 
# THE HISTORY AND THE PRESENT STATUS OF VARIABLES
###############################################################################


###############################################################################
# DSA Donor Specific Antibody
###############################################################################
class DSAPresent(StrEnum):
    """
    Notice: DSA is strongly related to `GraftRejectionPresent`.

    Treatment of DSA includes immunosuppressive drugs, IVIG, and plasmapheresis (PLEX).

    Treatment with immunosuppressive drugs does *NOT* imply SUSPECTED DSA,
    as many of immunosuppressive drugs are routinely used for "maintenance" therapy.

    IVIG and plasmapheresis (PLEX) during the post-transplant (post induction) phase DOES imply
    --> DSAPresent >  SUSPECTED (and possibly CONFIRMED)
    --> `GraftRejectionPresent` > SUSPECTED (and possibly CONFIRMED or BIOPSY_PROVEN)
    """
    CONFIRMED = "DSA diagnostic test positive, DSA diagnosis 'confirmed' or 'positive', or increase in immunosuppression due to DSA"
    SUSPECTED = "DSA suspected, DSA likely, DSA cannot be ruled out, DSA test result pending, or treatment with IVIG/plasmapheresis"
    NONE_OF_THE_ABOVE = "None of the above"

class DSAMention(SpanAugmentedMention):
    dsa_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of donor specific antibodies (DSA)?"
    )
    dsa: DSAPresent = Field(
        DSAPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents donor specific antibodies (DSA) as current, active, or being evaluated/treated now?"
    )

############################################################################################################
# Infection (** Any **)
#   * necessary for PNA and UTI infections that often do not have a confirmed infection type!
#   * useful as a secondary check to ensure more specific infection types are not missed
############################################################################################################
class InfectionPresent(StrEnum):
    CONFIRMED = "Infection confirmed by laboratory test or imaging, infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to infection"
    SUSPECTED = "Infection is suspected, likely, cannot be ruled out, infection is a differential diagnosis or infectious test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class InfectionMention(SpanAugmentedMention):
    infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of an infection?"
    )
    infection: InfectionPresent = Field(
        InfectionPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents infection as current, active, or being evaluated/treated now?"
    )

###############################################################################
# Infection (Viral)
###############################################################################
class ViralInfectionPresent(StrEnum):
    CONFIRMED = "Viral infection confirmed by laboratory test or imaging, viral infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to viral infection"
    SUSPECTED = "Viral infection is suspected, likely, cannot be ruled out, viral infection is a differential diagnosis or viral test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class ViralInfectionMention(SpanAugmentedMention):
    viral_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a viral infection?"
    )
    viral_infection: ViralInfectionPresent = Field(
        ViralInfectionPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents viral infection as current, active, or being evaluated/treated now?"
    )

###############################################################################
# Infection (Bacterial)
###############################################################################
class BacterialInfectionPresent(StrEnum):
    CONFIRMED = "Bacterial infection confirmed by laboratory test or imaging, bacterial infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to bacterial infection"
    SUSPECTED = "Bacterial infection is suspected, likely, cannot be ruled out, bacterial infection is a differential diagnosis or bacterial test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class BacterialInfectionMention(SpanAugmentedMention):
    bacterial_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a bacterial infection?"
    )
    bacterial_infection: BacterialInfectionPresent = Field(
        BacterialInfectionPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents bacterial infection as current, active, or being evaluated/treated now?"
    )

###############################################################################
# Infection (Fungal)
###############################################################################
class FungalInfectionPresent(StrEnum):
    CONFIRMED = "Fungal infection confirmed by laboratory test or imaging, fungal infection diagnosis was 'confirmed' or 'positive', or reduced immunosuppression due to fungal infection"
    SUSPECTED = "Fungal infection is suspected, likely, cannot be ruled out, fungal infection is a differential diagnosis or fungal test result is pending"
    NONE_OF_THE_ABOVE = "None of the above"

class FungalInfectionMention(SpanAugmentedMention):
    fungal_infection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of a fungal infection?"
    )
    fungal_infection: FungalInfectionPresent = Field(
        FungalInfectionPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents fungal infection as current, active, or being evaluated/treated now?"
    )

###############################################################################
# Graft Rejection
###############################################################################
class GraftRejectionPresent(StrEnum):
    """
    Notice: Graft rejection is strongly related to `DSAPresent`.

    Treatment of graft rejection includes immunosuppressive drugs, IVIG, and plasmapheresis (PLEX).

    Treatment with immunosuppressive drugs does *NOT* imply outcome is SUSPECTED,
    as many of immunosuppressive drugs are routinely used for "maintenance" therapy.

    IVIG and plasmapheresis (PLEX) during the post-transplant (post induction) phase DOES imply
    --> `GraftRejectionPresent` > SUSPECTED (and possibly CONFIRMED or BIOPSY_PROVEN)
    --> DSAPresent >  SUSPECTED (and possibly CONFIRMED)
    """
    BIOPSY_PROVEN = "Biopsy proven kidney graft rejection or pathology proven kidney graft rejection"
    CONFIRMED = "Kidney graft rejection was 'diagnosed', 'confirmed' or 'positive'"
    SUSPECTED = "Kidney graft rejection presumed, suspected, likely, cannot be ruled out, biopsy result pending, or treatment with IVIG/plasmapheresis"
    NONE_OF_THE_ABOVE = "None of the above"

class GraftRejectionMention(SpanAugmentedMention):
    graft_rejection_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of kidney graft rejection?"
    )
    graft_rejection: GraftRejectionPresent = Field(
        GraftRejectionPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents kidney graft rejection as current, active, or being evaluated/treated now?"
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
        description="What evidence documents kidney graft failure as current, active, or being evaluated/treated now?"
    )

###############################################################################
# PTLD
###############################################################################
class PTLDPresent(StrEnum):
    """
    Notice: PTLD treatments may also be used in 'rescue' therapy (DSA/graft rejection) or other cancers.
    One notable difference from other cancers (such as skin cancer) is the absence of "surgical excision" (lymphoma).
    """
    BIOPSY_PROVEN = "Biopsy proven or pathology proven PTLD"
    CONFIRMED = "PTLD was 'diagnosed', 'confirmed' or 'positive' or viral positive lymphoma"
    SUSPECTED = "PTLD presumed, suspected, likely, cannot be ruled out, PTLD biopsy result pending, or treatment with chemotherapy/radiation"
    NONE_OF_THE_ABOVE = "None of the above"

class PTLDMention(SpanAugmentedMention):
    ptld_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of post transplant lymphoproliferative disorder (PTLD)?"
    )
    ptld: PTLDPresent = Field(
        PTLDPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents post transplant lymphoproliferative disorder (PTLD) as current, active, or being evaluated/treated now?"
    )

###############################################################################
# Cancer
###############################################################################
class CancerPresent(StrEnum):
    """
    Notice: Cancer treatments may also be used in 'rescue' therapy (DSA/graft rejection).
    PTLD is a type of cancer. PTLD is a lymphoma and thus not treated with "surgical excision".
    Skin cancer (of which there are many types carcinoma and melanoma) is treated with surgical excision.
    """
    BIOPSY_PROVEN = "Biopsy proven or pathology proven cancer"
    CONFIRMED = "Cancer was 'diagnosed', 'confirmed' or 'positive'"
    SUSPECTED = "Cancer is presumed, suspected, likely, cannot be ruled out, biopsy of any lesion, or treatment with chemotherapy/radiation"
    NONE_OF_THE_ABOVE = "None of the above"

class CancerMention(SpanAugmentedMention):
    cancer_history: bool = Field(
        False, 
        description="Does the patient have a past medical history of cancer?"
    )
    cancer: CancerPresent = Field(
        CancerPresent.NONE_OF_THE_ABOVE, 
        description="What evidence documents cancer as current, active, or being evaluated/treated now?"
    )

###############################################################################
# Deceased
#  For tracking if the patient is noted to be deceased in any notes
###############################################################################
class DeceasedMention(SpanAugmentedMention):
    deceased: bool | None = Field(
        None, 
        description='Does the present encounter document that the patient is deceased?'
    )
    deceased_date: str | None = Field(
        None, 
        description=(
            'If the patient is deceased, include the date the patient became deceased. Use YYYY-MM-DD format if possible. '
            'Use None if there is no date recorded or if the patient is not observed as deceased.'
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
    rx_therapeutic_status_mention: RxTherapeuticStatusMention
    rx_compliance_mention: RxComplianceMention
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



class KidneyTransplantDonorGroupAnnotation(BaseModel): 
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


class KidneyTransplantLongitudinalAnnotation(BaseModel): 
    """
    An object-model for annotations of immune related adverse event (IRAE) 
    observations found in a patient's chart, relating specifically to kidney 
    transplants.

    This class only includes longitudinally variable mentions, i.e. those
    that can change over time, such as therapeutic status, compliance, infections,
    graft rejection/failure, DSA, PTLD, cancer, and deceased status.

    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate 
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """
    rx_therapeutic_status_mention: RxTherapeuticStatusMention
    rx_compliance_mention: RxComplianceMention
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




class KidneyTransplantComplianceGroupAnnotation(BaseModel): 
    """
    An object-model for annotations of immune related adverse event (IRAE) 
    observations found in a patient's chart, relating specifically to kidney 
    transplants. This class only includes therapeutic status and compliance mentions.
    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate 
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """
    rx_therapeutic_status_mention: RxTherapeuticStatusMention
    rx_compliance_mention: RxComplianceMention


class KidneyTransplantInfectionGroupAnnotation(BaseModel): 
    """
    An object-model for annotations of immune related adverse event (IRAE) 
    observations found in a patient's chart, relating specifically to kidney 
    transplants. This class only includes infection and cancer-related mentions.

    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate 
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """
    infection_mention: InfectionMention
    viral_infection_mention: ViralInfectionMention
    bacterial_infection_mention: BacterialInfectionMention
    fungal_infection_mention: FungalInfectionMention



class KidneyTransplantRejectionFailureGroupAnnotation(BaseModel): 
    """
    An object-model for annotations of immune related adverse event (IRAE) 
    observations found in a patient's chart, relating specifically to kidney 
    transplants. This class only includes graft rejection, DSA, graft failure mentions.

    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate 
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """
    dsa_mention: DSAMention
    graft_rejection_mention: GraftRejectionMention
    graft_failure_mention: GraftFailureMention
    

class KidneyTransplantPostTransplantMalignanciesAnnotation(BaseModel): 
    """
    An object-model for annotations of immune related adverse event (IRAE) 
    observations found in a patient's chart, relating specifically to kidney 
    transplants. This class only includes post transplant malignancies.

    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate 
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """
    ptld_mention: PTLDMention
    cancer_mention: CancerMention

class KidneyTransplantDeathGroupAnnotation(BaseModel): 
    """
    An object-model for annotations of immune related adverse event (IRAE) 
    observations found in a patient's chart, relating specifically to kidney 
    transplants. This class only includes deceased mentions.

    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate 
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """
    deceased_mention: DeceasedMention



###############################################################################
# Artifacts for Label Studio usage  
###############################################################################

# Enum describing all the relevant mention types' display labels
# Names of Enum members should be 1 to 1 with the KidneyTransplantAnnotation fields
class KidneyTransplantMentionLabels(StrEnum):
    donor_transplant_date_mention = auto()
    donor_type_mention = auto()
    donor_relationship_mention = auto()
    donor_hla_match_quality_mention = auto()
    donor_hla_mismatch_count_mention = auto()
    rx_therapeutic_status_mention = auto()
    rx_compliance_mention = auto()
    dsa_mention = auto()
    infection_mention = auto()
    viral_infection_mention = auto()
    bacterial_infection_mention = auto()
    fungal_infection_mention = auto()
    graft_rejection_mention = auto()
    graft_failure_mention = auto()
    ptld_mention = auto()
    cancer_mention = auto()
    deceased_mention = auto()

#  Groups to be used in the eventual labelstudio interface
# Right now this only encodes background, but could be used to organize/
# determine sorting order, etc
class KidneyTransplantMentionGroups(StrEnum):
    TRANSPLANT_DATE = auto()
    DONOR = auto()
    THERAPEUTIC = auto()
    COMPLIANCE = auto()
    DSA = auto()
    INFECTION = auto()
    REJECTION = auto()
    CANCER = auto()
    ENDPOINTS_FAILURE_DECEASED = auto()

kidney_transplant_mention_groups_metadata = {
    KidneyTransplantMentionGroups.TRANSPLANT_DATE : {
        "background": "#008B8B"
    },
    KidneyTransplantMentionGroups.DONOR : {
        "background": "#00FFFF"
    },
    KidneyTransplantMentionGroups.THERAPEUTIC : {
        "background": '#90ee90'
    },
    KidneyTransplantMentionGroups.COMPLIANCE : {
        "background": '#20b2aa'
    },
    KidneyTransplantMentionGroups.DSA : {
        "background": '#9370db'
    },
    KidneyTransplantMentionGroups.INFECTION : {
        "background": '#DC143C'
    },
    KidneyTransplantMentionGroups.REJECTION : {
        "background": "#FF00FF"
    },
    KidneyTransplantMentionGroups.CANCER : {
        "background": "#FF8C00"
    },
    KidneyTransplantMentionGroups.ENDPOINTS_FAILURE_DECEASED : {
        "background": "#00008B"
    },
}

# Tying the Label Enum to the Group Enum and other metadata (display strings, e.g.)
kidney_transplant_mention_ls_metadata = {
    KidneyTransplantMentionLabels.donor_transplant_date_mention : {
        "display": "Transplate Date",
        "group": KidneyTransplantMentionGroups.TRANSPLANT_DATE,
        "hotkey": "W",
        "hotkey_mnemonic": "Which day?",
    },
    KidneyTransplantMentionLabels.donor_type_mention : {
        "display": "Donor Type",
        "group": KidneyTransplantMentionGroups.DONOR,
        "hotkey": "L",
        "hotkey_mnemonic": "Living donor?",
    },
    KidneyTransplantMentionLabels.donor_relationship_mention : {
        "display": "Donor Relationship",
        "group": KidneyTransplantMentionGroups.DONOR,
        "hotkey": "S",
        "hotkey_mnemonic": "Sibling?",
    },
    KidneyTransplantMentionLabels.donor_hla_match_quality_mention : {
        "display": "Hla Match Quality",
        "group": KidneyTransplantMentionGroups.DONOR,
        "hotkey": "Q",
        "hotkey_mnemonic": "Quality?",
    },
    KidneyTransplantMentionLabels.donor_hla_mismatch_count_mention : {
        "display": "Hla Mismatch Count",
        "group": KidneyTransplantMentionGroups.DONOR,
        "hotkey": "M",
        "hotkey_mnemonic": "Mismatch?",
    },
    KidneyTransplantMentionLabels.rx_therapeutic_status_mention : {
        "display": "Rx Therapeutic",
        "group": KidneyTransplantMentionGroups.THERAPEUTIC,
        "hotkey": "E",
        "hotkey_mnemonic": "Effect?",
    },
    KidneyTransplantMentionLabels.rx_compliance_mention : {
        "display": "Rx Compliance",
        "group": KidneyTransplantMentionGroups.COMPLIANCE,
        "hotkey": "U",
        "hotkey_mnemonic": "Use?",
    },
    KidneyTransplantMentionLabels.dsa_mention : {
        "display": "DSA",
        "group": KidneyTransplantMentionGroups.DSA,
        "hotkey": "A",
        "hotkey_mnemonic": "Antibodies?",
    },
    KidneyTransplantMentionLabels.infection_mention : {
        "display": "Infection",
        "group": KidneyTransplantMentionGroups.INFECTION,
        "hotkey": "I",
        "hotkey_mnemonic": "Infection?",
    },
    KidneyTransplantMentionLabels.viral_infection_mention : {
        "display": "Viral",
        "group": KidneyTransplantMentionGroups.INFECTION,
        "hotkey": "V",
        "hotkey_mnemonic": "Viral?",
    },
    KidneyTransplantMentionLabels.bacterial_infection_mention : {
        "display": "Bacterial",
        "group": KidneyTransplantMentionGroups.INFECTION,
        "hotkey": "B",
        "hotkey_mnemonic": "Bacterial?",
    },
    KidneyTransplantMentionLabels.fungal_infection_mention : {
        "display": "Fungal",
        "group": KidneyTransplantMentionGroups.INFECTION,
        "hotkey": "G",
        "hotkey_mnemonic": "funGal?",
    },
    KidneyTransplantMentionLabels.graft_rejection_mention : {
        "display": "Graft Rejection",
        "group": KidneyTransplantMentionGroups.REJECTION,
        "hotkey": "R",
        "hotkey_mnemonic": "Rejection?",
    },
    KidneyTransplantMentionLabels.graft_failure_mention : {
        "display": "Graft Failure",
        "group": KidneyTransplantMentionGroups.ENDPOINTS_FAILURE_DECEASED,
        "hotkey": "F",
        "hotkey_mnemonic": "Failure?",
    },
    KidneyTransplantMentionLabels.ptld_mention : {
        "display": "PTLD",
        "group": KidneyTransplantMentionGroups.CANCER,
        "hotkey": "P",
        "hotkey_mnemonic": "PTLD?",
    },
    KidneyTransplantMentionLabels.cancer_mention : {
        "display": "Cancer",
        "group": KidneyTransplantMentionGroups.CANCER,
        "hotkey": "C",
        "hotkey_mnemonic": "Cancer?",
    },
    KidneyTransplantMentionLabels.deceased_mention    : {
        "display": "Deceased",
        "group": KidneyTransplantMentionGroups.ENDPOINTS_FAILURE_DECEASED,
        "hotkey": "D",
        "hotkey_mnemonic": "Deceased?",
    },
}
