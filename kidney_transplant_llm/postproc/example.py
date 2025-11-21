from kidney_transplant_llm.postproc import (
    schema,
    athena,
    filetool,
    pivot_table,
    rank_llm)

def highlights_donor_index():
    task = 'irae__highlights_donor_index'
    print('Step1: ', task)
    print(f'{task}.sql', '\t', f'create view {task}')
    print('#############################################')
    sql = athena.select_from_athena(
        sample = 'irae__sample_casedef_index',
        highlights = 'irae__highlights_donor')

    file_sql = filetool.path_highlights(f'{task}.sql')
    with open(str(file_sql), 'w') as f:
        f.write(sql)

    print('Step2: Pivot CSV sublabel_name --> as columns')
    print(f'{task}.csv', '\t', f'select * from {task}')
    print('#############################################')
    pivot_csv = pivot_table.pivot_highlights_csv(highlights_csv=f'{task}.csv')
    print(pivot_csv)

    print('Step3: Rank LLM term frequency')
    print('#############################################')
    input_csv = filetool.path_highlights(f'{task}.pivot.csv')
    output_csv = filetool.path_highlights(f'{task}.pivot.tf.csv')
    output_df = rank_llm.count_tf(input_csv, 'subject_ref')
    output_df.to_csv(output_csv, index=False)

    print('Step4: Review LLM term frequency')
    print('#############################################')
    print(output_csv)

if __name__ == '__main__':
    highlights_donor_index()
