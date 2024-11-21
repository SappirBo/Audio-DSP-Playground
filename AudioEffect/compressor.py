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
        self.process_python(data, rate)
        # self.process_rust(data, rate)

    def process_rust(self, data:np.ndarray, rate:int = 44100):
        process_data = data.astype(np.float64)
        audio_process_lib.compress(process_data, self.threshold, self.ratio, self.attack, self.release)
        np.copyto(data, process_data)

    def process_python(self, data:np.ndarray, rate:int = 44100):
        second:float = 1000.0
        attack_in_seconds:float = self.attack / second
        release_in_seconds:float = self.attack / second

        bits_to_attack:int = int(rate * attack_in_seconds)
        bits_to_release:int = int(rate * release_in_seconds)
        
        threshold_range:float = 100.0
        sample_max_val:float = 1.0
        sample_threashold_chunck:float = sample_max_val / threshold_range

        sample_threashold:float = self.threshold * sample_threashold_chunck

        apply_compression:bool = False
        attack_counter:int = 0
        release_counter:int = 0
        refinement:int = 0

        for i in range(len(data)):
            if abs(data[i][0]) > abs(sample_threashold) or abs(data[i][1]) > abs(sample_threashold):
                if apply_compression is False:
                    apply_compression = True
                    attack_counter = 0
                release_counter = 0
            
            if apply_compression:
                if attack_counter <= bits_to_attack:
                    refinement = int(attack_counter/ bits_to_attack)
                    left  = self.compress(data[i][0], refinement)
                    right = self.compress(data[i][1], refinement)
                    data[i] = [left, right]
                    attack_counter += 1
                elif release_counter < bits_to_release:
                    refinement = int(release_counter/ bits_to_release)
                    left  = self.compress(data[i][0], refinement)
                    right = self.compress(data[i][1], refinement)
                    data[i] = [left, right]
                    release_counter += 1
                else:
                    apply_compression = False

    def compress(self, sample:float, refinement:float) -> float:
        decrease:float = sample /  self.ratio
        factor:float = (self.ratio * refinement) if (self.ratio * refinement) > 1.0 else 1.0
        if self.ratio > 1:
            decrease = sample/factor
        sample = (1 - self.mix) * sample + (self.mix)*(decrease)

        return sample

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
                "min":-100.0,
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

   

