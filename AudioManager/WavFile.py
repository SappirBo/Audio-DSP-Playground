import numpy as np
from .WavReader import WavReader
from .WavData import WavData
from .WavWriter import WavWriter
from .AudioPlayer import AudioPlayer
from matplotlib import pyplot as plt
from matplotlib import style
import threading
from multiprocessing import Process




class WavFile:
    def __init__(self, path_to_wav: str = None) -> None:
        self.m_path: str = path_to_wav
        self.m_data: WavData = None
        self.m_channels:int = 0
        self.m_audio_player = AudioPlayer()
        if self.m_path is not None:
            self.__readWav()
    
    def setPathToWav(self,path_to_wav: str = None) -> None:
        if path_to_wav is None:
            return
        self.m_path = path_to_wav
        self.__readWav()

    def __readWav(self) -> None:
        wav_reader = WavReader()
        self.m_data = wav_reader.read_wav(self.m_path)
        if self.m_data == None:
            raise TypeError("Error: Samples is empty, please try again")

    def playAudio(self):
        if not self.m_path:
            return 
        self.m_audio_player.loadTrack(self.m_path)
        self.m_audio_player.playTrack()
    
    def stopAudio(self):
        self.m_audio_player.stopTrack()

    def exportWav(self, path_to_output:str):
        wav_writer = WavWriter()
        wav_writer.writeWav(path_to_output, self.m_data)

    def plotSamples(self):
        # thread = threading.Thread(target=self.__plotSamples)
        # thread.start()
        # self.__plotSamples()
        print("PLoting samples now")

    def __plotSamples(self):
        if self.m_data == None:
            return
        number_of_channels =self.m_data.getNumberOfChannels()
        if number_of_channels == 2:
            self.__plotStereo()
        elif number_of_channels == 1:
            self.__plotMono()
        else:
            raise TypeError("Error: channels number incorrect!")

    def __plotMono(self):
        # style.use('dark_background')
        f, plt_arr = plt.subplots(1, sharex = True)
        f.suptitle(self.m_path)

        plt_arr.plot(self.m_data.getSamples())

        plt.show()
    
    def __plotStereo(self):
        # style.use('dark_background')
        f, plt_arr = plt.subplots(2, sharex = True)
        f.suptitle(self.m_path)
        
        left_samples = [item[0] for item in self.m_data.getSamples()]
        right_samples = [item[1] for item in self.m_data.getSamples()]

        plt_arr[0].plot(left_samples)
        plt_arr[0].set_title("Left Channel")
        plt_arr[1].plot(right_samples)
        plt_arr[1].set_title("Right Channel")

        plt.show()

    def getNumChanels(self)->int:
        return self.m_data.m_num_channels

    def getAudioFrame(self):
        return self.m_audio_player.getCurrentFrame()

    def isAudioPlaying(self) -> bool:
        return self.m_audio_player.isPlaying()

    def getAudioSamplesPerFrame(self)->int:
        return self.m_audio_player.getSamplesPerFrame()