import pandas as pd

DIRICHLET_MIN_COUNT = 4

# Main dataframe we start with is our term frequency counted df 
df = pd.read_csv('data/irae/highlights/irae__highlights_donor_index.pivot.tf.csv')

# For each column/subvalue type, we want a separate df for checking uniqueness and double counts
subvalue_types = [
    "Donor Relationship",
    "Donor Type",
    "Hla Match Quality",
    "Hla Mismatch Count",
    "Transplant Date",
]

def print_counts_info(df: pd.DataFrame, subvalue_types: list[str]):
    print('================ Counting Possible Autoprocessing Info ================')
    # Get the unique subject ids
    unique_ids = df['subject_ref'].unique()
    print(f'DIRICHLET_MIN_COUNT cutoff (how many repeated observations to be sure) set to {DIRICHLET_MIN_COUNT}')
    print(f'Total unique subject ids: {len(unique_ids)}')

    for subvalue in subvalue_types:
        subvalue_df = df[df['column'] == subvalue]
        unique_subvalue_ids = subvalue_df['subject_ref'].unique()
        print(f'Subvalue Type: {subvalue}')
        print(f'\tUnique subject ids with this subvalue: {len(unique_subvalue_ids)}')

        # For each patient id, we check to see if there are 0/1/more than one rows with his subject_ref
        counts = subvalue_df['subject_ref'].value_counts()
        zeros = len([sid for sid in unique_ids if sid not in counts.index])
        ones = (counts == 1).sum()
        multiples = (counts > 1).sum()
        print(f'\tSubjects with NO observations for this subvalue: {zeros}')
        print(f'\tSubjects with DISCORDANT observations (more than 1 unique value per subject_ref) for this subvalue: {multiples}')
        print(f'\tSubjects with EXACTLY 1 row for this subvalue: {ones}')

        # Looking only at subject_refs with ones, check the counts for them
        counts_ones = counts[counts == 1]
        ids_above_cutoff = []
        if not counts_ones.empty:
            print(f'\t\tFor subject_refs with EXACTLY 1 row, checking counts against Dirichlet min count of {DIRICHLET_MIN_COUNT}:')
            # Point back to the subvalue_df to get the actual counts
            for sid in counts_ones.index.unique():
                max_count = max(subvalue_df[subvalue_df['subject_ref'] == sid]['count'].values)
                if max_count >= DIRICHLET_MIN_COUNT:
                    ids_above_cutoff += sid
            print(f'\t\tNumber of {subvalue} instances with count BELOW Dirichlet min count: {len(counts_ones.index.unique()) - len(set(ids_above_cutoff))}')
            print(f'\t\tNumber of {subvalue} instances with count above Dirichlet min count: {len(set(ids_above_cutoff))}')
            print('--------------------------------------------------')

if __name__ == '__main__':
    print_counts_info(df, subvalue_types)