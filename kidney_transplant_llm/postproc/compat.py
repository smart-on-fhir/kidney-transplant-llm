from pathlib import Path
import pandas as pd
from pandas import DataFrame
from kidney_transplant_llm.postproc.schema import *
from kidney_transplant_llm.postproc import filetool

def strip_ref(source:DataFrame, col_ref=DOCUMENT_REF) -> DataFrame:
    """
    :param source: DataFrame with "resource_ref" type columns
    :param col_ref: name of column with values like 'DocumentReference/"
    :return: stripped column with values like "1234-5678"
    """
    return source[col_ref].str.replace(r'^[^/]+/', '', regex=True)

def subject_to_id(source:DataFrame) -> None:
    """
    Inline PATIENT_ID for SUBJECT_REF
    """
    source[PATIENT_ID] = strip_ref(source, SUBJECT_REF)

def docref_to_id(source:DataFrame) -> None:
    """
    Inline DOCUMENT_ID for DOCUMENT_REF
    """
    source[DOCUMENT_ID] = strip_ref(source, DOCUMENT_REF)

def merge_csv(source:Path, target:Path, merge_on=DOCUMENT_ID, merge_add=ENCOUNTER_REF) -> None:
    """
    Update (overwrite!) the target with updated version containing merge_add column from source.
    If that doesn't sound safe to you, use merge instead :)

    :param source: DataFrame CSV file from Athena
    :param target: DataFrame CSV file from LLM
    :param merge_on: column name, usually the DOCUMENT_ID
    :param merge_add: column name, usually the ENCOUNTER_REF
    """
    merged = merge(
        source=pd.read_csv(source),
        target=pd.read_csv(target),
        merge_on=merge_on,
        merge_add=merge_add
    )
    merged.to_csv(target, index=False)
    print('updated ', target)

def merge(source:DataFrame, target:DataFrame, merge_on, merge_add) -> DataFrame:
    """
    Merge source and target DataFrames and get a resulting merged DataFrame.

    :param source: DataFrame CSV file from Athena
    :param target: DataFrame CSV file from LLM
    :param merge_on: column name, usually the DOCUMENT_ID
    :param merge_add: column name, usually the ENCOUNTER_REF
    """
    if merge_add in list(target.columns):
        raise Exception('skipping ', merge_add, ' already present in target')

    if merge_on not in list(source.columns):
        if merge_on == DOCUMENT_ID:
            source[DOCUMENT_ID] = strip_ref(source, DOCUMENT_REF)
        elif merge_on == PATIENT_ID:
            source[PATIENT_ID] = strip_ref(source, SUBJECT_REF)

    return target.merge(
        source[[merge_on, merge_add]],
        on=merge_on,
        how='left')

def merge_defaults():
    merge_csv(source=filetool.path_sample_index(),
              target=filetool.path_both_index_csv())

    merge_csv(source=filetool.path_sample_index(),
              target=filetool.path_donor_csv())

    merge_csv(source=filetool.path_sample_post(),
              target=filetool.path_long_post_10_csv())

if __name__ == '__main__':
    print('are you sure you want to update default CSV?')
    # merge_defaults()


