# TODO develop a time system
"""
Pick a course unit check then pick dateTime if the lecturer is not occupied in other course unit 

"""
import random
import re
import time
import webbrowser
from pathlib import Path

from flask import Flask,send_file

from Pdf_Generator.pdf_generator import main as generate_pdf_schedule



class TtGenerator:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        self.progress_var = 0
        self.Full_Time_table_dict=dict()
        self.Full_Time_table_list = list()
        self.TimeTable = {
            "MON": [],
            "TUE": [],
            "WED": [],
            "THUR": [],
            "FRI": [],
            "SAT": [],
            "SUN": [],
        }
        self.list_ = list()
        self.timeslots_lst = list()
        self.class_rooms_lst = list()
        self.created_lectures_details_lst = list()

        # self.edit_TimeTable_days()

        # TODO this generates the pdf file

    def random_generator(self, timeslots_lst, created_lectures_details_lst, class_rooms_lst,title,creator):

        self.timeslots_lst = timeslots_lst
        self.class_rooms_lst = class_rooms_lst
        self.created_lectures_details_lst = created_lectures_details_lst
        self.list_.clear()
        count_created_lectures = len(self.created_lectures_details_lst)

        for i in range(count_created_lectures):
            # TODO this is where if a lecturer has already got or picked time first priority
            # TODO if the rooms are over go get a brand new class rooms
            lecture_picked = random.choice(self.created_lectures_details_lst)

            time_picked = random.choice(self.timeslots_lst)

            space_picked = random.choice(self.class_rooms_lst)

            # TODO what if lecturer_dicts equates to zero when pop is done

            # TODO MANAGE TIME
            if len(self.timeslots_lst) == 0:
                # print("Overlapping IN TIME ")
                break
            # TODO if the rooms are over go get a brand new class rooms


            #TODO: THIS IS WHERE TO ADD THE CREATED TO THE LIST (Remeber to each the overlapping here)

            # print("<><><><><>",lecture_picked,time_picked)

            self.Full_Time_table_list.append(
                f'<{re.findall(r"<(.*?)>",lecture_picked)[2]}><{re.findall(r"<(.*?)>",lecture_picked)[0]}><{space_picked}><{re.findall(r"<(.*?)>",lecture_picked)[1]}><{re.findall(r"<(.*?)>",time_picked)[0]}><{re.findall(r"<(.*?)>",time_picked)[1]}><{re.findall(r"<(.*?)>", lecture_picked)[3]}>'
            )


            self.TimeTable[re.findall(r'<(.*?)>', time_picked)[0]].append(
                str(f'<{re.findall(r"<(.*?)>", lecture_picked)[2]}><{re.findall(r"<(.*?)>", lecture_picked)[0]}><{space_picked}><{re.findall(r"<(.*?)>", lecture_picked)[1]}><{re.findall(r"<(.*?)>", time_picked)[1]}><{re.findall(r"<(.*?)>", lecture_picked)[3]}>'))

            self.timeslots_lst.remove(time_picked)
            self.created_lectures_details_lst.remove(lecture_picked)
            self.class_rooms_lst.remove(space_picked)

            self.progress_var = int((((count_created_lectures - len(
                self.created_lectures_details_lst)) / count_created_lectures)) * 100)
            # print("Progress:", self.progress_var)

            # time.sleep(3)
        self.cleanPrint()
        generate_pdf_schedule(self.get__pdf_resources(),title=title,creator=creator)
        time.sleep(3)
        self.open_pdf()

    def cleanPrint(self):
        print(f'MON = {self.TimeTable["MON"]}')
        print(f'TUE = {self.TimeTable["TUE"]}')
        print(f'WED = {self.TimeTable["WED"]}')
        print(f'THUR = {self.TimeTable["THUR"]}')
        print(f'FRI = {self.TimeTable["FRI"]}')
        print(f'SAT = {self.TimeTable["SAT"]}')
        print(f'SUN = {self.TimeTable["SUN"]}')


    def open_pdf(self):

        pass


    # this should be in the model section
    def edit_TimeTable_days(self):
        print("Are there any days you want to be idle,then select then or pick no?")
        print('''
              MON - 1
              TUE - 2
              WED - 3
              THUR -4
              FRI - 5 
              SAT - 6
              SUN - 7
              None -0
              ''')
        disabled_none = 0
        try:
            disabled_days = int(input("Enter :"))
            disabled_none = disabled_days
        except:
            self.edit_TimeTable_days()

        # TODO THE TIMESLOTS AND THE LECTURES HAVE TO BE IN SYNC timeslot should not be less
        for i in range(1, 8):
            index_count = 0
            # TODO Learn how to use try block
            try:
                str(disabled_days).index(str(i))
                index_count = 1
            except:
                index_count = -1
                pass
            if i == 1 and index_count == 1:
                self.timeslots_lst.pop('MON')
            if i == 2 and index_count == 1:
                self.timeslots_lst.pop('TUE')
            if i == 3 and index_count == 1:
                self.timeslots_lst.pop('WED')
            if i == 4 and index_count == 1:
                self.timeslots_lst.pop('THUR')
            if i == 5 and index_count == 1:
                self.timeslots_lst.pop('FRI')
            if i == 6 and index_count == 1:
                self.timeslots_lst.pop('SAT')
            if i == 7 and index_count == 1:
                self.timeslots_lst.pop('SUN')

        if disabled_none == 0:
            pass
        else:
            try:
                str(disabled_none).index("8")
                disabled_none = 0
                self.edit_TimeTable_days()
            except:
                pass
            try:
                str(disabled_none).index("9")
                disabled_none = 0
                self.edit_TimeTable_days()
            except:
                pass

    def get__pdf_resources(self) -> list:
        # print(self.Full_Time_table_list)
        for faculty in  self.Full_Time_table_list:
            self.Full_Time_table_dict[str(f'{re.findall(r"<(.*?)>", faculty)[1]}')] = dict()  # the faculty dict

        for faculty in  self.Full_Time_table_dict.keys():
            for item in self.Full_Time_table_list:
                txt_item =str(f'{re.findall(r"<(.*?)>", item)[3]}')
                if  str(f'{re.findall(r"<(.*?)>", item)[1]}')== faculty:
                    sep_ = txt_item.split(',')
                    if len(sep_) > 1:
                        for i, text in enumerate(sep_):
                            self.Full_Time_table_dict[faculty][text] = list()
                    else:
                        self.Full_Time_table_dict[faculty][txt_item] = list()


        for faculty in self.Full_Time_table_dict.keys():
            for sub_group in self.Full_Time_table_dict[faculty].keys():
                for item in self.Full_Time_table_list:
                    if str(f'{re.findall(r"<(.*?)>", item)[1]}') == faculty:
                        txt_item=str(f'{re.findall(r"<(.*?)>", item)[3]}')
                        sep_ = txt_item.split(',',-1)
                        # print("Before", txt_item)
                        # print("Sep", sep_)
                        if len(sep_) > 1:

                            for i, text in enumerate(sep_):
                                key=str(f'{re.findall(r"<(.*?)>", item)[4]}')
                                day = None
                                if key == "MON":
                                    day = "Monday"
                                elif key == "TUE":
                                    day = "Tuesday"
                                elif key == "WED":
                                    day = "Wednesday"
                                elif key == "THUR":
                                    day = "Thursday"
                                elif key == "FRI":
                                    day = "Friday"
                                elif key == "SAT":
                                    day = "Saturday"
                                elif key == "SUN":
                                    day = "Sunday"
                                else:
                                    day = None

                                dict_ = {
                                }

                                a, b, c, d, e, f ,g= re.findall(r'<(.*?)>', item)
                                # print("+++",self.TimeTable[key][i])
                                name = d + "," + " " + a + "," + " " + g + "," + " " + c
                                dict_['name'] = name
                                dict_['days'] = day
                                dict_['time'] = f
                                dict_['color'] = "FF94EF"


                                self.Full_Time_table_dict[faculty][text].append(dict_)

                        else:
                            key = str(f'{re.findall(r"<(.*?)>", item)[4]}')
                            day = None
                            if key == "MON":
                                day = "Monday"
                            elif key == "TUE":
                                day = "Tuesday"
                            elif key == "WED":
                                day = "Wednesday"
                            elif key == "THUR":
                                day = "Thursday"
                            elif key == "FRI":
                                day = "Friday"
                            elif key == "SAT":
                                day = "Saturday"
                            elif key == "SUN":
                                day = "Sunday"
                            else:
                                day = None

                            dict_ = {
                            }

                            a, b, c, d, e, f, g = re.findall(r'<(.*?)>', item)
                            # print("+++",self.TimeTable[key][i])
                            name = d + "," + " " + a + "," + " " + g + "," + " " + c
                            dict_['name'] = name
                            dict_['days'] = day
                            dict_['time'] = f
                            dict_['color'] = "FF94EF"

                            self.Full_Time_table_dict[faculty][txt_item].append(dict_)


        print("This fine")
        print(self.Full_Time_table_dict)
        return self.Full_Time_table_dict
