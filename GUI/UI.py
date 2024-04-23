import os
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from threading import Thread
from queue import Queue
from enum import Enum, auto
import pickle
from tkinter.filedialog import askdirectory

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
TEXT_COLOR = '#eeeeee'

PATH = Path(__file__).parent / 'images'
PATH_ = Path(__file__).parent / 'forest-light.tcl'
PATH__ = Path(__file__).parent / 'forest-dark.tcl'


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


        self.style = ttk.Style(self)
        self.call("source", PATH_)
        self.call("source", PATH__)
        self.style.theme_use("forest-dark")
        self.title("Automatic Timetable Generator")
        # # self.overrideredirect(True)

        self.queue_message = Queue()
        self.bind("<<CheckQueue_Main>>", self.Check_Queue)
        self.run_after_period_thread()

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        # self.geometry()
        self.resizable(True, True)
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file=PATH / 'LU_logo.png')
        self.iconphoto(True, icon)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        self.title_bar = tk.Frame(self, bg=header_color, relief='sunken', padx=7)
        self.title_bar.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        # bind title bar
        self.project_name_var = tk.StringVar(value="Project Name")
        self.project_name = tk.Label(self.title_bar, anchor="center", text="Project Name", background=header_color,
                                     textvariable=self.project_name_var)
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

        # SUBMENUS IN SIDE BAR(Add , view
        # , List MANAGEMENT)

        # # Add to Resources Submenu
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color, relief='raised', bd=None)
        self.submenu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # TODO : Rectife this so that it can be handle the list items
        resource_submenu = SidebarSubMenu(self.submenu_frame,
                                          sub_menu_heading='Resources',
                                          sub_menu_options=Listener.preferenceList

                                          )
        resource_submenu.options["TimeSlots"].config(
            command=lambda: self.show_frame(TimeSlots, "Create TimeSlots", self.timeDimension, )

        )
        resource_submenu.options[Listener.preferenceList[2]].config(
            command=lambda: self.show_frame(Space, f"Create {Listener.preferenceList[2]}", self.space_, )
        )
        resource_submenu.options[Listener.preferenceList[4]].config(
            command=lambda: self.show_frame(Tutor, f"{Listener.preferenceList[4]}", self.lectures_, )
        )
        resource_submenu.options[Listener.preferenceList[3]].config(
            command=lambda: self.show_frame(Session, f"{Listener.preferenceList[3]}", self.lectures_, )
        )
        resource_submenu.options["Groups"].config(
            command=lambda: self.show_frame(Groups_, "Groups", self.lectures_, )
        )

        self.changeOnHover(resource_submenu.options["TimeSlots"], visualisation_frame_color, sidebar_color)
        self.changeOnHover(resource_submenu.options[Listener.preferenceList[2]], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(resource_submenu.options[Listener.preferenceList[3]], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(resource_submenu.options[Listener.preferenceList[4]], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(resource_submenu.options["Groups"], visualisation_frame_color, sidebar_color)

        resource_submenu.place(relx=0, rely=0.025, relwidth=1, relheight=5)

        generator_time_table = SidebarSubMenu(self.submenu_frame,
                                              sub_menu_heading='Time Table',
                                              sub_menu_options=["Generate Time Table",
                                                                "View TimeTable",
                                                                "Generate PDF",
                                                                ]

                                              )

        generator_time_table.options["Generate Time Table"].config(
            command=lambda: self.start_time_table_generation_thread()  # self.start_time_table_generation()
        )
        generator_time_table.options["View TimeTable"].config(
            command=self.view_time_table
        )
        generator_time_table.options["Generate PDF"].config(
            command=lambda: print("Generate PDF")
        )

        self.changeOnHover(generator_time_table.options["Generate Time Table"], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(generator_time_table.options["View TimeTable"], visualisation_frame_color, sidebar_color)
        self.changeOnHover(generator_time_table.options["Generate PDF"], visualisation_frame_color, sidebar_color)

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
            print("OPTIONS UPDATE", Listener.preferenceList)

    def view_time_table(self):
        self.listener__ = Listener()
        if self.isTimetabecreatedMainThread:
            print("VIEWNAME __", Listener.timeTableNameListener)
            print("VIEWNAME _", Listener.timeTableNameListener)
            # print("STATIC", TimeTableManager.get_time_table_name())
            if Listener.timeTableNameListener != "":
                self.show_frame(View, "Time table Metadata", self.timetableMetadata,
                                self.timeDimension, self.listener_)
            else:
                messagebox.showerror(title="Automatic Timetable Generator",
                                     message="No timetable information available")
        else:
            messagebox.showerror(title="Automatic Timetable Generator", message="No timetable information available")

    # function to change properties of button on hover
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

        self.show_frame(Home, "Time table Metadata", self.timetableMetadata,
                        self.timeDimension, self.listener_)

    def open_recent_files(self):
        path = askdirectory(title="Please select Project", initialdir=Listener.get_app_path_files())
        print(rf'{path}')
        print(f'{path}')

        file_path = os.path.join(path, "DumpFile.pickle")

        with open(rf'{file_path}',
                  "rb") as file:
            loaded_obj = pickle.load(file)

        Listener.saveInstanceDict=loaded_obj
        self.space_.save_instance_reload()
        self.lectures_.save_instance_reload()
        self.timetableMetadata.save_instance_reload()
        TutorsManager.save_instance_reload()
        Listener.save_instance_reload()
        self.timeDimension.save_instance_reload()
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
        print("executed")

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
        if len(self.timeDimension.get_algo_reources()) < num_tracker:
            messagebox.showwarning(title="Automatic Timetable Generator",
                                   message=f"Please Timeslot resources are not enough, add aleast {num_tracker - len(self.timeDimension.get_algo_reources())} more")
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
                messagebox.showwarning(title="Automatic Timetable Generator", message="This might lead to Timetable generation problems!")
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
        print("Current FRAME ==", cont)
        print(str(cont).split(".", -1)[-1])
        print("Splash'>")
        label.pack(side=tk.LEFT, padx=0, fill='both')
        self.current_frame = str(cont).split(".", -1)[-1]
        # frame.tkraise()

    def update_Options(self):
        # TODO : Rectife this so that it can be handle the list items
        resource_submenu = SidebarSubMenu(self.submenu_frame,
                                          sub_menu_heading='Resources',
                                          sub_menu_options=Listener.preferenceList

                                          )
        resource_submenu.options["TimeSlots"].config(
            command=lambda: self.show_frame(TimeSlots, "Create TimeSlots", self.timeDimension, )

        )
        resource_submenu.options[Listener.preferenceList[2]].config(
            command=lambda: self.show_frame(Space, f"Create {Listener.preferenceList[2]}", self.space_, )
        )
        resource_submenu.options[Listener.preferenceList[4]].config(
            command=lambda: self.show_frame(Tutor, f"{Listener.preferenceList[4]}", self.lectures_, )
        )
        resource_submenu.options[Listener.preferenceList[3]].config(
            command=lambda: self.show_frame(Session, f"{Listener.preferenceList[3]}", self.lectures_, )
        )
        resource_submenu.options["Groups"].config(
            command=lambda: self.show_frame(Groups_, "Groups", self.lectures_, )
        )

        self.changeOnHover(resource_submenu.options["TimeSlots"], visualisation_frame_color, sidebar_color)
        self.changeOnHover(resource_submenu.options[Listener.preferenceList[2]], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(resource_submenu.options[Listener.preferenceList[3]], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(resource_submenu.options[Listener.preferenceList[4]], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(resource_submenu.options["Groups"], visualisation_frame_color, sidebar_color)

        resource_submenu.place(relx=0, rely=0.025, relwidth=1, relheight=5)

        generator_time_table = SidebarSubMenu(self.submenu_frame,
                                              sub_menu_heading='Time Table',
                                              sub_menu_options=["Generate Time Table",
                                                                "View TimeTable",
                                                                "Generate PDF",
                                                                ]

                                              )

        generator_time_table.options["Generate Time Table"].config(
            command=lambda: self.start_time_table_generation_thread()  # self.start_time_table_generation()
        )
        generator_time_table.options["View TimeTable"].config(
            command=self.view_time_table
        )
        generator_time_table.options["Generate PDF"].config(
            command=lambda: print("Generate PDF")
        )

        self.changeOnHover(generator_time_table.options["Generate Time Table"], visualisation_frame_color,
                           sidebar_color)
        self.changeOnHover(generator_time_table.options["View TimeTable"], visualisation_frame_color, sidebar_color)
        self.changeOnHover(generator_time_table.options["Generate PDF"], visualisation_frame_color, sidebar_color)

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
        self.config(bg=sidebar_color)
        self.sub_menu_heading_label = tk.Label(self,
                                               text=sub_menu_heading,
                                               bg=sidebar_color,
                                               fg=TEXT_COLOR
                                               ,
                                               font=("Arial", 10)
                                               )
        self.sub_menu_heading_label.place(x=30, y=10, anchor="w")

        sub_menu_sep = ttk.Separator(self, orient='horizontal')
        sub_menu_sep.place(x=30, y=30, relwidth=0.8, anchor="w")

        self.options = {}
        for n, x in enumerate(sub_menu_options):
            self.options[x] = tk.Button(self,
                                        text=x,
                                        bg=sidebar_color,
                                        font=("Arial", 9, "bold"),
                                        bd=0,
                                        cursor='hand2',
                                        activebackground='#ffffff',
                                        fg=TEXT_COLOR
                                        )
            self.options[x].place(x=30, y=45 * (n + 1), anchor="w")


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
            print("xxxxxxxxxx")

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

app = TkinterApp()

# splash_.after(3000,app)
app.mainloop()
