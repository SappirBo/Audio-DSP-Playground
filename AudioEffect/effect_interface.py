import numpy as np
import sys
from abc import ABC, abstractmethod
import matplotlib as mpl

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
    
    @abstractmethod
    def get_effect_arguments(self)->dict:
        arguments:dict =  {
            "parameters":{
            "mix":{
                "p_type": "slider",
                "min":0.0,
                "max": 1.0
            },
            "level": {
                "p_type": "slider",
                "min":-10.0,
                "max": 10.0
            }
        }
        }
        return arguments
        
    def set_between_range(self, min:float , max:float, value:float) -> float:
        if value > max:
            return max
        elif value < min: 
            return min
        else: 
            return value
        
    def set_levels(self, level: float, data: np.ndarray):
        scale_level = 1 + abs(level / 10)
        print(f"Level={level}, Scaled level = {scale_level}")
        if level > 0:
            data *= scale_level
        elif level < 0:
            data /= scale_level

    def scale_from_dtype_to_fraction(self, data: np.ndarray):
        val_dtype = data.dtype
        if np.issubdtype(val_dtype, np.integer):
            info = np.iinfo(val_dtype)
            max_val = max(abs(info.min), abs(info.max))
            return data.astype(np.float32) / max_val
        else:
            # Data is already floating-point
            return data

    def scale_from_fraction_to_dtype(self, data: np.ndarray, arr_type: np.dtype):
        if np.issubdtype(arr_type, np.integer):
            info = np.iinfo(arr_type)
            max_val = max(abs(info.min), abs(info.max))
            data_int = np.clip(data * max_val, info.min, info.max - 1).astype(arr_type)
            return data_int
        else:
            return data.astype(arr_type)

    def plot_wav(self):
        pass  

