from .SpectrumAnalyzer import SpectrumAnalyzer
from AudioManager import WavFile
from tkinter import * 


class DisplayView:
    def __init__(self, root:Tk, wav_file:WavFile):
        self.switch_buttom:bool = False
        self.m_spectrum_analyzer = SpectrumAnalyzer(root, wav_file)
        pass

    def start(self)->None:
        self.m_spectrum_analyzer.start()

    def stop(self)->None:
        self.m_spectrum_analyzer.stop()

    def switch_display_system(self)->None:
        self.switch_buttom = not self.switch_buttom
        print(f"switch_buttom is {self.switch_buttom}")