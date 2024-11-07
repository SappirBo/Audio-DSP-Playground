import set_path
set_path.set_path_to_root()
from AudioManager import WavFile
from EffectChain import EffectChain

wav = WavFile("/home/sappirb/code/Spectrum-Analyzer/data/Audio_Processor_Drums.wav")

wav.play_audio()

wav.plot_samples()