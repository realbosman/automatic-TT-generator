from threading import Thread


class TimeDimension:
    instance = None
    countInstance = 0
    # TOD Make this  dynamic for the user (timeslots)
    '''
    This is a default timeslots dictionary
    '''

    def __init__(self):

        self.Days = {
            "headers": ["MON", "TUE", "WED", "THUR", "FRI", "SAT", "SUN"]
        }

        self.Sessions_List = [

            ['07:30-09:30', "07:30-09:30", "07:30-09:30", "07:30-09:30", "07:30-09:30", "07:30-09:30",
             "07:30-09:30"],
            ["10:00-13:00", "10:00-13:00", "10:00-13:00", "10:00-13:00", "10:00-13:00", "10:00-13:00",
             "10:00-13:00"],
            ["14:00-16:00", "14:00-16:00", "14:00-16:00", "14:00-16:00", "14:00-16:00", "14:00-16:00",
             "14:00-16:00"]
        ]

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
            cls.countInstance += 1
            print(cls.countInstance)
        else:

            print(cls.countInstance)

        return cls.instance

    def get_column_headers(self):
        return self.Days["headers"]

    def get_sessions(self) -> list:
        return self.Sessions_List

    def get_sessions_length(self) -> int:
        return int(len(self.Sessions_List))

    def edit_session(self, index, new_session):
        self.Sessions_List[index] = new_session

    def delete_session(self, index):
        self.Sessions_List.pop(index + 1)

    def add_new_session(self, new_session):
        self.Sessions_List.append(new_session)

    def get_algo_reources(self) -> list:
        algo_list = list()
        for lst in self.Sessions_List:
            for index, item in enumerate(lst):
                if item == '--------':
                    pass
                else:
                    algo_list.append(f'<{self.Days["headers"][index]}><{item}>')
        return algo_list



    def set_from_metadata_thread(self, lzt_: list):
        print("Threading started")
        new_thread = Thread(target=self.set_from_metadata, daemon=True,args=(lzt_,))  # I can pass args = "any" for the target
        new_thread.start()


    def set_from_metadata(self, lzt: list):
        correction_index = 0
        number_of_days_current =len(self.Days)
        for index, day in enumerate(lzt):
            dy = day.split("_")
            print(dy, "//[]", len(dy))
            if len(dy) > 1:
                try:
                    self.Days["headers"].pop(index - correction_index)
                except:
                    print(day, "already has been deleted !")

                for i, lst in enumerate(self.Sessions_List):
                    try:
                        lst.pop(index - correction_index)
                    except:
                        print("Time slot elemnt already deleted")
                    # print(self.Sessions_List)
                correction_index += 1

            else:
                self.Days["headers"].append(dy[0])
                set_1 =set(self.Days["headers"])
                self.Days["headers"],set_2 = self.sort_days(self.Days["headers"])
                if number_of_days_current == len(set_2):
                    print("No added days")
                elif number_of_days_current > len(set_2):
                    num=int(number_of_days_current - len(set_2))
                    print(num,"dayz removed")
                elif number_of_days_current < len(set_2):
                    num=int(len(set_2)-number_of_days_current)
                    print(int(num),"dayz added")



    def sort_days(self, lzt: list) -> list:
        mySet = set(lzt)
        print(mySet)
        list_ = list()
        for n, l in enumerate(mySet):
            list_.append(l)
        for index, day in enumerate(list_):
            if day == "MON":
                list_[index] = 1
            if day == "TUE":
                list_[index] = 2
            if day == "WED":
                list_[index] = 3
            if day == "THUR":
                list_[index] = 4
            if day == "FRI":
                list_[index] = 5
            if day == "SAT":
                list_[index] = 6
            if day == "SUN":
                list_[index] = 7
        print("My list =", list_)
        list_.sort()
        for index_, day_ in enumerate(list_):
            if day_ == 1:
                list_[index_] = "MON"
            if day_ == 2:
                list_[index_] = "TUE"
            if day_ == 3:
                list_[index_] = "WED"
            if day_ == 4:
                list_[index_] = "THUR"
            if day_ == 5:
                list_[index_] = "FRI"
            if day_ == 6:
                list_[index_] = "SAT"
            if day_ == 7:
                list_[index_] = "SUN"
        print("My sorted list =", list_)
        set2=set(list_)

        return list_,set2

# TODO LEFT WITH  TIME  EXPRESSIONS TRANSFORM INTO REAL TIME TO VALIDATE IT
