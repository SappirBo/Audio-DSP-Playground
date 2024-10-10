from tkinter import Menu,Tk, filedialog
import tkinter as tk
import json
from .EffectWindow import EffectWindow
from EffectChain import EffectChain

class MenuBar:
    def __init__(self, master: Tk, wav_select_callback, plot_wav_callback, close_callback, effect_chain:EffectChain):
        self.m_wav_select_callback = wav_select_callback
        self.m_plot_wav_callback = plot_wav_callback
        self.m_close_callback = close_callback

        self.m_selected_path = None
        self.m_master = master

        self.m_menu_bar = Menu(master)
        master.config(menu=self.m_menu_bar)
        self.m_menu_bar.add_command(label="Import Wav", command=self.selectWavFile)
        self.m_menu_bar.add_separator()
        # self.m_menu_bar.add_command(label="Show Amplitude", command=self.plotWavFile)
        # self.m_menu_bar.add_separator()

        effects_menu = Menu(self.m_menu_bar, tearoff=0)
        self.m_menu_bar.add_cascade(label="Effects", menu=effects_menu)
        effects_menu.add_command(label="Show Effects", command=lambda: self.effects_command(0))
        effects_menu.add_command(label="Add Effect", command=lambda: self.effects_command(1))
        effects_menu.add_command(label="Remove Effect", command=lambda: self.effects_command(2))

        self.m_menu_bar.add_command(label="Export Wav",command=lambda: testCommand(1))
        self.m_menu_bar.add_separator()
        self.m_menu_bar.add_command(label="Exit", command=master.quit)

        self.m_effect_chain = effect_chain
    
    def grace_exit(self):
        self.m_close_callback()
        # self.m_master.quit()

    def effects_command(self, code):
        if code == 0:
            print("Showing Effects...")
        elif code == 1:
            self.show_add_effect_window()
        elif code == 2:
            print("Removing Effect...")

    def remove_all_effects(self)->None:
        print("Removing Effect...")
        self.m_effect_chain.remove_all()

    def show_add_effect_window(self):
        """Open a new window to add effects from the effects.json file."""
        effect_window = tk.Toplevel(self.m_menu_bar)
        effect_window.title("Add Effects")

        # Read effects from a JSON file
        with open("effects.json", "r") as file:
            data = json.load(file)
            effects = data.get("effects", [])

        # Create a button for each effect
        for effect in effects:
            tk.Button(effect_window, text=effect, command=lambda e=effect: self.open_effect_configure(e)).pack()

    def open_effect_configure(self, effect_name):
        print(effect_name)
        # call here to EffectWindow
        with open("effects_params.json", "r") as file:
            data = json.load(file)
            effects = data.get("effects", {})
            effect_data = effects.get(effect_name, {})
        EffectWindow(self.m_master, effect_name, effect_data, self.add_effect)
        
    def selectWavFile(self):
        """
        69Open file explorer for the user to choose a WAV file.
        """
        file_types = [('WAV files', '*.wav')]
        wav_file_path = filedialog.askopenfilename(title="Select a WAV file", filetypes=file_types)
        if wav_file_path:
            self.m_wav_select_callback(wav_file_path)

    def plotWavFile(self):
        self.m_plot_wav_callback()

    def add_effect(self, config:dict):
        self.m_effect_chain.add_effect(config)

def dummy():
    print("DUMMY!")       
    
def testCommand(code:int):
    if code == 0:
        print("uploading!")
    if code == 1:
        print("Newing!")
    if code == 2:
        print("See You!")
    pass