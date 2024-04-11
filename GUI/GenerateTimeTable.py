import time
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence
from itertools import cycle

from threading import Thread
from queue import Queue
from enum import Enum, auto
from flask import Flask, send_file
from pathlib import Path
import re

from tk import *
#
from Algorithm.Algo import TtGenerator
from Algorithm.TimetableMetaData import TimetableMetaData
from Models.ClassRoomModel import SpaceManager
from Models.CourseUnitModel import SessionManager
from Models.Lecturer_Model import TutorsManager
from Models.TimeDimension import TimeDimension

IMG_PATH = Path(__file__).parent / 'assets'


# import openpyxl

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class GenerateTimeTable(tk.Frame):
    """
    The Groups class provides a way to view  the groups in the timetable.
    """
    def __init__(self, parent, cls,cls_=None):

        ttk.Frame.__init__(self, parent)
        self.progress_numder=0;
        self.gen_time_dimension=cls
        self.frame_=tk.Frame(self,background="black",)
        self.frame_.pack( fill=tk.BOTH,expand=1,anchor="center")

        self.queue_message = Queue()
        self.bind("<<CheckQueue>>", self.Check_Queue)
        self.txt_var=tk.StringVar(value="Generating TimeTable: 0%")


        self.algorithm_ = TtGenerator()





        self.animate_()

        self.ll = ttk.Label(self.frame_, textvariable=self.txt_var,background='black',font=16)
        self.ll.place(x=0,y=0,relx=0.4,rely=0.55)

        self.generate_thread()




    def animate_(self):
        # open the GIF and create a cycle iterator
        file_path = Path(__file__).parent / "assets/spinners.gif"
        with Image.open(file_path) as im:
            # create a sequence
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # length of each frame
            self.framerate = im.info["duration"]

        self.img_container = ttk.Label(self.frame_, image=next(self.image_cycle),border=None)
        self.img_container.place(x=0,y=0,relx=0.45,rely=0.4)
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """Update the image for each frame"""
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)

    def Check_Queue(self, e):
        """
       Read the queue
        """
        msg: Ticket
        msg = self.queue_message.get()
        if msg.ticket_type == TicketPurpose.UPDATE_PROGRESS_TEXT:
            self.txt_var.set(f'Generating TimeTable: {msg.ticket_value}%')
            if msg.ticket_value==100:
                self.txt_var.set(f'Generating TimeTable Done: 100%')
                # self.img_container.unpa



    def update_text(self):
        while self.algorithm_.progress_var <=100:
            ticket = Ticket(ticket_type=TicketPurpose.UPDATE_PROGRESS_TEXT,
                            ticket_value=self.algorithm_.progress_var)
            self.queue_message.put(ticket)
            self.event_generate("<<CheckQueue>>", when="tail")
            time.sleep(.2)  # This delay helps to relieve the  while and the processor
    def gen_process(self):
        self.space_ = SpaceManager()
        self.lectures_ = SessionManager()
        self.lecturers_ = TutorsManager()
        self.timetableMetadata = TimetableMetaData(self.gen_time_dimension)
        # print("DDDDDAAAYAYAYYA", self.gen_time_dimension.Days["headers"])
        self.algorithm_.random_generator(self.gen_time_dimension.get_algo_reources(),
                                         self.lectures_.get_algo_reources(),
                                         self.space_.get_algo_reources())

    def update_thread(self):
        new_thread = Thread(target=self.update_text, daemon=True)  # I can pass args = "any" for the target
        new_thread.start()


    def generate_thread(self):
        new_thread = Thread(target=self.gen_process, daemon=True)  # I can pass args = "any" for the target
        new_thread.start()
        self.update_thread()




# Ticketing system call
class TicketPurpose(Enum):
    UPDATE_PROGRESS_TEXT = auto()
    UPDATE_PROGRESS_HEADING = auto()


class Ticket:
    def __init__(self, ticket_type: TicketPurpose,
                 ticket_value: int):
        self.ticket_type = ticket_type
        self.ticket_value = ticket_value




