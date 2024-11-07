import numpy as np
import sys
import math
from .effect_interface import EffectInterface
import audio_process_lib

class Overdrive(EffectInterface):
    def __init__(self, mix:float = 0.5, level:float= 0):
        self.mix = self.set_between_range(0, 1, mix)
        self.level = self.set_between_range(-10,10,level)

    def process(self, data: np.ndarray, rate: int = 44100)->None:
        # self.process_python(data,rate)
        self.process_rust(data, rate)

    def process_rust(self, data: np.ndarray, rate: int = 44100)->None:
        process_data = data.astype(np.float64)
        audio_process_lib.overdrive(process_data, self.level, self.mix)
        np.copyto(data, process_data)

    def process_python(self, data: np.ndarray, rate: int = 44100)->None:
        for i in range(len(data)):
            # Extract left and right channels
            left_channel = data[i][0]
            right_channel = data[i][1]
            
            # Process each channel
            drived_left = self.__process_sample(left_channel)
            drived_right = self.__process_sample(right_channel)

            data[i] = [drived_left, drived_right]
        
        # self.set_levels(self.level, data)
        
    def __process_sample(self, sample:float):
        sample_abs = abs(sample)
        if sample_abs == 0:
            return 0
        elif sample_abs <= 1/3:
            return 2 * sample
        elif sample_abs > 1/3 and sample_abs <= 2/3:
            return (3 - (2 - 3 * sample)**2) / 3
        elif sample_abs > 2/3:
            return 1
        else:
            return 0
    
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