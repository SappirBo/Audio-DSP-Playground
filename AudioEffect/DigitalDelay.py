import numpy as np
from .EffectInterface import EffectInterface

class DigitalDelay(EffectInterface):
    def __init__(self, feedback:float=0.5, time:float=0.5,  mix:float=0.5):
        """
        Initialize the DigitalDelay effect with decay and mix parameters.
        
        Parameters:
        feedback (float): Controls the feedback duration of the delay. Values  range from 0 to 1.
        mix (float): Controls the mix between the original and reverberated sound. Values  range from 0 to 1.
        """
        self.feedback = self.set_between_range(0, 1, feedback)
        self.time = self.set_between_range(0, 10,time)
        self.mix = self.set_between_range(0,1, mix)
        self.delay_buffer = np.zeros_like(44100*1)

    def process(self, data: np.ndarray, rate=44100) -> None:
        """
        Apply a delay effect directly to the audio data in-place.
        
        Parameters:
        data (numpy.array): The audio data to process. This data will be modified in place.
        rate (int): The sampling rate of the audio data.
        """
        self.delay_buffer = np.zeros_like(data)
        self.delay_buffer = self.delay_buffer[0: int(44100 * self.time)]
        # samples_delayed: np.ndarray = np.zeros_like(data)
        # data.setflags(write=1)
        delay_index = 0
        for i in range(len(data)):
            new_sample =  data[i] * (1 - self.mix) +  self.delay_buffer[delay_index] * (self.mix)
            data[i] =  new_sample
            self.delay_buffer[delay_index] = new_sample * self.feedback
            delay_index += 1
            if delay_index == len(self.delay_buffer):
                delay_index = 0
            

    def process_get_new_ndarray(self, data, rate=44100):
        """
        Apply a delay effect directly to the audio data in-place.
        
        Parameters:
        data (numpy.array): The audio data to process. This data will be modified in place.
        rate (int): The sampling rate of the audio data.
        """
        self.delay_buffer = np.zeros_like(data)
        self.delay_buffer = self.delay_buffer[0: int(44100 * self.time)]
        samples_delayed: np.ndarray = np.zeros_like(data)
        delay_index = 0
        for i in range(len(data)):
            sample = data[i]
            new_sample =  sample * (1 - self.mix) +  self.delay_buffer[delay_index] * (self.mix)
            samples_delayed[i] =  new_sample
            self.delay_buffer[delay_index] = new_sample * self.feedback
            delay_index += 1
            if delay_index == len(self.delay_buffer):
                delay_index = 0
            
        return samples_delayed