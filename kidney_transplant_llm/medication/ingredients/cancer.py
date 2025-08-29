from enum import StrEnum

##########################################################
#
# Rx Cancer --> Cancer is CONFIRMED or at least SUSPECTED
#
##########################################################

class RxClassCancer(StrEnum):
    CHEMO = 'Cytotoxic chemotherapy'
    CHECKPOINT = 'Checkpoint inhibitors, especially PD-1, PDL-1, CTLA-4'
    CYTOKINE = 'Cytokine therapy, especially IL-2 and interferon alpha'
    CAR_T = 'Chimeric antigen receptor (CAR-T)'
    OTHER = 'Other drug indicated for treatment of cancer(s)'
    NONE = 'None of the above'
