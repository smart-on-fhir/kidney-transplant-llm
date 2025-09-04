from enum import StrEnum, auto
from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from pydantic import conint, confloat

class SpanAugmentedMention(BaseModel):
    has_mention: bool | None  # True, False, or None
    spans: list[str]

##########################################################
#
#               Immunosuppression
#
##########################################################
class DrugClassImmunosuppression(StrEnum):
    """
    Drug Class Immunosuppression
    """
    ANTIMET = 'Anti-Metabolite (ANTIMET)'
    CNI = 'Calcineurin Inhibitor (CNI)'
    STEROID = "Corticosteroid (CS)"
    MTOR = "mTOR Inhibitor (MTOR)"
    COSTIM = "Costimulation Blocker/blockade (COSTIM)"
    IG = "Immunoglobulin (IVIG)"
    NONE = 'None of the above'

#########################################################
# Immunosuppression Drug Class --> Ingredient

class AntiMetabolite(StrEnum):
    AZA = 'Azathioprine'
    MMF = 'Mycophenolate Mofetil'
    OTHER = 'Other anti-metabolite ingredient'
    NONE = 'None of the above'

class CalcineurinInhibitor(StrEnum):
    CYA = 'Cyclosporine'
    TAC = 'Tacrolimus'
    OTHER = 'Other calcineurin inhibitor ingredient'
    NONE = 'None of the above'

class Corticosteroid(StrEnum):
    MEDROL = 'Methylprednisolone'
    PDL = 'Prednisolone'
    PRED = 'Prednisone'
    OTHER = 'Other corticosteroid ingredient'

class CostimulationBlocker(StrEnum):
    BEL = 'Belatacept'
    ABA = 'Abatacept'
    OTHER = 'Other costimulation blocker ingredient '
    NONE = 'None of the above'

class MtorInhibitor(StrEnum):
    EVE = 'Everolimus'
    SRL = 'Sirolimus'
    OTHER = 'Other mTOR inhibitor ingredient'
    NONE = 'None of the above'

class PolyclonalAntibodies(StrEnum):
    ATG = 'Antithymocyte Globulin'
    NONE = 'None of the above'

class MonoclonalAntibodies(StrEnum):
    ALEM = 'Alemtuzumab'
    BASI = 'Basiliximab'
    DAC = 'Daclizumab' # Withdrawn 2009
    RTX = 'Rituximab'
    OTHER = 'Other Monoclonal antibody drug'
    NONE = 'None of the above'

class Immunoglobulin(StrEnum):
    IVIG = 'Intravenous Immunoglobulin (IVIG)'
    CYTOGAM = 'Cytogam (CMV-specific hyperimmune globulin)'
    OTHER = 'Other Immunoglobulin'
    NONE = 'None of the above'

################################################################################
#
#     Rx Drugs **NOT** transplant immunosuppression
#
###############################################################################

###############################################################################
# Drug Class Kidney

class DrugClassKidney(StrEnum):
    RAS = 'Renin–Angiotensin System (especially ACE, ARB, renin inhibitors/blockers)'
    Diuretic = 'Diuretic'
    BB = 'Beta Blocker'
    CCB = 'Calcium channel blocker'
    NSAID = 'non steroidal anti-inflammatory drug'
    CONTRAST = 'Iodinated contrast agents'
    OTHER = 'Other drug with known association to kidney (indication or nephrotoxicity)'
    NONE = 'None of the above'

###############################################################################
# Drug Class Rx Cancer --> possible Dx Cancer ?

class DrugClassCancer(StrEnum):
    CHEMO = 'Cytotoxic chemotherapy'
    CHECKPOINT = 'Checkpoint inhibitors, especially PD-1, PDL-1, CTLA-4'
    CYTOKINE = 'Cytokine therapy, especially IL-2 and interferon alpha'
    CAR_T = 'Chimeric antigen receptor (CAR-T)'
    OTHER = 'Other cancer drug'
    NONE = 'None of the above'

###############################################################################
# Drug Class Rx Infection --> possible Dx Infection ?

class DrugClassAntiInfective(StrEnum):
    VIRAL = 'Antiviral'
    BACTERIAL = 'Antibacterial'
    FUNGAL = 'Antifungal'
    PARASITE = 'Antiparasitic'
    OTHER = 'Other anti-infective'
    NONE = 'None of the above'

###############################################################################
# Certainty of evidence

class Certainty(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

###############################################################################
# FHIR Medication Request Attributes (to chart review)

class FreqNorm(StrEnum):
    QD = "QD"
    BID = "BID"
    TID = "TID"
    QID = "QID"
    WEEKLY = "WEEKLY"
    Q2W = "Q2W"
    Q4W = "Q4W"
    Q48H = "Q48H"
    PRN = "PRN"
    STAT = "STAT"
    OTHER = "OTHER"

class DispenseRequest:
    # dispenserequest.expectedSupplyDuration
    start_date = None
    end_date = None

class DosageInstruction:
    frequency = None
    quantity = None

class Dose(BaseModel):
    value: Optional[confloat(gt=0)] = None
    unit: Optional[str] = None

class Frequency(BaseModel):
    normalized: Optional[FreqNorm] = None
    raw_text: Optional[str] = None

class MRLikeEpisode(BaseModel):
    patient_id: str
    ingredient: str  # normalized generic
    drug_class: DrugClass
    intent: Intent
    route: Optional[Route] = None
    dose: Optional[Dose] = None
    frequency: Optional[Frequency] = None
    authored_on: Optional[date] = None
    start_date: Optional[date] = None
    stop_date: Optional[date] = None
    expected_supply_days: Optional[conint(ge=1)] = None
    number_of_repeats_allowed: Optional[conint(ge=0)] = None
    encounter_context: Optional[Literal["INPATIENT","OUTPATIENT","UNKNOWN"]] = "UNKNOWN"
    requester_service: Optional[str] = None
    evidence: List[EvidenceSpan] = []
    certainty: Certainty = Certainty.MEDIUM



###############################################################################
# AntiMetabolite
###############################################################################
class AntiMetaboliteMention(SpanAugmentedMention):
    history: bool = Field(
        False,
        description="Does the patient have a past medication history of an anti-metabolite medication?")

    phase: TreatmentPhase = Field(
        None,
        description="The treatment phase of the anti-metabolite medication")

    ingredient: AntiMetabolite = Field(
        AntiMetabolite.NONE,
        description="Which anti-metabolite ingredient is in the patient currently taking?")


