import json 
import os
from pydantic import BaseModel, Field

from kidney_transplant_llm.pydantic_utils import SpanAugmentedMention


###############################################################################
# History of Multiple Transplants
#
# Mentions relevant in tracking if this patient has a history of multiple transplants,
# renal or otherwise.
###############################################################################
class MultipleTransplantHistoryMention(SpanAugmentedMention):
    """
    Does this patient have a history of multiple transplants, renal or otherwise?
    For use in reevaluating the patients in our cohort, excluding patients with a history
    of multiple transplants from our analysis.
    """

    multiple_transplant_history: bool = Field(
        False, description="Whether there is any mention of a history of multiple transplants."
    )


###############################################################################
# Aggregated Annotation and Mention Classes
#
# This is the top-level structure for the pydantic models used in IRAE tasks.
###############################################################################


class MultipleTransplantHistoryAnnotation(BaseModel):
    """
    An object-model for annotations of patients with a history of multiple transplants.
    Take care to avoid false positives, like confusing information that only
    appears in family history for patient history. Annotations should indicate
    the relevant details of the finding, as well as some additional evidence
    metadata to validate findings post-hoc.
    """

    multiple_transplant_history_mention: MultipleTransplantHistoryMention


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)

    with open(f"{basedir}/schemas/irae_multiple_transplant_history.json", "w", encoding="utf8") as f:
        json.dump(MultipleTransplantHistoryAnnotation.model_json_schema(), f, indent=2)
