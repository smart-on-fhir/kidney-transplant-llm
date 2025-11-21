import pandas as pd
from pathlib import Path
from typing import List, Optional
from kidney_transplant_llm.postproc import filetool
from kidney_transplant_llm.postproc.schema import (
    SUBJECT_REF,
    ENCOUNTER_REF,
    DOCUMENT_REF,
    SORT_BY_DATE,
    ENC_ORDINAL,
    DOC_ORDINAL)

def pivot_highlights_df(
    df: pd.DataFrame,
    index_cols: Optional[List[str]] = None,
    name_col: str = "sublabel_name",
    value_col: str = "sublabel_value",
    aggfunc: str = "first",
) -> pd.DataFrame:
    """
    Pivot a long sublabel table into a wide format where each sublabel_name
    becomes its own column with sublabel_value as the cell value.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with at least `index_cols`, `name_col`, and `value_col`.
    index_cols : list of str, optional
        Columns to use as the index (grouping keys). If None, uses the
        standard Athena schema you described:
            [
                "subject_ref",
                "encounter_ref",
                "documentreference_ref",
                "sort_by_date",
                "enc_period_ordinal",
                "doc_ordinal",
            ]
    name_col : str, default "sublabel_name"
        Column name that contains the sublabel names (future wide columns).
    value_col : str, default "sublabel_value"
        Column name that contains the sublabel values (cell values).
    aggfunc : str or callable, default "first"
        Aggregation function to resolve duplicates for a given (index, name_col)
        pair. Common options: "first", "max", "min", "last", etc.

    Returns
    -------
    pd.DataFrame
        Wide-format DataFrame with index_cols plus one column per distinct
        sublabel_name.
    """
    if index_cols is None:
        index_cols = [
            SUBJECT_REF,
            ENCOUNTER_REF,
            DOCUMENT_REF,
            SORT_BY_DATE,
            ENC_ORDINAL,
            DOC_ORDINAL
        ]

    wide = (
        df.pivot_table(
            index=index_cols,
            columns=name_col,
            values=value_col,
            aggfunc=aggfunc,
        )
        .reset_index()
    )
    wide.columns.name = None
    return wide

def pivot_highlights_csv(highlights_csv:str = 'irae__highlights_donor.csv') -> Path:
    input_csv = filetool.path_highlights(highlights_csv)
    output_csv = Path(str(input_csv).replace('.csv', '.pivot.csv'))
    output_df = pivot_highlights_df(pd.read_csv(input_csv))
    output_df.to_csv(output_csv)
    return output_csv
