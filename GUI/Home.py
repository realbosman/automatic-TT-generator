import time
import tkinter as tk
from tkinter import ttk, messagebox

from threading import Thread
from queue import Queue
from enum import Enum, auto

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
from Algorithm.TimetableMetaData import TimetableMetaData
from Models.Listener import Listener

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class Home(tk.Frame):
    """
    The Home class provides a way to view and edit the time table metadata.
    """

    def __init__(self, parent, *cls):
        ttk.Frame.__init__(self, parent)

        # # Create custom style for scrollbar
        # style = ttk.Style()
        # style.theme_use("clam")  # Choose a theme (e.g., "clam")
        # style.configure("My.Vertical.TScrollbar", width=20)  # Set the width of the vertical scrollbar

        # print("TimetableMetaData.isInfoSet==", TimetableMetaData.isInfoSet)
        self.timeTableMetaData__, self.td, self.listenerr = cls
        # print(self.listenerr.getStateHome())
        Listener.set_state_home(True)
        # print(self.listenerr.getStateHome())
        self.project_name__ = ""
        self.project_creator__ = ""
        self.institute_name__ = ""
        self.email__ = ""
        self.days__ = list()
        self.preference_lst__ = list()

        self.project_name_var = tk.StringVar(value="Time table name")
        self.project_creator_var = tk.StringVar(value="Creator")
        self.project_email_var = tk.StringVar(value="example@example.com")
        self.project_institute_var = tk.StringVar(value="institute")
        self.mon_status_var = tk.StringVar(value="MON")
        self.tue_status_var = tk.StringVar(value="TUE")
        self.wed_status_var = tk.StringVar(value="WED")
        self.thur_status_var = tk.StringVar(value="THUR")
        self.fri_status_var = tk.StringVar(value="FRI")
        self.sat_status_var = tk.StringVar(value="SAT")
        self.sun_status_var = tk.StringVar(value="SUN")
        self.tutor_status_var = tk.StringVar(value="Instructor")
        self.session_status_var = tk.StringVar(value="CourseUnit")
        self.space_status_var = tk.StringVar(value="Classroom")
        self.update_thread()

        self.canvas = tk.Canvas(self, background=visualisation_frame_color)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=20)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.create_window((self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2), window=self.scrollable_frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set )

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # Bind mouse wheel event to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.canvas.pack(side="left", fill="both",  expand=True)
        self.scrollbar.pack(side="right", fill="y")


        #############################################################################
        self.width__ = 87
        self.frame_ = self.scrollable_frame
        # self.frame_.pack(expand=True, padx=(0, 20))

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

        self.mon_check = ttk.Checkbutton(self.courses_frame, text="MON",
                                         variable=self.mon_status_var, onvalue="MON", offvalue="MON_")

        self.tue_check = ttk.Checkbutton(self.courses_frame, text="TUE",
                                         variable=self.tue_status_var, onvalue="TUE", offvalue="TUE_")

        self.wed_check = ttk.Checkbutton(self.courses_frame, text="WED",
                                         variable=self.wed_status_var, onvalue="WED", offvalue="WED_")

        self.thur_check = ttk.Checkbutton(self.courses_frame, text="THUR",
                                          variable=self.thur_status_var, onvalue="THUR", offvalue="THUR_")

        self.fri_check = ttk.Checkbutton(self.courses_frame, text="FRI",
                                         variable=self.fri_status_var, onvalue="FRI", offvalue="FRI_")

        self.sat_check = ttk.Checkbutton(self.courses_frame, text="SAT",
                                         variable=self.sat_status_var, onvalue="SAT", offvalue="SAT_")

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

        self.classroom_check = ttk.Checkbutton(self.courses_frame, text="Classroom",
                                               variable=self.space_status_var, onvalue="Classroom",
                                               offvalue="Classroom_")

        self.room_check = ttk.Checkbutton(self.courses_frame, text="Rooms",
                                          variable=self.space_status_var, onvalue="Rooms", offvalue="Rooms_")

        self.space_check = ttk.Checkbutton(self.courses_frame, text="Space",
                                           variable=self.space_status_var, onvalue="Space", offvalue="Space_")

        self.space_label.grid(row=2, column=0, sticky='w')
        self.classroom_check.grid(row=3, column=0)
        self.room_check.grid(row=3, column=1)
        self.space_check.grid(row=3, column=2)

        self.session_label = ttk.Label(self.courses_frame, text="CourseUnit/Class/Session/Subject")

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
        #
        # Preferences Info
        self.breaks_frame = ttk.LabelFrame(self.frame_, text=f'Timetable Breaks (separate with "," )')
        self.breaks_frame.grid(row=2, column=0, columnspan=2, sticky="news", padx=20, pady=10)  # Adjust columnspan

        self.breaks_entry_variable =tk.StringVar(value="13:00-14:00")
        self.breaks_entry = ttk.Entry(self.breaks_frame, textvariable= self.breaks_entry_variable,width=100)
        self.breaks_entry.pack(fill=tk.X, expand=1, side='right', padx=10, pady=10
                               )  # Use sticky option to expand horizontally

        for widget in self.breaks_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Accept terms
        self.terms_frame = ttk.LabelFrame(self.frame_, text="Terms & Conditions")
        self.terms_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        self.terms_check = tk.Label(self.terms_frame, text="Please Note, All time is in 24 HOURS clock.")
        self.terms_check.grid(row=0, column=0)

        # Button
        button = ttk.Button(self.frame_, text="Save Information", command=self.save_thread)
        button.grid(row=4, column=0, sticky="news", padx=20, pady=10)

        #############################################################################

        # self.updateUI()
        # self.aut_save_thread()

        #############################################################################

    def updateUI(self):
        if TimetableMetaData.isInfoSet:
            # print(self.timeTableMetaData__.time_table_name)
            # print(self.timeTableMetaData__.preferences_list[0])
            self.project_name_var.set(TimetableMetaData.time_table_name)
            self.project_creator_var.set(TimetableMetaData.creator_name)
            self.project_email_var.set(TimetableMetaData.creators_email)
            self.project_institute_var.set(TimetableMetaData.institute_name)
            self.space_status_var.set(TimetableMetaData.preferences_list_[0])
            self.session_status_var.set(TimetableMetaData.preferences_list_[1])
            self.tutor_status_var.set(TimetableMetaData.preferences_list_[2])

        mylist = self.refresh_list_Home_timetable_metadata(self.td.Days)
        # print("myyy-",mylist)
        self.mon_status_var.set(mylist[0])
        self.tue_status_var.set(mylist[1])
        self.wed_status_var.set(mylist[2])
        self.thur_status_var.set(mylist[3])
        self.fri_status_var.set(mylist[4])
        self.sat_status_var.set(mylist[5])
        self.sun_status_var.set(mylist[6])

    def on_mousewheel(self, event):
        # On mouse wheel event, scroll the canvas
        try:
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        except:
            pass

    def save_information(self):

        if self.sat_status_var.get()[-1] == "_" and self.sun_status_var.get()[-1] == "_":
            Listener.isWeekendInclusive = True
        else:
            Listener.isWeekendInclusive = False

        if self.mon_status_var.get()[-1] == "_" and self.tue_status_var.get()[-1] == "_" and self.wed_status_var.get()[
            -1] == "_" and self.thur_status_var.get()[-1] == "_" and self.fri_status_var.get()[-1] == "_" and \
                self.sat_status_var.get()[-1] == "_" and self.sun_status_var.get()[-1] == "_":
            messagebox.showerror(title="Timetable Metadata Error",
                                 message="Days are not selected!,Please select a day.")
            Listener.isWeekendInclusive = False
            return
        elif self.project_creator_var.get() == "":
            messagebox.showerror(title="Timetable Metadata Error",
                                 message="Fields can't be left blank.")
            Listener.isWeekendInclusive = False
            return
        elif self.project_institute_var.get() == "":
            messagebox.showerror(title="Timetable Metadata Error",
                                 message="Fields can't be left blank.")
            Listener.isWeekendInclusive = False
            return
        elif self.project_name_var.get() == "":
            messagebox.showerror(title="Timetable Metadata Error",
                                 message="Fields can't be left blank.")
            Listener.isWeekendInclusive = False
            return
        elif self.space_status_var.get()[-1] == "_" or self.session_status_var.get()[-1] == "_" or \
                self.tutor_status_var.get()[-1] == "_":
            messagebox.showerror(title="Timetable Metadata Error",
                                 message="Fields can't be left blank.")
            Listener.isWeekendInclusive = False
            return

        else:
            break_list=self.breaks_entry_variable.get().split(',', -1)
            for break_ in break_list:
                Listener.breaks_entry_list.append(break_)
            print("BREAKKK",Listener.breaks_entry_list)
            self.days__.clear()
            self.preference_lst__.clear()
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

            self.preference_lst__.append(self.space_status_var.get())
            self.preference_lst__.append(self.session_status_var.get())
            self.preference_lst__.append(self.tutor_status_var.get())

            Listener.preferenceList[2] = self.space_status_var.get()
            Listener.preferenceList[3] = self.session_status_var.get()
            Listener.preferenceList[4] = self.tutor_status_var.get()
            Listener.isOptionsUpdated = True
            Listener.timeTableNameListener = self.project_name__
            # print("Updated", Listener.preferenceList)

            self.timeTableMetaData__.set_timetable_information(
                True,
                self.project_name__,
                self.project_creator__,
                self.institute_name__,
                self.email__,
                self.days__,
                self.preference_lst__
            )

    def auto_save(self):
        count__ = 0
        while True:
            count__ = count__ + 1
            time.sleep(.5)
            if self.sat_status_var.get()[-1] == "_" and self.sun_status_var.get()[-1] == "_":
                Listener.isWeekendInclusive = True
            else:
                Listener.isWeekendInclusive = False

            if self.mon_status_var.get()[-1] == "_" and self.tue_status_var.get()[-1] == "_" and \
                    self.wed_status_var.get()[
                        -1] == "_" and self.thur_status_var.get()[-1] == "_" and self.fri_status_var.get()[
                -1] == "_" and \
                    self.sat_status_var.get()[-1] == "_" and self.sun_status_var.get()[-1] == "_":
                # messagebox.showerror(title="Timetable Metadata Error",
                #                      message="Days are not selected!,Please select a day.")
                Listener.isWeekendInclusive = False
                return
            elif self.project_creator_var.get() == "":
                # messagebox.showerror(title="Timetable Metadata Error",
                #                      message="Fields can't be left blank.")
                Listener.isWeekendInclusive = False
                return
            elif self.project_institute_var.get() == "":
                # messagebox.showerror(title="Timetable Metadata Error",
                #                      message="Fields can't be left blank.")
                Listener.isWeekendInclusive = False
                return
            elif self.project_name_var.get() == "":
                # messagebox.showerror(title="Timetable Metadata Error",
                #                      message="Fields can't be left blank.")
                Listener.isWeekendInclusive = False
                return
            elif self.space_status_var.get()[-1] == "_" or self.session_status_var.get()[-1] == "_" or \
                    self.tutor_status_var.get()[-1] == "_":
                # messagebox.showerror(title="Timetable Metadata Error",
                #                      message="Fields can't be left blank.")
                Listener.isWeekendInclusive = False
                return

            else:
                self.days__.clear()
                self.preference_lst__.clear()
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

                self.preference_lst__.append(self.space_status_var.get())
                self.preference_lst__.append(self.session_status_var.get())
                self.preference_lst__.append(self.tutor_status_var.get())

                Listener.preferenceList[2] = self.space_status_var.get()
                Listener.preferenceList[3] = self.session_status_var.get()
                Listener.preferenceList[4] = self.tutor_status_var.get()
                Listener.isOptionsUpdated = True
                Listener.timeTableNameListener = self.project_name__
                # print("Updated", Listener.preferenceList)

                self.timeTableMetaData__.set_timetable_information(
                    True,
                    self.project_name__,
                    self.project_creator__,
                    self.institute_name__,
                    self.email__,
                    self.days__,
                    self.preference_lst__
                )
                Listener.set_state_home(False)
            # print(f"Home while {count__}")

    def save_thread(self):
        Listener.set_state_home(False)
        # print("Threading started")
        new_thread = Thread(target=self.save_information, daemon=True,
                            )  # I can pass args = "any" for the target
        new_thread.start()

    def aut_save_thread(self):
        new_thread_ = Thread(target=self.auto_save, daemon=True,
                             )  # I can pass args = "any" for the target
        new_thread_.start()

    def update_thread(self):
        # print("Threading started")
        new_thread = Thread(target=self.updateUI, daemon=True,
                            )  # I can pass args = "any" for the target
        new_thread.start()

    def refresh_list_Home_timetable_metadata(self, dict_: dict) -> list:
        myList = ["MON", "TUE", "WED", "THUR", "FRI", "SAT", "SUN"]
        list_two = list()
        for _day in myList:
            isdayIn = False
            for index, day in enumerate(dict_["headers"]):
                if _day == day:
                    isdayIn = True
                    break
            if isdayIn == True:
                str_ = _day
                list_two.append(str_)
            else:
                str_ = _day + "_"
                list_two.append(str_)

        return list_two

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
