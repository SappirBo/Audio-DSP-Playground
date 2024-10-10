import json
from .EffectInterface import EffectInterface
from .DigitalDelay import DigitalDelay
from .Overdrive import Overdrive


def updateEffectsJson():
    effects_list = getEffectsList()
    effects_dict = {"effects": effects_list}
    with open('effects.json', 'w') as f:
        json.dump(effects_dict, f)
    
def getEffectsList() -> list[str]:
    effects_list = [
        "Sappir",
        "BB Tubes",
        "API 2500",
        "SSL G-Channel",
        "SSL G-Equalizer",
        "SSL G-Master Buss Compressor",
        "SSL E-Channel",
        "Abbey Road RS124 Compressor",
        "Abbey Road J37 Tape",
        "Abbey Road TG Mastering Chain",
        "Abbey Road Saturator",
        "Kramer PIE Compressor",
        "Kramer HLS Channel",
        "CLA-2A Compressor / Limiter",
        "CLA-76 Compressor / Limiter"
    ]

    return effects_list

#ToDo: Read the current avaliable effects!

updateEffectsJson()