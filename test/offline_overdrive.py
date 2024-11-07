import set_path
set_path.set_path_to_root()
from AudioManager import WavFile
from EffectChain import EffectChain

wav = WavFile("/home/sappirb/code/Spectrum-Analyzer/data/Audio_Processor_Drums.wav")

eq_settings = {
    "effect_name": "Overdrive",
    "arguments":{
        "mix": 0.0,
        "level": 0.0
    }
}

effect_chain = EffectChain([eq_settings])
effect_chain.print_chain()

wav.update_effect_chain(effect_chain)

wav.play_audio(print_processing_time=True)

wav.plot_samples()