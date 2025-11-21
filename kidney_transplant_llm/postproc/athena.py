from pathlib import Path
from kidney_transplant_llm.postproc import filetool
from kidney_transplant_llm.postproc.schema import (
    SUBJECT_REF,
    DOCUMENT_REF,
    NOTE_REF,
    SORT_BY_DATE,
    ENC_ORDINAL,
    DOC_ORDINAL,
    SAMPLE_COLS,
    HIGHLIGHT_COLS,
    NLP_DONOR_GPT_OSS_120B)

def select_sql(highlights='irae__highlights_donor',
               sample='irae__sample_casedef_index',
               origin=NLP_DONOR_GPT_OSS_120B) -> str:
    """
    :param sample: SQL Table name of sample CaseDef
    :param highlights: SQL Table name of highlights LLM
    :param origin: default GPT_OSS_120B
    :return: str SELECT
    """
    view = filetool.name_view(highlights, sample)

    sample_cols = [f'sample.{col}' for col in SAMPLE_COLS]
    sample_cols = '\n,'.join(sample_cols)

    highlight_cols = [f'highlights.{col}' for col in HIGHLIGHT_COLS]
    highlight_cols = '\n,'.join(highlight_cols)

    _sql = [
        f"CREATE or replace view {view} AS",
        "SELECT distinct",
        sample_cols, ',',
        highlight_cols,
        f"FROM  {highlights} as highlights, {sample} as sample",
        f"WHERE highlights.{NOTE_REF} = sample.{DOCUMENT_REF}",
        f"AND   origin='{origin}'",
        f"ORDER BY {SUBJECT_REF}, {SORT_BY_DATE}, {ENC_ORDINAL}, {DOC_ORDINAL}",
        ";\n"
    ]
    return '\n'.join(_sql)

def select_sql_file(highlights='irae__highlights_donor',
                    sample='irae__sample_casedef_index',
                    origin=NLP_DONOR_GPT_OSS_120B) -> Path:

    view = filetool.name_view(highlights, sample)
    text_sql = select_sql(highlights, sample, origin)
    file_sql = filetool.path_highlights(f'{view}.sql')
    with open(str(file_sql), 'w') as f:
        f.write(text_sql)
    return file_sql
