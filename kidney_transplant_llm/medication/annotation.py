from typing import List
from pydantic import BaseModel, Field
from kidney_transplant_llm.medication.medicationrequest import (
    drug_type_desc,
    ingredient_desc,
    RxClassMention,
    IngredientMention
)
from kidney_transplant_llm.medication.ingredients.infection import RxClassAntiInfective
from kidney_transplant_llm.medication.ingredients.cancer import RxClassCancer
from kidney_transplant_llm.medication.ingredients.kidney import RxClassKidney
from kidney_transplant_llm.medication.ingredients.immunosuppression import (
    RxClassImmunosuppression,
    AntiMetabolite,
    CalcineurinInhibitor,
    Corticosteroid,
    CostimulationBlocker,
    MtorInhibitor,
    PolyclonalAntibodies,
    MonoclonalAntibodies,
    IVIG
)
##########################################################
#
#       Indications: infection, cancer, kidney
#
##########################################################
class RxClassAntiInfectiveMention(RxClassMention):
    drug_type: RxClassAntiInfective = Field(
        default=RxClassAntiInfective.NONE,
        description=drug_type_desc('anti-infective drug')
    )

##########################################################
class RxClassCancerMention(RxClassMention):
    drug_type: RxClassCancer = Field(
        default=RxClassCancer.NONE,
        description=drug_type_desc('cancer drug')
    )

##########################################################
class RxClassKidneyMention(RxClassMention):
    drug_type: RxClassKidney = Field(
        default=RxClassKidney.NONE,
        description=drug_type_desc('renal drug')
    )
##########################################################
#
#           Ingredients: immunosuppression only
#
##########################################################
class AntiMetaboliteMention(IngredientMention):
    ingredient: AntiMetabolite = Field(
        AntiMetabolite.NONE,
        description=ingredient_desc('anti-metabolite'))

class CalcineurinInhibitorMention(IngredientMention):
    ingredient: CalcineurinInhibitor = Field(
        CalcineurinInhibitor.NONE,
        description=ingredient_desc('Calcineurin Inhibitor (CNI)'))

class CorticosteroidMention(IngredientMention):
    ingredient: Corticosteroid = Field(
        default=Corticosteroid.NONE,
        description=ingredient_desc('Corticosteroid')
    )

class CostimulationBlockerMention(IngredientMention):
    ingredient: CostimulationBlocker = Field(
        default=CostimulationBlocker.NONE,
        description=ingredient_desc('Costimulation Blocker')
    )

class IVIGMention(IngredientMention):
    ingredient: IVIG = Field(
        default=IVIG.NONE,
        description=ingredient_desc('IVIG')
    )

class MtorInhibitorMention(IngredientMention):
    ingredient: MtorInhibitor = Field(
        default=MtorInhibitor.NONE,
        description=ingredient_desc('mTOR Inhibitor')
    )

class MonoclonalAntibodiesMention(IngredientMention):
    ingredient: MonoclonalAntibodies = Field(
        default=MonoclonalAntibodies.NONE,
        description=ingredient_desc('monoclonal antibodies')
    )

class PolyclonalAntibodiesMention(IngredientMention):
    ingredient: PolyclonalAntibodies = Field(
        default=PolyclonalAntibodies.NONE,
        description=ingredient_desc('polyclonal antibodies')
    )

##########################################################
class RxClassImmunosuppressionMention(RxClassMention):
    """
    NOTICE: do NOT change field names like 'antimet'
    "antimet" is the "real world" medical abbreviation and also used by `RxClassImmunosuppression`
    """
    drug_type: RxClassImmunosuppression = Field(
        default=RxClassImmunosuppression.NONE,
        description=drug_type_desc('Immunosuppressive drug')
    )

    antimet: AntiMetabolite = Field(
        AntiMetabolite.NONE,
        description=ingredient_desc('anti-metabolite')
    )

    cni: CalcineurinInhibitor = Field(
        CalcineurinInhibitor.NONE,
        description=ingredient_desc('Calcineurin Inhibitor (CNI)')
    )

    steroid: Corticosteroid = Field(
        default=Corticosteroid.NONE,
        description=ingredient_desc('Corticosteroid')
    )

    ivig: IVIGMention = Field(
        default=IVIG.NONE,
        description=ingredient_desc('IVIG')
    )

    costim: CostimulationBlocker = Field(
        default=CostimulationBlocker.NONE,
        description=ingredient_desc('Costimulation Blocker')
    )

    mtor: MtorInhibitor = Field(
        default=MtorInhibitor.NONE,
        description=ingredient_desc('mTOR Inhibitor')
    )

    monoclonal: MonoclonalAntibodies = Field(
        default=MonoclonalAntibodies.NONE,
        description=ingredient_desc('monoclonal antibodies')
    )

    polyclonal: PolyclonalAntibodies = Field(
        default=PolyclonalAntibodies.NONE,
        description=ingredient_desc('polyclonal antibodies')
    )

##########################################################
#
#      Annotation for all drug classes and ingredients
#
##########################################################

class MedicationAnnotation(BaseModel):
    rx_class_anti_infective: List[RxClassAntiInfectiveMention] = Field(..., min_length=1)
    rx_class_cancer: List[RxClassCancerMention] = Field(..., min_length=1)
    rx_class_kidney: List[RxClassKidneyMention] = Field(..., min_length=1)
    rx_class_immunosuppression: List[RxClassImmunosuppressionMention] = Field(..., min_length=1)


