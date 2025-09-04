from enum import StrEnum

##########################################################
#
# Rx AntiInfective --> Infection SUSPECTED (or CONFIRMED)
#
##########################################################

class RxClassAntiInfective(StrEnum):
    VIRAL = 'Antiviral'
    BACTERIAL = 'Antibacterial'
    FUNGAL = 'Antifungal'
    OTHER = 'Other anti-infective'
    NONE = 'None of the above'
