import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
from GUI import TimeslotsList
from GUI.Session import Session
from GUI.SessionsList import SessionsList
from GUI.Space import Space
from GUI.SpaceList import SpaceList
from GUI.TimeSlots import TimeSlots
from GUI.TimeslotsList import TimeslotsList
from GUI.Tutor import Tutor
from GUI.TutorsList import TutorsList
from Models.ClassRoomModel import ClassRooms
from Models.TimeDimension import TimeDimension

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#eeeeee'


PATH = Path(__file__).parent / 'images'
PATH_ = Path(__file__).parent / 'forest-light.tcl'
PATH__ = Path(__file__).parent / 'forest-dark.tcl'

# ------------------------------- ROOT WINDOW ----------------------------------


class Lectures:
    pass


class Courses:
    pass


class TkinterApp(tk.Tk):
    """
     The class creates a header and sidebar for the application. Also creates
    resources in the sidebar,
    """

    def __init__(self):
        tk.Tk.__init__(self)

        # Initialise the classes Here
        self.timeDimension=TimeDimension()
        self.timeDimension_space = TimeDimension()
        self.space_=ClassRooms()
        self.lectures_=Lectures()
        self.courses___=Courses()




        self.style = ttk.Style(self)
        self.call("source",PATH_)
        self.call("source", PATH__)
        self.style.theme_use("forest-dark")
        self.title("Automatic Timetable Generator")
        # # self.overrideredirect(True)

        # ------------- BASIC APP LAYOUT -----------------

        self.geometry("1100x700")
        # self.geometry()
        self.resizable(True, True)
        self.config(background=selectionbar_color)
        icon = tk.PhotoImage(file=PATH /'LU_logo.png')
        self.iconphoto(True, icon)

        # fake title bar
        self.title_bar = tk.Frame(self, bg=header_color, relief='sunken', padx=7)
        self.title_bar.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        # bind title bar
        self.title_bar.bind("<ButtonPress>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.move_window)

        self.title_label = tk.Label(self.title_bar, text='Automatic Timetable Generator', bg=header_color,
                                    fg=TEXT_COLOR)
        # self.title_label.place(relx=0, rely=0, relwidth=.16, relheight=1)
        # self.title_label.pack(side=tk.LEFT, fill=tk.Y)
        #
        # self.closeApp = tk.Label(self.title_bar, text='X', padx=8, bg=header_color, fg='red', font='bold',
        #                          relief='raised')
        #
        # self.closeApp.pack(side=tk.RIGHT, fill=tk.Y)
        # self.closeApp.bind('<Button-1>', self.quiter)

        # self.mode_switch = ttk.Checkbutton(
        #     self.title_bar, text="Mode", style="Switch", command=self.toggle_mode)
        # self.mode_switch.pack(side=tk.RIGHT, fill=tk.Y,padx=5)


        # self.gripper=ttk.Sizegrip()
        # self.gripper.place(relx=1,rely=1,anchor='se')
        # self.gripper.lift()

        # ---------------- HEADER ------------------------

        self.header = tk.Frame(self, bg=header_color, relief='raised', bd=1)
        self.header.config(
            highlightbackground=sidebar_color,
            highlightthickness=0.5
        )
        self.header.place(relx=0.2, rely=0.053, relwidth=.799, relheight=.05)

        # ---------------- SIDEBAR -----------------------
        # CREATING FRAME FOR SIDEBAR
        self.sidebar = tk.Frame(self, bg=sidebar_color, relief='raised')
        self.sidebar.config(
            highlightbackground="#808080",
            highlightthickness=0.5
        )
        self.sidebar.place(relx=0, rely=0.053, relwidth=0.2, relheight=1)

        # SUBMENUS IN SIDE BAR(Add , view
        # , List MANAGEMENT)

        # # Add to Resources Submenu
        self.submenu_frame = tk.Frame(self.sidebar, bg=sidebar_color, relief='raised')
        self.submenu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        resource_submenu = SidebarSubMenu(self.submenu_frame,
                                          sub_menu_heading='Add Resources',
                                          sub_menu_options=["TimeSlots",
                                                            "Classroom/Room/Space",
                                                            "Instructor/Lecturer/Tutor",
                                                            "Course/Class/Session"
                                                            ]
                                          )
        resource_submenu.options["TimeSlots"].config(
            command=lambda: self.show_frame(TimeSlots, "Create TimeSlots",cls=self.timeDimension)
        )
        resource_submenu.options["Classroom/Room/Space"].config(
            command=lambda: self.show_frame(Space, "Create Classroom/Room/Space",cls=self.timeDimension_space)
        )
        resource_submenu.options["Instructor/Lecturer/Tutor"].config(
            command=lambda: self.show_frame(Tutor, "Instructor/Lecturer/Tutor",cls=self.lectures_)
        )
        resource_submenu.options["Course/Class/Session"].config(
            command=lambda: self.show_frame(Session, "Course/Class/Session",cls=self.courses___)
        )

        resource_submenu.place(relx=0, rely=0.025, relwidth=1, relheight=0.3)

        list_submenu = SidebarSubMenu(self.submenu_frame,
                                      sub_menu_heading='View/Edit Resource Lists',
                                      sub_menu_options=["Timeslots",
                                                        "Classrooms/Rooms/Space",
                                                        "Instructors/Lecturers/Tutors",
                                                        "Courses/Classes/Sessions"
                                                        ]
                                      )
        list_submenu.options["Timeslots"].config(
            command=lambda: self.show_frame(TimeslotsList, "TimeSlots",cls=self.timeDimension)
        )
        list_submenu.options["Classrooms/Rooms/Space"].config(
            command=lambda: self.show_frame(SpaceList, "Classrooms/Rooms/Spaces - List",cls=self.timeDimension)
        )
        list_submenu.options["Instructors/Lecturers/Tutors"].config(
            command=lambda: self.show_frame(TutorsList, "Instructors/Lecturers/Tutors - List",cls=self.lectures_)
        )
        list_submenu.options["Courses/Classes/Sessions"].config(
            command=lambda: self.show_frame(SessionsList, "Courses/Classes/Sessions - List",cls=self.courses___)
        )

        list_submenu.place(relx=0, rely=0.4, relwidth=1, relheight=0.3)

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        self.container = ttk.Frame(self, relief="sunken")
        # self.container.config(highlightbackground=visualisation_frame_color, highlightthickness=0.5)
        self.container.place(relx=0.2, rely=0.105, relwidth=0.8, relheight=0.9)

        self.frames = {}


    ''''
    This function below calls the clases and passes in them these parameters cls is the model class created at the beginning of the initialisation
    '''

    def on_call_create(self,F,cls):
        frame = F(self.container,cls)

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

    def show_frame(self, cont, title,cls):
        """
        The function 'show_frame' is used to raise a specific frame (page) in
        the tkinter application and update the title displayed in the header.

        Parameters:
        cont (str): The name of the frame/page to be displayed.
        title (str): The title to be displayed in the header of the application.

        Returns:
        None
        """

        # frame = self.frames[cont]
        for widget in self.header.winfo_children():
            print("running widget 1")
            widget.destroy()
        for page in self.container.winfo_children():
            print("running widget 2")
            page.destroy()
        label = tk.Label(self.header,
                         text=title,
                         font=("Helvetica", 13),
                         bg=header_color,
                         fg=TEXT_COLOR)
        self.on_call_create(cont,cls=cls)
        label.pack(side=tk.LEFT, padx=0, fill='both')
        # frame.tkraise()


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


app = TkinterApp()
app.mainloop()
