from tkinter import Frame, Button
from tkinter import font as tkfont

class ControlButtons:
    def __init__(self, master, play_command, stop_command):
        self.frame = Frame(master)
        # self.play_button = Button(self.frame, text="Play", command=play_command)
        # self.stop_button = Button(self.frame, text="Stop", command=stop_command)
        custom_font = tkfont.Font(family="Helvetica", size=12)

        # Configure Play button
        self.play_button = Button(self.frame, text="Play", command=play_command,
                                  font=custom_font,  padx=10, pady=5, relief="raised", borderwidth=2)
        self.play_button.pack(side="left", padx=5, pady=5)

        # Configure Stop button
        self.stop_button = Button(self.frame, text="Stop", command=stop_command,
                                  font=custom_font,  padx=10, pady=5, relief="raised", borderwidth=2)
        self.stop_button.pack(side="left", padx=5, pady=5)

        # Layout the buttons
        self.play_button.pack(side="left", padx=5)
        self.stop_button.pack(side="left", padx=5)

    def pack(self, **pack_options):
        self.frame.pack(**pack_options)

    def grid(self, **grid_options):
        self.frame.grid(**grid_options)

    def place(self, **place_options):
        self.frame.place(**place_options)