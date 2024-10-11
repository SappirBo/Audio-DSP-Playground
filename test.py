import AudioManager 
import EffectChain
import numpy as np
# import sounddevice as sd


def print_sample(samples):
    for i in range(0,20):
        print(samples[i])

wav = AudioManager.WavFile("/home/sappirb/code/Spectrum-Analyzer/data/Audio_Processor_Clap.wav")

samples = wav.m_data.getSamples()
rate = 44100

effect_configs = [
    {
        "effect_name": "Overdrive",
        "arguments": {
            "mix": 0.5,
            "drive": 10,
            "level": 1.0
        }
    },
    {
        "effect_name": "DigitalDelay",
        "arguments": {
            "feedback": 0.9,
            "time": 0.15,
            "mix": 0.5
        }
    }
]

effect_chain = EffectChain.EffectChain(effect_configs)

new_samples = effect_chain.process(samples)

wav.write_samples(new_samples)

# sd.play(new_samples, samplerate=44100)
# sd.wait()  # Wait until the audio playback is finished

wav.exportWav("/home/sappirb/code/Spectrum-Analyzer/output/test_with_rev.wav")