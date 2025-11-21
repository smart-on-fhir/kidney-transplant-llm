from kidney_transplant_llm.postproc.schema import (
    SUBJECT_REF,
    DOCUMENT_REF,
    NOTE_REF,
    SORT_BY_DATE,
    ENC_ORDINAL,
    DOC_ORDINAL,
    SAMPLE_COLS,
    HIGHLIGHT_COLS,
    GPT_OSS_120B)

def select_from_athena(sample='irae__sample_casedef_index',
                       highlights='irae__highlights_donor',
                       origin=GPT_OSS_120B) -> str:
    """
    :param sample: SQL Table name of sample CaseDef
    :param highlights: SQL Table name of highlights LLM
    :param origin: default GPT_OSS_120B
    :return: str SELECT
    """
    view = highlights + '_' + sample.replace('irae__sample_casedef_', '')

    sample_cols = [f'sample.{col}' for col in SAMPLE_COLS]
    sample_cols = '\n,'.join(sample_cols)

    highlight_cols = [f'highlights.{col}' for col in HIGHLIGHT_COLS]
    highlight_cols = '\n,'.join(highlight_cols)

    _sql = [
        f"CREATE or replace view {view} AS",
        "SELECT distinct",
        sample_cols, ',',
        highlight_cols,
        f"FROM  {sample} as sample, {highlights} as highlights",
        f"WHERE highlights.{NOTE_REF} = sample.{DOCUMENT_REF}",
        f"AND   origin='{origin}'",
        f"ORDER BY {SUBJECT_REF}, {SORT_BY_DATE}, {ENC_ORDINAL}, {DOC_ORDINAL}",
    ]
    return '\n'.join(_sql)