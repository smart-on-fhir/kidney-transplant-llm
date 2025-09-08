from enum import StrEnum

##########################################################
#
# Rx Kidney
#
##########################################################
class RxClassKidney(StrEnum):
    RAS = 'Renin–Angiotensin System (especially ACE, ARB, renin inhibitors/blockers)'
    DIURETIC = 'Diuretic'
    STATIN = 'Statin'
    BB = 'Beta Blocker'
    CCB = 'Calcium Channel Blocker'
    NSAID = 'Non Steroidal Anti-Inflammatory Drug'
    OPIOID = 'Opioid medication'
    CONTRAST = 'Iodinated contrast agents'
    OTHER = 'Other drug indicated for treatment of kidney problem(s) or drug with known nephrotoxicity'
    NONE = 'None of the above'
