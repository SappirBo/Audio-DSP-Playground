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
        
    def set_levels(self,level,  sample:np.ndarray):
        sample_scaled = float(sample) / sys.maxsize
        level_scaled = float(level) / 100 
        sample_times_leveling = sample_scaled * level_scaled 
        sample_leveled = int(float(sys.maxsize) * sample_times_leveling) 
        return sample_leveled 