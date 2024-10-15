import json
from .EffectInterface import EffectInterface
from .DigitalDelay import DigitalDelay
from .Overdrive import Overdrive
from.Level import Level
from .EffectObjectMap import EffectObjectMap
import os

def update_effects_Json(effects_list:list[str] = None) -> None:
    effects_dict = {"effects": effects_list}
    with open('effects.json', 'w') as f:
        json.dump(effects_dict, f)

def update_effects_params_Json(effects_list:list[str] = None) -> None:
    effect_params_dict:dict = {}
    effect_map = EffectObjectMap()
    for effect_name in effects_list:
        effect = effect_map.get_single_effect_obj(effect_name)
        effect_params_dict[effect_name] = effect.get_effect_arguments()
    effects_dict = {"effects": effect_params_dict}
    write_dict_to_json("effects_params.json",effects_dict)

def write_dict_to_json(path:os.path, data:dict) ->None:
    with open(path, 'w') as f:
        json.dump(data, f) 
    
def get_effects_list() -> list[str]:
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
    return res

def map_out_interface(files_list:list) -> None:
    files_list.remove("EffectInterface.py")
    files_list.remove("EffectObjectMap.py")
    files_list.remove("__init__.py")

def remove_py_suffix(files_list: list) -> None:
    for i in range(len(files_list)):
        if files_list[i].endswith('.py'):
            files_list[i] = files_list[i][:-3]


'''
Start Script For AudioEffect
'''
effects_list:list[str] = get_effects_list()
update_effects_Json(effects_list)
update_effects_params_Json(effects_list)


