import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import threading
import librosa
from AudioManager import WavFile

class SpectrogramDisplay:
    def __init__(self, master, audio_source: WavFile):
        self.m_master = master
        self.m_audio_source = audio_source
        
        self.fig, self.m_ax = plt.subplots(figsize=(6, 3))
        self.m_canvas = FigureCanvasTkAgg(self.fig, master=self.m_master)
        self.m_canvas_widget = self.m_canvas.get_tk_widget()
        self.m_canvas_widget.pack()
        
        self.m_spectrogram_thread = None
        self.m_thread_flag = False

        # Parameters for STFT
        self.n_fft = 1024
        self.hop_length = 256
        self.sample_rate = self.m_audio_source.m_sample_rate
        self.window_size = self.n_fft

        # Initialize audio buffer
        self.audio_buffer = np.array([], dtype=np.float32)

        # Initialize spectrogram data
        self.num_freq_bins = int(1 + self.n_fft // 2)
        self.num_time_steps = 100
        self.spectrogram_data = np.zeros((self.num_freq_bins, self.num_time_steps))

        # Initialize image
        extent = [0, self.num_time_steps, 0, self.sample_rate / 2]
        self.im = self.m_ax.imshow(self.spectrogram_data,
                                aspect='auto',
                                origin='lower',
                                cmap='inferno',
                                extent=extent,
                                vmin=-80,
                                vmax=0)
        
        # Set up axes
        self.set_axes()

    def start(self):
        self.m_spectrogram_thread = threading.Thread(target=self.update_spectrogram, daemon=True)
        self.m_thread_flag = True
        self.m_spectrogram_thread.start()

    def stop(self):
        self.m_thread_flag = False

    def update_spectrogram(self):
        while self.m_thread_flag:
            while self.m_audio_source.is_audio_playing():
                audio_frame = self.m_audio_source.get_audio_frame_in_time_domain()

                # Handle stereo audio by converting to mono
                if audio_frame.ndim > 1:
                    audio_frame = np.mean(audio_frame, axis=1)

                # Ensure audio_frame is 1D
                audio_frame = np.squeeze(audio_frame)

                if audio_frame is None:
                    continue
                # Assuming audio_frame is a NumPy array of audio samples
                self.audio_buffer = np.concatenate((self.audio_buffer, audio_frame))

                # Process in chunks of window_size
                while len(self.audio_buffer) >= self.window_size:
                    window = self.audio_buffer[:self.window_size]
                    # Compute STFT
                    D = librosa.stft(window, n_fft=self.n_fft, hop_length=self.hop_length)
                    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

                    # Shift spectrogram data
                    self.spectrogram_data = np.roll(self.spectrogram_data, -1, axis=1)
                    # Update last column
                    self.spectrogram_data[:, -1] = S_db[:, 0]

                    # Remove processed samples
                    self.audio_buffer = self.audio_buffer[self.hop_length:]

                    # Update image
                    self.im.set_data(self.spectrogram_data)
                    self.m_canvas.draw()
            continue

    def set_axes(self):
        self.m_ax.set_xlabel('Time')
        self.m_ax.set_ylabel('Frequency (Hz)')

        # Frequency ticks
        freq_bins = np.linspace(0, self.sample_rate / 2, self.num_freq_bins)
        freq_ticks = np.linspace(0, self.sample_rate / 2, 10)
        freq_tick_pos = np.interp(freq_ticks, freq_bins, np.arange(self.num_freq_bins))
        self.m_ax.set_yticks(freq_tick_pos)
        self.m_ax.set_yticklabels(np.round(freq_ticks).astype(int))

        # Time ticks
        time_ticks = np.linspace(0, self.num_time_steps, 5)
        self.m_ax.set_xticks(time_ticks)
        self.m_ax.set_xticklabels([''] * len(time_ticks))
