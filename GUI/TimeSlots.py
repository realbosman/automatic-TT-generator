import time
import tkinter as tk
from tkinter import ttk



# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
from Models.TimeDimension import TimeDimension

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class TimeSlots(tk.Frame):
    """
    The time slots class provides a way to view and edit the time periods.
    """
    def __init__(self, parent,cls):

        ttk.Frame.__init__(self, parent)
        self.timeDimension_ = cls
        # self.config(bg=visualisation_frame_color)
        self.combo=tk.StringVar()
        self.combo2 = tk.StringVar()
        self.combo3 = tk.StringVar()



       #TODO: call all the timeslots methods here to show up when th ui is created

        # PLOT FRAME


#     TODO put all the functions here that are gonna help manage the  time slot

        self.combo_list = ["MON","TUE","WED","THUR","FRI","SAT","SUN"]
        self.combo_list2 = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]



        self.widgets_frame = ttk.LabelFrame(self, text="Create TimeSlots")
        # self.widgets_frame.pack(expand=0, side=tk.LEFT, padx=20, pady=10 ,anchor=tk.CENTER)
        self.widgets_frame.place(relx=.02, rely=.05, relwidth=.245, relheight=.5)





        self.status_combobox = ttk.Combobox(self.widgets_frame, values=self.combo_list,textvariable=self.combo)
        self.status_combobox.current(0)
        self.status_combobox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.startTime = ttk.Label(self.widgets_frame, text='start time')
        self.startTime.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.status_combobox2 = ttk.Combobox(self.widgets_frame, values=self.combo_list2)
        self.status_combobox2.current(0)
        self.status_combobox2.grid(row=3, column=0, padx=5, pady=5,sticky="w")

        self.status_combobox2_1 = ttk.Combobox(self.widgets_frame, values=self.combo_list2)
        self.status_combobox2_1.current(0)
        self.status_combobox2_1.grid(row=4, column=0,padx=5, pady=5,  sticky="e")

        self.endTime = ttk.Label(self.widgets_frame, text='end time')
        self.endTime.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        self.status_combobox3 = ttk.Combobox(self.widgets_frame, values=self.combo_list2)
        self.status_combobox3.current(0)
        self.status_combobox3.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

        self.status_combobox3_1 = ttk.Combobox(self.widgets_frame, values=self.combo_list2)
        self.status_combobox3_1.current(0)
        self.status_combobox3_1.grid(row=7, column=0, padx=5, pady=5, sticky="e")



        self.button = ttk.Button(self.widgets_frame, text="Insert", command=self.getData)
        self.button.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")

        self.separator = ttk.Separator(self.widgets_frame)
        self.separator.grid(row=9, column=0, padx=(20, 10), pady=10, sticky="ew")


        self.treeFrame = ttk.Frame(self)
        # self.treeFrame.pack(expand=False, side=tk.LEFT, pady=10,anchor=tk.CENTER)
        self.treeFrame.place(relx=.3, rely=.05, relwidth=.7, relheight=.85)
        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")
        print("Mee")

        cols = ("MON","TUE","WED","THUR","FRI","SAT","SUN")
        self.treeview = ttk.Treeview(self.treeFrame, show="headings",
                                yscrollcommand=self.treeScroll.set, columns=cols, height=20 )
        self.treeview.column("MON", width=50)
        self.treeview.column("TUE", width=50)
        self.treeview.column("WED", width=50)
        self.treeview.column("THUR", width=50)
        self.treeview.column("FRI", width=50)
        self.treeview.column("SAT", width=50)
        self.treeview.column("SUN", width=50)
        # self.treeview.rowconfigure

        self.treeview.pack(expand=tk.TRUE,fill=tk.BOTH,side=tk.LEFT)
        self.treeScroll.config(command=self.treeview.yview)


        self.updateUI()

    def getData(self):
        day=self.status_combobox.get()
        setTime=f'{self.status_combobox2.get()}:{self.status_combobox2_1.get()}-{self.status_combobox3.get()}:{self.status_combobox3_1.get()}'
        self.timeDimension_.edit_time_slot(day,setTime)
        # Insert row into treeview
        self.timeDimension_.tuple_time_slot()
        self.treeview.insert('', tk.END, values=self.timeDimension_.get_tuple_list_list(-1))

        # self.updateUI()

    def updateUI(self):
        self.treeview.heading(0, text="MON")
        self.treeview.heading(1, text="TUE")
        self.treeview.heading(2, text="WED")
        self.treeview.heading(3, text="THUR")
        self.treeview.heading(4, text="FRI")
        self.treeview.heading(5, text="SAT")
        self.treeview.heading(6, text="SUN")
        self.timeDimension_.tuple_time_slot()
        for i in range(self.timeDimension_.get_tuple_list_length()):
            self.treeview.insert('', tk.END, values=self.timeDimension_.get_tuple_list_list(i))





