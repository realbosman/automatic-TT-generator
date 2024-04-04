# TODO develop a time system
"""
Pick a course unit check then pick dateTime if the lecturer is not occupied in other course unit 

"""
import random
import re
from Pdf_Generator.pdf_generator import  main as generate_pdf_schedule



class TtGenerator:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, timeslots_lst, created_lectures_details_lst, class_rooms_lst):
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
        self.timeslots_lst = timeslots_lst
        self.class_rooms_lst = class_rooms_lst
        self.created_lectures_details_lst = created_lectures_details_lst
        # self.edit_TimeTable_days()
        self.random_generator()
        self.cleanPrint()

        # TODO this generates the pdf file
        generate_pdf_schedule(self.get__pdf_resources())

    def random_generator(self):
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
                print("Overlapping IN TIME ")
                break
            # TODO if the rooms are over go get a brand new class rooms

            self.TimeTable[re.findall(r'<(.*?)>', time_picked)[0]].append(
                str(f'<{re.findall(r"<(.*?)>", lecture_picked)[0]}><{space_picked}><{re.findall(r"<(.*?)>", lecture_picked)[1]}><{re.findall(r"<(.*?)>", time_picked)[1]}>'))

            self.timeslots_lst.remove(time_picked)
            self.created_lectures_details_lst.remove(lecture_picked)
            self.class_rooms_lst.remove(space_picked)

    def cleanPrint(self):
        print(f'MON = {self.TimeTable["MON"]}')
        print(f'TUE = {self.TimeTable["TUE"]}')
        print(f'WED = {self.TimeTable["WED"]}')
        print(f'THUR = {self.TimeTable["THUR"]}')
        print(f'FRI = {self.TimeTable["FRI"]}')
        print(f'SAT = {self.TimeTable["SAT"]}')
        print(f'SUN = {self.TimeTable["SUN"]}')

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
        # TODO I HAVE A PROBLEM WITH THE DAY / PDF MAPPING
        for key in self.TimeTable:
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

            for i in range(len(self.TimeTable[key])):
                dict_ = {
                }
                a, b, c, d = re.findall(r'<(.*?)>', self.TimeTable[key][i])
                name=a +" "+ b +" " + c
                dict_['name'] = name
                dict_['days'] = day
                dict_['time'] = d
                dict_['color'] = "FF94EF"
                self.list_.append(dict_)
        return  self.list_
