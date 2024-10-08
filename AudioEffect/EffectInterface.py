from abc import ABC, abstractmethod

class EffectInterface(ABC):
    @abstractmethod
    def process(self, data, rate):
        """
        Process the audio data.
        
        Parameters:
        data (numpy.array): The audio data to process.
        rate (int): The sampling rate of the audio data.
        
        Returns:
        numpy.array: The processed audio data.
        """
        pass