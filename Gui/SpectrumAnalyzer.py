import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import threading

from AudioManager import WavFile

class SpectrumAnalyzer:
    def __init__(self, master, audio_source: WavFile):
        self.m_master = master
        self.m_audio_source = audio_source
        self.fig, self.m_ax = plt.subplots(figsize=(6, 3))
        self.m_canvas = FigureCanvasTkAgg(self.fig, master=self.m_master)
        self.m_canvas_widget = self.m_canvas.get_tk_widget()
        self.m_canvas_widget.pack(fill=BOTH, expand=True)
        self.m_spectrum_analyzer_thread:threading.Thread = None
        self.m_thread_flag:bool = False
        self.setAxes()

    def start(self)->None:
        self.m_spectrum_analyzer_thread =  threading.Thread(target=self.update_spectrum) #, daemon=True)
        self.m_thread_flag = True
        self.m_spectrum_analyzer_thread.start()
        
    def stop(self)->None:
        self.m_thread_flag = False

    def update_spectrum(self):
        delay = 0.1
        while self.m_thread_flag:
            while self.m_audio_source.isAudioPlaying():
                fft_amplitude, fft_freq = self.m_audio_source.getAudioFrame()
                if fft_freq is not None and fft_amplitude is not None:
                    self.setAxes(fft_freq, fft_amplitude)
                    self.m_canvas.draw()
            continue

    def setAxes(self, fft_freq=None, fft_amplitude=None)->None:
        self.m_ax.clear()
        if fft_freq is not None and fft_amplitude is not None:
            self.m_ax.semilogx(fft_freq, fft_amplitude)
        
        self.m_ax.margins(0, 0.1)
        self.m_ax.grid(which='both', axis='both')
        self.m_ax.set_xscale('log')
        # self.m_ax.set_yscale('log')
        self.m_ax.set_yscale('symlog', linthresh=0.1)

        amplitude_ticks = np.array([1, 10, 25, 50, 100, 250, 500, 1000, 2000, 4000])
        self.m_ax.set_yticks(amplitude_ticks)
        self.m_ax.set_yticklabels(amplitude_ticks)
        
        frequencies = np.array([0, 30, 50, 100, 250, 500, 1000, 2000, 4000, 8000, 10000, 20000])
        frequencies[0] = 1 
        self.m_ax.set_xticks(frequencies)
        labels = ['0', '30', '50', '100', '250', '500', '1k', '2k', '4k', '8k', '10k', '20k']
        self.m_ax.set_xticklabels(labels)

        self.m_ax.set_ylim(1, 4000)
        self.m_ax.set_xlabel('Frequency (Hz)')
        self.m_ax.set_ylabel('Amplitude')
        self.m_ax.set_xlim(20, 20000)

