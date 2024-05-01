import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

from Models.Listener import Listener

_PATH = Path(__file__).parent / 'assets'
from tkinter import *
from PIL import Image, ImageTk
import fitz  # PyMuPDF

from threading import Thread
from queue import Queue
from enum import Enum, auto
from pathlib import Path

#
from Algorithm.TimetableMetaData import TimetableMetaData

IMG_PATH = Path(__file__).parent / 'assets'

# import openpyxl

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class View(tk.Frame):
    """
    The Groups class provides a way to view  the groups in the timetable.
    """

    def __init__(self, parent, *cls):

        ttk.Frame.__init__(self, parent)

        for arg in cls:
            self.listener_View = arg

        self.NameListener = self.listener_View.timeTableNameListener

        self.visualize_Time_table_thread()

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

    def gen_process(self, t_res, l_res, s_res, title, creator):

        self.timetableMetadata = TimetableMetaData(self.gen_time_dimension)
        # print("DDDDDAAAYAYAYYA", self.gen_time_dimension.Days["headers"])
        self.algorithm_.random_generator(t_res,
                                         l_res,
                                         s_res,
                                         title,
                                         creator
                                         )

    def update_thread(self):
        new_thread = Thread(target=self.update_text, daemon=True)  # I can pass args = "any" for the target
        new_thread.start()

    def generate_thread(self):
        new_thread = Thread(target=self.gen_process, daemon=True,
                            args=(self.gen_time_dimension.get_algo_reources(), self.lectures_.get_algo_reources(),
                                  self.space_.get_algo_reources(),
                                  self.get_metadata.time_table_name,
                                  self.get_metadata.creator_name,))  # I can pass args = "any" for the target
        new_thread.start()
        self.update_thread()

    def visualize_Time_table(self, parent, name):
        time.sleep(.2)
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
        if name == "":
            # print("Name:", name)
            messagebox.showerror(title="Error", message=f'<{name}>')
            return
        # print('Before')
        pdf_document = fitz.open(rf'{Listener.get_app_path_docs()}\{name}.pdf')
        # print('After')

        # Load and display each page of the PDF as a resized image
        self.images = []
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            # Resize the image
            img: Image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples).resize((800, 800))
            img: Image = ImageTk.PhotoImage(image=img)
            self.images.append(img)
            self.canvas.create_image(10, 10 + page_number * (img.height() + 10), anchor=NW, image=img)
            # print('Loop==',page_number)

        # Update the scroll region to include all the images
        self.frame_images.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        try:
          self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except:
            print("Exception,canvas not visible")

    def visualize_Time_table_thread(self):
        # print("FROM VISUAL Before ==", self.get_metadata.time_table_name,)
        # TODO STACK HERE
        time.sleep(0)
        new_thread_ = Thread(target=self.visualize_Time_table, daemon=True, args=(self,
                                                                                  Listener.timeTableNameListener,))  # I can pass args = "any" for the target
        new_thread_.start()

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
