from tkinter import * 
from .MenuBar import MenuBar
from .ControlButtons import ControlButtons
from .display_view import DisplayView
from .EffectOperation import EffectOperation
from AudioManager import WavFile
import sys



class MainScreen:
    def __init__(self, wav_file:WavFile) -> None:
        self.m_root = Tk(className=" Audio Prodaction ")
        self.m_wav_file = wav_file
        # self.m_org_path:str = ""
        self.m_display:DisplayView = None
        self.m_control_buttons:ControlButtons = None
        self.__setConfiguration()
        pass

    def run(self):
        self.m_root.mainloop()

    def __setConfiguration(self):
        self.m_root.geometry('809x500')
        self.m_root.resizable(width=False, height=False)
        self.m_menu_bar = MenuBar(
            self.m_root, self.handle_wav_selection, 
            self.handle_wav_plot, 
            self.on_close, 
            self.handle_effect_chain_change,
            self.on_display_button_click)
        self.m_display = DisplayView(self.m_root, self.m_wav_file)
        self.m_control_buttons = ControlButtons(self.m_root, self.on_play_click, self.on_stop_click)
        self.m_control_buttons.pack(pady=20)
        self.m_root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_play_click(self):
        if self.m_wav_file.is_audio_playing():
            self.on_stop_click()
        self.m_display.start()
        if self.m_wav_file is None:
            return
        # self.m_wav_file.update_effect_chain(self.m_effect_chain)
        self.m_wav_file.play_audio()
    
    def on_stop_click(self):
        if self.m_wav_file is None:
            return
        self.m_wav_file.stop_audio()
        self.m_display.stop()
    
    def on_display_button_click(self)->None:
        self.m_display.switch_display_system()
    
    def handle_wav_selection(self, wav_file_path: str):
        self.on_stop_click()
        self.m_wav_file.set_path_to_wav(wav_file_path)
    
    def handle_effect_chain_change(self, operation:EffectOperation, config:dict = None, ):
        match operation:
            case EffectOperation.ADD_EFFECT:
                print("EffectOperation: adding")
                self.m_wav_file.add_to_effect_chain(config)
            case EffectOperation.REMOVE_EFFECT:
                print("EffectOperation: removing effect (Not implemented yet)")
            case EffectOperation.REMOVE_ALL:
                print("EffectOperation: remove all effects")
                self.m_wav_file.remove_all_effect_chain()


    ## NOT WORKING RIGHT NOW
    def handle_wav_plot(self):
        self.m_wav_file.plot_samples()

    def on_close(self):
        self.on_stop_click() 
        self.m_root.quit() 
        sys.exit()



