import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import threading
from pygame import mixer

from AudioManager import WavFile

class SpectrumAnalyzer:
    def __init__(self, master, audio_source: WavFile):
        self.master = master
        self.audio_source = audio_source
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=BOTH, expand=True)

    def start(self):
        spectrum_analyzer_thread =  threading.Thread(target=self.update_spectrum) #, daemon=True)
        spectrum_analyzer_thread.start()

    def update_spectrum(self):
        while self.audio_source.isAudioPlaying() == False:
            print("SpectrumAnalyzer: update_spectrum, isAudioPlaying = ", self.audio_source.isAudioPlaying())
            while self.audio_source.isAudioPlaying():
                print("SpectrumAnalyzer: update_spectrum, isAudioPlaying = ", self.audio_source.isAudioPlaying()) 
                samples = np.frombuffer(self.audio_source.getAudioFrame(), dtype=np.int16)
                fft_result = np.fft.rfft(samples)
                fft_freq = np.fft.rfftfreq(len(samples), 1 / 44100)  # Assuming 44100 Hz sample rate
                
                self.ax.clear()
                self.ax.semilogx(fft_freq, np.abs(fft_result))
                self.ax.set_xlabel('Frequency (Hz)')
                self.ax.set_ylabel('Amplitude')
                self.ax.set_xlim(20, 20000)  # Human hearing range
                self.canvas.draw()
                plt.pause(0.1)
            continue
        print("SpectrumAnalyzer: update_spectrum, Out") 