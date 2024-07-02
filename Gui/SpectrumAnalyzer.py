import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import threading
from pygame import mixer
import time

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

    def start(self)->None:
        self.m_spectrum_analyzer_thread =  threading.Thread(target=self.update_spectrum) #, daemon=True)
        self.m_thread_flag = True
        self.m_spectrum_analyzer_thread.start()
        
    def stop(self)->None:
        self.m_thread_flag = False

    def update_spectrum(self):
        while self.m_thread_flag:
            while self.m_audio_source.isAudioPlaying():
                samples = self.m_audio_source.getAudioFrame()
                if len(samples) > 0:
                    fft_result = np.fft.rfft(samples)
                    fft_freq = np.fft.rfftfreq(len(samples), 1 / 44100)
                    
                    self.m_ax.clear()
                    self.m_ax.semilogx(fft_freq, np.abs(fft_result))

                    self.m_ax.margins(0,0.1)
                    self.m_ax.grid(which='both', axis='both')
                    self.m_ax.set_xlim(20, 20000)  # Set fixed x-axis limits
                    # self.m_ax.set_ylim(0,48434120)  # Set fixed y-axis limits
                    self.m_ax.set_xlabel('Frequency (Hz)')
                    self.m_ax.set_ylabel('Amplitude')
                    self.m_canvas.draw()
            continue