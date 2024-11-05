import numpy as np
from scipy import signal

import audio_process_lib

from .effect_interface import EffectInterface
import audio_process_lib

class Compressor(EffectInterface):
    def __init__(self, mix:float=0.0, level:float=0.0, threshold:float=0.0, ratio:float=1.0, attack:float=1.0, release:float=1.0):
        self.mix = mix
        self.level = level
        self.threshold = threshold if threshold < 0.0 else 0.0
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
        one_second = 1000.0
        attack_in_seconds:float = self.attack / one_second
        release_in_seconds:float = self.release / one_second

        bits_to_attack = rate * attack_in_seconds
        bits_to_release = rate * release_in_seconds

        audio_process_lib.mult(1/2, data)

        print("HERE")
        pass

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
                "min":0.0,
                "max": 1.0
            },
            "level": {
                "min":-10.0,
                "max": 10.0
            },
            "threshold":{
                "min":-30,
                "max": 0.0
            },
            "ratio":{
                "min": 1,
                "max": 8
            },
            "attack":{
                "min":1,
                "max": 5000
            },
            "release":{
                "min":1,
                "max": 5000
            }
        }
        }
        return arguments
        

