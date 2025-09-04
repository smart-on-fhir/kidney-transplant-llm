from enum import StrEnum, auto
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
    IVIG = "Immunoglobulin (IVIG)"
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
    ATG = 'Antithymocyte Globulin (ATG)'
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
    OTHER = 'Other drug with known association to kidney (indication for treatment or nephrotoxicity)' #TODO revise prompt
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
    OTHER = 'Other anti-infective'
    NONE = 'None of the above'

###############################################################################
# Certainty of evidence TODO ?

class Certainty(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

#########################################################
# Immunosuppression Intent

class TreatmentPhase(StrEnum):
    """
    Treatment Phase
    """
    INDUCTION = "Induction therapy"
    MAINTENANCE = "Maintenance therapy"
    RESCUE = "Rescue therapy"
    NONE = 'None of the above'

###############################################################################
# Template
###############################################################################
class MedicationMention(SpanAugmentedMention):

    status: RxStatus = Field(
        default=RxStatus.NONE,
        description='What is the status of this medication?')

    phase: TreatmentPhase = Field(
        default=TreatmentPhase.NONE,
        description="What is the treatment phase of this medication")

    # TODO: Dosage and Frequency --> expectedSupplyDuration(days)

    ingredient = None
    # ingredient: AntiMetabolite = Field(
    #     AntiMetabolite.NONE,
    #     description="Which anti-metabolite ingredient is in this documented medication?") # TODO: wordsmith


###############################################################################
# AntiMetabolite
###############################################################################
class AntiMetaboliteMention(MedicationMention):
    ingredient: AntiMetabolite = Field(
        AntiMetabolite.NONE,
        description="Which anti-metabolite ingredient is in this documented medication?")
