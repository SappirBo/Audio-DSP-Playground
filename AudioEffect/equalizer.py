import numpy as np
from scipy import signal 
from .effect_interface import EffectInterface


class Equalizer(EffectInterface):
    def __init__(self, mix:float=0.0, level:float=0.0,analog:bool=False, high_pass:int = 22000, low_pass:int = 0,
                 Peak:int =0, Peak_Q:float =0.0, Peak_gai:float = 0.0, eq_params:list[dict] = None) :
        self.mix = mix
        self.level = level
        self.analog = analog
        if eq_params is None:
            eq_params = [
                {
                    "type": "high",
                    "cutoff":high_pass
                },
                {
                    "type": "low",
                    "cutoff":low_pass
                }
            ]
        self.eq_params:list[dict] = eq_params
        pass

    def process(self, data:np.ndarray, rate:int = 44100):
        """
        Process the audio data.
        
        Parameters:
        data (numpy.array): The audio data to process.
        rate (int): The sampling rate of the audio data.
        """
        for param in self.eq_params:
            type = param.get('type')
            cutoff = param.get('cutoff')
            b, a = self.create_fillter(cutoff=cutoff, filter_type=type)
            filtered_data = signal.filtfilt(b, a, data, axis=0)
            data[:] = filtered_data

    def create_fillter(self,order:int=5, cutoff:int=500, rate:int=44100, filter_type:str='low', analog:bool=False):
        '''
        Create new Butterworth digital and analog filters

        Params:
        '''
        b,a = signal.butter(5, cutoff, fs=rate, btype=filter_type)

        return b,a

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
                "level": {
                    "p_type": "slider",
                    "min":-10.0,
                    "max": 10.0,
                    "default": 0.0
                },
                "high_pass":{
                    "p_type": "slider",
                    "min":15,
                    "max":22000,
                    "default":15
                },
                "low_pass":{
                    "p_type": "slider",
                    "min":15,
                    "max":22000,
                    "default":22000
                },
                "Peak":{
                    "p_type": "slider",
                    "min":15,
                    "max":22000,
                    "default":500
                },
                "Peak_Q":{
                    "p_type": "slider",
                    "min":1.0,
                    "max":10.0,
                    "default":1.0
                },
                "Peak_gain":{
                    "p_type": "slider",
                    "min":-10.0,
                    "max":10.0,
                    "default":0.0
                }
            }
        }
        return arguments


 
     