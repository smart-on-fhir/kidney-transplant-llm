import json 
import os
from enum import StrEnum

from pydantic import BaseModel, Field

from kidney_transplant_llm.pydantic_utils import MedicationMention

##########################################################
#
#           Immunosuppression ** DRUG CLASS **
#
##########################################################
class RxClassImmunosuppression(StrEnum):
    """
    RxClass Immunosuppression
    """

    ANTIMET = "Anti-Metabolite (ANTIMET)"
    CNI = "Calcineurin Inhibitor (CNI)"
    STEROID = "Corticosteroid (CS)"
    MTOR = "mTOR Inhibitor (MTOR)"
    COSTIM = "Costimulation Blocker/blockade (COSTIM)"
    IVIG = "Immunoglobulin (IVIG)"
    POLYCLONAL = "Polyclonal antibody (e.g., ATG, ALG)"
    MONOCLONAL = "Monoclonal antibody (mAb, e.g., basiliximab, rituximab)"
    OTHER = "Other immunosuppressive drug"
    NONE = "None of the above"


class RxIngredientImmunosuppression(StrEnum):
    """
    The specific immunosuppressive drug ingredient
    """

    # ANTIMET Types
    AZA = "Azathioprine"
    MMF = "Mycophenolate Mofetil"
    ANTIMET_OTHER = "Other anti-metabolite ingredient"
    # CNI Types
    CYA = "Cyclosporine"
    TAC = "Tacrolimus"
    CNI_OTHER = "Other calcineurin inhibitor ingredient"
    # STEROID Types
    MEDROL = "Methylprednisolone"
    PDL = "Prednisolone"
    PRED = "Prednisone"
    STEROID_OTHER = "Other corticosteroid ingredient"
    # COSTIM Types
    BEL = "Belatacept"
    ABA = "Abatacept"
    COSTIM_OTHER = "Other Costimulation blocker ingredient"
    # IVIG Types
    IVIG = "Intravenous Immunoglobulin (IVIG)"
    CYTOGAM = "Cytogam (CMV-specific hyperimmune globulin)"
    IVIG_OTHER = "Other immunoglobulin therapy"
    # MTOR Types
    EVE = "Everolimus"
    SRL = "Sirolimus"
    MTOR_OTHER = "Other mTOR inhibitor ingredient"
    # MONOCLONAL Types
    ALEM = "Alemtuzumab"
    BASI = "Basiliximab"
    DAC = "Daclizumab"
    RTX = "Rituximab"
    MONOCLONAL_OTHER = "Other Monoclonal antibody drug"
    # POLYCLONAL Types
    ATG = "Antithymocyte Globulin (ATG)"
    POLYCLONAL_OTHER = "Other polyclonal antibodies ingredient"
    NONE = "None of the above"



class ImmunosuppressiveMedicationMention(MedicationMention):
    """
    Mentions of ImmunosuppressiveMedications for this given chart.
    """

    drug_class: RxClassImmunosuppression = Field(
        default=RxClassImmunosuppression.NONE,
        description="Extract the Immunosuppressive drug class or therapy modality documented for this medication, if present",
    )

    ingredient: RxIngredientImmunosuppression = Field(
        default=RxIngredientImmunosuppression.NONE,
        description="Extract the specific immunosuppressive drug ingredient documented for this medication, if present",
    )


##############################################################################
# Aggregated Annotation and Mention Classes
#
# This is the top-level structure for the pydantic models used in IRAE tasks.
###############################################################################


class ImmunosuppressiveMedicationsAnnotation(BaseModel):
    """
    All mentions of ImmunosuppressiveMedications for this given chart.
    """

    immunosuppressive_medication_mentions: list[ImmunosuppressiveMedicationMention] = Field(
        default_factory=list,
        description="All mentions of ImmunosuppressiveMedications for this given chart.",
    )


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)

    with open(f"{basedir}/schemas/irae_medications.json", "w", encoding="utf8") as f:
        json.dump(ImmunosuppressiveMedicationMention.model_json_schema(), f, indent=2)
