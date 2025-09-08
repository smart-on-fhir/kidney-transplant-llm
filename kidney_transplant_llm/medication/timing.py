from enum import StrEnum
from typing import Optional, Dict, Any

GTS_SYSTEM = "http://terminology.hl7.org/CodeSystem/v3-GTSAbbreviation"

###############################################################################
# @@@ GPT5 generated @@@
###############################################################################

class RxFrequency(StrEnum):
    QD = "QD"       # once daily
    BID = "BID"     # twice daily
    TID = "TID"     # three times daily
    QID = "QID"     # four times daily
    QOD = "QOD"     # every other day
    Q6H = "Q6H"
    Q8H = "Q8H"
    Q12H = "Q12H"
    WEEKLY = "WEEKLY"
    Q2W = "Q2W"
    Q4W = "Q4W"
    MONTHLY = "MONTHLY"
    OTHER = "OTHER" # use timing_text
    NONE = "None of the above"

# Minimal mapper -> FHIR Timing
# periodUnit must be one of: 's'|'min'|'h'|'d'|'wk'|'mo'|'a'
_TIMING_MAP: Dict[RxFrequency, Dict[str, Any]] = {
    RxFrequency.QD:   {"repeat": {"frequency": 1, "period": 1, "periodUnit": "d"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "QD", "display": "every day"}]}},
    RxFrequency.BID:  {"repeat": {"frequency": 2, "period": 1, "periodUnit": "d"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "BID", "display": "2 times a day"}]}},
    RxFrequency.TID:  {"repeat": {"frequency": 3, "period": 1, "periodUnit": "d"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "TID", "display": "3 times a day"}]}},
    RxFrequency.QID:  {"repeat": {"frequency": 4, "period": 1, "periodUnit": "d"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "QID", "display": "4 times a day"}]}},
    RxFrequency.QOD:  {"repeat": {"frequency": 1, "period": 2, "periodUnit": "d"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "QOD", "display": "every other day"}]}},
    RxFrequency.Q6H:  {"repeat": {"frequency": 1, "period": 6, "periodUnit": "h"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "Q6H", "display": "every 6 hours"}]}},
    RxFrequency.Q8H:  {"repeat": {"frequency": 1, "period": 8, "periodUnit": "h"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "Q8H", "display": "every 8 hours"}]}},
    RxFrequency.Q12H: {"repeat": {"frequency": 1, "period": 12, "periodUnit": "h"},
                               "code": {"coding": [{"system": GTS_SYSTEM, "code": "Q12H", "display": "every 12 hours"}]}},
    RxFrequency.WEEKLY: {"repeat": {"frequency": 1, "period": 1, "periodUnit": "wk"}},
    RxFrequency.Q2W:    {"repeat": {"frequency": 1, "period": 2, "periodUnit": "wk"}},
    RxFrequency.Q4W:    {"repeat": {"frequency": 1, "period": 4, "periodUnit": "wk"}},
    RxFrequency.MONTHLY:{"repeat": {"frequency": 1, "period": 1, "periodUnit": "mo"}},
}

def frequency_to_fhir_timing(
    freq: RxFrequency,
    *,
    prn: Optional[bool] = None,
    timing_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Emit a minimal FHIR Timing for a shorthand frequency.
    - PRN is not encoded in Timing; return as a side channel you can attach to Dosage as `asNeededBoolean`.
    - If freq == OTHER, return only text (caller can fill repeat by hand if desired).
    """
    if freq == RxFrequency.OTHER:
        return {"code": {"text": timing_text} if timing_text else None} | {"_note": "Provide repeat manually if known."}

    timing = _TIMING_MAP[freq].copy()
    if timing_text:
        timing["code"] = timing.get("code", {})
        timing["code"]["text"] = timing_text
    # PRN note for caller
    if prn is not None:
        timing["_prn"] = prn  # not standard Timing; carry along for Dosage.asNeededBoolean
    return timing
