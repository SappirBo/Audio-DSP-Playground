import wave
from .WavData import WavData


class WavWriter:
    def __init__(self) -> None:
        pass

    def write_wav(self, file_path, data: WavData):
        if data is None:
            raise TypeError("Error writing a Wav File: data is None!")
        samples    = data.getSamples()
        samplerate  = data.getSampleRate()
        n_channels = data.getNumberOfChannels()
        sampwidth  = data.getSampwidth()

        # Open the WAV file
        with wave.open(file_path, 'wb') as wav_file:
            # Set audio parameters and write data
            wav_file.setparams((n_channels, sampwidth, samplerate, samples.shape[0], 'NONE', 'Uncompressed'))
            wav_file.writeframes(samples.tobytes())