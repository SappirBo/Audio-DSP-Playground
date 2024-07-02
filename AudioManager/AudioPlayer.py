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
        # pygame.mixer.init(frequency=44100, size=-16, channels=2)
        self.m_track:str = None
    
    def loadTrack(self, file_path):
        """Load a track from a file path."""
        self.m_track = file_path
        pygame.mixer.music.load(self.m_track)
        
        print(f"Loaded: {self.m_track}")
    
    def playTrack(self):
        """play the specified WAV file"""
        thread = threading.Thread(target=self.__play)
        thread.start()

    def __play(self):
        pygame.mixer.music.play()
        print(f"Playing: {self.m_track}")
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(2) 

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
        sound = pygame.mixer.Sound()
        return np.frombuffer(sound.get_raw(), dtype=np.int16)
    
    def isPlaying(self) -> bool:
        return pygame.mixer.get_busy()
