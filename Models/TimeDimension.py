class TimeDimension:
    instance = None
    countInstance = 0
    # TOD Make this  dynamic for the user (timeslots)
    '''
    This is a default timeslots dictionary
    '''

    def __init__(self):

        self.TimeSlotsDict = {
            "MON": ["07:30-09:30", "10:00-13:00", "02:00-16:00"],
            "TUE": ["07:30-09:30", "10:00-13:00", "02:00-16:00"],
            "WED": ["07:30-09:30", "10:00-13:00", "02:00-16:00"],
            "THUR": ["07:30-09:30", "10:00-13:00", "02:00-16:00"],
            "FRI": ["07:30-09:30", "10:00-13:00", "02:00-16:00"],
            "SAT": ["07:30-09:30", "10:00-13:00", "02:00-16:00"],
            "SUN": ["07:30-09:30", "10:00-13:00", "02:00-16:00"]
        }
        self.tupleList = list()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
            cls.countInstance += 1
            print(cls.countInstance)
        else:

            print(cls.countInstance)

        return cls.instance

    def edit_time_slots(self, new_time_slots_object):
        self.TimeSlotsDict = new_time_slots_object

    def edit_time_slot(self, day, data):
        self.TimeSlotsDict[day].append(data)

    def get_time_slots(self):
        return self.TimeSlotsDict

    def get_time_slot(self, day):
        return self.TimeSlotsDict[day]

    def tuple_time_slot(self):
        self.tupleList.clear()

        sessionNum = 0
        for key in self.TimeSlotsDict:
            if (len(self.TimeSlotsDict[key]) > sessionNum):
                sessionNum = len(self.TimeSlotsDict[key])

            else:
                sessionNum = sessionNum
        if (sessionNum == 0):
            self.tupleList.append(ListCreator())
        else:
            for i in range(sessionNum):
                lzt = ListCreator()
                for k in self.TimeSlotsDict:
                    if len(self.TimeSlotsDict[k]) < (i + 1):
                        lzt.add_to_list('--------')
                    else:
                        lzt.add_to_list(self.TimeSlotsDict[k][i])
                self.tupleList.append(lzt.get_list())

        print(self.tupleList)

    '''
    Use this method to edit the TimeDict 
    '''

    def edit_dict_time_slot(self, new_tuple, index_):
        new_tuple_ = new_tuple

        for index, key in enumerate(self.TimeSlotsDict.keys()):
            tempLzt = self.TimeSlotsDict[key]
            print(index_, len(tempLzt), key)

            if index_ >= len(tempLzt):
                if (new_tuple_[index] != '--------'):
                    tempLzt.append(new_tuple_[index])
                    self.TimeSlotsDict[key] = tempLzt
                else:
                    pass

            else:
                if (new_tuple_[index] != '--------'):
                    tempLzt[index_] = new_tuple_[index]
                    self.TimeSlotsDict[key] = tempLzt
                else:
                    pass
        print(self.TimeSlotsDict, "<><><><><")

        print(">>>>>>", self.tupleList)

    def remove_row_(self,row_to_remove):

        for index, key in enumerate(self.TimeSlotsDict.keys()):
            if row_to_remove >= len(self.TimeSlotsDict[key]):
                pass
            else:
                list_=self.TimeSlotsDict[key]
                list_.pop(row_to_remove)
                self.TimeSlotsDict[key]=list_
        print(">>>>> Removed Row",self.TimeSlotsDict)





    def get_tuple_list_length(self):
        return len(self.tupleList)

    def get_tuple_list_list(self, pos):
        print(self.tupleList)
        return self.tupleList[pos]

    def new_time_slots(self, day, data_list):
        self.TimeSlotsDict = {
            "MON": [],
            "TUE": [],
            "WED": [],
            "THUR": [],
            "FRI": [],
            "SAT": [],
            "SUN": []
        }




# TODO ADD BREAK POINTS

class ListCreator:
    def __init__(self):
        self.lst = []

    def get_list(self):
        return self.lst

    def add_to_list(self, data):
        self.lst.append(data)

# t=TimeDimension()
# t.tuple_time_slot()
# f=t.get_tuple_list_list(1)
# print(f)
