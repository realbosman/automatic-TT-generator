import time
import tkinter as tk
from tkinter import ttk, messagebox
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
from Models.Tutor_Model import TutorsManager
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

    def __init__(self, parent, *cls):

        ttk.Frame.__init__(self, parent)
        self.progress_number = 0;

        for index, arg in enumerate(cls):
            print("Running args")
            if index == 0:
                self.gen_time_dimension = arg
            if index == 1:
                self.get_metadata = arg
            if index == 2:
                self.space_ = arg
            if index == 3:
                self.lectures_ = arg
            if index == 4:
                self.lecturers_ = arg
            if index == 5:
                self.algorithm_ = arg
            if index == 5:
                self.listener___ = arg
        # print("FROM VISUAL After args ==", self.get_metadata.time_table_name)

        # print("cls>>>>",cls)

        # print(" self.get_metadata.time_table_name,==", self.get_metadata.time_table_name,)

        self.name_timetable = self.get_metadata.time_table_name
        # print("FROM VISUAL After args plus name ==", self.get_metadata.time_table_name, self.name_timetable)
        self.frame_ = tk.Frame(self, background="black", )
        self.frame_.pack(fill=tk.BOTH, expand=1, anchor="center")

        self.queue_message = Queue()
        self.bind("<<CheckQueue_gen>>", self.Check_Queue)
        self.txt_var = tk.StringVar(value="Generating TimeTable: 0%")
        self.txt_var_ = tk.StringVar()
        self.global_stop_execution = False

        self.animate_()
        # print(" After ANimate args plus name ==", self.get_metadata.time_table_name, self.name_timetable)

        self.ll = ttk.Label(self.frame_, textvariable=self.txt_var, background='black', font=16)
        self.ll.place(x=0, y=0, relx=0.4, rely=0.55)
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

        self.img_container = ttk.Label(self.frame_, image=next(self.image_cycle), border=None, background="black")
        self.img_container.place(x=0, y=0, relx=0.45, rely=0.4)
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
            if msg.ticket_value == 100:
                # print("Before 100 ==", self.get_metadata.time_table_name, self.name_timetable)
                self.txt_var.set(f'Generating TimeTable Done: 100%')
                self.txt_var_.set(f'Preparing .....')
                self.visualize_Time_table_thread()
                # print("after 100  and thread==", self.get_metadata.time_table_name, self.name_timetable)
                # print("Running")
                self.unbind("<<CheckQueue_gen>>")

    def update_text(self):
        try:
            while self.algorithm_.progress_var <= 100:
                ticket = Ticket(ticket_type=TicketPurpose.UPDATE_PROGRESS_TEXT,
                                ticket_value=self.algorithm_.progress_var)
                self.queue_message.put(ticket)
                self.event_generate("<<CheckQueue_gen>>", when="tail")
                time.sleep(.2)
        except:
            print("<<CheckQueue_gen>> already unbound")

        # This delay helps to relieve the  while and the processor

    def gen_process(self, t_res, l_res, s_res, title, creator,tutor_lst):

        self.timetableMetadata = TimetableMetaData(self.gen_time_dimension)
        # print("DDDDDAAAYAYAYYA", self.gen_time_dimension.Days["headers"])
        self.algorithm_.random_generator(t_res,
                                         l_res,
                                         s_res,
                                         title,
                                         creator,
                                         tutor_lst
                                         )

    def update_thread(self):
        new_thread = Thread(target=self.update_text, daemon=True)  # I can pass args = "any" for the target
        new_thread.start()

    def generate_thread(self):
        new_thread = Thread(target=self.gen_process, daemon=True,
                            args=(self.gen_time_dimension.get_algo_reources(), self.lectures_.get_algo_reources(),
                                  self.space_.get_algo_reources(),
                                  self.get_metadata.time_table_name, self.get_metadata.creator_name,
                                  self.lectures_.tutors_lst(),))  # I can pass args = "any" for the target
        new_thread.start()
        self.update_thread()

    def visualize_Time_table(self, parent, name):
        time.sleep(.5)
        for widget in parent.winfo_children():
            # print("running widget 1")
            widget.destroy()
        # Create a vertical scrollbar
        self.scrollbar = tk.Scrollbar(parent)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a canvas
        self.canvas = tk.Canvas(parent, width=800, height=600, yscrollcommand=self.scrollbar.set)
        self.canvas.place(relx=.5, rely=.5, anchor=tk.CENTER)
        # self.canvas.tkraise()

        # Link scrollbar to canvas
        self.scrollbar.config(command=self.canvas.yview)

        # Enable mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Create a frame inside the canvas to hold the images
        self.frame_images = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_images, anchor=tk.CENTER)

        # Open the PDF file
        # self.listener__ = Listener()
        Listener.isTimeTableCreated = False

        try:
            print("Listener.timeTableNameListener}======",Listener.timeTableNameListener)
            pdf_document = fitz.open(rf'{Listener.get_app_path_docs()}\{Listener.timeTableNameListener}.pdf')
            # print()
        except:
            messagebox.showerror(title="Error", message="Timetable generation error invalid file name")
            return

        # Load and display each page of the PDF as a resized image
        self.images = []
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            # Resize the image
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples).resize((800, 800))
            img = ImageTk.PhotoImage(image=img)
            self.images.append(img)
            self.canvas.create_image(10, 10 + page_number * (img.height() + 10), anchor=NW, image=img)
        # Update the scroll region to include all the images
        self.frame_images.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        Listener.isTimeTableCreated = True
        Listener.timeTableNameListener = name
        # To set the timetable name from any frame
        # TimeTableManager.set_time_table_name(name)

        # To get the timetable name from any frame

        # print("Name:", name)
        # print("LISTENER NAME", Listener.timeTableNameListener)
        # print("STATIC", TimeTableManager.get_time_table_name())

    def on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except:
            print("Exception in on_mousewheel method GenerateTimeTable.py")

    def visualize_Time_table_thread(self):
        # print("FROM VISUAL Before ==", self.get_metadata.time_table_name,)
        # TODO STACK HERE
        new_thread_ = Thread(target=self.visualize_Time_table, daemon=True, args=(self.frame_,
                                                                                  Listener.timeTableNameListener,))  # I can pass args = "any" for the target
        new_thread_.start()
        self.get_metadata.time_table_name = self.name_timetable

        # print("FROM VISUAL After==", self.get_metadata.time_table_name)


# Ticketing system call
class TicketPurpose(Enum):
    UPDATE_PROGRESS_TEXT = auto()
    UPDATE_PROGRESS_HEADING = auto()


class Ticket:
    def __init__(self, ticket_type: TicketPurpose,
                 ticket_value: int):
        self.ticket_type = ticket_type
        self.ticket_value = ticket_value
