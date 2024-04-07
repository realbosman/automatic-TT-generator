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


class Session(tk.Frame):
    """
    The RoomsClassesSpace class provides a way to view and edit the space.
    """

    def __init__(self, parent, cls,cls_=None):
        ttk.Frame.__init__(self, parent)
        self.session__ = cls
        # self.config(bg=visualisation_frame_color)
        self.combo = tk.StringVar()
        self.combo2 = tk.StringVar()
        self.combo3 = tk.StringVar()

        # TODO: call all the timeslots methods here to show up when th ui is created

        # PLOT FRAME

        #     TODO put all the functions here that are gonna help manage the  time slot

        self.widgets_frame = ttk.LabelFrame(self, text="Current TimeSlots")
        self.widgets_frame.pack(expand=1, fill='x')

        self.label1 = ttk.Label(self.widgets_frame, text="Add Row")
        self.label1.pack(expand=0, fill='y', side=tk.LEFT)
        self.label1.bind("<Button-1>", self.add_new_session)

        self.separator = ttk.Separator(self.widgets_frame, orient='vertical')
        self.separator.pack(expand=0, fill='y', side=tk.LEFT, padx=10)

        self.label2 = ttk.Label(self.widgets_frame, text="Save")
        self.label2.pack(expand=0, fill='y', side=tk.LEFT)
        self.label2.bind("<Button-1>", self.on_save)

        self.label3 = ttk.Label(self.widgets_frame, text="Delete selected Row")
        self.label3.pack(expand=0, fill='y', side=tk.RIGHT, padx=10)
        self.label3.bind("<Button-1>", self.delete_row_)

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

        cols = self.session__.get_column_headers()
        print(cols)
        self.treeview = ttk.Treeview(self.treeFrame, show="headings", columns=cols,
                                     xscrollcommand=self.treeScroll_x.set,
                                     yscrollcommand=self.treeScroll.set, height=20)
        self.treeview.configure(style="Custom.Treeview")

        # TODO to check and update the size of the column

        self.treeview['columns'] = self.session__.get_column_headers()

        self.treeview.pack(expand=tk.TRUE, fill=tk.BOTH, side=tk.LEFT)
        self.treeScroll.config(command=self.treeview.yview)
        self.treeScroll_x.config(command=self.treeview.xview)
        self.treeview.bind("<Double-1>", self.on_double_clicked)

        #     TODO this needs to run in a thread
        self.updateUI()

    def updateUI(self):

        headings = self.session__.get_column_headers()

        print("heads", headings)
        for col_ in headings:
            self.treeview.column(col_, width=50, anchor='c')
            self.treeview.heading(col_, text=col_)

        for i in range(int(self.session__.get_sessions_length())):
            self.treeview.insert('', tk.END, values=self.session__.get_sessions()[i])

    def add_new_session(self, event):
        values_lst = list()
        for i in range(len(self.session__.get_column_headers())):
            values_lst.append('--------')

        self.treeview.insert('', tk.END, values=values_lst)
        self.session__.add_new_session(values_lst)

    def on_double_clicked(self, event):
        region_clicked = self.treeview.identify_region(event.x, event.y)

        '''
        identify the region that was double clicked
        '''
        if region_clicked not in ["tree", "cell"]:
            return

        column = self.treeview.identify_column(event.x)
        print(self.treeview.selection(), "///", )
        columnIndex = int(column[1:]) - 1
        selected_iid = self.treeview.focus()
        selected_values = self.treeview.item(selected_iid)
        selected_text = selected_values.get("values")
        print(self.treeview.selection(), "///", selected_values)
        column_box = self.treeview.bbox(selected_iid, column)
        print(self.treeview.selection(), "///", column_box)

        # TODO Test this with bigger row tex to ensure that this below stands out
        if ((1307 / column_box[0]) > 2.3):
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
        else:
            entry_edit = ttk.Combobox(self.treeview, width=column_box[2],values=["BSC IT 1","BSC CS 1"])
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
    def delete_row_(self, event):
        index_to_delete = None
        for index, child in enumerate(self.treeview.get_children()):
            if child == self.treeview.focus():
                index_to_delete = index - 1
                break

        if str(self.treeview.focus()) != '':
            if int(self.session__.get_sessions_length()) == 1:
                values_lst = list()
                for i in range(len(self.session__.get_column_headers())):
                    values_lst.append('--------')

                self.session__.add_new_session(values_lst)
                self.treeview.insert('', tk.END,
                                     values=values_lst)
                self.session__.delete_session(index_to_delete)

                self.treeview.delete(self.treeview.focus())
                # self.updateUI()
                print(self.treeview.get_children())
                print(self.session__.get_sessions())


            else:

                self.session__.delete_session(index_to_delete)
                self.treeview.delete(self.treeview.focus())

                print(self.treeview.get_children())
                # print(self.treeview.item(*self.treeview.get_children()))
                print(self.session__.get_sessions())



        else:
            print("Else:", self.treeview.focus())

    def on_enter_press(self, e):
        new_text = e.widget.get()

        if new_text == '':
            # TODO add a popup to alert tyhe user that this field in blank either fill it or leave it
            print('Object is None ')
            new_text = '--------'

        selected_iid = e.widget.editing_item_iid
        column_index = e.widget.editing_column_index
        current_values = self.treeview.item(selected_iid).get("values")
        current_values[column_index] = new_text
        self.treeview.item(selected_iid, values=current_values)
        index_to_add = None
        for index, child in enumerate(self.treeview.get_children()):
            if child == selected_iid:
                index_to_add = index
                break
        e.widget.destroy()
        self.session__.edit_session(index_to_add, current_values)

        # print(current_values)

    def onFocusOut(self, e):
        print("running")
        e.widget.destroy()

    def on_save(self, event):
        print("Save clicked")
