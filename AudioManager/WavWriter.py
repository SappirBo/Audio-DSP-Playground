import wave
from .WavData import WavData


class WavWriter:
    def __init__(self) -> None:
        pass

    def writeWav(self, file_path, data: WavData):
        if data is None:
            raise TypeError("Error writing a Wav File: data is None!")
        samples    = data.getSamples()
        framerate  = data.getFrameRate()
        n_channels = data.getNumberOfChannels()
        sampwidth  = data.getSampwidth()

        # Open the WAV file
        with wave.open(file_path, 'wb') as wav_file:
            # Set audio parameters and write data
            wav_file.setparams((n_channels, sampwidth, framerate, samples.shape[0], 'NONE', 'Uncompressed'))
            wav_file.writeframes(samples.tobytes())