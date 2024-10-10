import numpy as np
from typing import List, Dict
from AudioEffect import EffectInterface, Overdrive, DigitalDelay


class EffectChain(EffectInterface):
    def __init__(self, effect_configs: List[Dict]):
        """
        Initialize the EffectChain with a list of effect configurations.

        Parameters:
        effect_configs (List[Dict]): A list of effect configurations. Each configuration is a dict containing:
            - 'effect_name': The name of the effect class (as a string)
            - 'arguments': A dict of arguments to pass to the effect class constructor
        """
        self.effects:list[EffectInterface] = []
        
        # Map effect names to their corresponding classes
        effect_class_map = {
            'DigitalDelay': DigitalDelay,
            'Overdrive': Overdrive,
        }

        for config in effect_configs:
            effect_name = config.get('effect_name')
            arguments = config.get('arguments', {})
            effect_class = effect_class_map.get(effect_name)

            if effect_class is None:
                raise ValueError(f"Unknown effect name: {effect_name}")

            # Instantiate the effect with the provided arguments
            effect_instance = effect_class(**arguments)
            self.effects.append(effect_instance)

    def process(self, data: np.ndarray, rate: int = 44100):
        """
        Apply the chain of effects to the audio data.

        Parameters:
        data (numpy.array): The audio data to process.
        rate (int): The sampling rate of the audio data.

        Returns:
        numpy.array: The processed audio data.
        """
        processed_data = data.copy()

        for effect in self.effects:
            processed_data = effect.process(processed_data, rate)

        return processed_data


