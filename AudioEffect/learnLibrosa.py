import librosa

audio_data, sampling_rate = librosa.load('data/Audio_Processor_Drums.wav', sr=22050)

duration = librosa.get_duration(audio_data, sr=sampling_rate)

print(duration)

new_audio = librosa.effects.time_stretch(audio_data, 2)

duration = librosa.get_duration(audio_data, sr=sampling_rate)

print(duration)

