import numpy as np
from .EffectInterface import EffectInterface

class SimpleReverb(EffectInterface):
    def __init__(self, decay=0.5, mix=0.5):
        """
        Initialize the SimpleReverb effect with decay and mix parameters.
        
        Parameters:
        decay (float): Controls the decay duration of the reverb. Values  range from 0 to 1.
        mix (float): Controls the mix between the original and reverberated sound. Values  range from 0 to 1.
        """
        self.decay = decay
        self.mix = mix

    def process(self, data, rate=44100):
        """
        Apply a simple reverb effect directly to the audio data in-place.
        
        Parameters:
        data (numpy.array): The audio data to process. This data will be modified in place.
        rate (int): The sampling rate of the audio data.
        """
        echo_gap = int(rate * 0.2)  # Fixed 50ms initial gap
        echo = np.zeros_like(data)
        echo[echo_gap:] = data[:-echo_gap] * self.decay
        return data * (1 - self.mix) + echo * self.mix