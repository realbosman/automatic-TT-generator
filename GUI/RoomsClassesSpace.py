import time
import tkinter as tk
from tkinter import ttk
import openpyxl

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class RoomsClassesSpace(tk.Frame):
    """
    The RoomsClassesSpace class provides a way to view and edit the space.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # TODO change color
        self.config(bg=visualisation_frame_color,)
        self.style = ttk.Style(self)
        self.tk.call("source", "forest-light.tcl")
        self.tk.call("source", "forest-dark.tcl")
        self.style.theme_use("forest-dark")

        # TODO: call all the  methods here to show up when th ui is created

        self.combo_list = ["Subscribed", "Not Subscribed", "Other"]



        self.widgets_frame = ttk.LabelFrame(self, text="Insert Row")
        # self.widgets_frame.pack(expand=0, side=tk.LEFT, padx=20, pady=10 ,anchor=tk.CENTER)
        self.widgets_frame.place(relx=.02, rely=.05, relwidth=.245, relheight=.5)

        self.name_entry = ttk.Entry(self.widgets_frame)
        self.name_entry.insert(0, "Name")
        self.name_entry.bind("<FocusIn>", lambda e: self.name_entry.delete('0', 'end'))
        self.name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

        self.age_spinbox = ttk.Spinbox(self.widgets_frame, from_=18, to=100)
        self.age_spinbox.insert(0, "Age")
        self.age_spinbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.status_combobox = ttk.Combobox(self.widgets_frame, values=self.combo_list)
        self.status_combobox.current(0)
        self.status_combobox.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.a = tk.BooleanVar()
        self.checkbutton = ttk.Checkbutton(self.widgets_frame, text="Employed", variable=self.a)
        self.checkbutton.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        self.button = ttk.Button(self.widgets_frame, text="Insert", command=self.insert_row)
        self.button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        self.separator = ttk.Separator(self.widgets_frame)
        self.separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")

        self.mode_switch = ttk.Checkbutton(
            self.widgets_frame, text="Mode", style="Switch", command=self.toggle_mode)
        self.mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

        self.treeFrame = ttk.Frame(self)
        # self.treeFrame.pack(expand=False, side=tk.LEFT, pady=10,anchor=tk.CENTER)
        self.treeFrame.place(relx=.3, rely=.05, relwidth=.7, relheight=.85)
        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")


        cols = ("Name", "Age", "Subscription", "Employment")
        self.treeview = ttk.Treeview(self.treeFrame, show="headings",
                                yscrollcommand=self.treeScroll.set, columns=cols, height=13)
        self.treeview.column("Name", width=100)
        self.treeview.column("Age", width=50)
        self.treeview.column("Subscription", width=100)
        self.treeview.column("Employment", width=100)
        self.treeview.pack(expand=tk.TRUE,fill=tk.BOTH,side=tk.LEFT)
        self.treeScroll.config(command=self.treeview.yview)

        self.load_data()


        # # //////////////////////////////////////////////////////////////////
        # self.plot_frame = tk.Frame(self, bg=visualisation_frame_color)
        # self.plot_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    #     TODO put all the functions here that are gonna help manage

    def load_data(self):
        self.path = "./people.xlsx"
        self.workbook = openpyxl.load_workbook(self.path)
        self.sheet = self.workbook.active

        self.list_values = list(self.sheet.values)
        print(self.list_values)
        for col_name in self.list_values[0]:
            self.treeview.heading(col_name, text=col_name)

        for value_tuple in self.list_values[1:]:
            self.treeview.insert('', tk.END, values=value_tuple)

    def insert_row(self):
        self.name = self.name_entry.get()
        self.age = int(self.age_spinbox.get())
        self.subscription_status = self.status_combobox.get()
        self.employment_status = "Employed" if self.a.get() else "Unemployed"

        print(self.name, self.age, self.subscription_status, self.employment_status)

        # Insert row into Excel sheet
        path = "./people.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        row_values = [self.name, self.age, self.subscription_status, self.employment_status]
        sheet.append(row_values)
        workbook.save(path)

        # Insert row into treeview
        self.treeview.insert('', tk.END, values=row_values)

        # Clear the values
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, "Name")
        self.age_spinbox.delete(0, "end")
        self.age_spinbox.insert(0, "Age")
        self.status_combobox.set(self.combo_list[0])
        self.checkbutton.state(["!selected"])

    def toggle_mode(self):
        if self.mode_switch.instate(["selected"]):
            self.style.theme_use("forest-light")
        else:
            self.style.theme_use("forest-dark")

