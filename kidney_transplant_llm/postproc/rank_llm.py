from pathlib import Path
import pandas as pd
from kidney_transplant_llm.postproc.schema import *
from kidney_transplant_llm.postproc import filetool

EXCLUDE_COLS = [PATIENT_ID, DOCUMENT_ID]
EXCLUDE_VALS = [NOT_MENTIONED, NONE_OF_THE_ABOVE]

###############################################################################
# Term Frequency for each column
###############################################################################
def count_tf_both_index(stratifier:str = PATIENT_ID, first=False) -> pd.DataFrame:
    return count_tf(parsed_csv=filetool.path_both_index_csv(), stratifier=stratifier, first=first)

def count_tf_donor(stratifier:str = PATIENT_ID, first=False) -> pd.DataFrame:
    return count_tf(parsed_csv=filetool.path_donor_csv(), stratifier=stratifier, first=first)

def count_tf_ongitudinal(stratifier:str = PATIENT_ID, first=False) -> pd.DataFrame:
    return count_tf(parsed_csv=filetool.path_long_post_10_csv(), stratifier=stratifier, first=first)

def count_tf(parsed_csv:Path|str, stratifier:str = PATIENT_ID, first=False) -> pd.DataFrame:
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

###############################################################################
# Main
###############################################################################
def main():
    print('processing TF (term frequency) counts')

    both_csv = filetool.path_both_index_csv()
    donor_csv = filetool.path_donor_csv()
    longitudinal_csv = filetool.path_long_post_10_csv()

    for target_csv in [both_csv, donor_csv, longitudinal_csv]:
        for first in [True, False]:
            first_label = 'first' if first else 'all'
            for stratifier in [PATIENT_ID]:
                target_out = f'{target_csv}.{stratifier}.{first_label}.cnt.csv'

                df_target = count_tf(target_csv, stratifier=stratifier, first=first)
                df_target.to_csv(target_out, index=False)
                print(target_out)

if __name__ == '__main__':
    main()
