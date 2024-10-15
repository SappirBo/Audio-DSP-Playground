import numpy as np
import sys
import math
from .EffectInterface import EffectInterface

class Overdrive(EffectInterface):
    def __init__(self, mix:float = 0.5, drive:float = 0, level:float= 0):
        self.mix = self.set_between_range(0, 1, mix)
        self.drive = self.set_between_range(0,10,drive)
        self.level = self.set_between_range(-10,10,level)

    def process(self, data: np.ndarray, rate: int = 44100)->None:
        for i in range(len(data)):
            # Extract left and right channels
            left_channel = data[i][0]
            right_channel = data[i][1]
            
            # Process each channel
            drived_left = self.__process_sample(left_channel)
            drived_right = self.__process_sample(right_channel)

            data[i] = [drived_left, drived_right]
        
        self.set_levels(self.level, data)
        
    def __process_sample(self, sample:float):
        drive_amout, slop = self.scail_acoording_to_drive()
        sample_abs = abs(sample)
        if sample_abs == 0:
            return 0
        elif sample_abs <= 1/3:
            return slop * sample
        elif sample_abs > 1/3 and sample_abs <= 2/3:
            return (drive_amout - (2 - drive_amout * sample)**2) / drive_amout
        elif sample_abs > 2/3:
            return 1
        else:
            return 0
 
    def scail_acoording_to_drive(self):
        drive_amout = self.drive/10 + 3.0
        cut_pont = (drive_amout - (2 - drive_amout * 1/3)**2 ) / drive_amout
        slop = float(cut_pont / (1/3))
        return drive_amout, slop
    
    def get_effect_arguments(self)->dict:
        arguments:dict =  {
            "parameters":{
                "mix":{
                    "min":0.0,
                    "max": 1.0
                },
                "drive":{
                    "min":0.0,
                    "max": 10.0
                },
                "level": {
                    "min":-10.0,
                    "max": 10.0
                }
            }
        }
        return arguments