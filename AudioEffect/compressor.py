import numpy as np
from scipy import signal

import audio_process_lib

from .effect_interface import EffectInterface
import audio_process_lib

class Compressor(EffectInterface):
    def __init__(self, mix:float=0.0, level:float=0.0, threshold:float=0.0, ratio:float=1.0, attack:float=1.0, release:float=1.0):
        self.mix = mix
        self.level = level
        self.threshold = threshold if threshold < 0.0 else 0.0 # threshold is number [0,-100]
        self.ratio = ratio if ratio > 1.0 else 1.0
        self.attack = attack
        self.release = release
        pass

    def process(self, data:np.ndarray, rate:int = 44100):
        """
        Process the audio data.
        
        Parameters:
        data (numpy.array): The audio data to process.
        rate (int): The sampling rate of the audio data.
        """ 

        process_data = data.astype(np.float64)
        print(f"Max value of data {data.max()}, min value: {data.min()}")

        audio_process_lib.compress(process_data, self.threshold, self.ratio, self.attack, self.release)

        np.copyto(data, process_data)

    def print_args(self):
        print(f"mix = {self.mix}")
        print(f"level = {self.level}")
        print(f"threshold = {self.threshold}")
        print(f"ratio = {self.ratio}")
        print(f"attack = {self.attack}")
        print(f"release = {self.release}")

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
            },
            "threshold":{
                "p_type": "slider",
                "min":-30,
                "max": 0.0
            },
            "ratio":{
                "p_type": "slider",
                "min": 1,
                "max": 8
            },
            "attack":{
                "p_type": "slider",
                "min":1,
                "max": 5000
            },
            "release":{
                "p_type": "slider",
                "min":1,
                "max": 5000
            }
        }
        }
        return arguments

   

