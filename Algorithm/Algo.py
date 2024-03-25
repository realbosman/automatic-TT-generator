# TODO develop a time system
"""
Pick a course unit check then pick dateTime if the lecturer is not occupied in other course unit 

"""
import random
import re


class TtGenerator:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, timeslots, created_lectures_details, class_rooms, lecturer_dicts):
        self.TimeTable = {
            "MON": [],
            "TUE": [],
            "WED": [],
            "THUR": [],
            "FRI": [],
            "SAT": [],
            "SUN": [],
        }
        self.timeSlotObject = timeslots
        self.lecturer_dicts = lecturer_dicts
        self.class_rooms = class_rooms
        self.created_lectures_details = created_lectures_details
        self.edit_TimeTable_days()
        self.random_generator()

    def random_generator(self):
        count_created_lectures = len(self.created_lectures_details)

        for i in range(count_created_lectures):
            # TODO this is where if a lecturer has already got or picked time first priority
            # if the rooms are over go get a brand new class rooms
            gen_l = random.choice(list(self.created_lectures_details))
            key, val = random.choice(list(self.timeSlotObject.items()))
            class_name, class_capacity = random.choice(list(self.class_rooms.items()))

            lecturer = None

            # TODO what if lecturer_dicts equates to zero when popis done
            for key_, value in self.lecturer_dicts.items():
                # print(f'lecturer = {key_}/ {value} / {gen_l}')

                if value == gen_l:
                    lecturer = key_
                    # print(f'lecturer = {lecturer}')
                    # print(f'lecturer = {key_}/ {value} / {gen_l}')
                    # print(self.lecturer_dicts)
                    self.lecturer_dicts.pop(key_)
                    break

            if len(list(self.timeSlotObject[key])) == 0:
                self.timeSlotObject.pop(key)
                self.random_generator()
                print("pop used")
                break

            gen_time = random.choice(list(self.timeSlotObject[key]))
            self.TimeTable[key].append(str(f'<{gen_l}><{class_name}><{lecturer}><{gen_time}>'))
            words_between_angle_brackets = re.findall(r'<(.*?)>',
                                                      str(f'<{gen_l}><{class_name}><{lecturer}><{gen_time}>'))
            print(words_between_angle_brackets)
            self.timeSlotObject[key].remove(gen_time)
            self.created_lectures_details.remove(gen_l)
            self.class_rooms.pop(class_name)
            # print(f'classes = {self.class_rooms.keys()}')

        # print(self.TimeTable)

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
                self.timeSlotObject.pop('MON')
            if i == 2 and index_count == 1:
                self.timeSlotObject.pop('TUE')
            if i == 3 and index_count == 1:
                self.timeSlotObject.pop('WED')
            if i == 4 and index_count == 1:
                self.timeSlotObject.pop('THUR')
            if i == 5 and index_count == 1:
                self.timeSlotObject.pop('FRI')
            if i == 6 and index_count == 1:
                self.timeSlotObject.pop('SAT')
            if i == 7 and index_count == 1:
                self.timeSlotObject.pop('SUN')

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
