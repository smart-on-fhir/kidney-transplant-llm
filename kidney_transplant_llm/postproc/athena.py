from kidney_transplant_llm.postproc.schema import GPT_OSS_120B
from kidney_transplant_llm.postproc.schema import (
    SAMPLE_COLS,
    HIGHLIGHT_COLS)

def select_from_athena(sample='irae__sample_casedef_index',
                       highlights='irae__highlights_donor',
                       origin=GPT_OSS_120B) -> str:
    """
    :param sample: SQL Table name of sample CaseDef
    :param highlights: SQL Table name of highlights LLM
    :param origin: default GPT_OSS_120B
    :return: str SELECT
    """
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
