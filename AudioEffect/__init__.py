import json
from .EffectInterface import EffectInterface
from .DigitalDelay import DigitalDelay
from .Overdrive import Overdrive
import os

def updateEffectsJson():
    effects_list = getEffectsList()
    effects_dict = {"effects": effects_list}
    with open('effects.json', 'w') as f:
        json.dump(effects_dict, f)
    
def getEffectsList() -> list[str]:
    effects_list_tmp = [
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


    effects_list = res = get_all_files_in_this_dir()
    map_out_interface(res)
    remove_py_suffix(res)

    return effects_list

def get_all_files_in_this_dir() -> list:
    
    dir_path = os.path.dirname(os.path.realpath(__file__)) # folder path
    res = [] # list to store files

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)): # check if current path is a file
            res.append(path)
    print(res)
    return res

def map_out_interface(files_list:list) -> None:
    files_list.remove("EffectInterface.py")
    files_list.remove("__init__.py")

def remove_py_suffix(files_list: list) -> None:
    for i in range(len(files_list)):
        if files_list[i].endswith('.py'):
            files_list[i] = files_list[i][:-3]


updateEffectsJson()