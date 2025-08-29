from enum import Enum
from dataclasses import dataclass
from typing import Optional
import re

###############################################################################
# @@@ GPT5 generated @@@
###############################################################################
UCUM_SYSTEM = "http://unitsofmeasure.org"

@dataclass(frozen=True)
class UnitValue:
    llm: str            # canonical UCUM code (use this in FHIR.code)
    human: str          # display label (show this to humans)
    system: str = UCUM_SYSTEM

class MedicationUnit(Enum):
    # Mass
    MG  = UnitValue("mg",  "milligram (mg)")
    G   = UnitValue("g",   "gram (g)")
    UG  = UnitValue("ug",  "microgram (ug / mcg)")
    KG  = UnitValue("kg",  "kilogram (kg)")

    # Volume
    ML  = UnitValue("mL",  "milliliter (mL)")
    L   = UnitValue("L",   "liter (L)")

    # International Units
    U   = UnitValue("U",    "unit (U)")
    IU  = UnitValue("[iU]", "international unit ([iU])")

    # Countable units
    TABLET      = UnitValue("{tablet}",      "tablet")
    CAPSULE     = UnitValue("{capsule}",     "capsule")
    PUFF        = UnitValue("{puff}",        "puff")
    PATCH       = UnitValue("{patch}",       "patch")
    SUPPOSITORY = UnitValue("{suppository}", "suppository")

    # Ratios
    MG_PER_ML          = UnitValue("mg/mL",       "milligram per milliliter (mg/mL)")
    MG_PER_KG          = UnitValue("mg/kg",       "milligram per kilogram (mg/kg)")
    U_PER_KG           = UnitValue("U/kg",        "units per kilogram (U/kg)")
    UG_PER_KG_PER_MIN  = UnitValue("ug/kg/min",   "microgram per kilogram per minute (ug/kg/min)")

    # Time units (for infusion rates)
    H   = UnitValue("h",   "hour (h)")
    MIN = UnitValue("min", "minute (min)")
    D   = UnitValue("d",   "day (d)")

    # Convenience accessors
    @property
    def code(self) -> str:  # alias for llm
        return self.value.llm

    @property
    def llm(self) -> str:
        return self.value.llm

    @property
    def human(self) -> str:
        return self.value.human

    @property
    def system(self) -> str:
        return self.value.system

# ---- Normalization helper (optional) ----

_ALIASES = {
    # mass
    "mcg": "ug", "μg": "ug", "microgram": "ug",
    "milligram": "mg", "gram": "g", "kilogram": "kg",
    # volume
    "ml": "mL", "milliliter": "mL", "litre": "L", "liter": "L",
    # IU/unit
    "iu": "[iU]", "International Unit": "[iU]",
    "unit": "U", "units": "U",
    # countable
    "tab": "{tablet}", "tabs": "{tablet}", "tablet": "{tablet}",
    "cap": "{capsule}", "caps": "{capsule}", "capsule": "{capsule}",
    "puff": "{puff}", "actuation": "{puff}",
    "patch": "{patch}",
    "supp": "{suppository}", "suppository": "{suppository}",
    # ratios
    "mg/ml": "mg/mL", "mg per ml": "mg/mL",
    "u/kg": "U/kg", "unit/kg": "U/kg", "units/kg": "U/kg",
    "ug/kg/min": "ug/kg/min", "mcg/kg/min": "ug/kg/min", "μg/kg/min": "ug/kg/min",
    # time
    "hr": "h", "hour": "h", "hours": "h",
    "minute": "min", "minutes": "min",
    "day": "d", "days": "d",
}

# Map UCUM code → enum member for fast lookup
_CODE_TO_MEMBER = {m.code: m for m in MedicationUnit}

def normalize_unit(text: str) -> Optional[MedicationUnit]:
    """
    Normalize free-text to a MedicationUnit. Returns None if unknown.
    """
    if not text:
        return None
    t = text.strip()

    # direct code match (case-sensitive first)
    if t in _CODE_TO_MEMBER:
        return _CODE_TO_MEMBER[t]

    # case-insensitive code match
    for code, member in _CODE_TO_MEMBER.items():
        if t.lower() == code.lower():
            return member

    # alias match
    key = re.sub(r"\s+", " ", t).strip()
    code = _ALIASES.get(key) or _ALIASES.get(key.lower())
    if code and code in _CODE_TO_MEMBER:
        return _CODE_TO_MEMBER[code]

    return None

# ---- Example usage ----
# m = MedicationUnit.MG
# m.llm -> "mg"
# m.human -> "milligram (mg)"
# m.system -> "http://unitsofmeasure.org"
# normalize_unit("mcg") -> MedicationUnit.UG
