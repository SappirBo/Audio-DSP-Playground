import numpy as np
from .effect_interface import EffectInterface
import audio_process_lib


class Level(EffectInterface):
    def __init__(self, level:float= 0):
        self.level = self.set_between_range(-10,10,level)

    def process(self, data: np.ndarray, rate: int = 44100)->None:
        self.process_python(data,rate)
        # self.process_rust(data,rate)

    def process_python(self, data: np.ndarray, rate: int = 44100)->None:
        # if self.level < 0:
        #     factor = -1 - self.level / 10.0
        # else :
        #     factor = +1 + self.level / 10.0
        factor = 1 + (self.level / 10.0)
        
        for i in range(len(data)):
            data[i] = data[i] * factor

    def process_rust(self, data: np.ndarray, rate: int = 44100)->None:
        process_data = data.astype(np.float64)
        audio_process_lib.process_levels(process_data, self.level)
        np.copyto(data, process_data)     

    def get_effect_arguments(self)->dict:
        arguments:dict =  {
            "parameters":{
                "level": {
                    "p_type": "slider",
                    "min":-10.0,
                    "max": 10.0,
                    "default":0.0
                }
            }
        }
        return arguments