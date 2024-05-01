import re

from Models.Listener import Listener
from Models.Tutor_Model import TutorsManager


class CourseUnitModel:
    '''
    This class creates a new CourseUnitModel
    '''

    def __init__(self, course_unit_name, course_unit_faculty):
        self.CourseUnitName = ""
        self.CourseUnitFaculty = ""
        self.CourseUnitName = course_unit_name
        self.CourseUnitFaculty = course_unit_faculty

    def __getitem__(self, item):
        return item

    def getCourseUnitDetails(self):
        return [self.CourseUnitName, self.CourseUnitFaculty]

    def printCourseDetails(self):
        print(f'Lecturer {self.CourseUnitName}  and Faculty {self.CourseUnitFaculty}')


class SessionManager:
    '''
       This class manages the space
       '''

    instance = None
    countInstance = 0

    def __init__(self):

        self.Groups_set = set()
        self.faculty_set = set()

        self.Headers = {
            "headers": ["Name", "Tutor", "Faculty", "Group", "Capacity"]
        }

        self.Session_List = [
            ["WEB", "Madam MIREMBE", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["DIPS1205 DATABASE PLANNING & MANAGEMENT", "KALEMA PETER", "SCIENCE", "DIP CS 1"],
            ["DIPS1202 INTERNET TECHNOLOGIES & WEB AUTHORING", "LUBOWA SAMUEL", "SCIENCE", "DIP CS 1"],
            ["DIPS1204 DISCOVER I NETWORKING BASICS", "NAIGENDE DUNCAN", "SCIENCE", "DIP CS 1"],
            ["DIPS1203 COMPUTER MAINTANANCE & TROUBLE SHOOTING", "NAGAWA VIOLET", "SCIENCE", "DIP CS 1"],
            ["DIPS1201 INTRODUCTION TO COMPUTERSCIENCE & TECHNOLOGY II", "BABIRYE NANTEZA LUCY", "SCIENCE", "DIP CS 1"],
            ["CSC 1201 SYSTEMANALYSIS & DESIGN", "LUBOWA SAMUEL", "SCIENCE", "DIP CS 1"],
            ["CSC 1202 OBJECT ORIENTED PROGRAMMING", "KALEMA PETER", "SCIENCE", "DIP CS 1"],
            ["PROGRAMMING", "KASOZI BRIAN", "SCIENCE", "DIP CS 1"],
            ["CSC 1204 COMPUTATIONAL STATISTICS", "NAMAGEMBE OLIVIA", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["WEB DEVELOPMENT TECHNOLOGIES", "MIREMBE EVA", "SCIENCE", "BSC IT 1"],
            ["CSC 1202 OBJECTORIENTED PROGRAMMING", "Mr. KASAAZI George William", "SCIENCE", "BSC IT 1"],
            ["COMPUTER 1 CSC 1203 DATABASE MANAGEMENT SYSTEMS", "KALEMA PETER", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["CSC 1201 SYSTEM ANALYSIS & DESIGN", "LUBOWA SAMUEL", "SCIENCE", "BSC CS 1,BSC IT 1"],
            ["CSC1104 PRINCIPLES OF PROGRAMMING", "KASOZI BRIAN", "SCIENCE", "BSC IT 1"],
            ["My", "Tony", "BAM", "BAM 1"]
        ]
        self.session_number_tracker = list()
        self.session_number_tracker.append(0)
        self.count_session_number = 0

        self.set_groups_cu()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
            cls.countInstance += 1
            # print(cls.countInstance)
        else:
            pass

            # print(cls.countInstance)

        return cls.instance

    def get_column_headers(self):
        return self.Headers["headers"]

    def get_sessions(self) -> list:
        return self.Session_List

    def get_sessions_length(self) -> int:
        return int(len(self.Session_List))

    def edit_session(self, index, new_session):
        self.Session_List[index] = new_session
        # TODO need  a thread and the append if at all a lecture teaches more than one
        for lst in TutorsManager.get_tutors():
            for i, Name in enumerate(lst):
                if Name == new_session[1]:
                    # TODO if at all a lecture teaches more than one
                    return
        lst_ = [f'{new_session[1]}', f'{new_session[0]}', '--------']
        TutorsManager.add_new_tutor(lst_, index=None)

    def set_groups_cu(self):
        for index, lst in enumerate(self.Session_List):
            d = lst[3].split(',')
            if len(d) > 1:
                for i, sub_group in enumerate(d):
                    if d[i] == "--------":
                        pass
                    else:
                        self.Groups_set.add(f'<{lst[2]}><{d[i]}>')
            else:
                if lst[3] == "--------":
                    pass
                else:
                    self.Groups_set.add(f'<{lst[2]}><{lst[3]}>')
        # print(self.Groups_set)
        # print(self.get_faculty_cu())

    def get_faculty_cu(self):
        for index, lst in enumerate(self.Session_List):
            if lst[2] == "--------":
                pass
            else:
                self.faculty_set.add(lst[2])
        return self.faculty_set

    def get_sub_groups(self):
        self.set_groups_cu()
        return self.Groups_set

    def get_sub_groups_commbo(self) -> list:
        self.get_sub_groups()
        lst = list()
        for item in self.Groups_set:
            lst.append(str(re.findall(r"<(.*?)>", item)[1]))
        return lst

    def delete_session(self, index):
        self.Session_List.pop(index + 1)

    def add_new_session(self, new_session):
        self.Session_List.append(new_session)
        lst = [f'{new_session[1]}', f'{new_session[0]}', '--------']
        TutorsManager.add_new_tutor(lst)

    def get_algo_reources(self) -> list:
        algo_list = list()
        for lst in self.Session_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'<{lst[2]}><{lst[3]}><{lst[0]}><{lst[1]}>')
        return algo_list

    def update_tutor_list(self) -> list:
        algo_list = list()
        for lst in self.Session_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'<{lst[2]}><{lst[3]}><{lst[0]}><{lst[1]}>')
        return algo_list

    def get_tutors_(self):
        lst = list()
        lst2 = list()

        # getting the names of all Tutors to know who is already in the list
        for n in TutorsManager.Space_List:
            for i in n:
                lst2.append(n[0])

        lst = self.update_tutor_list()

        for lecture in lst:
            if str(re.findall(r"<(.*?)>", lecture)[3]) in lst2:
                pass
            else:
                TutorsManager.Space_List.append(
                    [str(re.findall(r"<(.*?)>", lecture)[3]), str(re.findall(r"<(.*?)>", lecture)[2]), '--------'], )

        return TutorsManager.Space_List

    def check_for_empty_slots(self) -> bool:
        for lst in self.Session_List:
            for item in lst:
                if item == '--------':
                    return True

    def get_the_number_of_Tutor_sessions(self) -> int:
        Tutor_dict = dict()
        Tutor_list = list()
        tutor_track_no_session = 0
        for Tutor in self.Session_List:
            Tutor_dict[Tutor[1]] = list()
            Tutor_list.append(Tutor[1])

        for key in Tutor_dict.keys():
            count = 0
            for item in Tutor_list:
                if key == item:
                    count = count + 1
            Tutor_dict[key].append(count)
            if count >= tutor_track_no_session:
                tutor_track_no_session = count
        # print(Tutor_dict)
        # print(tutor_track_no_session)
        Tutor_dict.clear()
        Tutor_list.clear()

        return tutor_track_no_session

    # make sure to run this in the background
    def get_largest_session_number_in_a_subgroup(self) -> int:
        lst = self.get_sub_groups_commbo()
        lst2 = self.get_algo_reources()
        # print("COMBO",lst)
        # print("RES", lst2)
        temp = 0

        for item in lst:
            # print("count_session_number = ",self.count_session_number)
            self.count_session_number = 0
            # print("back to zero", self.count_session_number)

            for k in lst2:
                # print("k", k)
                d = str(re.findall(r"<(.*?)>", k)[1]).split(',')

                # print('d=', d)

                if len(d) > 1:
                    # print('Length d')
                    for i, sub_group in enumerate(d):
                        if item == sub_group:
                            # print(f'{item} == {sub_group}')
                            self.count_session_number = self.count_session_number + 1

                else:
                    if item == d[0]:
                        # print('else')
                        # print(f'{item} == {d[0]}')
                        self.count_session_number = self.count_session_number + 1

            # print(item, "====", self.count_session_number)
            if self.count_session_number >= temp:
                temp = self.count_session_number
            # print("LLL", temp)

        return temp

    def tutors_lst(self) -> list:
        tutors_set = set()
        for lst in self.Session_List:
            # print(lst[1])
            tutors_set.add(lst[1])
            # print("TUTR=====", tutors_set)
        return list(tutors_set)

    def save_instance_(self):
        Listener.saveInstanceDict["SessionManager"] = {
            "Session_List": self.Session_List
        }

    # Reset every variable to pepare new file
    def new_file_(self):
        self.Groups_set = set()
        self.faculty_set = set()

        self.Headers = {
            "headers": ["Name", "Tutor", "Faculty", "Group", "Capacity"]
        }

        self.Session_List = [
            ["Session Name", "Tutor Name", "Faculty Name", "Group Name", "AUTO"],

        ]
        self.session_number_tracker = list()
        self.session_number_tracker.append(0)
        self.count_session_number = 0

        self.set_groups_cu()

    def save_instance_reload(self):

        self.Session_List = Listener.saveInstanceDict["SessionManager"]["Session_List"]


