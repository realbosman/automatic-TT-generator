from threading import Thread




class TimeDimension:
    instance = None
    countInstance = 0
    # TOD Make this  dynamic for the user (timeslots)
    '''
    This is a default timeslots dictionary
    '''

    def __init__(self,cls=None):
        self.timetable_metadata=cls
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
        self.set_from_metadata(lzt_)

    def set_from_metadata(self, lzt: list):

        for index, day in enumerate(lzt):
            correction_index = 0
            dy = day.split("_")
            anyDelete= False
            # print(dy, "//[]", len(dy))
            if len(dy) > 1:

               if day[-1] == "_":

                   try:
                       for d_i , d_d in  enumerate(self.Days["headers"]):
                           if dy[0] == d_d:
                               correction_index = d_i
                               print(dy[0], "=======", self.Days["headers"][correction_index])
                               self.Days["headers"].pop(d_i)
                               daylist = self.Days["headers"]
                               self.Days["headers"] = daylist
                               print(day, " has been deleted !")
                               print(self.Days["headers"], " list now !")

                               anyDelete = True
                   except:
                       pass
                    # print(day, "already has been deleted !")

                   if anyDelete:
                       for i, lst in enumerate(self.Sessions_List):
                           try:
                               lst.pop(correction_index)
                           except:
                               pass
                               # print("Time slot elemnt already deleted")
                           # print(self.Sessions_List)


            else:
                isDayin = False
                for check_dy in self.Days["headers"]:
                    if dy[0] == check_dy:
                        # print("day already in",self.Days,dy[0])
                        isDayin = True
                        break
                if isDayin == False:
                    self.Days["headers"].append(dy[0])
                    self.Days["headers"], index_to_add_in_lsts = self.sort_days(self.Days["headers"],dy[0])
                    print("index_to_add_in_lst,",index_to_add_in_lsts,len(self.Sessions_List[0]))
                    # print("day inserted in",self.Days,dy[0])

                    for index_to_add, lst___ in enumerate(self.Sessions_List):
                        if index_to_add_in_lsts == 0:
                            temp_lst=lst___
                            temp_lst2=list()
                            temp_lst2.append('--------')
                            for item in temp_lst:
                                temp_lst2.append(item)
                            self.Sessions_List[index_to_add]=temp_lst2
                        elif (index_to_add_in_lsts+1) > len(self.Sessions_List[0]):
                                temp_lst_ = lst___
                                temp_lst_.append('--------')
                                self.Sessions_List[index_to_add] = temp_lst_
                        elif (index_to_add_in_lsts+1) > len(self.Sessions_List[1]):
                                temp_lst_ = lst___
                                temp_lst_.append('--------')
                                self.Sessions_List[index_to_add] = temp_lst_
                        elif (index_to_add_in_lsts+1) > len(self.Sessions_List[2]):
                                temp_lst_ = lst___
                                temp_lst_.append('--------')
                                self.Sessions_List[index_to_add] = temp_lst_
                        else:
                            temp_lst_1=lst___[index_to_add_in_lsts :]
                            print(temp_lst_1)
                            temp_lst_2 = lst___[: index_to_add_in_lsts]
                            print(temp_lst_2)
                            var_='--------'
                            new_temp_lst_ =[x for x in temp_lst_2]+[var_]+[x for x in temp_lst_1]
                            print(new_temp_lst_)
                            self.Sessions_List[index_to_add] = new_temp_lst_



    def sort_days(self, lzt: list,day_insert:str):
        mySet = set(lzt)
        print(mySet)
        list_ = list()
        index_to_add_in_lst=0
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
        # print("My list =", list_)
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
        # print("My sorted list =", list_)
        for z_, z in enumerate(list_):
            if z==day_insert:
                index_to_add_in_lst=z_


        return list_,index_to_add_in_lst

    def refresh_list_Home_timetable_metadata(self)->list:
        myList=["MON","TUE", "WED","THUR","FRI","SAT","SUN"]
        list_two=list()
        for _day in myList:
            isdayIn=False
            for index, day in enumerate(self.Days["headers"]):
                if _day==day:
                    isdayIn=True
                    break
            if isdayIn == True:
                str_=_day
                list_two.append(str_)
            else:
                str_ = _day + "_"
                list_two.append(str_)

        return  list_two








# TODO LEFT WITH  TIME  EXPRESSIONS TRANSFORM INTO REAL TIME TO VALIDATE IT
