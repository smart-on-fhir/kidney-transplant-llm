from enum import StrEnum

##########################################################
#
# Rx Kidney
#
##########################################################

class RxClassKidney(StrEnum):
    RAS = 'Renin–Angiotensin System (especially ACE, ARB, renin inhibitors/blockers)'
    Diuretic = 'Diuretic'
    BB = 'Beta Blocker'
    CCB = 'Calcium channel blocker'
    NSAID = 'non steroidal anti-inflammatory drug'
    CONTRAST = 'Iodinated contrast agents'
    OTHER = 'Other ingredient with known association to kidney (indication for treatment or nephrotoxic)'
    NONE = 'None of the above'
