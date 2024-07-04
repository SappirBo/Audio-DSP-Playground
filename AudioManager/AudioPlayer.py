'''
https://www.studytonight.com/tkinter/music-player-application-using-tkinter
'''

import pygame
import threading
import numpy as np

class AudioPlayer:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()
        self.m_track:str = None
        self.m_sound_object = None
        self.m_current_track_time:float = -1.0 #when track is running, holds the time
        self.m_samples_per_sec = 4096
        self.m_samples:np.NDArray = None
        self.m_sampling_rate = 44100
    
    def loadTrack(self, file_path):
        """Load a track from a file path."""
        self.m_track = file_path
        pygame.mixer.music.load(self.m_track)
        self.m_sound_object = pygame.mixer.Sound(self.m_track)
        self.initRawSamplesOfAudio()
        print(f"Loaded: {self.m_track}")
    
    def playTrack(self):
        """play the specified WAV file"""
        thread = threading.Thread(target=self.__play)
        thread.start()

    def __play(self):
        pygame.mixer.music.play()
        milisec_to_seconds = 1000
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(self.m_sampling_rate/self.m_samples_per_sec)
            self.m_current_track_time = pygame.mixer.music.get_pos() / milisec_to_seconds
        self.m_current_track_time=-1

    def stopTrack(self):
        """Stop the currently playing music."""
        pygame.mixer.music.stop()

    def pauseTrack(self):
        """Pause the currently playing music."""
        pygame.mixer.music.pause()

    def unpauseTrack(self):
        """Resume playing the paused music."""
        pygame.mixer.music.unpause()

    def getCurrentFrame(self) ->tuple:
        if self.isPlaying == False:
            return
        if self.m_sound_object:
            start_point = int(self.m_samples_per_sec * self.m_current_track_time)
            frame = self.m_samples[start_point : start_point+self.m_samples_per_sec]
            return self.__timeToFrequncyDomain(frame)
    
    def __timeToFrequncyDomain(self, buffer:np.ndarray)->tuple:
        fft_amplitude = None
        fft_freq   = None
        if len(buffer) > 0:
            fft_result = np.fft.rfft(buffer)
            fft_freq = np.fft.rfftfreq(len(buffer), 1 / 44100)
            fft_amplitude = 2 * np.abs(fft_result) / len(buffer)
        return fft_amplitude, fft_freq
  
    def isPlaying(self) -> bool:
        return pygame.mixer.music.get_busy()
    
    def initRawSamplesOfAudio(self):
        raw_audio = self.m_sound_object.get_raw()
        samples = np.frombuffer(raw_audio, dtype=np.int16)
        self.m_samples = samples

    def splitChannels(self) -> tuple:
        left_channel  = self.m_samples[0::2]
        right_channel = self.m_samples[1::2]
        print("length of Left samples: ",len(left_channel),"| length/44100 =", len(left_channel)/44100)
        print("length of Right samples: ",len(right_channel),"| length/44100 =", len(right_channel)/44100)
        return left_channel,right_channel


        
