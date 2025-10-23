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

def path_both_index_csv() -> Path | None:
    """
    :return: path to `BOTH_INDEX` containing donor and "non" donor characteristics in casedef INDEX
    """
    if path_phi_dir():
        file_csv = path_phi_dir() / BOTH_INDEX / GPT_OSS_CSV
        if file_csv.exists():
            return file_csv
    print(f'{BOTH_INDEX} was missing')
    return None

def path_donor_csv() -> Path | None:
    """
    :return: path to `DONOR_INDEX` containing donor characteristics in casedef INDEX
    """
    if path_phi_dir():
        file_csv = path_phi_dir() / DONOR_INDEX / GPT_OSS_CSV
        if file_csv.exists():
            return file_csv
    print(f'{DONOR_INDEX} was missing')
    return None

def path_long_post_10_csv() -> Path | None:
    """
    :return: path to `LONGITUDINAL_POST_10` containing donor characteristics in casedef POST
    :return:
    """
    if path_phi_dir():
        file_csv = path_phi_dir() / LONGITUDINAL_POST_10 / GPT_OSS_CSV
        if file_csv.exists():
            return file_csv
    print(f'{LONGITUDINAL_POST_10} was missing')
    return None

def path_sample_pre() -> Path | None:
    return path_sample(SAMPLE_PRE_CSV)

def path_sample_index() -> Path | None:
    return path_sample(SAMPLE_INDEX_CSV)

def path_sample_post() -> Path | None:
    return path_sample(SAMPLE_POST_CSV)

def path_sample(sample_csv: str) -> Path | None:
    if path_phi_dir():
        file_csv = path_phi_dir() / 'sample_casedef' / sample_csv
        if file_csv.exists():
            print(file_csv)
            return file_csv
    return None

def path_e3(target_dir, file_csv=GPT_OSS_CSV) -> str:
    return Path(E3_IRAE_DIR) / target_dir / 'output' / file_csv

def copy_e3_files() -> str:
    """
    :return: bash script to SCP files from E3
    """
    cmd = list()
    target_list = [
        BOTH_INDEX,
        DONOR_INDEX,
        DONOR_INDEX_10,
        LONGITUDINAL_INDEX_10,
        LONGITUDINAL_POST_10
    ]
    cmd.append(f"cd {path_phi_dir()}")
    for target in target_list:
        cmd.append(f"mkdir -p {target}")
        cmd.append(f"cd {target}")
        cmd.append(f"scp {path_e3(target)} .")
        cmd.append(f"cd ..")
    cmd.append(f"ls -lah")
    return '\n'.join(cmd)


if __name__ == '__main__':
    print('Convenience bash helper to create folder paths so you dont lose your mind DIY by hand')
    print(copy_e3_files())
