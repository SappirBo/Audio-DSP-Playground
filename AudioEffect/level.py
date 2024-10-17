import numpy as np
from .effect_interface import EffectInterface

class Level(EffectInterface):
    def __init__(self, level:float= 0):
        self.level = self.set_between_range(-10,10,level)

    def process(self, data: np.ndarray, rate: int = 44100)->None:
        self.set_levels(self.level, data)
            
    def get_effect_arguments(self)->dict:
        arguments:dict =  {
            "parameters":{
                "level": {
                    "min":-10.0,
                    "max": 10.0
                }
            }
        }
        return arguments