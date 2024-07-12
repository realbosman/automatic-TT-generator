import time
import tkinter as tk
from tkinter import ttk, messagebox

# import openpyxl

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------
from Models.Listener import Listener

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'
my_pink="#f7b2b2"
sidebar_color_ = visualisation_frame_color
visualisation_frame_color_ = my_pink


class Session(tk.Frame):
    """
    The RoomsClassesSpace class provides a way to view and edit the space.
    """

    def __init__(self, parent, *cls):
        ttk.Frame.__init__(self, parent)

        for arg in cls:
            self.session__ = arg
        # self.config(bg=visualisation_frame_color)
        self.combo = tk.StringVar()
        self.combo2 = tk.StringVar()
        self.combo3 = tk.StringVar()
        # these are default values
        self.storeWidth = [100, 100, 100, 100,100, 100,100,100]
        # v = tk.Scrollbar(self)


        # TODO: call all the timeslots methods here to show up when th ui is created

        # PLOT FRAME

        #     TODO put all the functions here that are gonna help manage the  time slot

        self.widgets_frame = ttk.LabelFrame(self, text="Current TimeSlots")
        self.widgets_frame.pack(expand=1, fill='x')

        self.label1 = ttk.Label(self.widgets_frame, text="Add Row",foreground=TEXT_COLOR)
        self.label1.pack(expand=0, fill='y', side=tk.LEFT)
        self.label1.bind("<Button-1>", self.add_new_session)

        self.separator = ttk.Separator(self.widgets_frame, orient='vertical')
        self.separator.pack(expand=0, fill='y', side=tk.LEFT, padx=10)

        self.label2 = ttk.Label(self.widgets_frame, text="Save",foreground=TEXT_COLOR)
        self.label2.pack(expand=0, fill='y', side=tk.LEFT)
        self.label2.bind("<Button-1>", self.on_save)

        self.separator2 = ttk.Separator(self.widgets_frame, orient='vertical')
        self.separator2.pack(expand=0, fill='y', side=tk.LEFT, padx=10)

        self.label2_ = ttk.Label(self.widgets_frame, text="Allocate More",foreground=TEXT_COLOR)
        self.label2_.pack(expand=0, fill='y', side=tk.LEFT)
        self.label2_.bind("<Button-1>", self.on_more_allocate)

        self.label3 = ttk.Label(self.widgets_frame, text="Delete selected Row",foreground=TEXT_COLOR)
        self.label3.pack(expand=0, fill='y', side=tk.RIGHT, padx=10,)
        self.label3.bind("<Button-1>", self.delete_row_,)

        self.changeOnHover(self.label3, visualisation_frame_color_,
                           sidebar_color_)
        self.changeOnHover(self.label2, visualisation_frame_color_,
                           sidebar_color_)
        self.changeOnHover(self.label1, visualisation_frame_color_,
                           sidebar_color_)
        self.changeOnHover(self.label2_, visualisation_frame_color_,
                           sidebar_color_)

        self.warnings_frame=tk.Frame(self)
        self.warnings_frame.pack(expand=1, fill='x')



        self.separator = ttk.Separator(self)
        self.separator.pack()



        self.treeFrame = ttk.Frame(self)
        self.treeFrame.pack(expand=1, anchor=tk.CENTER, fill=tk.BOTH, pady=(0, 15), padx=(10, 10))

        # self.allocate_more = tk.Frame(self,border=1,background="green")
        # self.allocate_more.pack(expand=1, anchor=tk.CENTER, fill=tk.BOTH, pady=(0, 15), padx=(10, 10))
        #
        # # Add form to allocate_more frame
        # self.create_form(self.allocate_more)



        # self.treeFrame.place(relx=.3, rely=.05, relwidth=.7, relheight=.85)
        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")

        # # Define a custom style for the treeview
        # self.treeScroll_x_style = ttk.Style()
        # self.treeScroll_x_style.configure("Custom.Scrollbar", height=30)

        self.treeScroll_x = ttk.Scrollbar(self.treeFrame, orient="horizontal")
        self.treeScroll_x.pack(side="bottom", fill="x",ipady=10)
        # self.treeScroll_x.configure(style="Custom.Scrollbar")

        # Define a custom style for the treeview
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview", rowheight=30)  # Set your desired row height here

        cols = self.session__.get_column_headers()
        # print(cols)
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

        # function to change properties of button on hover

    def changeOnHover(self, view, colorOnHover, colorOnLeave):

        # adjusting backgroung of the widget
        # background on entering widget
        view.bind("<Enter>", func=lambda e: view.config(
            background=colorOnHover,foreground=visualisation_frame_color))

        # background color on leving widget
        view.bind("<Leave>", func=lambda e: view.config(
            background=colorOnLeave,foreground=TEXT_COLOR))

    def updateUI(self):

        headings = self.session__.get_column_headers()

        # print("heads", headings)
        for col_ in headings:
            self.treeview.column(col_, width=150, anchor='w', stretch=tk.YES)
            self.treeview.heading(col_, text=col_)

        for i in range(int(self.session__.get_sessions_length())):
            values = self.session__.get_sessions()[i]
            for col_index, value in enumerate(values):
                col_width = len(str(value)) * 8  # Adjust the multiplier as needed
                current_width = self.treeview.column(headings[col_index], option="width")
                if col_width > current_width:
                    self.treeview.column(headings[col_index], width=col_width)
                    self.storeWidth[col_index] = col_width

                # if len(values) == 4:
                #     values.append("AUTO")
                # else:
                #     pass


            self.treeview.insert('', tk.END, values=values)

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
        # print(self.treeview.selection(), "///", )
        columnIndex = int(column[1:]) - 1
        selected_iid = self.treeview.focus()
        selected_values = self.treeview.item(selected_iid)
        selected_text = selected_values.get("values")
        # print(self.treeview.selection(), "///", selected_values)
        column_box = self.treeview.bbox(selected_iid, column)
        # print(self.treeview.selection(), "///", column_box, "///", self.storeWidth)

        # TODO Test this with bigger row tex to ensure that this below stands out

        if column_box[2] == self.storeWidth[-4]:
            # print("ON ME", column_box[0])
            entry_edit = ttk.Combobox(self.treeview, width=column_box[2], values=(10,20,30,40,50,60,70,80,90,100))
            # record the column index and id
            entry_edit.editing_column_index = columnIndex
            entry_edit.editing_item_iid = selected_iid
            entry_edit.insert(0, selected_text[columnIndex])
            # print(selected_text[columnIndex])
            entry_edit.select_range(0, tk.END)

            entry_edit.focus()

            entry_edit.place(x=column_box[0],
                             y=column_box[1],
                             w=column_box[2],
                             h=column_box[3],
                             )

            entry_edit.bind("<FocusOut>", self.onFocusOut)
            entry_edit.bind("<Return>", self.on_enter_press)
        elif column_box[2] == self.storeWidth[-5]:
            # print("ON ME", column_box[0])
            entry_edit = ttk.Combobox(self.treeview, width=column_box[2], values=(self.session__.get_sub_groups_commbo()))
            # record the column index and id
            entry_edit.editing_column_index = columnIndex
            entry_edit.editing_item_iid = selected_iid
            entry_edit.insert(0, selected_text[columnIndex])
            # print(selected_text[columnIndex])
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
            entry_edit = ttk.Entry(self.treeview, width=column_box[2])
            # record the column index and id
            entry_edit.editing_column_index = columnIndex
            entry_edit.editing_item_iid = selected_iid
            entry_edit.insert(0, selected_text[columnIndex])
            # print(selected_text[columnIndex])
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
                # print(self.treeview.get_children())
                # print(self.session__.get_sessions())


            else:

                self.session__.delete_session(index_to_delete)
                self.treeview.delete(self.treeview.focus())

                # print(self.treeview.get_children())
                # print(self.treeview.item(*self.treeview.get_children()))
                # print(self.session__.get_sessions())



        else:
            pass
            # print("Else:", self.treeview.focus())

    def on_enter_press(self, e):
        new_text = e.widget.get()

        # print("nn=",new_text[-5:])
        print("nn=", new_text[0:4])
        if new_text[-4:]==".com" or new_text[-3:]==".ug" or new_text[0:4]=="http":
            pass
        else:
            new_text = new_text.upper()



        if new_text == '':
            # TODO add a popup to alert tyhe user that this field in blank either fill it or leave it
            # print('Object is None ')
            new_text = '--------'
            e.widget.destroy()
            messagebox.showerror("Empty Field", message="This field should not be empty!")
            return
        else:
            new_text=str(new_text)
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

            # print("Cureent values:",current_values)
            # print("INDEXXX",index)

            self.session__.edit_session(index_to_add, current_values)
            e.widget.destroy()
            if Listener.iswarningOnSession==False:
                        messagebox.showwarning(title="Warning", message="Please all fields must be in caps and names of Tutors,Groups and Faculties  "
                                         "reoccurring should be consistent with the spellings and spaces to ensure ensure "
                                         "timetable consistency.")
                        Listener.iswarningOnSession = True

    def onFocusOut(self, e):
        # print("running")
        e.widget.destroy()
        self.label4.destroy()


    def on_save(self, event):
        print("Save clicked")

    def on_more_allocate(self, event):
        print("more allocate clicked")
        # self.allocate_more.tkraise(self.treeFrame)

    def create_form(self, parent):
        # Create form elements
        ttk.Label(parent, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = ttk.Entry(parent)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(parent, text="Age:").grid(row=1, column=0, padx=10, pady=5)
        self.age_entry = ttk.Entry(parent)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(parent, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        self.email_entry = ttk.Entry(parent)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        submit_button = ttk.Button(parent, text="Submit", command=self.on_submit)
        submit_button.grid(row=3, columnspan=2, pady=10)

    def on_submit(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        print(f"Name: {name}, Age: {age}, Email: {email}")

