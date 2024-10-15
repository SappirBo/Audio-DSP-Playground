import numpy as np
import sys
from abc import ABC, abstractmethod

class EffectInterface(ABC):
    @abstractmethod
    def process(self, data:np.ndarray, rate:int = 44100):
        """
        Process the audio data.
        
        Parameters:
        data (numpy.array): The audio data to process.
        rate (int): The sampling rate of the audio data.
        """
        pass

    def set_between_range(self, min:float , max:float, value:float) -> float:
        if value > max:
            return max
        elif value < min: 
            return min
        else: 
            return value
    
    def get_effect_arguments(self)->dict:
        arguments:dict =  {
            "parameters":{
            "mix":{
                "min":0.0,
                "max": 1.0
            },
            "level": {
                "min":-10.0,
                "max": 10.0
            }
        }
        }
        return arguments
        
    def set_levels(self,level:float,  samples:np.ndarray):
        # scale_level = 1 + level/10
        # if level > 0:
        #     samples *= abs(scale_level)
        # elif level < 0:
        #     samples /= abs(scale_level)
        # else:
        #     pass
        pass
