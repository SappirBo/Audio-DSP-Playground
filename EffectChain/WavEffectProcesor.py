from .effect_chain import EffectChain
from AudioManager import WavFile



class WavEffectProcesor:
    def __init__(self, wav_file:WavFile, effect_chain: EffectChain):
        self.wav_file = wav_file
        self.effect_chain = effect_chain
        pass

    def process_effect(self):
        if self.wav_file is None or self.effect_chain is None:
            return
        wav_data = self.wav_file.m_data
        samples = wav_data.getSamples()
        new_samples = self.effect_chain.process(samples,rate=44100)

        self.wav_file.write_samples(new_samples)
        self.wav_file.export_wav()

