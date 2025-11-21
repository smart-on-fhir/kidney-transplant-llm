from pathlib import Path
import pandas as pd
from kidney_transplant_llm.postproc.schema import *

EXCLUDE_COLS = SAMPLE_COLS
EXCLUDE_VALS = [NOT_MENTIONED, NONE_OF_THE_ABOVE]

###############################################################################
# Term Frequency for each column
###############################################################################
def count_tf(parsed_csv:Path|str, stratifier:str = SUBJECT_REF, first=False) -> pd.DataFrame:
    """
    Get Term Frequency for each CSV column, stratified by `stratifier`.
    From parsed_csv count the number of times (term frequency) of each column:value pair.

    :param parsed_csv: LLM output CSV
    :param stratifier: by PAITENT_ID or any supported column in the CSV
    :param first: only get the first hit (highest TF)
    :return: string output tsv
    """
    df = pd.read_csv(parsed_csv)
    out_rows = list()

    for col in df.columns:
        if col in EXCLUDE_COLS or '_spans_' in col:
            # print(f'Skipping {col}')
            continue

        df_filtered = df[df[col].notna() & ~df[col].isin(EXCLUDE_VALS)]

        if first:
            term_freq = (df_filtered
                         .groupby([stratifier, col])
                         .size()
                         .reset_index(name='cnt')
                         .sort_values(by=[stratifier, 'cnt'], ascending=[True, False])
                         .groupby(stratifier, as_index=False)
                         .first())
        else:
            term_freq = (df_filtered.groupby([stratifier, col])
                         .size()
                         .reset_index(name='cnt')
                         .sort_values(by=[stratifier, 'cnt'], ascending=[True, False]))

        # Append structured rows
        for _, row in term_freq.iterrows():
            out_rows.append({
                stratifier: row[stratifier],
                "column": col,
                "value": row[col],
                "count": row["cnt"]
            })
    return pd.DataFrame(out_rows)
