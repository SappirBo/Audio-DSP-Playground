import AudioEffect
import AudioManager 
import numpy as np

def print_sample(samples):
    for i in range(0,20):
        print(samples[i])

wav = AudioManager.WavFile("/home/sappirb/code/Spectrum-Analyzer/data/Audio_Processor_Guitar.wav")

samples = wav.m_data.getSamples()
rate = 44100
# print_sample(samples)
# print("------------------------------------")
# rev = AudioEffect.DigitalDelay(feedback=1,time=0.1, mix=0.5)
# new_samples = rev.process(samples,rate)
# wav.write_samples(new_samples)
# print_sample(wav.m_data.getSamples())


drive = AudioEffect.Overdrive(drive=10, mix=1, level=1)

new_samples = drive.process(samples,44100)
wav.write_samples(new_samples)


wav.exportWav("/home/sappirb/code/Spectrum-Analyzer/output/test_with_rev.wav")