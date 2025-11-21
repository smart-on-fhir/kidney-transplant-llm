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
    return path_sample(f'{SAMPLE_PRE}.csv')

def path_sample_index() -> Path | None:
    return path_sample(f'{SAMPLE_INDEX}.csv')

def path_sample_post() -> Path | None:
    return path_sample(f'{SAMPLE_POST}.csv')

def path_sample(sample_csv: str) -> Path | None:
    return path_phi_dir() / 'sample_casedef' / sample_csv

def path_highlights(highlights_csv='irae__highlights_donor.csv') -> Path | None:
        return path_phi_dir() / 'highlights' / highlights_csv
