import os
from pathlib import Path
from kidney_transplant_llm.postproc.schema import *

###############################################################################
# build path to CSV
###############################################################################
def path_phi_dir() -> Path | None:
    if 'LLM_PHI_DIR' not in os.environ:
        print("LLM_PHI_DIR not defined in environment")
    return Path(os.environ['LLM_PHI_DIR']) / 'irae'

def path_sample_pre() -> Path | None:
    return path_sample(SAMPLE_PRE_CSV)

def path_sample_index() -> Path | None:
    return path_sample(SAMPLE_INDEX_CSV)

def path_sample_post() -> Path | None:
    return path_sample(SAMPLE_POST_CSV)

def path_sample(sample_csv: str) -> Path | None:
    return path_phi_dir() / 'sample_casedef' / sample_csv

def path_highlights(highlights_csv='irae__highlights_donor.csv',
                    highlights_dir=HIGHLIGHTS_DONOR_INDEX_100) -> Path | None:
        return path_phi_dir() / highlights_dir / highlights_csv
