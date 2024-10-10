import numpy as np
import sys
import math
from .EffectInterface import EffectInterface

class Overdrive(EffectInterface):
    def __init__(self, mix:float, drive:float, level:float):
        self.mix = self.set_between_range(0, 1, mix)
        self.drive = self.set_between_range(0,10,drive)
        self.level = self.set_between_range(0,10,level)

    def process(self, data: np.ndarray, rate: int = 44100):
        samples_drived: np.ndarray = np.zeros_like(data)
        for i in range(len(data)):
            # Extract left and right channels
            left_channel = data[i][0]
            right_channel = data[i][1]
            
            left_channel = self.__scail_from_int_to_fraction(left_channel)
            right_channel = self.__scail_from_int_to_fraction(right_channel)

            # Process each channel
            drived_left = self.__process_sample(left_channel)
            drived_right = self.__process_sample(right_channel)

            drived_left = self.__scail_from_fraction_to_int(drived_left)
            drived_right = self.__scail_from_fraction_to_int(drived_right)

            samples_drived[i] = [drived_left, drived_right]
        
        return samples_drived
        
    def __process_sample(self, sample:float):
        
        sample_abs = abs(sample)
        if sample_abs == 0:
            return 0
        elif sample_abs <= 1/3:
            return 2 * sample
        elif sample_abs > 1/3 and sample_abs <= 2/3:
            return (3 - math.pow(2 - 3*sample)) / 3
        elif sample_abs > 2/3:
            return 1
        else:
            return 0


    def __scail_from_int_to_fraction(self, num):
        max_16byte_int = 32767
        return float(num/ max_16byte_int)

    def __scail_from_fraction_to_int(self, num):
        max_16byte_int = 32767
        return int(num* max_16byte_int)