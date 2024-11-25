import numpy as np
from typing import List, Dict
from AudioEffect import EffectInterface, Overdrive, DigitalDelay, EffectObjectMap


class EffectChain(EffectInterface):
    def __init__(self, effect_configs: List[Dict]=None):
        """
        Initialize the EffectChain with a list of effect configurations.

        Parameters:
        effect_configs (List[Dict]): A list of effect configurations. Each configuration is a dict containing:
            - 'effect_name': The name of the effect class (as a string)
            - 'arguments': A dict of arguments to pass to the effect class constructor
        """
        self.effects:list[EffectInterface] = []

        self.set_effect_config(effect_configs)

    def set_effect_config(self, effect_configs: List[Dict]=None):
        if effect_configs is None:
            return
        for config in effect_configs:
            self.add_effect(config)

    def add_effect(self, config:Dict):
        effect_name = config.get('effect_name')
        arguments = config.get('arguments', {})
        effect_map = EffectObjectMap()
        effect_class = effect_map.get_single_effect_class(effect_name)

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
        """
        for effect in self.effects:
            effect.process(data, rate)

    def remove_all(self)->None:
        self.print_chain()
        self.effects.clear()
        self.print_chain()
        
    def print_chain(self)->None:
        print(self.effects)

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
                }
            }
        }
        return arguments