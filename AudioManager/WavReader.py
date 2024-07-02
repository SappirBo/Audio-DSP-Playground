import wave
import numpy as np
from .WavData import WavData

class WavReader:
    def __init__(self) -> None:
        pass

    def read_wav(self, file_path: str) -> WavData:
        with wave.open(file_path, 'rb') as wav_file:
            # Extract audio data
            n_channels, sampwidth, framerate, n_frames, comptype, compname = wav_file.getparams()

            frames = wav_file.readframes(n_frames)

        # Convert byte data to numpy array
        if sampwidth == 1:
            dtype = np.uint8  # 8-bit WAV files
        elif sampwidth == 2:
            dtype = np.int16  # 16-bit WAV files
        else:
            raise ValueError("ValueError: Only supports 8 or 16 bit audio formats.")

        audio_data = np.frombuffer(frames, dtype=dtype)

        # Handle stereo files by separating channels
        if n_channels == 2:
            audio_data = np.reshape(audio_data, (n_frames, 2))
        
        wav_data = WavData(audio_data, framerate, n_channels, sampwidth)
        
        return wav_data