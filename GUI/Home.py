import time
import tkinter as tk
from tkinter import ttk

from threading import Thread
from queue import Queue
from enum import Enum, auto

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class Home(tk.Frame):
    """
    The RoomsClassesSpace class provides a way to view and edit the space.
    """

    def __init__(self, parent, cls):
        ttk.Frame.__init__(self, parent)
        self.timeTableMetaData__ = cls

        self.project_name__=""
        self.project_creator__=""
        self.institute_name__=""
        self.email__=""
        self.days__=list()
        self.preference_lst__=list()

        self.project_name_var = tk.StringVar(value="Time table name")
        self.project_creator_var = tk.StringVar(value="Creator")
        self.project_email_var = tk.StringVar(value="example@example.com")
        self.project_institute_var = tk.StringVar(value="institute")

        #############################################################################
        self.width__ = 87
        self.frame_ = ttk.Frame(self)
        self.frame_.pack(expand=True)
        # Saving User Info
        self.user_info_frame = ttk.LabelFrame(self.frame_, text="Timetable Metadata")
        self.user_info_frame.grid(row=0, column=0, padx=5, pady=10)

        self.frame_project_name = ttk.Frame(self.user_info_frame)
        self.frame_project_name.pack(expand=False, anchor="w")

        self.project_name = ttk.Label(self.frame_project_name, text="Project Name:")
        self.project_name.pack(side=tk.LEFT, padx=5, )

        self.project_name_entry = ttk.Entry(self.frame_project_name, width=self.width__,
                                            textvariable=self.project_name_var)
        self.project_name_entry.pack(side=tk.RIGHT, fill='y', anchor="e")

        self.frame_creator_name = ttk.Frame(self.user_info_frame)
        self.frame_creator_name.pack(expand=False, anchor="w")

        self.creator_name = ttk.Label(self.frame_creator_name, text="Creator's Name:")
        self.creator_name.pack(side=tk.LEFT, padx=5, )

        self.project_creator_entry = ttk.Entry(self.frame_creator_name, width=self.width__,
                                               textvariable=self.project_creator_var)
        self.project_creator_entry.pack(side=tk.RIGHT, fill='y', anchor="e")

        self.frame_comp_name = ttk.Frame(self.user_info_frame)
        self.frame_comp_name.pack(expand=False, anchor="w")

        self.company_name = ttk.Label(self.frame_comp_name, text="Institute:")
        self.company_name.pack(side=tk.LEFT, padx=5, )

        self.project_company_entry = ttk.Entry(self.frame_comp_name, width=self.width__,
                                               textvariable=self.project_institute_var)
        self.project_company_entry.pack(side=tk.RIGHT, fill='y', anchor="e", )

        self.frame_email_name = ttk.Frame(self.user_info_frame)
        self.frame_email_name.pack(expand=True, anchor="w")

        self.email = ttk.Label(self.frame_email_name, text="Creators' Email:")
        self.email.pack(side=tk.LEFT, padx=5, )

        email_entry = ttk.Entry(self.frame_email_name, width=self.width__, textvariable=self.project_email_var)
        email_entry.pack(side=tk.RIGHT, fill='y', anchor="e", )

        for widget in self.user_info_frame.winfo_children():
            widget.pack_configure(padx=10, pady=5)

        # Preferences Info
        self.courses_frame = ttk.LabelFrame(self.frame_, text="Peferrences")
        self.courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

        self.days_label = ttk.Label(self.courses_frame, text="Days in a Week")
        self.mon_status_var = tk.StringVar(value="MON")
        self.mon_check = ttk.Checkbutton(self.courses_frame, text="MON",
                                         variable=self.mon_status_var, onvalue="MON", offvalue="MON_")

        self.tue_status_var = tk.StringVar(value="TUE")
        self.tue_check = ttk.Checkbutton(self.courses_frame, text="TUE",
                                         variable=self.tue_status_var, onvalue="TUE", offvalue="TUE_")

        self.wed_status_var = tk.StringVar(value="WED")
        self.wed_check = ttk.Checkbutton(self.courses_frame, text="WED",
                                         variable=self.wed_status_var, onvalue="WED", offvalue="WED_")

        self.thur_status_var = tk.StringVar(value="THUR")
        self.thur_check = ttk.Checkbutton(self.courses_frame, text="THUR",
                                          variable=self.thur_status_var, onvalue="THUR", offvalue="THUR_")

        self.fri_status_var = tk.StringVar(value="FRI")
        self.fri_check = ttk.Checkbutton(self.courses_frame, text="FRI",
                                         variable=self.fri_status_var, onvalue="FRI", offvalue="FRI_")
        self.sat_status_var = tk.StringVar(value="SAT_")
        self.sat_check = ttk.Checkbutton(self.courses_frame, text="SAT",
                                         variable=self.sat_status_var, onvalue="SAT", offvalue="SAT_")
        self.sun_status_var = tk.StringVar(value="SUN_")
        self.sun_check = ttk.Checkbutton(self.courses_frame, text="SUN",
                                         variable=self.sun_status_var, onvalue="SUN", offvalue="SUN_")

        self.days_label.grid(row=0, column=0, sticky='w')
        self.mon_check.grid(row=1, column=0)
        self.tue_check.grid(row=1, column=1, sticky='w')
        self.wed_check.grid(row=1, column=2, sticky='w')
        self.thur_check.grid(row=1, column=3, sticky='w')
        self.fri_check.grid(row=1, column=4, sticky='w')
        self.sat_check.grid(row=1, column=5, sticky='w')
        self.sun_check.grid(row=1, column=6, sticky='w')

        self.space_label = ttk.Label(self.courses_frame, text="Classroom/Room/Space")
        self.space_status_var = tk.StringVar(value="Classroom")
        self.classroom_check = ttk.Checkbutton(self.courses_frame, text="Classroom",
                                               variable=self.space_status_var, onvalue="Classroom",
                                               offvalue="Classroom_")

        self.room_check = ttk.Checkbutton(self.courses_frame, text="Room",
                                          variable=self.space_status_var, onvalue="Room", offvalue="Room_")

        self.space_check = ttk.Checkbutton(self.courses_frame, text="Space",
                                           variable=self.space_status_var, onvalue="Space", offvalue="Space_")

        self.space_label.grid(row=2, column=0, sticky='w')
        self.classroom_check.grid(row=3, column=0)
        self.room_check.grid(row=3, column=1)
        self.space_check.grid(row=3, column=2)

        self.session_label = ttk.Label(self.courses_frame, text="CourseUnit/Class/Session/Subject")
        self.session_status_var = tk.StringVar(value="CourseUnit")
        self.course_unit_check = ttk.Checkbutton(self.courses_frame, text="CourseUnit",
                                                 variable=self.session_status_var, onvalue="CourseUnit",
                                                 offvalue="CourseUnit_")

        self.class_check = ttk.Checkbutton(self.courses_frame, text="Class",
                                           variable=self.session_status_var, onvalue="Class", offvalue="Class_")

        self.session_check = ttk.Checkbutton(self.courses_frame, text="Session",
                                             variable=self.session_status_var, onvalue="Session", offvalue="Session_")
        self.subject_check = ttk.Checkbutton(self.courses_frame, text="Subject",
                                             variable=self.session_status_var, onvalue="Subject", offvalue="Subject_")

        self.session_label.grid(row=4, column=0, sticky='w')
        self.course_unit_check.grid(row=5, column=0)
        self.class_check.grid(row=5, column=1)
        self.session_check.grid(row=5, column=2)
        self.subject_check.grid(row=5, column=3)

        self.tutor_label = ttk.Label(self.courses_frame, text="Instructor/Lecturer/Tutor")
        self.tutor_status_var = tk.StringVar(value="Instructor")
        self.instructor_unit_check = ttk.Checkbutton(self.courses_frame, text="Instructor",
                                                     variable=self.tutor_status_var, onvalue="Instructor",
                                                     offvalue="Instructor_")

        lecturer_check = ttk.Checkbutton(self.courses_frame, text="Lecturer",
                                         variable=self.tutor_status_var, onvalue="Lecturer", offvalue="Lecturer_")

        tutor_check = ttk.Checkbutton(self.courses_frame, text="Tutor",
                                      variable=self.tutor_status_var, onvalue="Tutor", offvalue="Tutor_")

        self.tutor_label.grid(row=6, column=0, sticky='w')
        self.instructor_unit_check.grid(row=7, column=0)
        lecturer_check.grid(row=7, column=1)
        tutor_check.grid(row=7, column=2)

        for widget in self.courses_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Accept terms
        self.terms_frame = ttk.LabelFrame(self.frame_, text="Terms & Conditions")
        self.terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

        self.terms_check = tk.Label(self.terms_frame, text="Please note, All time are in 24 HOURS clock.")
        self.terms_check.grid(row=0, column=0)

        # Button
        button = ttk.Button(self.frame_, text="Save Information", command=self.save_information)
        button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        #############################################################################

    def save_information(self):
        self.project_name__ = self.project_name_var.get()
        self.project_creator__ = self.project_creator_var.get()
        self.email__ = self.project_email_var.get()
        self.institute_name__ = self.project_institute_var.get()

        self.days__.append(self.mon_status_var.get())
        self.days__.append(self.tue_status_var.get())
        self.days__.append(self.wed_status_var.get())
        self.days__.append(self.thur_status_var.get())
        self.days__.append(self.fri_status_var.get())
        self.days__.append(self.sat_status_var.get())
        self.days__.append(self.sun_status_var.get())


        self.preference_lst__: list = [self.space_status_var,
                                self.session_status_var,
                                self.tutor_status_var]

        self.timeTableMetaData__.set_timetable_information(
            self.project_name__,
            self.project_creator__,
            self.institute_name__,
            self.email__,
            self.days__,
            self.preference_lst__
        )


    def Check_Queue(self, e):
        """
       Read the queue
        """
        msg: Ticket
        msg = self.queue_message.get()
        if msg.ticket_type == TicketPurpose.UPDATE_PROGRESS_TEXT:
            self.treeview.insert('', tk.END, values=msg.ticket_value)
        if msg.ticket_type == TicketPurpose.UPDATE_PROGRESS_HEADING:
            self.treeview.column(msg.ticket_value[0], width=50, anchor='c')
            self.treeview.heading(msg.ticket_value[0], text=msg.ticket_value[0])


# Ticketing system call
class TicketPurpose(Enum):
    UPDATE_PROGRESS_TEXT = auto()
    UPDATE_PROGRESS_HEADING = auto()


class Ticket:
    def __init__(self, ticket_type: TicketPurpose,
                 ticket_value: list):
        self.ticket_type = ticket_type
        self.ticket_value = ticket_value