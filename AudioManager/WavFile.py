import numpy as np
from .WavReader import WavReader
from .WavData import WavData
from .WavWriter import WavWriter
from .Player import Player
from EffectChain import EffectChain
from matplotlib import pyplot as plt
from multiprocessing import Process
from multiprocessing import shared_memory



class WavFile:
    def __init__(self, path_to_wav: str = None) -> None:
        self.m_path: str = path_to_wav
        self.m_data: WavData = None
        self.m_effect_chain:EffectChain = EffectChain()
        self.m_channels:int = 0
        self.m_samples:np.ndarray = None
        self.m_sample_rate:int = 44100
        self.m_audio_player = Player()
        if self.m_path is not None:
            self.__read_wav()
    
    def set_path_to_wav(self,path_to_wav: str = None) -> None:
        if path_to_wav is None:
            return
        self.m_path = path_to_wav
        self.__read_wav()

    def __read_wav(self) -> None:
        wav_reader = WavReader()
        self.m_data = wav_reader.read_wav(self.m_path)
        if self.m_data == None:
            raise TypeError("Error: Samples is empty, please try again")
        self.m_samples, self.m_sample_rate, self.m_channels = self.m_audio_player.get_wav_samples_in_sd_format(self.m_path, self.m_data.get_samples_dtype())

    def play_audio(self):
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

        self.m_audio_player.load_samples(samples, self.m_sample_rate, self.m_channels)
        self.m_audio_player.play_track()

    def __process_samples_in_process(self, shape, dtype, shm_name):
        # Attach to existing shared memory
        shm = shared_memory.SharedMemory(name=shm_name)
        samples = np.ndarray(shape, dtype=dtype, buffer=shm.buf)

        # Perform processing (modifies samples in place)
        self.m_effect_chain.process(samples, self.m_sample_rate)

        # Close shared memory in worker process
        shm.close()

    def stop_audio(self):
        self.m_audio_player.stop_track()

    def export_wav(self, path_to_output:str=None):
        wav_writer = WavWriter()
        if path_to_output is None:
            wav_writer.write_wav(self.m_path, self.m_data)
        else:
            wav_writer.write_wav(path_to_output, self.m_data)

    def plot_samples(self):
        # thread = threading.Thread(target=self.__plot_samples)
        # thread.start()
        # self.__plot_samples()
        print("Temporery Stoped")

    def __plot_samples(self):
        if self.m_data == None:
            return
        number_of_channels =self.m_data.getNumberOfChannels()
        if number_of_channels == 2:
            self.__plot_stereo()
        elif number_of_channels == 1:
            self.__plot_mono()
        else:
            raise TypeError("Error: channels number incorrect!")

    def __plot_mono(self):
        # style.use('dark_background')
        f, plt_arr = plt.subplots(1, sharex = True)
        f.suptitle(self.m_path)

        plt_arr.plot(self.m_data.getSamples())

        plt.show()
    
    def __plot_stereo(self):
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

    def get_num_chanels(self)->int:
        return self.m_data.m_num_channels

    def get_audio_frame(self):
        return self.m_audio_player.get_current_frame()

    def is_audio_playing(self) -> bool:
        return self.m_audio_player.is_playing()

    def get_audio_samples_per_frame(self)->int:
        return self.m_audio_player.get_samples_per_frame()
    
    def write_samples(self, new_samples: np.ndarray)-> None:
        self.m_data.m_samples = new_samples

    def update_effect_chain(self, effect_chain:EffectChain)->None:
        self.m_effect_chain = effect_chain

    def add_to_effect_chain(self, config:dict):
        self.m_effect_chain.add_effect(config)

    def remove_all_effect_chain(self):
        self.m_effect_chain.remove_all()



