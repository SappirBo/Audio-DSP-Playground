import sounddevice as sd
import threading
import numpy as np
import soundfile as sf

class Player:
    def __init__(self) -> None:
        self.m_track: str = None
        self.m_samples: np.ndarray = None
        self.m_sampling_rate: int = None
        self.m_channels: int = None
        self.m_current_track_time: float = -1.0  # when track is running, holds the time
        self.m_samples_per_frame: int = 4096
        self.m_stream: sd.OutputStream = None
        self.m_is_playing: bool = False
        self.m_current_frame_index: int = 0

    def get_wav_samples_in_sd_format(self, path:str)->tuple:
        data, samplerate = sf.read(path, dtype='int16')
        samples = data
        if len(data.shape) > 1:
            channels = data.shape[1]
        else:
            channels = 1
        return samples, samplerate, channels

    def loadSamples(self, samples: np.ndarray, sampling_rate: int, channels: int = None):
        """Load a track from a NumPy array of samples."""
        self.m_samples = samples
        self.m_sampling_rate = sampling_rate
        if channels is not None:
            self.m_channels = channels
        else:
            if len(samples.shape) > 1:
                self.m_channels = samples.shape[1]
            else:
                self.m_channels = 1
        print("Track loaded from samples.")

    def playTrack(self):
        """Play the loaded track."""
        if self.m_samples is None:
            print("No track loaded.")
            return
        if self.m_is_playing:
            print("Track is already playing.")
            return
        thread = threading.Thread(target=self.__play, daemon=True)
        thread.start()

    def __play(self):
        self.m_is_playing = True
        self.m_current_track_time = self.m_current_frame_index / self.m_sampling_rate

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            if not self.m_is_playing:
                outdata.fill(0)
                return
            end_index = self.m_current_frame_index + frames
            if end_index > len(self.m_samples):
                end_index = len(self.m_samples)
                out_frames = end_index - self.m_current_frame_index
                outdata[:out_frames] = self.m_samples[self.m_current_frame_index:end_index]
                outdata[out_frames:] = 0
                self.m_is_playing = False
                raise sd.CallbackStop()
            else:
                outdata[:] = self.m_samples[self.m_current_frame_index:end_index]
            self.m_current_frame_index = end_index
            self.m_current_track_time = self.m_current_frame_index / self.m_sampling_rate

        self.m_stream = sd.OutputStream(
            samplerate=self.m_sampling_rate,
            channels=self.m_channels,
            dtype='int16',
            callback=callback
        )
        with self.m_stream:
            while self.m_is_playing:
                sd.sleep(100)

    def stopTrack(self):
        """Stop the currently playing music."""
        self.m_is_playing = False
        if self.m_stream:
            self.m_stream.abort()
            self.m_stream.close()
            self.m_stream = None
        self.m_current_frame_index = 0
        self.m_current_track_time = -1

    def pauseTrack(self):
        """Pause the currently playing music."""
        self.m_is_playing = False

    def unpauseTrack(self):
        """Resume playing the paused music."""
        if not self.m_is_playing and self.m_current_frame_index < len(self.m_samples):
            self.m_is_playing = True
            thread = threading.Thread(target=self.__resume, daemon=True)
            thread.start()

    def __resume(self):
        self.m_is_playing = True

        def callback(outdata, frames, time, status):
            if status:
                print(status)
            if not self.m_is_playing:
                outdata.fill(0)
                return
            end_index = self.m_current_frame_index + frames
            if end_index > len(self.m_samples):
                end_index = len(self.m_samples)
                out_frames = end_index - self.m_current_frame_index
                outdata[:out_frames] = self.m_samples[self.m_current_frame_index:end_index]
                outdata[out_frames:] = 0
                self.m_is_playing = False
                raise sd.CallbackStop()
            else:
                outdata[:] = self.m_samples[self.m_current_frame_index:end_index]
            self.m_current_frame_index = end_index
            self.m_current_track_time = self.m_current_frame_index / self.m_sampling_rate

        self.m_stream = sd.OutputStream(
            samplerate=self.m_sampling_rate,
            channels=self.m_channels,
            dtype='int16',
            callback=callback
        )
        with self.m_stream:
            while self.m_is_playing:
                sd.sleep(100)

    def getCurrentFrame(self):
        if not self.isPlaying():
            return None
        start_point = self.m_current_frame_index
        end_point = start_point + self.m_samples_per_frame
        if end_point > len(self.m_samples):
            return None
        frame = self.m_samples[start_point:end_point]
        if self.m_channels > 1:
            # Convert stereo to mono by averaging the channels
            frame = frame.mean(axis=1)
        return self.__timeToFrequncyDomain(frame)

    def __timeToFrequncyDomain(self, buffer: np.ndarray) -> tuple:
        fft_amplitude = None
        fft_freq = None
        if len(buffer) > 0:
            fft_result = np.fft.rfft(buffer)
            fft_freq = np.fft.rfftfreq(len(buffer), 1 / self.m_sampling_rate)
            fft_amplitude = 2 * np.abs(fft_result) / self.m_samples_per_frame
        return fft_amplitude, fft_freq

    def isPlaying(self) -> bool:
        return self.m_is_playing

    def splitChannels(self) -> tuple:
        if self.m_channels > 1:
            left_channel = self.m_samples[:, 0]
            right_channel = self.m_samples[:, 1]
        else:
            left_channel = self.m_samples
            right_channel = None
        print("Length of Left samples: ", len(left_channel), "| length/44100 =", len(left_channel) / self.m_sampling_rate)
        if right_channel is not None:
            print("Length of Right samples: ", len(right_channel), "| length/44100 =", len(right_channel) / self.m_sampling_rate)
        return left_channel, right_channel

    def getSamplesPerFrame(self) -> int:
        return self.m_samples_per_frame
