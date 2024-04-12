import time
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk, ImageSequence
from itertools import cycle
from pathlib import Path
from tkinter import *
from PIL import ImageTk, Image

from Models.Listener import Listener

_PATH = Path(__file__).parent / 'assets'
from tkinter import *
from PIL import Image, ImageTk
import fitz  # PyMuPDF

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
        self.get_metadata=cls_
        print(" self.get_metadata.time_table_name,==", self.get_metadata.time_table_name,)
        self.frame_=tk.Frame(self,background="black",)
        self.frame_.pack( fill=tk.BOTH,expand=1,anchor="center")

        self.queue_message = Queue()
        self.bind("<<CheckQueue>>", self.Check_Queue)
        self.txt_var=tk.StringVar(value="Generating TimeTable: 0%")
        self.txt_var_ = tk.StringVar()
        self.global_stop_execution=False


        self.algorithm_ = TtGenerator()





        self.animate_()

        self.ll = ttk.Label(self.frame_, textvariable=self.txt_var,background='black',font=16)
        self.ll.place(x=0,y=0,relx=0.4,rely=0.55)
        self.ll2 = ttk.Label(self.frame_, textvariable=self.txt_var_, background='black', font=16)
        # self.ll2.place(x=0, y=0, relx=0.4, rely=0.65)


        self.generate_thread()




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

        self.img_container = ttk.Label(self.frame_, image=next(self.image_cycle),border=None)
        self.img_container.place(x=0,y=0,relx=0.45,rely=0.4)
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """Update the image for each frame"""
        try:
            self.img_container.configure(image=next(self.image_cycle))
            self.after(self.framerate, self.next_frame)
        except:
            print("spinner already deleted")


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
                self.txt_var_.set(f'Preparing .....')
                self.visualize_Time_table_thread()
                print("Running")
                self.unbind("<<CheckQueue>>")





    def update_text(self):
        while self.algorithm_.progress_var <=100:
            ticket = Ticket(ticket_type=TicketPurpose.UPDATE_PROGRESS_TEXT,
                            ticket_value=self.algorithm_.progress_var)
            self.queue_message.put(ticket)
            self.event_generate("<<CheckQueue>>", when="tail")
            time.sleep(.2)  # This delay helps to relieve the  while and the processor

    def gen_process(self,title,creator):
        self.space_ = SpaceManager()
        self.lectures_ = SessionManager()
        self.lecturers_ = TutorsManager()
        self.timetableMetadata = TimetableMetaData(self.gen_time_dimension)
        # print("DDDDDAAAYAYAYYA", self.gen_time_dimension.Days["headers"])
        self.algorithm_.random_generator(self.gen_time_dimension.get_algo_reources(),
                                         self.lectures_.get_algo_reources(),
                                         self.space_.get_algo_reources(),
                                         title,
                                         creator
                                         )

    def update_thread(self):
        new_thread = Thread(target=self.update_text, daemon=True)  # I can pass args = "any" for the target
        new_thread.start()


    def generate_thread(self):
        new_thread = Thread(target=self.gen_process, daemon=True,args=(self.get_metadata.time_table_name,self.get_metadata.creator_name))  # I can pass args = "any" for the target
        new_thread.start()
        self.update_thread()


    def visualize_Time_table(self,parent,):
        time.sleep(5)
        for widget in self.frame_.winfo_children():
            # print("running widget 1")
            widget.destroy()
        # Create a vertical scrollbar
        self.scrollbar = tk.Scrollbar(parent)
        self. scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas
        self.canvas = tk.Canvas(parent, width=700,height=600, yscrollcommand=self.scrollbar.set)
        self.canvas.place(relx=.5, rely=.5, anchor=tk.CENTER)
        # self.canvas.tkraise()

        # Link scrollbar to canvas
        self.scrollbar.config(command=self.canvas.yview)

        # Enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Create a frame inside the canvas to hold the images
        self.frame_images = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_images, anchor=tk.NW)

        # Open the PDF file
        self.listener__ = Listener()
        self.timetableMetadata = TimetableMetaData(self.gen_time_dimension)


        pdf_document = fitz.open(f'{self.listener__.get_app_path()}\{self.timetableMetadata.time_table_name}.pdf')

        # Load and display each page of the PDF as a resized image
        self.images = []
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            # Resize the image
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples).resize((700, 700))
            img = ImageTk.PhotoImage(image=img)
            self.images.append(img)
            self.canvas.create_image(10, 10 + page_number * (img.height() + 10), anchor=NW, image=img)
        # Update the scroll region to include all the images
        self.frame_images.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self,event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def visualize_Time_table_thread(self):
        new_thread = Thread(target=self.visualize_Time_table, daemon=True,args=(self.frame_,))  # I can pass args = "any" for the target
        new_thread.start()





# Ticketing system call
class TicketPurpose(Enum):
    UPDATE_PROGRESS_TEXT = auto()
    UPDATE_PROGRESS_HEADING = auto()


class Ticket:
    def __init__(self, ticket_type: TicketPurpose,
                 ticket_value: int):
        self.ticket_type = ticket_type
        self.ticket_value = ticket_value




