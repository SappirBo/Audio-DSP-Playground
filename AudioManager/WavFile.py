import numpy as np
from .WavReader import WavReader
from .WavData import WavData
from .WavWriter import WavWriter
# from .AudioPlayer import AudioPlayer 
from .Player import Player
from EffectChain import EffectChain
from matplotlib import pyplot as plt
from matplotlib import style
import threading
from multiprocessing import Process
from multiprocessing import shared_memory



class WavFile:
    def __init__(self, path_to_wav: str = None) -> None:
        self.m_path: str = path_to_wav
        self.m_data: WavData = None
        self.m_effect_chain:EffectChain = None
        self.m_channels:int = 0
        self.m_samples:np.ndarray = None
        self.m_sample_rate:int = 44100
        # self.m_audio_player = AudioPlayer()
        self.m_audio_player = Player()
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
        self.m_samples, self.m_sample_rate, self.m_channels = self.m_audio_player.get_wav_samples_in_sd_format(self.m_path)


    # def playAudio(self):
    #     if not self.m_path:
    #         return 
    #     thread = threading.Thread(target=self.__process_and_play_audio, daemon=True)
    #     thread.start()
        
    # def __process_and_play_audio(self):
    #     samples = self.m_samples.copy()
    #     samples.setflags(write=1)

    #     self.m_effect_chain.process(samples, self.m_sample_rate)

    #     self.m_audio_player.loadSamples(samples, self.m_sample_rate, self.m_channels)
    #     self.m_audio_player.playTrack()

    def playAudio(self):
        if not self.m_path:
            return 

        samples = self.m_samples.copy()
        samples.setflags(write=1)

        # Create shared memory block
        shm = shared_memory.SharedMemory(create=True, size=samples.nbytes)
        # Create a numpy array backed by shared memory
        shm_samples = np.ndarray(samples.shape, dtype=samples.dtype, buffer=shm.buf)
        # Copy data into shared memory
        np.copyto(shm_samples, samples)

        # Start process to process samples
        p = Process(target=self.__process_samples_in_process, args=(samples.shape, samples.dtype, shm.name))
        p.start()
        p.join()

        # After processing, read from shared memory
        processed_samples = np.ndarray(samples.shape, dtype=samples.dtype, buffer=shm.buf)

        # Copy processed data back to samples
        samples = processed_samples.copy()

        # Close and unlink shared memory
        shm.close()
        shm.unlink()

        self.m_audio_player.loadSamples(samples, self.m_sample_rate, self.m_channels)
        self.m_audio_player.playTrack()

    def __process_samples_in_process(self, shape, dtype, shm_name):
        # Attach to existing shared memory
        shm = shared_memory.SharedMemory(name=shm_name)
        samples = np.ndarray(shape, dtype=dtype, buffer=shm.buf)

        # Perform processing (modifies samples in place)
        self.m_effect_chain.process(samples, self.m_sample_rate)

        # Close shared memory in worker process
        shm.close()

    def stopAudio(self):
        self.m_audio_player.stopTrack()

    def exportWav(self, path_to_output:str=None):
        wav_writer = WavWriter()
        if path_to_output is None:
            wav_writer.writeWav(self.m_path, self.m_data)
        else:
            wav_writer.writeWav(path_to_output, self.m_data)

    def plotSamples(self):
        # thread = threading.Thread(target=self.__plotSamples)
        # thread.start()
        # self.__plotSamples()
        print("Temporery Stoped")

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
    
    def write_samples(self, new_samples: np.ndarray)-> None:
        self.m_data.m_samples = new_samples

    def update_effect_chain(self, effect_chain:EffectChain)->None:
        self.m_effect_chain = effect_chain