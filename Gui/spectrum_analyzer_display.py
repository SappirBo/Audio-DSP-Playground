import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
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
        
        self.m_frequency_label = Label(self.m_master, text="Frequency: N/A", font=("Arial", 12)) # Label widget to display the frequency
        self.m_frequency_label.pack()

        # Initialize previous amplitudes and a m_lock for thread safety
        self.m_prev_amplitudes = None
        self.m_lock = threading.Lock()

        self.m_spectrum_analyzer_thread:threading.Thread = None
        self.m_thread_flag:bool = False
        self.set_axes()
        
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)# Connect the mouse motion event handler

    def start(self)->None:
        self.m_spectrum_analyzer_thread =  threading.Thread(target=self.update_spectrum, daemon=True)
        self.m_thread_flag = True
        self.m_spectrum_analyzer_thread.start()
        
    def stop(self)->None:
        self.m_thread_flag = False
        # self.reset_axes()

    def update_spectrum(self):
        while self.m_thread_flag:
            while self.m_audio_source.is_audio_playing():
                result = self.m_audio_source.get_audio_frame_in_frequncy_domain()
                if result is None:
                    continue
                fft_amplitude, fft_freq = result
                if fft_freq is not None and fft_amplitude is not None:
                    self.set_axes(fft_freq, fft_amplitude)
                    self.m_canvas.draw()
            continue

    def set_axes(self, fft_freq=None, fft_amplitude=None)->None:
        self.m_ax.clear()
        if fft_freq is not None and fft_amplitude is not None:
            self.filter_non_positive(fft_freq, fft_amplitude)

            plot_amplitudes = self.get_plot_amplitude(fft_freq, fft_amplitude)

            blue, = sns.color_palette("muted", 1)
            self.m_ax.plot(fft_freq, plot_amplitudes, color=blue, lw=1.5)
            self.m_ax.fill_between(fft_freq, plot_amplitudes, color=blue, alpha=0.3)
            self.m_ax.set_xscale('log')
        self.__set_axesGrid()

    def filter_non_positive(self, fft_freq, fft_amplitude):
        # Filter out non-positive frequencies
        positive_indices = fft_freq > 0
        fft_freq = fft_freq[positive_indices]
        fft_amplitude = fft_amplitude[positive_indices]

    def get_plot_amplitude(self, fft_freq, fft_amplitude):
        """This function takes the current ampplitude and prev ones -> and return current amplitude with a bit of decay"""
        # Apply decay to the amplitudes
        with self.m_lock:
            if self.m_prev_amplitudes is None:
                # Initialize previous amplitudes
                self.m_prev_amplitudes = fft_amplitude.copy()
            else:
                # Apply decay
                self.m_prev_amplitudes = self.apply_decay(self.m_prev_amplitudes, fft_amplitude, fft_freq)
            # Use the decayed amplitudes for plotting
            plot_amplitudes = self.m_prev_amplitudes.copy()
            return plot_amplitudes

    def apply_decay(self, m_prev_amplitudes, new_amplitudes, frequencies):
        decay_rates = self.calculate_decay_rates(frequencies) # Define decay rates (higher frequencies decay faster)

        updated_amplitudes = np.zeros_like(new_amplitudes)

        for i in range(len(new_amplitudes)):
            if new_amplitudes[i] >= m_prev_amplitudes[i]: # Amplitude increased, update directly
                updated_amplitudes[i] = new_amplitudes[i]
            else: # Amplitude decreased, apply decay
                updated_amplitudes[i] = m_prev_amplitudes[i] * decay_rates[i]
                if updated_amplitudes[i] < new_amplitudes[i]:# Ensure it doesn't go below the new amplitude
                    updated_amplitudes[i] = new_amplitudes[i]
        return updated_amplitudes

    def calculate_decay_rates(self, frequencies):
        """
        Define decay rates based on frequency
        For example, lower frequencies have decay rates closer to 1 (slow decay)
        and higher frequencies have lower decay rates (faster decay)
        """
        frequencies = np.where(frequencies <= 0, 1e-10, frequencies)

        # Normalize frequencies to [0, 1]
        min_freq = np.log10(20)
        max_freq = np.log10(20000)
        log_freqs = np.log10(frequencies)
        normalized_freqs = (log_freqs - min_freq) / (max_freq - min_freq)

        # Invert so lower frequencies have lower normalized values
        normalized_freqs = 0.45 - normalized_freqs

        # Map normalized frequencies to decay rates between 0.7 and 0.99
        decay_rates = 0.7 + 0.29 * normalized_freqs

        return decay_rates

    def reset_axes(self)->None:
        self.m_ax.clear()
        self.__set_axesGrid()
        
    def __set_axesGrid(self)->None:
        self.m_ax.margins(0, 0.1)
        self.m_ax.grid(which='both', axis='both')
        self.m_ax.set_xscale('log')
        self.m_ax.set_yscale('symlog', linthresh=0.1)

        amplitude_ticks = np.array([1, 10, 25, 50, 100, 250, 500, 1000, 2000, 4000])
        self.m_ax.set_yticks(amplitude_ticks)
        self.m_ax.set_yticklabels(amplitude_ticks)
        
        frequencies = np.array([0, 30, 50, 100, 250, 500, 1000, 2000, 4000, 8000, 10000, 20000])
        frequencies[0] = 1 
        self.m_ax.set_xticks(frequencies)
        labels = ['0', '30', '50', '100', '250', '500', '1k', '2k', '4k', '8k', '10k', '20k']
        self.m_ax.set_xticklabels(labels)

        self.m_ax.set_xlim(20, 20000)
        self.m_ax.set_ylim(1, 4000)
        self.m_ax.set_xlabel('Frequency (Hz)')
        self.m_ax.set_ylabel('Amplitude')

        pos = []
        def onclick(event):
            pos.append([event.xdata,event.ydata])
            # print("pos: ", pos)
        self.fig.canvas.mpl_connect('button_press_event', onclick)
                
    def on_mouse_move(self, event):
            if event.inaxes == self.m_ax:
                x = event.xdata
                if x is not None:
                    frequency = x
                    # Update the label with the frequency value
                    self.m_frequency_label.config(text=f"Frequency: {frequency:.2f} Hz")
            else:
                self.m_frequency_label.config(text="Frequency: N/A")

