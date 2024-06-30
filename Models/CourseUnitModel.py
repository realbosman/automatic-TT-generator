import re

from Models.Listener import Listener
from Models.Tutor_Model import TutorsManager
from itertools import groupby



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
            "headers": ["Name", "Tutor", "Faculty", "Program", "Capacity"]
        }

        self.Session_List = [
            ["DIPS1205 DATABASE PLANNING & MANAGEMENT", "KALEMA PETER", "SCIENCE", "DIP CS 1"],
            ["DIPS1202 INTERNET TECHNOLOGIES & WEB AUTHORING", "LUBOWA SAMUEL", "SCIENCE", "DIP CS 1"],
            ["DIPS1204 DISCOVER I NETWORKING BASICS", "NAIGENDE DUNCAN", "SCIENCE", "DIP CS 1"],
            ["DIPS1203 COMPUTER MAINTANANCE & TROUBLE SHOOTING", "Ms. Nagawa Viola", "SCIENCE", "DIP CS 1"],
            ["DIPS1201 INTRODUCTION TO COMPUTERSCIENCE & TECHNOLOGY II", "BABIRYE NANTEZA LUCY", "SCIENCE", "DIP CS 1"],
            ["CSC 1201 SYSTEMANALYSIS & DESIGN", "LUBOWA SAMUEL", "SCIENCE", "DIP CS 1"],
            ["CSC 1202 OBJECT ORIENTED PROGRAMMING", "KALEMA PETER", "SCIENCE", "DIP CS 1"],
            ["PROGRAMMING", "Mr KASOZI BRIAN", "SCIENCE", "DIP CS 1"],
            ["CSC 1204 COMPUTATIONAL STATISTICS", "NAMAGEMBE OLIVIA", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["WEB DEVELOPMENT TECHNOLOGIES", "MIREMBE EVA", "SCIENCE", "BSC IT 1"],
            ["CSC 1202 OBJECTORIENTED PROGRAMMING", "Mr. KASAAZI George William", "SCIENCE", "BSC IT 1"],
            ["COMPUTER 1 CSC 1203 DATABASE MANAGEMENT SYSTEMS", "KALEMA PETER", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["CSC 1201 SYSTEM ANALYSIS & DESIGN", "LUBOWA SAMUEL", "SCIENCE", "BSC CS 1,BSC IT 1"],
            ["CSC1104 PRINCIPLES OF PROGRAMMING", "Mr KASOZI BRIAN", "SCIENCE", "BSC IT 1"],
            ["CSC 3202 SOFTWARE ENGINEERING", "Ms. Nagawa Viola", "SCIENCE", "BSC IT 3"],
            ["CSC 3201 COMPUTER GRAPHICS & ANNIMATIONS", "Mr. KIRUMIRA, Samuel", "SCIENCE",
             "BSC GEN 3,BSC IT 3,BSC CS 3"],
            ["August Academic literacy and reading skills", "Justine Lugolobi", "SCIENCE",
             "LLB 1,B.ENVI.DES 1,BAFT I,BCMHP I"],
            ["MATHEMATICS 2 MTH 2203 Numerical Analysis", "Dr. Fr. Kiwanuka Henry", "SCIENCE", "BSC GEN 2,BSC CS 2"],
            ["MATHEMATICS 2 Partial Differential Equations", "Dr. Senyange Bob", "SCIENCE", "BSC GEN 2,BSC FM 2"],
            ["STA 1201 TIME SERIES & INDEX NUMBERS", "MUJUNI PEREZ", "SCIENCE", "BSC GEN 2,BSC ECON & STAT 2"],
            ["STA2102 DEMOGRAPHIC & SOCIAL STATISTICS ", "MUJUNI PEREZ", "SCIENCE", "BSC ECON & STAT 2,BSC GEN 3"],
            ["MATHEMATICS 3 MTH 3201 Number Theory", "Dr. Fr. Kiwanuka Henry", "SCIENCE", "BSC GEN 3"],
            ["STA 3203 NATIONAL INCOME ACCOUNTS", "Mr. Kato Bbosa John", "SCIENCE", "BSC GEN 3"],
            ["MTC 3201 NUMERICAL ANALYSIS II", "Dr. Fr. Kiwanuka Henry", "SCIENCE", "BSC GEN 3,BSC FM 3"],
            ["ECO 1202 PRINCIPLES OF DEVELOPMENT ECONOMICS", "FREDRICK KATO", "SCIENCE", "BSC ECON & STAT 1"],
            ["ECO 1201 MACROECONOMICS I", "FREDRICK KATO", "SCIENCE", "BSC GEN 1,BSC ECON & STAT 1"],
            ["MTC 1201 CALCULUS II", "DR. BOB SSENYANGE", "SCIENCE", "BSC GEN 1,BSC ECON & STAT 1"],
            ["METHODOLOGY & DATA ANALYSIS", "DR. MBABAZI FULGENSIA", "SCIENCE", "BSC ECON & STAT 2"],
            ["STA1102 STATISTICAL ORGANISATION", "NAMAGEMBE CHARLOTTEE", "SCIENCE", "BSC GEN 1,BSC ECON & STAT 1"]

        ]

        self.Session_List_ = [
            ["DIPS1205 DATABASE PLANNING & MANAGEMENT", "KALEMA PETER", "SCIENCE", "DIP CS 1"],
            ["DIPS1202 INTERNET TECHNOLOGIES & WEB AUTHORING", "LUBOWA SAMUEL", "SCIENCE", "DIP CS 1"],
            ["DIPS1204 DISCOVER I NETWORKING BASICS", "NAIGENDE DUNCAN", "SCIENCE", "DIP CS 1"],
            ["DIPS1203 COMPUTER MAINTANANCE & TROUBLE SHOOTING", "Ms. Nagawa Viola", "SCIENCE", "DIP CS 1"],
            ["DIPS1201 INTRODUCTION TO COMPUTERSCIENCE & TECHNOLOGY II", "BABIRYE NANTEZA LUCY", "SCIENCE", "DIP CS 1"],
            ["CSC 1201 SYSTEMANALYSIS & DESIGN", "LUBOWA SAMUEL", "SCIENCE", "DIP CS 1"],
            ["CSC 1202 OBJECT ORIENTED PROGRAMMING", "KALEMA PETER", "SCIENCE", "DIP CS 1"],
            ["PROGRAMMING", "Mr KASOZI BRIAN", "SCIENCE", "DIP CS 1"],
            ["CSC 1204 COMPUTATIONAL STATISTICS", "NAMAGEMBE OLIVIA", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["WEB DEVELOPMENT TECHNOLOGIES", "MIREMBE EVA", "SCIENCE", "BSC IT 1"],
            ["CSC 1202 OBJECTORIENTED PROGRAMMING", "Mr. KASAAZI George William", "SCIENCE", "BSC IT 1"],
            ["COMPUTER 1 CSC 1203 DATABASE MANAGEMENT SYSTEMS", "KALEMA PETER", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["CSC 1201 SYSTEM ANALYSIS & DESIGN", "LUBOWA SAMUEL", "SCIENCE", "BSC CS 1,BSC IT 1"],
            ["CSC1104 PRINCIPLES OF PROGRAMMING", "Mr KASOZI BRIAN", "SCIENCE", "BSC IT 1"],
            ["CSC 3202 SOFTWARE ENGINEERING", "Ms. Nagawa Viola", "SCIENCE", "BSC IT 3"],
            ["CSC 3201 COMPUTER GRAPHICS & ANNIMATIONS", "Mr. KIRUMIRA, Samuel", "SCIENCE",
             "BSC GEN 3,BSC IT 3,BSC CS 3"],
            ["August Academic literacy and reading skills", "Justine Lugolobi", "SCIENCE",
             "LLB 1,B.ENVI.DES 1,BAFT I,BCMHP I"],
            ["MATHEMATICS 2 MTH 2203 Numerical Analysis", "Dr. Fr. Kiwanuka Henry", "SCIENCE", "BSC GEN 2,BSC CS 2"],
            ["MATHEMATICS 2 Partial Differential Equations", "Dr. Senyange Bob", "SCIENCE", "BSC GEN 2,BSC FM 2"],
            ["STA 1201 TIME SERIES & INDEX NUMBERS", "MUJUNI PEREZ", "SCIENCE", "BSC GEN 2,BSC ECON & STAT 2"],
            ["STA2102 DEMOGRAPHIC & SOCIAL STATISTICS ", "MUJUNI PEREZ", "SCIENCE", "BSC ECON & STAT 2,BSC GEN 3"],
            ["MATHEMATICS 3 MTH 3201 Number Theory", "Dr. Fr. Kiwanuka Henry", "SCIENCE", "BSC GEN 3"],
            ["STA 3203 NATIONAL INCOME ACCOUNTS", "Mr. Kato Bbosa John", "SCIENCE", "BSC GEN 3"],
            ["MTC 3201 NUMERICAL ANALYSIS II", "Dr. Fr. Kiwanuka Henry", "SCIENCE", "BSC GEN 3,BSC FM 3"],
            ["ECO 1202 PRINCIPLES OF DEVELOPMENT ECONOMICS", "FREDRICK KATO", "SCIENCE", "BSC ECON & STAT 1"],
            ["ECO 1201 MACROECONOMICS I", "FREDRICK KATO", "SCIENCE", "BSC GEN 1,BSC ECON & STAT 1"],
            ["MTC 1201 CALCULUS II", "DR. BOB SSENYANGE", "SCIENCE", "BSC GEN 1,BSC ECON & STAT 1"],
            ["METHODOLOGY & DATA ANALYSIS", "DR. MBABAZI FULGENSIA", "SCIENCE", "BSC ECON & STAT 2"],
            ["STA1102 STATISTICAL ORGANISATION", "NAMAGEMBE CHARLOTTEE", "SCIENCE", "BSC GEN 1,BSC ECON & STAT 1"]

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

    def set_new_list(self):
        self.Session_List=self.Session_List_

    def get_sessions(self) -> list:
        return self.Session_List

    def get_sessions_length(self) -> int:
        return int(len(self.Session_List))

    def edit_session(self, index, new_session):
        self.Session_List[index] = new_session
        # TODO need  a thread and the append if at all a lecture teaches more than one
        # print("NSHGSGSGJGS",new_session)
        # for lst in TutorsManager.get_tutors():
        #     for i, Name in enumerate(lst):
        #         if Name == new_session[1]:
        #             # TODO if at all a lecture teaches more than one
        #             return
        lst_ = [f'{new_session[1]}', f'{new_session[0]}', f'{new_session[2]}']
        TutorsManager.add_new_tutor(lst_, index)
        # print("lishshds,",lst_)

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
        lst = [f'{new_session[1]}', f'{new_session[0]}', f'{new_session[2]}']
        TutorsManager.add_new_tutor(lst)
        # print("lst new session",lst)

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

        # TutorsManager.Tutor_List=algo_list
        return algo_list

    def get_tutors_(self):
        lst = list()
        lst2 = list()

        # getting the names of all Tutors to know who is already in the list
        for n in TutorsManager.Tutor_List:
            for i in n:
                lst2.append(n[0])
                # print('This now  =-=',TutorsManager.Tutor_List )


        lst = self.update_tutor_list()


        for lecture in lst:
            if str(re.findall(r"<(.*?)>", lecture)[3]) in lst2:
                pass
            else:
                TutorsManager.Tutor_List.append(
                    [str(re.findall(r"<(.*?)>", lecture)[3]), str(re.findall(r"<(.*?)>", lecture)[2]), str(re.findall(r"<(.*?)>", lecture)[0])], )
                # print("This==", [str(re.findall(r"<(.*?)>", lecture)[3]), str(re.findall(r"<(.*?)>", lecture)[2]), str(re.findall(r"<(.*?)>", lecture)[0])])

        # Sort the list by the first element (tutor's name)
        TutorsManager.Tutor_List.sort(key=lambda x: x[0].upper())

        # Group the sorted list by the first element (tutor's name)
        grouped_tutors = [list(group) for key, group in groupby(TutorsManager.Tutor_List, key=lambda x: x[0])]

        # Flatten the grouped list back into the original format
        TutorsManager.Tutor_List = [item for sublist in grouped_tutors for item in sublist]

        # self.replace_lec(0,1)

        # print("TutorsManager.Tutor_List ===",TutorsManager.Tutor_List)

        return TutorsManager.Tutor_List

    def replace_lec(self,index,next_index):
        # print("NNN")
        lect_pointer = TutorsManager.Tutor_List[index][0]
        # print("NNN-",TutorsManager.Tutor_List[index])

        if (len(TutorsManager.Tutor_List) > index+1):
            if (len(TutorsManager.Tutor_List) > next_index):
                # print("top;;;;;;")
                if lect_pointer == TutorsManager.Tutor_List[next_index][0]:
                    TutorsManager.Tutor_List[index + 1][0] = "->"
                    self.replace_lec(index, next_index + 1)
                    # print("Made it",TutorsManager.Tutor_List[index + 1])
                else:
                    self.replace_lec(next_index, next_index + 1)
                    # print("Made Next")










    def check_for_empty_slots(self) -> bool:
        for lst in self.Session_List:
            for item in lst:
                if item == '--------':
                    return True

    def check_for_empty_slots_(self) -> bool:
        return False

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
            "headers": ["Name", "Tutor", "Faculty", "Program", "Capacity"]
        }

        self.Session_List = [
            ['--------', '--------', '--------', '--------', '--------'],

        ]
        self.session_number_tracker = list()
        self.session_number_tracker.append(0)
        self.count_session_number = 0

        self.set_groups_cu()

    def save_instance_reload(self):

        self.Session_List = Listener.saveInstanceDict["SessionManager"]["Session_List"]


