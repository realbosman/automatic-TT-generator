# TODO develop a time system
"""
Pick a course unit check then pick dateTime if the lecturer is not occupied in other course unit 

"""
import random


class TtGenerator:
    instance = None
    timeSlotObject = None
    created_lectures_details = None

    TimeTable = {
        "MON": [],
        "TUE": [],
        "WED": [],
        "THUR": [],
        "FRI": [],
        "SAT": [],
        "SUN": [],
    }

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, timeslots, created_lectures_details):
        self.timeSlotObject = timeslots
        self.created_lectures_details = created_lectures_details
        self.random_generator()

    def random_generator(self):
        countCreatedLectures = len(self.created_lectures_details)

        for i in range(countCreatedLectures):
            genL = random.choice(list(self.created_lectures_details))
            genD = key, val = random.choice(list(self.timeSlotObject.items()))

            if (len(list(self.timeSlotObject[key])) == 0):
                self.timeSlotObject.pop(key)
                self.random_generator()
                print("pop used")
                break

            genTime = random.choice(list(self.timeSlotObject[key]))
            self.TimeTable[key].append(str(genL + genTime))
            self.timeSlotObject[key].remove(genTime)
            self.created_lectures_details.remove(genL)
        # print(self.TimeTable)

    def cleanPrint(self):
        print(f'MON = {self.TimeTable["MON"]}')
        print(f'TUE = {self.TimeTable["TUE"]}')
        print(f'WED = {self.TimeTable["WED"]}')
        print(f'THUR = {self.TimeTable["THUR"]}')
        print(f'FRI = {self.TimeTable["FRI"]}')
        print(f'SAT = {self.TimeTable["SAT"]}')
        print(f'SUN = {self.TimeTable["SUN"]}')
