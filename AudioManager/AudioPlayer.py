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
        self.m_frames_per_sec = 24
        self.m_samples:np.NDArray = None
    
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
            pygame.time.Clock().tick(self.m_frames_per_sec)
            self.m_current_track_time = pygame.mixer.music.get_pos() / milisec_to_seconds
        self.m_current_track_time=-1

    def stopTrack(self):
        """Stop the currently playing music."""
        pygame.mixer.music.stop()
        print("Music stopped.")

    def pauseTrack(self):
        """Pause the currently playing music."""
        pygame.mixer.music.pause()
        print("Music paused.")

    def unpauseTrack(self):
        """Resume playing the paused music."""
        pygame.mixer.music.unpause()
        print("Music resumed.")

    def getCurrentFrame(self):
        if self.isPlaying == False:
            print("Nothing Is Running ")
            return
        if self.m_sound_object:
            fs = 441000
            frame_size = int(fs/self.m_frames_per_sec)
            start_point = int(frame_size * self.m_current_track_time)
            return self.m_samples[start_point : start_point+frame_size]
  
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


        
