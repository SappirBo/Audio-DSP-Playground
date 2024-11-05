import set_path
set_path.set_path_to_root()
from AudioManager import WavFile
from EffectChain import EffectChain

wav = WavFile("/home/sappirb/code/Spectrum-Analyzer/data/Audio_Processor_Drums.wav")

print(wav.m_data.toString())

eq_settings = {
    "effect_name": "Equalizer",
    "arguments":{
        "mix": 0.0,
        "level": 0.0,
        "eq_params": [
            {
                "type": 'high',
                "cutoff": 300,
                "Q_factor": 0
            },
            {
                "type": 'low',
                "cutoff": 2500,
                "Q_factor": 0
            }
        ]
    }
}

effect_chain = EffectChain([eq_settings])
effect_chain.print_chain()

wav.update_effect_chain(effect_chain)

wav.play_audio()

wav.plot_samples()