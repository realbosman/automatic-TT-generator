import os
import threading
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
import pyglet

import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from threading import Thread
from queue import Queue
from enum import Enum, auto
import pickle
from tkinter.filedialog import askdirectory
from tkinter import font as tkfont

from Algorithm.Algo import TtGenerator
from Algorithm.TimetableMetaData import TimetableMetaData
from GUI import Tutor
from GUI.GenerateTimeTable import GenerateTimeTable
from GUI.Groups_ import Groups_
from GUI.Home import Home
from GUI.Session import Session

from GUI.Space import Space

from GUI.Splash import Splash
from GUI.TimeSlots import TimeSlots
from GUI.Tutor import Tutor
from GUI.View import View

from GUI.variables_ import Global_variables
from Models.ClassRoomModel import SpaceManager
from Models.CourseUnitModel import SessionManager
from Models.Tutor_Model import TutorsManager
from Models.Listener import Listener
from Models.TimeDimension import TimeDimension

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
my_pink="#f7b2b2"
sidebar_color_ = "#d2cccc"
visualisation_frame_color_ = my_pink
TEXT_COLOR = '#eeeeee'
TEXT_COLOR_="black"
my_white="#f5f5f5"


PATH = Path(__file__).parent / 'assets'
PATH_ = Path(__file__).parent / 'forest-light.tcl'
PATH__ = Path(__file__).parent / 'forest-dark.tcl'
image_path = Path(__file__).parent / 'assets'/'brand2.png'
image_path_ = Path(__file__).parent / 'assets'/'mmk.png'


# ------------------------------- ROOT WINDOW ----------------------------------


class TkinterApp(tk.Tk):
    """
     The class creates a header and sidebar for the application. Also creates
    resources in the sidebar,
    """

    def __init__(self):
        tk.Tk.__init__(self)

        # Initialise the classes Here

        # Get the path to the Documents folder

        self.listener_ = Listener()
        self.isTimetabecreatedMainThread = False
        # print("Path to the Documents folder", self.listener_.get_app_path())
        self.space_ = SpaceManager()
        self.lectures_ = SessionManager()
        self.lecturers_ = TutorsManager()
        self.is_Option_Update = False
        self.current_frame = "Splash"  # Initially

        self.timeDimension = TimeDimension()
        self.timetableMetadata = TimetableMetaData(self.timeDimension)
        self.algorithm_ = TtGenerator(self.lectures_)
        self.isHomeSaved = True
        self.uname_var = tk.StringVar(master=self,value="")
        self.pass_var = tk.StringVar(master=self,value="")

        self.style = ttk.Style(self)
        self.call("source", PATH_)
        self.call("source", PATH__)
        self.style.theme_use("forest-light")
        self.title("Automatic Timetable Generator")
        # # self.overrideredirect(True)

        self.welcome()



        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        # self.geometry()
        self.resizable(True, True)
        self.config(background=selectionbar_color)
        self.icon = tk.PhotoImage(file=PATH / 'logo.png')
        self.iconphoto(True, self.icon)

        # self.render_GUI()

    def welcome(self):
        # Welcome
        frame_P = tk.Frame(self, background="#d2cccc")
        frame_P.pack(fill=tk.BOTH, expand=tk.YES)

        frame_top = tk.Frame(frame_P, height=150, bg="#d2cccc",background="#d2cccc")
        frame_top.pack(fill=tk.X, pady=(0, 0))

        # Load the image

        self.image = tk.PhotoImage(file=image_path, )

        # Create a label to display the image
        label = tk.Label(frame_top, image=self.image, background="#d2cccc", )
        label.pack()

        label_text = "UGANDA MARTYRS UNIVERSITY"

        # Create a Canvas widget
        canvas = tk.Canvas(frame_top, width=500, height=50, background="#d2cccc", bg="#d2cccc", highlightthickness=0,
                           bd=0)
        canvas.pack()
        # Create a style
        style = ttk.Style()

        # Configure the style to have a white background
        style.configure("White.TButton", background="#f7b2b2")

        # Specify the font
        # Specify the path to the Stonehenge.ttf file
        # font_path = PATH / "stonehen.ttf"
        # pyglet.font.add_file(font_path)

        # Load the font from the file
        # Create a font object using the specified font path

        font = ("Helvetica", 21, "bold")

        # Call the function to color the first letter red
        self.color_first_letter(canvas, font=font)

        # ttk.Label(frame_top, text="UGANDA MARTYRS UNIVERSITY",font=("Helvetica", 21, "bold")).pack()
        ttk.Label(frame_top, text="WELCOME TO THE AUTOMATIC TIMETABLE GENERATOR", font=("stonehen", 20, "bold"),
                  foreground='red', background="#d2cccc").pack(pady=10)

        frame = tk.Frame(frame_P, background=my_white, relief="raised", border=2, padx=10, pady=10,width=300)
        frame.pack(expand=tk.YES)




        self.auth_list = list()
        self.auth_list.append("Admin")
        self.auth_list.append("admin")
        self.auth_list.append("uname")
        self.auth_list.append("pass")
        # validate numeric entry
        ttk.Label(frame, text="Admin Username:", width=100, foreground='black', background=my_white).pack()


        # Create a style
        self.style = ttk.Style()

        # Configure the style to have a white background for the entry field
        self.style.configure("White.TEntry", insertbackground="white")

        username_entry = ttk.Entry(frame, validate="focus", style="White.TEntry", textvariable=self.uname_var,width=100)
        username_entry.pack(pady=10, expand=True)

        # validate alpha entry
        ttk.Label(frame, text="password:", width=100, foreground='black', background=my_white).pack()
        password_entry = ttk.Entry(frame, validate="focus", textvariable=self.pass_var,width=100)

        password_entry.pack(pady=10, expand=True)
        password_entry.configure(background="white")



        # validate alpha entry

        lbtn = tk.Button(frame, text="Login", bg="#f7b2b2", fg="white", width="20", command=self.loginn)
        lbtn.pack(pady=10, expand=True)

    def color_first_letter(self,canvas, text="UGANDA,MARTYRS,UNIVERSITY", font=None):
        x = 10  # Initial x position
        sep_=text.split(',', -1)
        # Create the white background rectangle
        canvas.create_rectangle(0, 0, 600, 80, fill="#d2cccc", outline="#d2cccc")
        canvas.create_text(x, 10, text=sep_[0][0], font=font, fill='red', anchor='nw')
        canvas.create_text(x + 20, 10, text=sep_[0][1:], font=font ,fill="black", anchor='nw')
        # Increase x position for the next word
        x +=130
        canvas.create_text(x, 10, text=sep_[1][0], font=font, fill='red', anchor='nw')
        canvas.create_text(x + 24, 10, text=sep_[1][1:], font=font,fill="black", anchor='nw')
        # Increase x position for the next word
        x += 145
        canvas.create_text(x, 10, text=sep_[2][0], font=font, fill='red', anchor='nw')
        canvas.create_text(x + 20, 10, text=sep_[2][1:], font=font, fill="black", anchor='nw')
        # Increase x position for the next word
        x += 120


    def loginn(self):
        print(self.uname_var.get())
        if self.uname_var.get()=="Admin" and self.pass_var.get()=="admin":
            for widget in self.winfo_children():
                widget.destroy()
            self.render_GUI()
        else:
            for widget in self.winfo_children():
                widget.destroy()
                self.style.theme_use("forest-dark")
            self.render_GUI()
            # messagebox.showwarning(title="Automatic Timetable Generator",message="Login failed ,please try again.")



    def render_GUI(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.queue_message = Queue()
        self.bind("<<CheckQueue_Main>>", self.Check_Queue)
        self.run_after_period_thread()

        # Creating Menubar
        menubar = tk.Menu(self)

        # Adding File Menu and commands
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file)
        file.add_command(label='New File', command=self.new_file_)
        file.add_command(label='Open...', command=self.open_recent_files)
        file.add_command(label='Save', command=self.on_save)
        file.add_command(label='Demo', command=self.demo)
        file.add_separator()
        file.add_command(label='Exit', command=self.on_closing)

        # Adding Home Menu
        menubar.add_command(label='Home',
                            command=lambda: self.show_frame(Home, "Time table Metadata", self.timetableMetadata,
                                                            self.timeDimension, self.listener_))
        menubar.add_command(label='Edit', command=lambda: print("Edit"))
        menubar.add_command(label='Help', command=lambda: print("Help"))

        self.config(menu=menubar)

        # fake title bar
        self.title_bar = tk.Frame(self, bg=my_pink, relief='sunken', padx=7)
        self.title_bar.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        # bind title bar
        self.project_name_var = tk.StringVar(value="Project Name")
        self.project_name = tk.Label(self.title_bar, anchor="center", text="Project Name", background=my_pink,foreground="black",
                                     textvariable=self.project_name_var,font=("Arial", 14,"bold"))
        self.project_name.pack(fill=tk.Y, expand=1)

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color, relief='raised', bd=1)
        self.header.config(
            highlightbackground=sidebar_color,
            highlightthickness=0.5
        )
        self.header.place(relx=0.2, rely=0.053, relwidth=.799, relheight=.05)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color, relief='raised', )
        self.sidebar.config(
            highlightbackground="#808080",
            highlightthickness=0.5
        )
        self.sidebar.place(relx=0, rely=0.053, relwidth=0.2, relheight=1)

        # UNIVERSITY LOGO AND NAME
        # self.brand_frame = tk.Frame(self.sidebar, bg=sidebar_color)
        # self.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        self.image_side = tk.PhotoImage(file=image_path_, )

        # Create a label to display the image
        label_side = tk.Label(self.sidebar, image=self.image_side, background="#d2cccc", )
        label_side.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        # SUBMENUS IN SIDE BAR(Add , view
        # , List MANAGEMENT)

        # # Add to Resources Submenu
        self.submenu_frame = tk.Frame(self.sidebar, bg="#d2cccc", relief='raised', bd=None)
        self.submenu_frame.place(relx=0, rely=0.15, relwidth=1, relheight=1)

        # TODO : Rectife this so that it can be handle the list items
        self.resource_submenu = SidebarSubMenu(self.submenu_frame,
                                          sub_menu_heading='Resources',
                                          sub_menu_options=Listener.preferenceList

                                          )
        self.resource_submenu.options["TimeSlots"].config(
            command=lambda: self.show_frame(TimeSlots, "Create TimeSlots", self.timeDimension, )

        )
        self.resource_submenu.options[Listener.preferenceList[2]].config(
            command=lambda: self.show_frame(Space, f"Create {Listener.preferenceList[2]}", self.space_, )
        )
        self.resource_submenu.options[Listener.preferenceList[4]].config(
            command=lambda: self.show_frame(Tutor, f"{Listener.preferenceList[4]}", self.lectures_, )
        )
        self.resource_submenu.options[Listener.preferenceList[3]].config(
            command=lambda: self.show_frame(Session, f"{Listener.preferenceList[3]}", self.lectures_, )
        )
        self.resource_submenu.options["Groups"].config(
            command=lambda: self.show_frame(Groups_, "Groups", self.lectures_, )
        )

        self.changeOnHover(self.resource_submenu.options["TimeSlots"], visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[2]], visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[3]],  visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[4]], visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options["Groups"],  visualisation_frame_color_, sidebar_color_)

        self.resource_submenu.place(relx=0, rely=0.025, relwidth=1, relheight=5)

        generator_time_table = SidebarSubMenu(self.submenu_frame,
                                              sub_menu_heading='TimeTable Operations',
                                              sub_menu_options=["Generate TimeTable",
                                                                "View TimeTable",
                                                                "Generate PDF",
                                                                ]

                                              )

        generator_time_table.options["Generate TimeTable"].config(
            command=lambda: self.start_time_table_generation_thread()  # self.start_time_table_generation()
        )
        generator_time_table.options["View TimeTable"].config(
            command=self.view_time_table
        )
        generator_time_table.options["Generate PDF"].config(
            command=lambda: self.gen_time_table()
        )

        self.changeOnHover(generator_time_table.options["Generate TimeTable"], visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(generator_time_table.options["View TimeTable"],  visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(generator_time_table.options["Generate PDF"],  visualisation_frame_color_, sidebar_color_)

        generator_time_table.place(relx=0, rely=0.4, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        self.container = tk.Frame(self, relief="sunken")

        self.container.place(relx=0.2, rely=0.105, relwidth=0.8, relheight=0.9)

        self.frames = {}

        self.show_frame(Splash, " ", self.timetableMetadata, self.timeDimension, self.listener_)

    ''''
    This function below calls the clases and passes in them these parameters cls is the model class created at the beginning of the initialisation
    '''

    def run_after_period(self):
        count = 1
        prev_project_name = self.timetableMetadata.time_table_name
        preferencelstMain = Listener.preferenceList
        # print("Before Updated", Listener.preferenceList)

        while True:
            count = count + 1
            self.isTimetabecreatedMainThread = Listener.isTimeTableCreated
            # print(count)
            # print("After Updated", Listener.preferenceList)

            if Listener.isOptionsUpdated == True:
                for widget in self.submenu_frame.winfo_children():
                    # print("running widget 1")
                    widget.destroy()
                ticket = Ticket(ticket_type=TicketPurpose.UPDATE_OPTIONS,
                                ticket_value=1)
                self.queue_message.put(ticket)
                self.event_generate("<<CheckQueue_Main>>", when="tail")

                # self.update_Options(3)

            if Listener.preferenceList[4] != preferencelstMain[4]:
                # print("CHANGED", Listener.preferenceList)
                preferencelstMain = Listener.preferenceList
                self.is_Option_Update = True
                for widget in self.submenu_frame.winfo_children():
                    # print("running widget 1")
                    widget.destroy()
                ticket = Ticket(ticket_type=TicketPurpose.UPDATE_OPTIONS,
                                ticket_value=1)
                self.queue_message.put(ticket)
                self.event_generate("<<CheckQueue_Main>>", when="tail")
                # self.update_Options(4)

            if self.timetableMetadata.time_table_name == prev_project_name:
                pass
            # print("The same")
            else:
                ticket = Ticket(ticket_type=TicketPurpose.UPDATE_PROGRESS_PROJECT_NAME,
                                ticket_value=self.timetableMetadata.time_table_name)
                prev_project_name = self.timetableMetadata.time_table_name
                self.queue_message.put(ticket)
                self.event_generate("<<CheckQueue_Main>>", when="tail")

            if count == 5:
                ticket = Ticket(ticket_type=TicketPurpose.REMOVE_SPLASH,
                                ticket_value="splash")

                self.queue_message.put(ticket)
                self.event_generate("<<CheckQueue_Main>>", when="tail")



            if Listener.get_state_home() == False:
                ticket = Ticket(ticket_type=TicketPurpose.UPDATE_PROGRESS_HOME,
                                ticket_value=1)
                self.queue_message.put(ticket)
                self.event_generate("<<CheckQueue_Main>>", when="tail")

            else:
                ticket = Ticket(ticket_type=TicketPurpose.UPDATE_PROGRESS_HOME,
                                ticket_value=0)
                self.queue_message.put(ticket)
                self.event_generate("<<CheckQueue_Main>>", when="tail")

            # print("StateHome",self.listener_.getStateHome())
            time.sleep(.6)
            # Make count 10
            if count > 1000:
                count = 10

    def run_after_period_thread(self):
        new_thread = Thread(target=self.run_after_period, daemon=True,
                            )  # I can pass args = "any"
        new_thread.start()

    def Check_Queue(self, e):
        """
       Read the queue
        """
        msg: Ticket
        msg = self.queue_message.get()
        if msg.ticket_type == TicketPurpose.UPDATE_PROGRESS_HOME:
            # print(msg.ticket_value)
            if msg.ticket_value == 1:
                self.isHomeSaved = True
            else:
                self.isHomeSaved = False
        if msg.ticket_type == TicketPurpose.UPDATE_PROGRESS_PROJECT_NAME:
            self.project_name_var.set(msg.ticket_value)

        if msg.ticket_type == TicketPurpose.REMOVE_SPLASH:
            if msg.ticket_value == "splash":
                self.new_file_()
                for page in self.container.winfo_children():
                    # print(type(Splash),"I want SPlASH", type(page))
                    page.destroy()
                    self.show_frame(Home, "Time table Metadata", self.timetableMetadata, self.timeDimension,
                                    self.listener_)
        if msg.ticket_type == TicketPurpose.UPDATE_OPTIONS:
            if msg.ticket_value == 1:
                self.update_Options()
                Listener.isOptionsUpdated = False
            # print("OPTIONS UPDATE", Listener.preferenceList)

    def view_time_table(self):
        self.listener__ = Listener()
        if self.isTimetabecreatedMainThread:
            # print("VIEWNAME __", Listener.timeTableNameListener)
            # print("VIEWNAME _", Listener.timeTableNameListener)
            # print("STATIC", TimeTableManager.get_time_table_name())
            if Listener.timeTableNameListener != "":
                self.show_frame(View, "Time table Metadata", self.timetableMetadata,
                                self.timeDimension, self.listener_)
            else:
                messagebox.showerror(title="Automatic Timetable Generator",
                                     message="No timetable information available")
        else:
            messagebox.showerror(title="Automatic Timetable Generator", message="No timetable information available")

    def gen_time_table(self):
        self.listener__ = Listener()
        if self.isTimetabecreatedMainThread:
            # print("VIEWNAME __", Listener.timeTableNameListener)
            # print("VIEWNAME _", Listener.timeTableNameListener)
            # print("STATIC", TimeTableManager.get_time_table_name())
            if Listener.timeTableNameListener != "":
                messagebox.showinfo(title="Automatic Timetable Generator",
                                     message=f'Path to the generated Timetable is: {Listener.get_app_path_docs()}\{Listener.timeTableNameListener}.pdf')
            else:
                messagebox.showerror(title="Automatic Timetable Generator",
                                     message="No timetable information available")
        else:
            messagebox.showerror(title="Automatic Timetable Generator", message="No timetable information available")

    # function to change properties of button on hover.
    def changeOnHover(self, view, colorOnHover, colorOnLeave):


        # adjusting backgroung of the widget
        # background on entering widget
        view.bind("<Enter>", func=lambda e: view.config(
            background=colorOnHover))

        # background color on leving widget
        view.bind("<Leave>", func=lambda e: view.config(
            background=colorOnLeave))

    def demo(self):

        with open(rf'./DumpFile.pickle',
                  "rb") as file:
            loaded_obj = pickle.load(file)

        Listener.saveInstanceDict = loaded_obj
        self.space_.save_instance_reload()
        self.lectures_.save_instance_reload()
        self.timetableMetadata.save_instance_reload()
        TutorsManager.save_instance_reload()
        Listener.save_instance_reload()
        self.timeDimension.save_instance_reload()
        self.isHomeSaved = True
        # self.lectures_.set_new_list()

        self.show_frame(Home, "Time table Metadata", self.timetableMetadata,
                        self.timeDimension, self.listener_)

    def open_recent_files(self):
        path = askdirectory(title="Please select Project", initialdir=Listener.get_app_path_files())
        # print(rf'{path}')
        # print(f'{path}')

        file_path = os.path.join(path, "DumpFile.pickle")

        with open(rf'{file_path}',
                  "rb") as file:
            loaded_obj = pickle.load(file)

        Listener.saveInstanceDict = loaded_obj
        self.space_.save_instance_reload()
        self.lectures_.save_instance_reload()
        self.timetableMetadata.save_instance_reload()
        TutorsManager.save_instance_reload()
        Listener.save_instance_reload()
        self.timeDimension.save_instance_reload()
        self.isHomeSaved = True
        self.show_frame(Home, "Time table Metadata", self.timetableMetadata,
                        self.timeDimension, self.listener_)

        # iterate through the files to restore the last state

    def new_file_(self):

        self.space_.new_file_()
        self.lectures_.new_file_()
        self.timetableMetadata.new_file_()
        TutorsManager.new_file_()
        Listener.new_file_()
        self.timeDimension.new_file_()
        # print("executed")

        self.isHomeSaved = True
        self.show_frame(Home, "Time table Metadata", self.timetableMetadata,
                        self.timeDimension, self.listener_)

    def on_save(self):

        # Specify the file path
        file_path = os.path.join(Listener.get_app_path_files(), f'{Listener.timeTableNameListener}')
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # TODO: SAVE ALL THE STATES
        file_path = os.path.join(file_path, "DumpFile.pickle")

        # save the instances in the LIstener dictionary
        self.space_.save_instance_()
        self.lectures_.save_instance_()
        self.timeDimension.save_instance_()
        TutorsManager.save_instance_()
        self.timetableMetadata.save_instance_()
        Listener.save_instance_()

        # Open the file in binary write mode
        with open(file_path, "wb") as file:
            # Serialize and save the object to the file
            pickle.dump(Listener.saveInstanceDict, file)
            # pass

        messagebox.showinfo(title="Automatic Timetable Generator", message="Saved successfully")

    def on_closing(self):
        isTrue = messagebox.askyesno(title="Automatic Timetable Generator", message="Do you want to save this project.")
        if isTrue:
            # Specify the file path
            file_path = os.path.join(Listener.get_app_path_files(), f'{Listener.timeTableNameListener}')
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            file_path = os.path.join(file_path, "DumpFile.pickle")

            # save the instances in the LIstener dictionary
            self.space_.save_instance_()
            self.lectures_.save_instance_()
            self.timeDimension.save_instance_()
            TutorsManager.save_instance_()
            self.timetableMetadata.save_instance_()
            Listener.save_instance_()

            # Open the file in binary write mode
            with open(file_path, "wb") as file:
                # Serialize and save the object to the file
                pickle.dump(Listener.saveInstanceDict, file)
                # pass

            messagebox.showinfo(title="Automatic Timetable Generator", message="Saved successfully")
            self.destroy()
        else:
            self.destroy()

    def start_time_table_generation(self):
        num_tracker = self.lectures_.get_largest_session_number_in_a_subgroup() + 1  # Add 1 to prevent overlapping
        num_tutor_tracker = self.lectures_.get_the_number_of_Tutor_sessions() + 1
        Listener.tutor_with_highest_session_ = num_tutor_tracker - 1
        Listener.group_with_highest_session_ = num_tracker - 1
        # Listener.get_time_slot_count=num_tracker-1
        length_time_slot = len(self.timeDimension.get_algo_reources())
        if length_time_slot < num_tracker:
            messagebox.showwarning(title="Automatic Timetable Generator",
                                   message=f"Please Timeslot resources are not enough, add aleast {num_tracker - length_time_slot} more")
            return
        if length_time_slot < num_tutor_tracker:
            messagebox.showwarning(title="Automatic Timetable Generator",
                                   message=f"Please Timeslot resources are not enough, add aleast {num_tutor_tracker - length_time_slot} more")
            return

        isTrue = ShowMsg().pop_msg()
        if isTrue:

            self.show_frame(GenerateTimeTable, "Generate Time Table", self.timeDimension, self.timetableMetadata,
                            self.space_,
                            self.lectures_, self.lecturers_, self.algorithm_, self.listener_)
        else:
            print(' Generation faild')

    def start_time_table_generation_thread(self):
        thread = Thread(target=self.start_time_table_generation, daemon=True)  # I can pass args = "any" for the target
        thread.start()

    def on_call_create(self, F, *cls):
        for w in self.container.winfo_children():
            w.destroy()

        frame = F(self.container, *cls)

        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def move_app(self, e):
        self.geometry(f'+{e.x_root - self.winfo_x()}+{e.y_root - self.winfo_y()}')

    def quiter(self, e):
        self.quit()

    def start_move(self, event):
        global lastx, lasty
        lastx = event.x_root
        lasty = event.y_root

    def move_window(self, event):
        global lastx, lasty
        deltax = event.x_root - lastx
        deltay = event.y_root - lasty
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))
        lastx = event.x_root
        lasty = event.y_root

    def toggle_mode(self):
        if self.mode_switch.instate(["selected"]):
            self.style.theme_use("forest-light")
        else:
            self.style.theme_use("forest-dark")

    def show_frame(self, cont, title, *cls):
        """
        The function 'show_frame' is used to raise a specific frame (page) in
        the tkinter application and update the title displayed in the header.

        Parameters:
        cont (str): The name of the frame/page to be displayed.
        title (str): The title to be displayed in the header of the application.

        Returns:
        None
        """
        if self.isHomeSaved == True:
            self.isHomeSaved == False
            pass
        else:
            isTrue = ShowMsg().pop_msg(title="Automatic Timetable Generator", qn="Do want to continue without saving?")

            if isTrue == True:
                self.isHomeSaved = True
                Listener.set_state_home(False)
                messagebox.showwarning(title="Automatic Timetable Generator",
                                       message="This might lead to Timetable generation problems!")
                pass
            else:
                return



        if self.current_frame == "Session'>":
            if self.lectures_.check_for_empty_slots():
                messagebox.showerror(title="Automatic Timetable Generator",
                                     message="Some fields are empty, Please fill them or delete the row.")
                return

        # frame = self.frames[cont]
        for widget in self.header.winfo_children():
            # print("running widget 1")
            widget.destroy()

        for page in self.container.winfo_children():
            # print("running widget 2",page)
            page.destroy()
        label = tk.Label(self.header,
                         text=title,
                         font=("Helvetica", 13),
                         bg=header_color,
                         fg=TEXT_COLOR)

        self.on_call_create(cont, *cls)
        # print("Current FRAME ==", cont)
        print(str(cont).split(".", -1)[-1])
        # print("Splash'>")
        label.pack(side=tk.LEFT, padx=0, fill='both')
        self.current_frame = str(cont).split(".", -1)[-1]
        # frame.tkraise()



        if   str(cont).split(".", -1)[-1] == "Splash'>" :
            pass
        elif str(cont).split(".", -1)[-1] == "Home'>":


            try:
                print("Yeeees")
                self.resource_submenu.options[Listener.preferenceList[0]].config(background=sidebar_color_)
                self.resource_submenu.options[Listener.preferenceList[2]].config(background=sidebar_color_)
                self.resource_submenu.options[Listener.preferenceList[3]].config(background=sidebar_color_)
                self.resource_submenu.options[Listener.preferenceList[4]].config(background=sidebar_color_)
                self.resource_submenu.options["Groups"].config(background=sidebar_color_)
            except:
                pass

        else:
            try:
                if str(cont).split(".", -1)[-1] == "Tutor'>":
                    self.resource_submenu.options[Listener.preferenceList[4]].unbind("<Enter>")
                    self.resource_submenu.options[Listener.preferenceList[4]].unbind("<Leave>")
                    self.resource_submenu.options[Listener.preferenceList[4]].configure(
                        activebackground=visualisation_frame_color, )

                else:
                    self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[4]],
                                       visualisation_frame_color_, sidebar_color_)
                    self.resource_submenu.options[Listener.preferenceList[4]].config(background=sidebar_color_, )

                if str(cont).split(".", -1)[-1] == "Session'>":
                    self.resource_submenu.options[Listener.preferenceList[3]].unbind("<Enter>")
                    self.resource_submenu.options[Listener.preferenceList[3]].unbind("<Leave>")
                    self.resource_submenu.options[Listener.preferenceList[3]].config(
                        activebackground=visualisation_frame_color)
                else:
                    self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[3]],
                                       visualisation_frame_color_, sidebar_color_)
                    self.resource_submenu.options[Listener.preferenceList[3]].config(background=sidebar_color_)

                if str(cont).split(".", -1)[-1] == "Space'>":
                    self.resource_submenu.options[Listener.preferenceList[2]].unbind("<Enter>")
                    self.resource_submenu.options[Listener.preferenceList[2]].unbind("<Leave>")
                    self.resource_submenu.options[Listener.preferenceList[2]].config(
                        activebackground=visualisation_frame_color)
                else:
                    self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[2]],
                                       visualisation_frame_color_, sidebar_color_)
                    self.resource_submenu.options[Listener.preferenceList[2]].config(background=sidebar_color_)

                if str(cont).split(".", -1)[-1] == "Groups_'>":
                    self.resource_submenu.options["Groups"].unbind("<Enter>")
                    self.resource_submenu.options["Groups"].unbind("<Leave>")
                    self.resource_submenu.options["Groups"].config(activebackground=visualisation_frame_color)
                else:
                    self.changeOnHover(self.resource_submenu.options["Groups"],
                                       visualisation_frame_color_, sidebar_color_)
                    self.resource_submenu.options["Groups"].config(background=sidebar_color_)

                if str(cont).split(".", -1)[-1] == "TimeSlots'>":
                    self.resource_submenu.options[Listener.preferenceList[0]].unbind("<Enter>")
                    self.resource_submenu.options[Listener.preferenceList[0]].unbind("<Leave>")
                    self.resource_submenu.options[Listener.preferenceList[0]].config(
                        activebackground=visualisation_frame_color)
                else:
                    self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[0]],
                                       visualisation_frame_color_, sidebar_color_)
                    self.resource_submenu.options[Listener.preferenceList[0]].config(background=sidebar_color_)


            except:
                print("Render error bg options")


    def update_Options(self):
        # TODO : Rectife this so that it can be handle the list items
        self.resource_submenu = SidebarSubMenu(self.submenu_frame,
                                          sub_menu_heading='Resources',
                                          sub_menu_options=Listener.preferenceList

                                          )
        self.resource_submenu.options["TimeSlots"].config(
            command=lambda: self.show_frame(TimeSlots, "Create TimeSlots", self.timeDimension, )

        )
        self.resource_submenu.options[Listener.preferenceList[2]].config(
            command=lambda: self.show_frame(Space, f"Create {Listener.preferenceList[2]}", self.space_, )
        )
        self.resource_submenu.options[Listener.preferenceList[4]].config(
            command=lambda: self.show_frame(Tutor, f"{Listener.preferenceList[4]}", self.lectures_, )
        )
        self.resource_submenu.options[Listener.preferenceList[3]].config(
            command=lambda: self.show_frame(Session, f"{Listener.preferenceList[3]}", self.lectures_, )
        )
        self.resource_submenu.options["Groups"].config(
            command=lambda: self.show_frame(Groups_, "Groups", self.lectures_, )
        )

        self.changeOnHover(self.resource_submenu.options["TimeSlots"],  visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[2]],  visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[3]], visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options[Listener.preferenceList[4]], visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(self.resource_submenu.options["Groups"],  visualisation_frame_color_, sidebar_color_)

        self.resource_submenu.place(relx=0, rely=0.025, relwidth=1, relheight=5)

        generator_time_table = SidebarSubMenu(self.submenu_frame,
                                              sub_menu_heading='TimeTable Operations',
                                              sub_menu_options=["Generate TimeTable",
                                                                "View TimeTable",
                                                                "Generate PDF",
                                                                ]

                                              )

        generator_time_table.options["Generate TimeTable"].config(
            command=lambda: self.start_time_table_generation_thread()  # self.start_time_table_generation()
        )
        generator_time_table.options["View TimeTable"].config(
            command=self.view_time_table
        )
        generator_time_table.options["Generate PDF"].config(
            command=lambda: self.gen_time_table()
        )

        self.changeOnHover(generator_time_table.options["Generate TimeTable"], visualisation_frame_color_,
                           sidebar_color_)
        self.changeOnHover(generator_time_table.options["View TimeTable"], visualisation_frame_color_, sidebar_color_)
        self.changeOnHover(generator_time_table.options["Generate PDF"], visualisation_frame_color_, sidebar_color_)

        generator_time_table.place(relx=0, rely=0.4, relwidth=1, relheight=0.3)


# ------------------------ MULTIPAGE FRAMES ------------------------------------


# ----------------------------- CUSTOM WIDGETS ---------------------------------


class MultiselectDropdown(tk.Frame):
    """
    Creates a multi-select dropdown menu.

    Attributes:
    -parent(Frame): The parent frame in which the dropdown menu will be created.
    -text(str): The text that will be displayed on the dropdown button.
    -items_list(list): A list of items that will be displayed in the dropdown menu.
    """

    def __init__(self, parent, text, items_list):
        tk.Frame.__init__(self, parent)
        self.text = text
        self.items_list = items_list
        self.menubutton = tk.Menubutton(self, text=self.text + " 🡫",
                                        bg="white"
                                        )
        self.menu = tk.Menu(self.menubutton, tearoff=False, bg="white")
        self.menubutton.configure(menu=self.menu)
        self.menubutton.config(bg=selectionbar_color)
        self.menubutton.pack()
        self.choices = {}

        self.create_dropdown()

    def create_dropdown(self):
        """
        Creates the checkbuttons for each item in the items_list and adds it to
        the menu widget.
        """
        for choice in self.items_list:
            self.choices[choice] = tk.IntVar(value=1)
            self.menu.add_checkbutton(label=choice,
                                      variable=self.choices[choice],
                                      onvalue=1, offvalue=0
                                      )

    def get_selected_items(self):
        """
        Returns a list of items that are selected by the user from the dropdown
        menu.
        """
        selected_items = []
        for name, var in self.choices.items():
            if var.get() == 1:
                selected_items.append(name)
        return selected_items

    def deselect_all(self):
        """
        Deselects all the items in dropdown .
        """
        for name, var in self.choices.items():
            var.set(0)


class CustomCombobox(tk.Frame):
    """
    A custom tkinter combobox widget that allows for multiple selections.
    """

    def __init__(self, parent, items_list=[], display_text="default"):
        tk.Frame.__init__(self, parent)
        self.display_text = display_text
        self.cb_var = tk.StringVar(value=display_text)
        self.items_list = items_list
        self.combobox = ttk.Combobox(self, textvariable=self.cb_var,
                                     values=items_list
                                     )
        self.combobox.pack(side=tk.LEFT)
        self.selected_items = {}
        self.postselection_command = None

    def get(self):
        """
        Returns the current selection of the combobox.
        """
        return self.cb_var.get()

    def update_list(self, updated_list):
        """
        updates the items_list of combobox.
        """
        self.combobox.config(values=updated_list)

    def add_command(self, command):
        """
        adds a command function that will be called after an item is selected.
        """
        self.combobox.config(postcommand=command)

    def enbl_mltpl_sel(self):
        """
        enables multiple selections in the combobox.
        """
        self.combobox.bind("<<ComboboxSelected>>", self.add_selection)

    def add_selection(self, event):
        """
        This function is called when an item is selected from the combobox.
        It checks if the selected item is not the default display text and if
        the item is not already present in the selected items list. If the item
        is not present in the list, it creates a dictionary object for the
        selected item with a label and a button. The label displays the selected
        item and the button is used to remove the selection.
        """
        selected_item = self.cb_var.get()
        if not selected_item == self.display_text:
            if selected_item not in list(self.selected_items.keys()):
                self.selected_items[selected_item] = {
                    "label": tk.Label(self, text=selected_item),
                    "Button": tk.Button(self, text=" X", bg=selectionbar_color,
                                        bd=0, foreground='red', cursor='hand2',
                                        command=lambda: self.remove_selection(
                                            id=selected_item
                                        )
                                        )
                }
                self.update_selection(self.selected_items[selected_item])
                self.post_selection_command()

    def update_selection(self, dict):
        """
        Update the UI with the selected item
        """
        dict["label"].pack(side=tk.LEFT)
        dict["Button"].pack(side=tk.LEFT)

    def remove_selection(self, id):
        """
        Remove a selected item from the selected_items dictionary and update
        the UI.
        """
        self.selected_items[id]["label"].pack_forget()
        self.selected_items[id]["Button"].pack_forget()
        del self.selected_items[id]
        self.post_selection_command()

    def post_selection_command(self):
        """
        Execute the command added after an item is selected.
        """
        if self.postselection_command:
            self.postselection_command
        else:
            pass


class SidebarSubMenu(tk.Frame):
    """
    A submenu which can have multiple options and these can be linked with
    functions.
    """

    def __init__(self, parent, sub_menu_heading, sub_menu_options):
        """
        parent: The frame where submenu is to be placed
        sub_menu_heading: Heading for the options provided
        sub_menu_operations: Options to be included in sub_menu
        """
        tk.Frame.__init__(self, parent)
        self.config(bg="#d2cccc")
        self.sub_menu_heading_label = ttk.Label(self,
                                               text=sub_menu_heading,
                                                padding=5
                                                ,background="#d2cccc",
                                                foreground="black"
                                               ,
                                               font=("Arial", 14,"bold")
                                               ,justify="left"
                                               )
        self.sub_menu_heading_label.place(x=0, y=10, relwidth=1,anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=0, y=30, relwidth=1, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(self,
                                        text=x,
                                        bg="#d2cccc",
                                        font=("Arial", 11),
                                        bd=0,
                                        anchor="w",  # Align text to the left horizontally
                                        height="1"
                                        ,justify="left",
                                        # cursor='hand2',

                                        fg=TEXT_COLOR_
                                        )
            self.options[x].place(x=0, y=46 * (n + 1), relwidth=1,anchor="w" ) # Align text to the left horizontally

    def on_button_click(self, btn_clicked):
        print(self.options)
        for  button in self.options.keys():

            if button == btn_clicked:
                self.options[button].config(bg=visualisation_frame_color)
                print(button, btn_clicked)
                print("OBJ", self.options[button])
            else:
                self.options[button].config(bg=sidebar_color)




class ShowMsg:

    def pop_msg(self, title="Automatic Timetable Generator", qn="Do you want to generate new  time table ?") -> bool:
        """
       Msg show
        """
        respo = messagebox.askyesno(
            title,
            qn

        )

        if (respo == True):
            print("Generating.......")


        else:
            print("Generating failed")

        # messagebox.showinfo(title=None, message="Generated")
        return respo


# Ticketing system call
class TicketPurpose(Enum):
    UPDATE_PROGRESS_TEXT = auto()
    UPDATE_PROGRESS_HOME: int = auto()
    UPDATE_PROGRESS_HEADING = auto()
    UPDATE_PROGRESS_PROJECT_NAME: str = auto()
    REMOVE_SPLASH: str = auto()
    UPDATE_OPTIONS: int = auto()


class Ticket:
    def __init__(self, ticket_type: TicketPurpose,
                 ticket_value):
        self.ticket_type = ticket_type
        self.ticket_value = ticket_value


# splash_=Splash()



if __name__ == '__main__':
    app = TkinterApp()

    # splash_.after(3000,app)
    app.mainloop()

