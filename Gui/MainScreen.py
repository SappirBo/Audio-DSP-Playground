from tkinter import * 
from .MenuBar import MenuBar
from .ControlButtons import ControlButtons
from .SpectrumAnalyzer import SpectrumAnalyzer
from AudioManager import WavFile


class MainScreen:
    def __init__(self, wav_file:WavFile) -> None:
        self.m_root = Tk(className=" Audio Prodaction ")
        self.m_wav_file = wav_file
        self.__setConfiguration()
        pass

    def run(self):
        self.m_root.mainloop()

    def __setConfiguration(self):
        self.m_root.geometry('600x100')
        # self.m_root.configure(background='black')
        self.m_menu_bar = MenuBar(self.m_root, self.handleWavSelection, self.handleWavPlot)
        self.spectrum_analyzer = SpectrumAnalyzer(self.m_root, self.m_wav_file)
        self.spectrum_analyzer.start()
        self.control_buttons = ControlButtons(self.m_root, self.on_play_click, self.on_stop_click)
        self.control_buttons.pack(pady=20)

    def on_play_click(self):
        if self.m_wav_file is None:
            return
        self.m_wav_file.playAudio()
    
    def on_stop_click(self):
        if self.m_wav_file is None:
            return
        self.m_wav_file.stopAudio()
    
    def on_button_click(self):
        print("Button clicked!")
    
    def handleWavSelection(self, wav_file_path: str):
        self.on_stop_click()
        self.m_wav_file.setPathToWav(wav_file_path)

    def handleWavPlot(self):
        self.m_wav_file.plotSamples()


if __name__ == "__main__":
    app = MainScreen()
    app.run()
        