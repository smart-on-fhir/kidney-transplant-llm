from enum import StrEnum

##########################################################
#
#           Immunosuppression ** DRUG CLASS **
#
##########################################################
class RxClassImmunosuppression(StrEnum):
    """
    RxClass Immunosuppression
    """
    ANTIMET = 'Anti-Metabolite (ANTIMET)'
    CNI = 'Calcineurin Inhibitor (CNI)'
    STEROID = "Corticosteroid (CS)"
    MTOR = "mTOR Inhibitor (MTOR)"
    COSTIM = "Costimulation Blocker/blockade (COSTIM)"
    IVIG = "Immunoglobulin (IVIG)"
    POLYCLONAL = "Polyclonal antibody (e.g., ATG, ALG)"
    MONOCLONAL = "Monoclonal antibody (mAb, e.g., basiliximab, rituximab)"
    OTHER = 'Other immunosuppressive drug'
    NONE = 'None of the above'

##########################################################
#
#           Immunosuppression ** INGREDIENTS **
#
##########################################################

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
    NONE = 'None of the above'

class CostimulationBlocker(StrEnum):
    BEL = 'Belatacept'
    ABA = 'Abatacept'
    OTHER = 'Other Costimulation blocker ingredient '
    NONE = 'None of the above'

class IVIG(StrEnum):
    IVIG = 'Intravenous Immunoglobulin (IVIG)'
    CYTOGAM = 'Cytogam (CMV-specific hyperimmune globulin)'
    OTHER = 'Other immunoglobulin therapy'
    NONE = 'None of the above'

class MtorInhibitor(StrEnum):
    EVE = 'Everolimus'
    SRL = 'Sirolimus'
    OTHER = 'Other mTOR inhibitor ingredient'
    NONE = 'None of the above'

class MonoclonalAntibodies(StrEnum):
    ALEM = 'Alemtuzumab'
    BASI = 'Basiliximab'
    DAC = 'Daclizumab' # Withdrawn 2009
    RTX = 'Rituximab'
    OTHER = 'Other Monoclonal antibody drug'
    NONE = 'None of the above'

class PolyclonalAntibodies(StrEnum):
    ATG = 'Antithymocyte Globulin (ATG)'
    OTHER = 'Other polyclonal antibodies ingredient'
    NONE = 'None of the above'


