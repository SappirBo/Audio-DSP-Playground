from .spectrum_analyzer_display import SpectrumAnalyzer
from .spectrogram_display import SpectrogramDisplay
from AudioManager import WavFile
from tkinter import * 


class DisplayView:
    def __init__(self, root: Tk, wav_file: WavFile):
        self.switch_button = False
        self.m_spectrum_analyzer = SpectrumAnalyzer(root, wav_file)
        self.m_spectrogram_display = SpectrogramDisplay(root, wav_file)
        self.current_display = self.m_spectrum_analyzer
        # Initially show the spectrum analyzer
        self.m_spectrogram_display.m_canvas_widget.pack_forget()

    def start(self):
        self.current_display.start()

    def stop(self):
        self.current_display.stop()

    def switch_display_system(self):
        self.current_display.stop()
        if self.switch_button:
            # Switch to spectrum analyzer
            self.m_spectrogram_display.m_canvas_widget.pack_forget()
            self.m_spectrum_analyzer.m_canvas_widget.pack(fill=BOTH, expand=True)
            self.current_display = self.m_spectrum_analyzer
        else:
            # Switch to spectrogram display
            self.m_spectrum_analyzer.m_canvas_widget.pack_forget()
            self.m_spectrogram_display.m_canvas_widget.pack(fill=BOTH, expand=True)
            self.current_display = self.m_spectrogram_display
        self.current_display.start()
        self.switch_button = not self.switch_button
