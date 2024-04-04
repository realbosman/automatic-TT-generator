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
        self.Sessions_List.pop(index)

    def add_new_session(self, new_session):
        self.Sessions_List.append(new_session)

    def get_algo_reources(self) -> list:
        algo_list = list()
        for lst in self.Sessions_List:
            for index, item in enumerate(lst):
                if item=='--------':
                    pass
                else:
                    algo_list.append(f'<{self.Days["headers"][index]}><{item}>')
        return algo_list


    def set_from_metadata(self,lzt:list):
        correction_index = 0
        for index, day in enumerate(lzt):

            if day[-1] == "_":
                self.Days["headers"].pop(index - correction_index)

                for i, lst in enumerate(self.Sessions_List):
                    lst.pop(index - correction_index)
                    print(self.Sessions_List)
                correction_index += 1
        print(self.Days)
        print(self.Sessions_List)
        print(self.get_sessions())

# TODO LEFT WITH  TIME  EXPRESSIONS TRANSFORM INTO REAL TIME TO VALIDATE IT



