import set_path
set_path.set_path_to_root()
from AudioManager import WavFile
from EffectChain import EffectChain

wav = WavFile("/home/sappirb/code/Spectrum-Analyzer/data/Audio_Processor_Clap.wav")

eq_settings = {
    "effect_name": "DigitalDelay",
    "arguments":{
        "feedback":0.5,
        "time": 1.0,
        "mix": 0.5,
        "level": 0.0
    }
}

effect_chain = EffectChain([eq_settings])
effect_chain.print_chain()

wav.update_effect_chain(effect_chain)

wav.play_audio(print_processing_time=True)

wav.plot_samples()