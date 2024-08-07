import itertools
from collections.abc import Mapping
import time
from math import ceil, floor
from pathlib import Path
from datetime import time
import datetime
import re
import time as tm

import sys
from textwrap import wrap
from reportlab.lib.pagesizes import A4
import attr
import click
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from Models.Listener import Listener

EM = 0.6  ### TODO: Eliminate

WEEKDAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
FULL_WEEK_EN = ["Sunday"] + WEEKDAYS_EN + ["Saturday"]
FULL_WEEK_MON_EN = WEEKDAYS_EN + ["Saturday", "Sunday"]

DAY_REGEXES = [
    ("Sunday", "Sun?"),
    ("Monday", "M(on?)?"),
    ("Tuesday", "T(ue?)?"),
    ("Wednesday", "W(ed?)?"),
    ("Thursday", "Thu?|H|R"),
    ("Friday", "F(ri?)?"),
    ("Saturday", "Sat?"),
]

GREY = (0.8, 0.8, 0.8)

COLORS = [
    GREY,
    (1, 0, 0),  # red
    (0, 1, 0),  # blue
    (0, 0, 1),  # green
    (0, 1, 1),  # cyan
    (1, 1, 0),  # yellow
    (0.5, 0, 0.5),  # purple
    (1, 1, 1),  # white
    (1, 0.5, 0),  # orange
    (1, 0, 1),  # magenta
]


class Schedule:
    def __init__(self, days, day_names=None):
        self.events = []
        self.days = list(days)
        if day_names is None:
            self._day_names = lambda d: d
        elif isinstance(day_names, Mapping):
            self._day_names = day_names.__getitem__
        elif not callable(day_names):
            raise TypeError("day_names must be a callable or dict")
        else:
            self._day_names = day_names

    def add_event(self, event):
        self.events.append(event)

    def day_names(self):
        return map(self._day_names, self.days)

    def all_events(self):
        return self.events

    def events_on_day(self, day):
        return [e for e in self.events if day in e.days]

    @property
    def number_of_days(self):
        return len(self.days)

    # The font and pagesize of the canvas must already have been set.
    # x,y: upper-left corner of schedule to render (counting times along the
    # edge; `render` should not draw anything outside the given box)
    def render(
            self,
            canvas,
            width,
            height,
            x,
            y,
            font_size,
            show_times=True,
            min_time=None,
            max_time=None,
            subgroup="subgroup",
            creator=None,
            title=None
    ):
        # print(f'X:{x} Y:{y}')
        if min_time is None:
            min_time = max(
                min(time2hours(ev.start_time) for ev in self.all_events()) - 0.5, 0
            )
        if max_time is None:
            max_time = min(
                max(time2hours(ev.end_time) for ev in self.all_events()) + 0.5, 24
            )

        # print("MAX_TIME =",max_time,"MIN_TIME =",min_time,subgroup)

        # List of hours to label and draw a line across
        hours = range(floor(min_time) + 1, ceil(max_time))
        line_height = font_size * 1.2
        # Font size of the day headers at the top of each column:
        header_size = font_size * 1.2
        # Height of the boxes in which the day headers will be drawn:
        day_height = header_size * 1.2
        # Font size of the time labels at the left of each hour:
        time_size = font_size / 1.2
        # Boundaries of where this method is allowed to draw stuff:
        area = Box(x, y, width, height)

        canvas.setFontSize(time_size)
        # Gap between the right edge of the time labels and the left edge of
        # the schedule box.  I don't remember how I came up with this formula.
        time_gap = 0.2 * canvas.stringWidth(":00")
        if show_times:
            time_width = time_gap + max(canvas.stringWidth(f"{i}:00") for i in hours)
        else:
            time_width = 0

        sched = Box(
            x + time_width,
            y - day_height,
            width - time_width,
            height - day_height,
        )

        hour_height = sched.height / (max_time - min_time)
        day_width = sched.width / self.number_of_days
        line_width = floor(day_width / (font_size * EM))

        # Border around schedule and day headers:
        canvas.rect(sched.ulx, sched.lry, sched.width, area.height)

        # Day headers text:
        # print("header_size :",header_size)
        canvas.setFontSize(header_size)
        for i, day in enumerate(self.day_names()):
            canvas.drawCentredString(
                sched.ulx + day_width * (i + 0.5),
                area.uly - line_height,
                day,
            )

        # Underline beneath day headers:
        canvas.line(sched.ulx, sched.uly, sched.lrx, sched.uly)

        # Lines across each hour:
        canvas.setDash([2], 0)
        for i in range(floor(min_time), ceil(max_time)):
            y = sched.uly - (i - min_time) * hour_height
            canvas.line(sched.ulx, y, sched.lrx, y)
            y_30 = y - (hour_height / 2)
            canvas.line(sched.ulx, y_30, sched.lrx, y_30)

        # Lines between each day:
        canvas.setDash([], 0)
        for i in range(1, self.number_of_days):
            x = sched.ulx + i * day_width
            canvas.line(x, area.uly, x, area.lry)

        if show_times:
            canvas.setFontSize(time_size)
            for i in range(floor(min_time), ceil(max_time)):
                y = sched.uly - (i - min_time) * hour_height
                canvas.drawRightString(
                    sched.ulx - time_gap,
                    y - time_size / 2,
                    f"{i}:00",
                )
                # Draw the 30-minute time labels
                y_30 = y - (hour_height / 2)
                canvas.drawRightString(
                    sched.ulx - time_gap,
                    y_30 - time_size / 2,
                    f"{i}:30",
                )

        # Events:
        canvas.setFontSize(font_size)
        for i, day in enumerate(self.days):
            dx = sched.ulx + day_width * i
            for ev in self.events_on_day(day):
                ebox = Box(
                    dx,
                    sched.uly - (time2hours(ev.start_time) - min_time) * hour_height,
                    day_width,
                    ev.length * hour_height,
                )
                # Event box:
                canvas.setStrokeColorRGB(0, 0, 0)
                canvas.setFillColorRGB(*ev.color)
                canvas.rect(*ebox.rect(), stroke=1, fill=1)
                canvas.setFillColorRGB(0, 0, 0)

                if ev.color[1] <= 0.33333:
                    # Background color is too dark; print text in white
                    canvas.setFillColorRGB(1, 1, 1)

                # Event text:
                ### TODO: Use PLATYPUS or whatever for this part:
                text = sum((wrap(t, line_width) for t in ev.text), [])
                link_url = "NO LINK"
                try:

                    new_event = str(re.findall(r"<(.*?)>", ev.text[0])[0])
                    link_url = str(re.findall(r"<(.*?)>", ev.text[0])[1])

                    text = sum((wrap(t, line_width) for t in [new_event]), [])
                    # print("text===", new_event)
                except:
                    pass
                    # print("Exception in  pdf generation")

                tmp_size = None
                if len(text) * line_height > ebox.height:
                    tmp_size = ebox.height / len(text) / 1.2
                    canvas.setFontSize(tmp_size)
                    line_height = tmp_size * 1.2
                y = (
                        ebox.lry
                        + ebox.height / 2
                        + len(text) * line_height / 2
                        + (tmp_size or font_size) / 3
                )
                for t in text:
                    y -= line_height
                    canvas.drawCentredString(ebox.ulx + day_width / 2, y, t)

                    if link_url != "NO LINK":
                        canvas.linkURL(link_url, (
                            ebox.ulx - (day_width / 100), y - line_height, ebox.ulx + (day_width / 1.1), y + line_height))

                if tmp_size is not None:
                    canvas.setFontSize(font_size)
                    line_height = font_size * 1.2

        if True:
            # Background color is too dark; print text in white
            canvas.setFillColorRGB(0, 0, 0)
        canvas.setFontSize(header_size)
        canvas.drawCentredString(300, 745, title)
        canvas.drawCentredString(300, 730, subgroup)
        canvas.bookmarkPage(subgroup)
        canvas.drawCentredString(300, 50,
                                 f'Generated by {creator} on {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}')
        canvas.drawCentredString(300, 30,
                                 f'Email: {Listener.cEmail}.')
        canvas.drawCentredString(300, 10,
                                 f'All time is in {Listener.timeZone}.')


@attr.s
class Event:
    start_time = attr.ib(validator=attr.validators.instance_of(time))
    end_time = attr.ib(validator=attr.validators.instance_of(time))
    text = attr.ib()
    color = attr.ib()
    days = attr.ib()  # List of days

    def __attrs_post_init__(self):
        if self.start_time >= self.end_time:
            raise ValueError("Event must start before it ends")

    @property
    def length(self):
        """The length of the event in hours"""
        return timediff(self.start_time, self.end_time)


@attr.s
class Box:
    ulx = attr.ib()
    uly = attr.ib()
    width = attr.ib()
    height = attr.ib()

    @property
    def lrx(self):
        return self.ulx + self.width

    @property
    def lry(self):
        return self.uly - self.height

    def rect(self):
        return (self.ulx, self.lry, self.width, self.height)


def parse_time(s):
    m = re.fullmatch(r"([0-9]{1,2})(?:[:.]?([0-9]{2}))?", s.strip())
    if m:
        return time(int(m[1]), int(m[2] or 0))
    else:
        raise ValueError(s)


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def eliminate_duplicates(data):
    seen = set()
    result = []
    for item in data:
        if item[0] not in seen:
            result.append(item)
            seen.add(item[0])
    return result


def main(
        infile: dict,
        color=True,
        outfile=None,
        start_time: time = None,
        end_time: time = None,
        no_times: bool = False,
        scale: float = None,
        portrait=True,
        no_weekends=True,
        start_monday=True,
        font="Helvetica",
        font_size=9,
        title="Title",
        creator="creator",
        breaks_list=None,
        contact_info=None

) -> bool:
    """
    Weekly schedule typesetter

    Visit <https://github.com/jwodder/schedule> for more information.
    """
    # print("EMAMAMAMAMMAM=",contact_info)
    ispdfCreated = False
    if font in available_fonts():
        font_name = font
    else:
        # Assume we've been given a path to a .ttf file
        font_name = "CustomFont"
        pdfmetrics.registerFont(TTFont(font_name, font))
    if portrait:
        page_width, page_height = pagesizes.portrait(pagesizes.letter)
    else:
        page_width, page_height = pagesizes.landscape(pagesizes.letter)
    colors = COLORS if color else [GREY]
    if no_weekends:
        week = WEEKDAYS_EN
    elif start_monday:
        week = FULL_WEEK_MON_EN
    else:
        week = FULL_WEEK_EN

    if outfile is None:
        outfile_name = str(Path(f'{Listener.get_app_path_docs()}\{Listener.timeTableNameListener}').with_suffix(".pdf"))
        outfile = click.open_file(outfile_name, "wb")

    c = Canvas(outfile, (page_width, page_height))
    c.setFont(font_name, font_size)
    if scale is not None:
        factor = 1 / scale
        c.translate(
            (1 - factor) * page_width / 2,
            (1 - factor) * page_height / 2,
        )
        c.scale(factor, factor)

    data = list()
    # print("infile.keys()==",infile.keys())

    for faculty in sorted(infile.keys()):

        for i, sub_group in enumerate(sorted(infile[faculty].keys())):
            if i == 0:
                data.append((f"{faculty}", f'{sub_group}'))
            else:
                data.append((f"-", f'{sub_group}'))
    # print("DATA+++",data)

    w, h = A4
    h = h - 100
    max_rows_per_page = 30
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 20

    xlist = [x + x_offset for x in [0, 130, 100]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    bookmarks = []
    c.setFontSize(12)
    c.drawCentredString(300, 745, title)
    c.setFontSize(10)
    # c.setFillColorRGB(247/255.0, 178/255.0, 178/255.0)
    # print(infile)
    faculty_ = " "
    for rows in grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        # print("Rows=====", rows)
        # c.grid(xlist, ylist[:len(rows) + 1])
        count = 0
        # print("ylist >>",ylist)
        for y, row in zip(ylist[:-1], rows):
            count += 1
            # print("Row", row)
            # print("Row", row[0])
            if row[0] != "-":
                faculty_ = row[0]
            for x, cell in zip(xlist, row):
                # Check if the cell is the name field
                if str(cell) in infile.keys():
                    c.drawString(x + 2, y - padding + 3, str(cell))
                else:
                    for sub_group in infile[faculty_].keys():
                        if sub_group == str(cell):
                            toc_item = f"{count}.{str(cell)}"
                            # print("XCELL___", x, cell)
                            dest_name = str(cell)
                            # print("dest", dest_name)
                            # print(y,"<<<<y")
                            Rect_cords = (x + 2, y - 10, 400, y - 20)
                            c.drawString(x + 2, y - padding + 3, toc_item)
                            # c.rect(*Rect_cords)
                            c.linkAbsolute(toc_item, dest_name, Rect=Rect_cords)

                        elif str(cell) == "":
                            # print("XCELL", x, cell)
                            c.drawString(x + 2, y - padding + 3, str(cell + "-----------"))

        c.showPage()

    # getting max and min time
    sched_time = Schedule(week)
    for faculty in infile.keys():
        for sub_group in infile[faculty].keys():
            if len(infile[faculty][sub_group]) != 0:
                for ev in read_events(infile[faculty][sub_group], colors=colors):
                    sched_time.add_event(ev)

    start_time = max(
        min(time2hours(ev.start_time) for ev in sched_time.all_events()) - 0.5, 0
    )
    end_time = min(
        max(time2hours(ev.end_time) for ev in sched_time.all_events()) + 0.5, 24
    )

    for faculty in sorted(infile.keys()):

        for sub_group in sorted(infile[faculty].keys()):
            sched = Schedule(week)
            if len(infile[faculty][sub_group]) != 0:
                for ev in read_events(infile[faculty][sub_group], colors=colors):
                    sched.add_event(ev)
                sched.render(
                    c,
                    x=inch,
                    y=page_height - inch,
                    width=page_width - 2 * inch,
                    height=page_height - 2 * inch,
                    font_size=font_size,
                    show_times=not no_times,
                    min_time=start_time,
                    max_time=end_time,
                    subgroup=sub_group,
                    creator=creator,
                    title=title
                )

                for ev in read_events(breaks_list, colors=colors):
                    sched.add_event(ev)
                sched.render(
                    c,
                    x=inch,
                    y=page_height - inch,
                    width=page_width - 2 * inch,
                    height=page_height - 2 * inch,
                    font_size=font_size,
                    show_times=not no_times,
                    min_time=start_time,
                    max_time=end_time,
                    subgroup=sub_group,
                    creator=creator,
                    title=title
                )
                c.showPage()
    bookmarks = []
    c.setFontSize(12)
    c.drawCentredString(300, 745, "CONTACT INFORMATION")
    c.setFontSize(10)

    # print(infile)
    faculty_ = " "
    data2 = list()
    xlist = [x + x_offset for x in [0, 220, 100]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    for item in contact_info:
        data2.append([item[0], item[-1]])
    data2 = eliminate_duplicates(data2)

    max_rows_per_page = 30
    for rows in grouper(data2, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        # print("Rows=====", rows)
        # c.grid(xlist, ylist[:len(rows) + 1])
        count = 0
        # print("ylist >>",ylist)
        for y, row in zip(ylist[:-1], rows):

            count += 1
            # print("Row", row)
            # print("Row", row[0])
            for i, (x, cell) in enumerate(zip(xlist, row)):
                c.setFontSize(10)
                # Check if the cell is the second value in the row
                if i == 1:
                    c.setFillColorRGB(0, 0, 1)  # Set color to blue
                else:
                    c.setFillColorRGB(0, 0, 0)  # Set color to black

                c.drawString(x + 2, y - padding + 3, str(cell))

        c.showPage()
    c.save()
    ispdfCreated = True
    return ispdfCreated


def read_events(list_dict, colors):
    for dict_ in list_dict:
        text = dict_['name'].splitlines()
        days = dict_["days"]
        timestr = dict_["time"]
        start_str, _, end_str = timestr.partition("-")
        try:
            start = parse_time(start_str)
            end = parse_time(end_str)
        except ValueError:
            raise ValueError
        if 'color' in dict_.keys():
            m = re.fullmatch(
                r"\s*#?\s*([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})\s*",
                dict_["color"],
            )
            if not m:
                raise click.UsageError("Invalid color: " + repr(dict_["color"]))
            color = (
                int(m.group(1), 16) / 255,
                int(m.group(2), 16) / 255,
                int(m.group(3), 16) / 255,
            )
        else:
            pass
        yield Event(
            start_time=start,
            end_time=end,
            text=text,
            color=color,
            days=[days]  # [d for d, rgx in DAY_REGEXES if re.search(rgx, days)],
        )


def time2hours(t):
    return t.hour + (t.minute + (t.second + t.microsecond / 1000000) / 60) / 60


def timediff(t1, t2):
    # Returns the difference between two `datetime.time` objects as a number of
    # hours
    return time2hours(t2) - time2hours(t1)


def available_fonts():
    return Canvas("").getAvailableFonts()
