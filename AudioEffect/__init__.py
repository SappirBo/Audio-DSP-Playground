import json
from .effect_interface import EffectInterface
from .digital_delay import DigitalDelay
from .overdrive import Overdrive
from.level import Level
from .effect_object_map import EffectObjectMap
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
        if effect:
            effect_params_dict[effect_name] = effect.get_effect_arguments()
    effects_dict = {"effects": effect_params_dict}
    write_dict_to_json("effects_params.json",effects_dict)

def write_dict_to_json(path:os.path, data:dict) ->None:
    with open(path, 'w') as f:
        json.dump(data, f) 
    
def get_effects_list() -> list[str]:
    effects_list = get_all_files_in_this_dir()
    map_out_interface(effects_list)
    remove_py_suffix(effects_list)
    file_name_to_class_name(effects_list)

    return effects_list

def file_name_to_class_name(files_list:list) -> None:
    for i in range(len(files_list)):
        files_list[i] = file_name_to_class_name_converter(files_list[i])

def get_all_files_in_this_dir() -> list: 
    dir_path = os.path.dirname(os.path.realpath(__file__)) # folder path
    res = [] # list to store files

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)): # check if current path is a file
            res.append(path)
    return res

def map_out_interface(files_list:list) -> None:
    files_list.remove("effect_interface.py")
    files_list.remove("effect_object_map.py")
    files_list.remove("__init__.py")

def remove_py_suffix(files_list: list) -> None:
    for i in range(len(files_list)):
        if files_list[i].endswith('.py'):
            files_list[i] = files_list[i][:-3]

def file_name_to_class_name_converter(file_name:str)->str:
        if file_name is None or file_name == "":
            print(f"EffectObjectMap (file_name_to_class_name_converter): file name is empty or None")
            return None
        if file_name[-3:] == ".py":
            file_name = file_name[:-3]
        
        class_name:str = ""
        upper_flag:bool = False
        
        for i in range(len(file_name)):
            if i == 0:
                class_name += file_name[i].upper()
            elif file_name[i] == '_':
                upper_flag = True
            elif upper_flag:
                class_name += file_name[i].upper()
                upper_flag = False
            else:
                class_name += file_name[i]
        return class_name

'''
Start Script For AudioEffect
'''
effects_list:list[str] = get_effects_list()
update_effects_Json(effects_list)
update_effects_params_Json(effects_list)


