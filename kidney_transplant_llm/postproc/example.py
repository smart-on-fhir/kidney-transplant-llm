from kidney_transplant_llm.postproc import (
    schema,
    athena,
    filetool,
    pivot_table,
    rank_llm)
from postproc.schema import SUBJECT_REF


def highlights_donor_index():
    task = 'irae__highlights_donor_index'
    print('######################################################################')
    print('TASK: ', task)
    print(f'Step1: ', 'create view {task}')
    print(f'Output: {task}.sql')
    sql = athena.select_from_athena(
        sample = 'irae__sample_casedef_index',
        highlights = 'irae__highlights_donor')

    file_sql = filetool.path_highlights(f'{task}.sql')
    with open(str(file_sql), 'w') as f:
        f.write(sql)
    print('######################################################################')
    print('Step2: Pivot CSV sublabel_name --> as columns')
    print(f'Input: {task}.csv')
    print(f'Output: {task}.pivot.csv')
    output_csv = pivot_table.pivot_highlights_csv(highlights_csv=f'{task}.csv')
    print(output_csv)

    print('######################################################################')
    print('Step3: Rank LLM term frequency')
    input_csv = filetool.path_highlights(f'{task}.pivot.csv')
    output_csv = filetool.path_highlights(f'{task}.pivot.tf.csv')
    output_df = rank_llm.count_tf(input_csv, stratifier=SUBJECT_REF)
    output_df.to_csv(output_csv, index=False)
    print(output_csv)
    print('######################################################################')

if __name__ == '__main__':
    highlights_donor_index()
