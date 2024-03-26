import time
import tkinter as tk
from tkinter import ttk

# import openpyxl

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class Space(tk.Frame):
    """
    The RoomsClassesSpace class provides a way to view and edit the space.
    """

    def __init__(self, parent, cls):
        ttk.Frame.__init__(self, parent)
        self.timeDimension__ = cls
        # self.config(bg=visualisation_frame_color)
        self.combo = tk.StringVar()
        self.combo2 = tk.StringVar()
        self.combo3 = tk.StringVar()

        # TODO: call all the timeslots methods here to show up when th ui is created

        # PLOT FRAME

        #     TODO put all the functions here that are gonna help manage the  time slot

        self.combo_list = ["MON", "TUE", "WED", "THUR", "FRI", "SAT", "SUNnn"]
        self.combo_list2 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14",
                            "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]

        self.widgets_frame = ttk.LabelFrame(self, text="Current TimeSlots")
        self.widgets_frame.pack(expand=1, fill='x')

        self.label1 = ttk.Button(self.widgets_frame, text="Add Row", command=self.add_new_session)
        self.label1.pack(expand=0, fill='y', side=tk.LEFT)

        self.separator = ttk.Separator(self.widgets_frame, orient='vertical')
        self.separator.pack(expand=0, fill='y', side=tk.LEFT, padx=10)

        self.label2 = ttk.Button(self.widgets_frame, text="Save")
        self.label2.pack(expand=0, fill='y', side=tk.LEFT)

        self.label3 = ttk.Button(self.widgets_frame, text="Delete selected Row", command=self.delete_row_)
        self.label3.pack(expand=0, fill='y', side=tk.RIGHT)

        self.separator = ttk.Separator(self)
        self.separator.pack()

        self.treeFrame = ttk.Frame(self)
        self.treeFrame.pack(expand=1, anchor=tk.CENTER, fill=tk.BOTH)
        # self.treeFrame.place(relx=.3, rely=.05, relwidth=.7, relheight=.85)
        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")

        self.treeScroll_x = ttk.Scrollbar(self.treeFrame, orient="horizontal")
        self.treeScroll_x.pack(side="bottom", fill="x")

        # Define a custom style for the treeview
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", rowheight=30)  # Set your desired row height here
        cols = ("MON", "TUE", "WED", "THUR", "FRI", "SAT", "SUN")
        self.treeview = ttk.Treeview(self.treeFrame, show="headings",
                                     xscrollcommand=self.treeScroll_x.set,
                                     yscrollcommand=self.treeScroll.set, columns=cols, height=20)
        self.treeview.configure(style="Custom.Treeview")
        self.treeview.column("MON", width=50)
        self.treeview.column("TUE", width=50)
        self.treeview.column("WED", width=50)
        self.treeview.column("THUR", width=50)
        self.treeview.column("FRI", width=50)
        self.treeview.column("SAT", width=50)
        self.treeview.column("SUN", width=50)
        # self.treeview.rowconfigure

        self.treeview.pack(expand=tk.TRUE, fill=tk.BOTH, side=tk.LEFT)
        self.treeScroll.config(command=self.treeview.yview)
        self.treeScroll_x.config(command=self.treeview.xview)
        self.treeview.bind("<Double-1>", self.on_double_clicked)

        self.updateUI()

    def getData(self):
        day = self.status_combobox.get()
        setTime = f'{self.status_combobox2.get()}:{self.status_combobox2_1.get()}-{self.status_combobox3.get()}:{self.status_combobox3_1.get()}'
        self.timeDimension__.edit_time_slot(day, setTime)
        # Insert row into treeview
        self.timeDimension__.tuple_time_slot()

        self.treeview.insert('', tk.END, values=self.timeDimension__.get_tuple_list_list(-1))

        # self.updateUI()

    def updateUI(self):
        self.treeview.heading(0, text="MON")
        self.treeview.heading(1, text="TUE")
        self.treeview.heading(2, text="WED")
        self.treeview.heading(3, text="THUR")
        self.treeview.heading(4, text="FRI")
        self.treeview.heading(5, text="SAT")
        self.treeview.heading(6, text="SUN")
        self.timeDimension__.tuple_time_slot()
        for i in range(self.timeDimension__.get_tuple_list_length()):
            self.treeview.insert('', tk.END, values=self.timeDimension__.get_tuple_list_list(i))

    def add_new_session(self):
        self.treeview.insert('', tk.END, values=['--------', '--------', '--------', '--------', '--------', '--------',
                                                 '--------'])
        # self.timeDimension__.add_to_tuple_time_slot(
        #     ['--------', '--------', '--------', '--------', '--------', '--------', '--------'])
        # self.timeDimension__.tuple_time_slot()

    def on_double_clicked(self, event):
        region_clicked = self.treeview.identify_region(event.x, event.y)

        '''
        identify the region that was double clicked
        '''
        if region_clicked not in ["tree", "cell"]:
            return

        column = self.treeview.identify_column(event.x)
        # print(self.treeview.selection(),"///")
        columnIndex = int(column[1:]) - 1
        selected_iid = self.treeview.focus()
        selected_values = self.treeview.item(selected_iid)
        selected_text = selected_values.get("values")

        column_box = self.treeview.bbox(selected_iid, column)

        entry_edit = ttk.Entry(self.treeview, width=column_box[2])
        # record the column index and id
        entry_edit.editing_column_index = columnIndex
        entry_edit.editing_item_iid = selected_iid
        entry_edit.insert(0, selected_text[columnIndex])
        print(selected_text[columnIndex])
        entry_edit.select_range(0, tk.END)

        entry_edit.focus()

        entry_edit.place(x=column_box[0],
                         y=column_box[1],
                         w=column_box[2],
                         h=column_box[3],
                         )

        entry_edit.bind("<FocusOut>", self.onFocusOut)
        entry_edit.bind("<Return>", self.on_enter_press)



    # TODO I got work to do  regarding with the iceasing number in the fiirst print below
    def delete_row_(self):

        print(type(self.treeview.focus()),int(self.treeview.focus()[1:]))
        if str(self.treeview.focus()) != '':
            self.timeDimension__.remove_row_(int(self.treeview.focus()[1:]))
            for item in self.treeview.get_children():
                self.treeview.delete(item)
            self.treeview.update()
            self.updateUI()
            print("selection ==", self.treeview.focus())

    def on_enter_press(self, e):
        new_text = e.widget.get()

        if new_text == '':
            print('Object is None ')

        else:
            selected_iid = e.widget.editing_item_iid
            column_index = e.widget.editing_column_index
            current_values = self.treeview.item(selected_iid).get("values")
            current_values[column_index] = new_text
            self.treeview.item(selected_iid, values=current_values)
            e.widget.destroy()
            self.timeDimension__.edit_dict_time_slot(current_values, int(selected_iid[1:]) - 1)

        # print(current_values)

    def onFocusOut(self, e):
        print("running")
        e.widget.destroy()
