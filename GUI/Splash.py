
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk, ImageSequence
from itertools import cycle
from pathlib import Path


_PATH = Path(__file__).parent / 'assets'
from tkinter import *
from PIL import Image, ImageTk



from pathlib import Path


IMG_PATH = Path(__file__).parent / 'assets'


# import openpyxl

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class Splash(tk.Frame):
    """
    The Groups class provides a way to view  the groups in the timetable.
    """
    def __init__(self, parent, *cls):


        ttk.Frame.__init__(self, parent)
        self.txt_var=tk.StringVar(value="")
        self.frame_ = tk.Frame(self, background="black", )
        self.frame_.pack(fill=tk.BOTH, expand=1, anchor="center")



        self.animate_()

        self.ll = ttk.Label(self.frame_, textvariable=self.txt_var,background='black',font=16)
        self.ll.place(x=0,y=0,relx=0.4,rely=0.55)





    def animate_(self):
        # open the GIF and create a cycle iterator
        file_path = Path(__file__).parent / "assets/spp_smaller.gif"
        with Image.open(file_path) as im:
            # create a sequence
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # length of each frame
            self.framerate = im.info["duration"]

        self.img_container = ttk.Label(self.frame_, image=next(self.image_cycle),background="black",border=None)
        self.img_container.place(x=0,y=0,relx=0.45,rely=0.4)
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """Update the image for each frame"""
        try:
            self.img_container.configure(image=next(self.image_cycle))
            self.after(self.framerate, self.next_frame)
        except:
            print("spinner already deleted")




