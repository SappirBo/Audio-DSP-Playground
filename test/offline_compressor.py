import set_path
set_path.set_path_to_root()
from AudioManager import WavFile
from EffectChain import EffectChain

wav = WavFile("/home/sappirb/code/Spectrum-Analyzer/data/Audio_Processor_Drums.wav")


settings = {
    "effect_name": "Compressor",
    "arguments":{
        "mix": 0.0,
        "level": 0.0,
        "threshold": 0.0,
        "ratio":10.0,
        "attack":0,
        "release": 150
    }
}

effect_chain = EffectChain([settings])
effect_chain.print_chain()

wav.update_effect_chain(effect_chain)

wav.play_audio()

wav.plot_samples()