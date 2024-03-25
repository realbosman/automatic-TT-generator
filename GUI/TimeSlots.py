import time
import tkinter as tk
from tkinter import ttk



# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class TimeSlots(tk.Frame):
    """
    The time slots class provides a way to view and edit the time periods.
    """
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.config(bg=visualisation_frame_color)

       #TODO: call all the timeslots methods here to show up when th ui is created

        # PLOT FRAME
        self.plot_frame = tk.Frame(self, bg=visualisation_frame_color)
        self.plot_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

#     TODO put all the functions here that are gonna help manage the  time slot
