# TODO develop a time system
"""
Pick a course unit check then pick dateTime if the lecturer is not occupied in other course unit 

"""
import random


class TtGenerator:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, timeslots, created_lectures_details, class_rooms,lecturer_dicts):
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
        self.lecturer_dicts=lecturer_dicts
        self.class_rooms=class_rooms
        self.created_lectures_details = created_lectures_details
        self.edit_TimeTable_days()
        self.random_generator()

    def random_generator(self):
        countCreatedLectures = len(self.created_lectures_details)

        for i in range(countCreatedLectures):
            #TODO this is where if a lecturer has already got or picked time first priority
            #if the rooms are over go get a brand new class rooms
            genL = random.choice(list(self.created_lectures_details))
            key, val = random.choice(list(self.timeSlotObject.items()))
            className, classCapacity = random.choice(list(self.class_rooms.items()))

            lecturer=None
            for value, key_ in self.lecturer_dicts.items():
                print(f'lecturer = {key_} / {genL}')

                if key_ == genL:
                    lecturer=key_
                    print(f'lecturer = {lecturer}')
                    break

            if (len(list(self.timeSlotObject[key])) == 0):
                self.timeSlotObject.pop(key)
                self.random_generator()
                print("pop used")
                break

            genTime = random.choice(list(self.timeSlotObject[key]))
            self.TimeTable[key].append(str(f'<{genL}><{className}><{lecturer}><{genTime}>'))
            self.timeSlotObject[key].remove(genTime)
            self.created_lectures_details.remove(genL)
            self.class_rooms.pop(className)
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
        disabledNone = 0
        try:
            disabledDays = int(input("Enter :"))
            disabledNone = disabledDays
        except:
            self.edit_TimeTable_days()

        # TODO THE TIMESLOTS AND THE LECTURES HAVE TO BE IN SYNC timeslot should not be less
        for i in range(1, 8):
            indexCount = 0
            try:
                str(disabledDays).index(str(i))
                indexCount = 1
            except:
                indexCount = -1
                pass
            if (i == 1 and indexCount == 1):
                self.timeSlotObject.pop('MON')
            if (i == 2 and indexCount == 1):
                self.timeSlotObject.pop('TUE')
            if (i == 3 and indexCount == 1):
                self.timeSlotObject.pop('WED')
            if (i == 4 and indexCount == 1):
                self.timeSlotObject.pop('THUR')
            if (i == 5 and indexCount == 1):
                self.timeSlotObject.pop('FRI')
            if (i == 6 and indexCount == 1):
                self.timeSlotObject.pop('SAT')
            if (i == 7 and indexCount == 1):
                self.timeSlotObject.pop('SUN')

        if (disabledNone == 0):
            pass
        else:
            try:
                str(disabledNone).index("8")
                disabledNone = 0
                self.edit_TimeTable_days()
            except:
                pass
            try:
                str(disabledNone).index("9")
                disabledNone = 0
                self.edit_TimeTable_days()
            except:
                pass
