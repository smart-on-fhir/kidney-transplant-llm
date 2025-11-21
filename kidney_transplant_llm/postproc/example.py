from kidney_transplant_llm.postproc.schema import (
    SAMPLE_PRE,
    SAMPLE_INDEX,
    SAMPLE_POST,
    SUBJECT_REF,
    ENCOUNTER_REF,
    NLP_GPT_OSS_120B,
    NLP_DONOR_GPT_OSS_120B)
from kidney_transplant_llm.postproc import (
    athena,
    filetool,
    pivot_table,
    cumulative)

def pipeline(highlights:str, sample:str, origin:str):
    view = filetool.name_view(highlights, sample)
    print('######################################################################')
    print('VIEW: ', view)
    print(f'Step1: create view {view}')
    output_sql = athena.create_view_sql(highlights= highlights, sample=sample, origin=origin)

    print(f'Output: {output_sql}')
    print('######################################################################')
    print('Step2: Pivot CSV sublabel_name --> as columns')
    print(f'Input: {view}.csv')
    output_csv = pivot_table.pivot_highlights_csv(highlights_csv=f'{view}.csv')
    print(output_csv)

    print('######################################################################')
    print('Step3: Rank LLM term frequency')
    input_csv = filetool.path_highlights(f'{view}.pivot.csv')
    output_csv = filetool.path_highlights(f'{view}.pivot.tf.csv')
    output_df = rank_llm.count_tf(input_csv, stratifier=SUBJECT_REF)
    output_df.to_csv(output_csv, index=False)
    print(output_csv)
    print('######################################################################')

def highlights_donor_index(highlights:str = 'irae__highlights_donor',
                           sample:str = SAMPLE_INDEX,
                           origin:str=NLP_DONOR_GPT_OSS_120B):
    pipeline(highlights, sample, origin)

def highlights_longitudinal(highlights:str = 'irae__highlights_longitudinal',
                            sample:str = SAMPLE_POST,
                            origin:str= NLP_GPT_OSS_120B):
    pipeline(highlights, sample, origin)

if __name__ == '__main__':
    highlights_donor_index()
    highlights_longitudinal()
