from AudioManager import WavFile
from AudioEffect import *
from Gui import MainScreen

if __name__ == "__main__":
    wav_file = WavFile()
    app = MainScreen(wav_file)
    app.run() 