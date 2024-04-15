# import time
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import re

from tk import *
#


IMG_PATH = Path(__file__).parent / 'assets'

# import openpyxl

# -------------------------- DEFINING GLOBAL VARIABLES -------------------------

selectionbar_color = '#3C3F3F'
sidebar_color = '#3C3F3F'
header_color = '#3C3F3F'
visualisation_frame_color = "#2B2B2B"
TEXT_COLOR = '#AFB1B3'


class Groups_(tk.Frame):
    """
    The Groups class provides a way to view  the groups in the timetable.
    """
    def __init__(self, parent, *cls):

        ttk.Frame.__init__(self, parent)

        for arg in cls:
            self.session_manager=arg
        self.cf = CollapsingFrame(self)
        self.cf.pack(fill=tk.BOTH)
        print(IMG_PATH)

        # option group 1

        self.frame_list=list()
        self.render_groups()

    def render_groups(self):
        self.frame_list.clear()
        self.session_manager.set_groups_cu()

        for i , faculty in enumerate(self.session_manager.get_faculty_cu()):
            self.frame_list.append(ttk.Frame(self.cf, padding=10))
            print(self.session_manager.get_sub_groups(),self.session_manager.get_faculty_cu())
            for j,sub_group in enumerate(self.session_manager.get_sub_groups()):
                print(re.findall(r"<(.*?)>", sub_group)[0]," ",  faculty)
                if re.findall(r"<(.*?)>", sub_group)[0] ==  faculty:
                    ttk.Checkbutton(self.frame_list[i], text=f'{re.findall(r"<(.*?)>", sub_group)[1]}').pack(fill=tk.X)
            self.cf.add(child=self.frame_list[i], title=f'{faculty}')




class CollapsingFrame(ttk.Frame):
    """A collapsible frame widget that opens and closes with a click."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        # widget images
        self.images = [
            tk.PhotoImage(file=IMG_PATH / 'icons8_double_up_24px.png'),
            tk.PhotoImage(file=IMG_PATH / 'icons8_double_right_24px.png')
        ]




    def add(self, child, title="", bootstyle=None, **kwargs):
        """Add a child to the collapsible frame

        Parameters:

            child (Frame):
                The child frame to add to the widget.

            title (str):
                The title appearing on the collapsible section header.

            bootstyle (str):
                The style to apply to the collapsible section header.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        if child.winfo_class() != 'TFrame':
            return

        # style_color = Bootstyle.ttkstyle_widget_color(bootstyle)
        frm = ttk.Frame(self)
        frm.grid(row=self.cumulative_rows, column=0, sticky=tk.EW)

        # header title
        header = ttk.Label(
            master=frm,
            text=title,

        )
        if kwargs.get('textvariable'):
            header.configure(textvariable=kwargs.get('textvariable'))
        header.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        # header toggle button
        def _func(c=child):
            return self._toggle_open_close(c)

        btn = ttk.Button(
            master=frm,
            image=self.images[0],

            command=_func
        )
        btn.pack(side=tk.RIGHT)

        # assign toggle button to child so that it can be toggled
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky=tk.NSEW)

        # increment the row assignment
        self.cumulative_rows += 2

    def _toggle_open_close(self, child):
        """Open or close the section and change the toggle button
        image accordingly.

        Parameters:

            child (Frame):
                The child element to add or remove from grid manager.
        """
        if child.winfo_viewable():
            child.grid_remove()
            child.btn.configure(image=self.images[1])
        else:
            child.grid()
            child.btn.configure(image=self.images[0])


