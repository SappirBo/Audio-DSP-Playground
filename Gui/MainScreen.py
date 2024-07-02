from tkinter import * 
from .MenuBar import MenuBar
from .ControlButtons import ControlButtons
from .SpectrumAnalyzer import SpectrumAnalyzer
from AudioManager import WavFile


class MainScreen:
    def __init__(self, wav_file:WavFile) -> None:
        self.m_root = Tk(className=" Audio Prodaction ")
        self.m_wav_file = wav_file
        self.m_spectrum_analyzer:SpectrumAnalyzer = None
        self.m_control_buttons:ControlButtons = None
        self.__setConfiguration()
        pass

    def run(self):
        self.m_root.mainloop()

    def __setConfiguration(self):
        self.m_root.geometry('2000x1000')
        self.m_root.resizable(width=False, height=False)
        self.m_menu_bar = MenuBar(self.m_root, self.handleWavSelection, self.handleWavPlot)
        self.m_spectrum_analyzer = SpectrumAnalyzer(self.m_root, self.m_wav_file)
        self.m_control_buttons = ControlButtons(self.m_root, self.on_play_click, self.on_stop_click)
        self.m_control_buttons.pack(pady=20)
        self.m_root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_play_click(self):
        self.m_spectrum_analyzer.start()
        if self.m_wav_file is None:
            return
        self.m_wav_file.playAudio()
    
    def on_stop_click(self):
        if self.m_wav_file is None:
            return
        self.m_wav_file.stopAudio()
        self.m_spectrum_analyzer.stop()
    
    def on_button_click(self):
        print("Button clicked!")
    
    def handleWavSelection(self, wav_file_path: str):
        self.on_stop_click()
        self.m_wav_file.setPathToWav(wav_file_path)

    def handleWavPlot(self):
        self.m_wav_file.plotSamples()

    def on_close(self):
        self.on_stop_click() 
        self.m_root.quit() 