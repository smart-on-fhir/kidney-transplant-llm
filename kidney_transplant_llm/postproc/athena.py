import pandas as pd
from typing import List, Optional
from kidney_transplant_llm.postproc import filetool
from kidney_transplant_llm.postproc.schema import (
    SUBJECT_REF,
    ENCOUNTER_REF,
    DOCUMENT_REF,
    SORT_BY_DATE,
    ENC_ORDINAL,
    DOC_ORDINAL,
    SAMPLE_COLS,
    HIGHLIGHT_COLS)
from postproc.schema import GPT_OSS_120B


def select_from_athena(sample='irae__sample_casedef_index',
                       highlights='irae__highlights_donor',
                       origin=GPT_OSS_120B) -> str:

    sample_cols = [f'sample.{col}' for col in SAMPLE_COLS]
    sample_cols = '\n\t,'.join(sample_cols)

    highlight_cols = [f'highlights.{col}' for col in HIGHLIGHT_COLS]
    highlight_cols = '\n\t,'.join(highlight_cols)

    _select = "SELECT distinct" + f"\n\t{sample_cols} \n\t,{highlight_cols}"
    _from =  f"\nFROM {sample} as sample, \n\t {highlights} as highlights "
    _where = "\nWHERE highlights.note_ref = sample.documentreference_ref"
    _origin = f"\n AND\torigin='{origin}'"
    _order = "\nORDER by \n\t" + "subject_ref, sort_by_date, enc_period_ordinal, doc_ordinal"

    return _select + _from + _where + _origin + _order

def tabularize(sample_highlight_csv:str) -> pd.DataFrame:
    sample_highlight_csv = filetool.path_highlights(sample_highlight_csv)
    if sample_highlight_csv.exists():
        df = pd.read_csv(sample_highlight_csv)
        return pivot_sublabels_wide(df)
    raise Exception(f"File {sample_highlight_csv} does not exist")

def pivot_sublabels_wide(
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

    # Flatten column index if needed (pivot_table may produce a MultiIndex)
    wide.columns.name = None

    return wide

if __name__ == "__main__":
    print(select_from_athena())
    df_wide = tabularize('irae__highlights_donor.csv')
    print(df_wide.head())
    df_wide.to_csv("irae__highlights_donor.wide.csv", index=False)


