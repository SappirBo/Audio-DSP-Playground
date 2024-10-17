from .effect_interface import EffectInterface
from .digital_delay import DigitalDelay
from .overdrive import Overdrive
from .equalizer import Equalizer
from .level import Level

class EffectObjectMap:
    def __init__(self):
        '''
        This class is a Effect name to Effect object converter.
        Here all the effects map will be updated and used to get a single onject of an EffectInteface. 
        '''
        self.effect_class_map = {
            'DigitalDelay': DigitalDelay,
            'Overdrive': Overdrive,
            'Level': Level,
            "Equalizer": Equalizer
        }
        pass

    def get_single_effect_obj(self, effect_name:str)->EffectInterface:
        # effect_name = self.file_name_to_class_name_converter(effect_name)
        if effect_name not in self.effect_class_map:
            print(f"EffectChain: get_single_effect_obj: {effect_name} not found in effect class map!")
            return 
        else:
            return self.effect_class_map.get(effect_name)()
        
    def get_single_effect_class(self, effect_name:str)->EffectInterface:
        if effect_name not in self.effect_class_map:
            print(f"EffectChain: get_single_effect_obj: {effect_name} not found in effect class map!")
            return 
        else:
            return self.effect_class_map.get(effect_name)
        
    # def file_name_to_class_name_converter(self, file_name:str)->str:
    #     if file_name is None or file_name == "":
    #         print(f"EffectObjectMap (file_name_to_class_name_converter): file name is empty or None")
    #         return None
    #     if file_name[-3:] == ".py":
    #         file_name = file_name[:-3]
        
    #     class_name:str = ""
    #     upper_flag:bool = False
        
    #     for i in range(len(file_name)):
    #         if i == 0:
    #             class_name += file_name[i].upper()
    #         elif file_name[i] == '_':
    #             upper_flag = True
    #         elif upper_flag:
    #             class_name += file_name[i].upper()
    #             upper_flag = False
    #         else:
    #             class_name += file_name[i]
    #     return class_name

