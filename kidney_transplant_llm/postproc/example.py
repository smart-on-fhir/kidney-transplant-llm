from kidney_transplant_llm.postproc import (
    schema,
    athena,
    filetool,
    pivot_table,
    rank_llm)

if __name__ == '__main__':
    print('Step1: SQL select * from (....) download as CSV')
    print('##############################')
    sql = athena.select_from_athena()
    print(sql)

    print('Step2: Pivot CSV sublabel_name --> as columns')
    print('#############################################')
    input_csv = 'irae__highlights_donor.csv'
    pivot_table.pivot_highlights_csv(input_csv)

    print('Step3: Rank LLM term frequency')
    print('#############################################')
    input_csv = filetool.path_highlights('irae__highlights_donor.pivot.csv')
    output_csv = filetool.path_highlights('irae__highlights_donor.pivot.tf.csv')
    output_df = rank_llm.count_tf(input_csv)
    output_df.to_csv(output_csv, index=False)

    print('Step4: Review LLM term frequency')
    print('#############################################')
    print(output_csv)
