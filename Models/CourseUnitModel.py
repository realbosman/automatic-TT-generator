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
            # "headers": ["NAME", "TUTOR", "FACULTY", "PROGRAM", "NO OF STUDENTS"]
            "headers": ["NAME", "TUTOR", "FACULTY", "PROGRAM", "NO OF STUDENTS", 'MODE OF TEACHING', "TUTOR'S EMAIL","LINK"]
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
        self.Session_List = self.Session_List_

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
                FAC_ = f'FACULTY OF {lst[2]}'
                algo_list.append(f'<{FAC_}><{lst[3]}><{lst[0]}><{lst[1]}><{lst[4]}><{lst[5]}><{lst[7]}><{lst[4]}>')
        return algo_list

    def update_tutor_list(self) -> list:
        algo_list = list()
        for lst in self.Session_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'<{lst[2]}><{lst[3]}><{lst[0]}><{lst[1]}><{lst[6]}>')

        # TutorsManager.Tutor_List=algo_list
        return algo_list

    def get_tutors_(self):
        lst = list()
        lst2 = list()

        TutorsManager.Tutor_List.clear()
        # getting the names of all Tutors to know who is already in the list
        for n in TutorsManager.Tutor_List:
            for i in n:
                lst2.append(n[0])
                # print('This now  =-=',TutorsManager.Tutor_List )

        lst = self.update_tutor_list()
        # print("<><><><",lst)

        for lecture in lst:
            if str(re.findall(r"<(.*?)>", lecture)[3]) in lst2:
                # print("Already in")
                pass
            else:
                TutorsManager.Tutor_List.append(
                    [str(re.findall(r"<(.*?)>", lecture)[3]), str(re.findall(r"<(.*?)>", lecture)[2]),
                     str(re.findall(r"<(.*?)>", lecture)[0]), str(re.findall(r"<(.*?)>", lecture)[4])])
                # print("This==", [str(re.findall(r"<(.*?)>", lecture)[3]), str(re.findall(r"<(.*?)>", lecture)[2]), str(re.findall(r"<(.*?)>", lecture)[0])])

        # Sort the list by the first element (tutor's name)
        TutorsManager.Tutor_List.sort(key=lambda x: x[0].upper())

        # Group the sorted list by the first element (tutor's name)
        grouped_tutors = [list(group) for key, group in groupby(TutorsManager.Tutor_List, key=lambda x: x[0])]

        # Flatten the grouped list back into the original format
        TutorsManager.Tutor_List = [item for sublist in grouped_tutors for item in sublist]

        # self.replace_lec(0,1)
        new_updatded_list = list()
        last_index_for_lect = 0
        next_index = 0

        for index___, item in enumerate(TutorsManager.Tutor_List):
            # print(item,index___)
            # print("LLLKKLKLLKLKL")
            # print(last_index_for_lect+next_index ,"==",index___)
            equ_index = last_index_for_lect + next_index
            if equ_index == index___:
                next_index = index___
                new_updatded_list.append(item)
                for i, item_next in enumerate(TutorsManager.Tutor_List[index___ + 1:]):
                    v0, v1, v2, v3 = item_next
                    if item_next[0] == item[0]:
                        new_updatded_list.append([" ", v1, v2, v3])
                        # print("UU-====", last_index_for_lect," ",i, ["----", v1, v2, v3], index___)
                    else:
                        last_index_for_lect = i + 1
                        # print("N-====",last_index_for_lect,["----", v1, v2, v3],index___)
                        # print(new_updatded_list)
                        break

        # print("TutorsManager.Tutor_List ===",TutorsManager.Tutor_List)

        return new_updatded_list

    def replace_lec(self, index, next_index):
        # print("NNN")
        lect_pointer = TutorsManager.Tutor_List[index][0]
        # print("NNN-",TutorsManager.Tutor_List[index])

        if (len(TutorsManager.Tutor_List) > index + 1):
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
            # "headers": ["NAME", "TUTOR", "FACULTY", "PROGRAM", "NO OF STUDENTS"]
            "headers": ["NAME", "TUTOR", "FACULTY", "PROGRAM", "NO OF STUDENTS", 'MODE OF TEACHING', "TUTOR'S EMAIL","LINK"]
        }

        self.Session_List = [
            ['--------', '--------', '--------', '--------', '--------', '--------', '--------','--------'],

        ]
        self.session_number_tracker = list()
        self.session_number_tracker.append(0)
        self.count_session_number = 0

        self.set_groups_cu()

    def save_instance_reload(self):

        self.Session_List = Listener.saveInstanceDict["SessionManager"]["Session_List"]
        TutorsManager.Tutor_List.clear()
        self.Session_List__= [
            ['DIPS 2204 ETHICS IN AN IT ENVIROMENT', 'DR. CELESTINE SAFARI ', 'SCIENCE', 'DIP CS II', 10, 'BLENDED',
             'snamagembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 1204 COMPUTATIONAL STATISTICS', 'NAMAGEMBE OLIVIA', 'SCIENCE', 'BSC IT I,BSC CS I', 65, 'BLENDED',
             'snamagembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['MTC 2201 PARTIAL DIFFERENCIAL EQUATIONS ', 'DR. BOB SSENYANGE', 'SCIENCE', 'BSC GEN II,BSC FM II', 3,
             'BLENDED', 'bssenyange@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['MTC 3201 NUMERICAL ANALYSIS II', 'DR. HENRY KIWANUKA ', 'SCIENCE', 'BSC GEN III', 7, 'BLENDED',
             'hkiwanuka@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS1205 DATABASE PLANNING & MANAGEMENT', 'KALEMA PETER', 'SCIENCE', 'DIP CS I', 25, 'ONLINE',
             'pkalema@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS 2202 COMPUTER GRAPHICS & ANNIMATION', 'MUCHAKE BRIAN', 'SCIENCE', 'DIP CS II', 10, 'BLENDED',
             'bmuchake@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 1201 SYSTEM ANALYSIS & DESIGN', 'BABIRYE NANTEZA LUCY', 'SCIENCE', 'BSC CS I,BSC IT I', 65, 'BLENDED',
             'nbabirye@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO 1202 PRINCIPLES OF DEVELOPMENT ECONOMICS', 'FREDRICK KATO', 'SCIENCE', 'BSC ECON & STAT I,BSC GEN I',
             13, 'BLENDED', 'not available',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 2201 USER INTERFACE DESIGN & DEVELOPMENT', 'MIREMBE EVA', 'SCIENCE', 'BSC IT II,BSC CS II', 27,
             'BLENDED', 'emirembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO 2201 MACROECONOMICS II', 'KIMONO PAUL', 'SCIENCE', 'BSC ECON & STAT II,BSC GEN II', 13, 'PHYSICAL ',
             'paulkimono@yahoo.com',"NO LINK"],
            ['CSC 3201 COMPUTER GRAPHICS & ANNIMATIONS', 'MUCHAKE BRIAN', 'SCIENCE',
             'BSC IT III,BSC CS III,BSC GEN III', 40, 'ONLINE', 'bmuchake@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO3202 PUBLIC SECTOR ECONOMICS', 'KAKUNGULU MOSES', 'SCIENCE', 'BSC ECON & STAT III', 11, 'BLENDED',
             'mkakungulu@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['COMPUTER ARCHITECTURE', 'LUBOWA SAMUEL', 'SCIENCE', 'DIP CS I', 25, 'ONLINE', 'slubowa@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['COMPUTER ARCHITECTURE & ORGANISATION', 'LUBOWA SAMUEL', 'SCIENCE', 'BSC IT I', 45, 'ONLINE',
             'slubowa@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['MTC 1201 CALCULUS II', 'DR. BOB SSENYANGE ', 'SCIENCE', 'BSC ECON & STAT I,BSC GEN I', 13, 'BLENDED',
             'bssenyange@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 2206 COMPILER DESIGN & CONSTRUCTION', 'xxxx', 'SCIENCE', 'BSC CS II', 7, 'BLENDED', 'not available',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA 2201 PROBABILITY THEORY', 'LOKOLIMOI JOHN BOSCO', 'SCIENCE', 'BSC GEN II', 1, 'BLENDED',
             'jblokolimoi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA2102 DEMOGRAPHIC & SOCIAL STATISTICS', 'MUJUNI PEREZ', 'SCIENCE', 'BSC ECON & STAT II', 11, 'BLENDED',
             'pmujuni@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA 2201 PROBABILITY THEORY', 'LOKOLIMOI JOHN BOSCO', 'SCIENCE', 'BSC FM II', 2, 'BLENDED',
             'jblokolimoi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 3203 ENTREPRENEURSHIP', 'BYARUGABA BENJAMIN', 'SCIENCE', 'BSC IT III,BSC CS III', 33, 'BLENDED',
             'not available',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA 3201 DEMOGRAPHIC & SOCIAL STATISTICS', 'MUJUNI PEREZ', 'SCIENCE', 'BSC GEN III', 7, 'BLENDED',
             'pmujuni@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS 2204 PROGRAMMING METHODOOGY WITH VB.NET', 'BABIRYE NANTEZA LUCY', 'SCIENCE', 'DIP CS II', 10,
             'BLENDED', 'nbabirye@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 1205 LOGIC PROGRAMMING', 'xxxx', 'SCIENCE', 'BSC CS I', 20, 'BLENDED', 'not available',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA1202 MATHEMATHICAL STATISTICS 1', 'LOKOLIMOI JOHN BOSCO', 'SCIENCE', 'BSC ECON & STAT I', 12,
             'BLENDED', 'jblokolimoi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CLS 2201 ORIGINAL & CRITICAL LANGUAGE SKILLS', 'PROF. LAURA OTAALA', 'SCIENCE',
             'BSC IT II,BSC CS II,BSC GEN II,BSC ECON & STAT II,BSC FM II', 41, 'BLENDED', 'lotaala@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 3202 SOFTWARE ENGINEERING', 'LUBOWA SAMUEL', 'SCIENCE', 'BSC CS III,BSC GEN III', 16, 'BLENDED',
             'slubowa@umu.ac.ug ',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS1202 INTERNET TECHNOLOGIES & WEB AUTHORING', 'LUWAGA DENIS', 'SCIENCE', 'DIP CS I', 25, 'ONLINE',
             'dluwaga@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 1202  OBJECT ORIENTED PROGRAMMING ', 'SSEMWEZI ANDREW', 'SCIENCE', 'BSC IT I,BSC CS I', 65, 'ONLINE',
             'assemwezi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC1201 COMPUTER PROGRAMMING', 'KUBANJA MARTIN ', 'SCIENCE',
             'BSC ECON & STAT I,BSC IT II,BSC CS II,BSC GEN II', 40, 'ONLINE', 'mkubanja@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO 3201 INTERMEDIATE MARCOECONOMIC THEORY', 'MUBIINZI GEOFFREY', 'SCIENCE',
             'BSC GEN III,BSC ECON & STAT III', 18, 'BLENDED', 'gmubiinzi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS1103 INTRODUCTION TO PROGRAMMING', 'KASOZI BRIAN', 'SCIENCE', 'DIP CS I', 25, 'ONLINE',
             'bkasozi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC1104 PRINCIPLES OF PROGRAMMING', 'KASOZI BRIAN', 'SCIENCE', 'BSC IT I', 45, 'ONLINE',
             'bkasozi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA1102 STATISTICAL ORGANISATION ', 'NAMAGEMBE CHARLOTTEE ', 'SCIENCE', 'BSC ECON & STAT I,BSC GEN I', 13,
             'BLENDED', 'snamagembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['MTC 1202 ORDINARY EQUSTIONS I', 'DR. OLIVIA NABAWANDA', 'SCIENCE', 'BSC GEN II', 1, 'BLENDED',
             'onabawanda@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA1102 STATISTICAL ORGANISATION ', 'NAMAGEMBE CHARLOTTEE ', 'SCIENCE', 'BSC ECON & STAT II', 11,
             'BLENDED', 'onabawanda@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA 3203 NATIONAL INCOME ACCOUNTS', 'DR. MBABAZI FULGENSIA', 'SCIENCE', 'BSC GEN III', 7, 'ONLINE',
             'fmbabazi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA3202 NATIONAL ACCOUNTS & INCOME ANALYSIS', 'DR. MBABAZI FULGENSIA', 'SCIENCE', 'BSC ECON & STAT III',
             11, 'ONLINE', 'fmbabazi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['WEB DEVELOPMENT TECHNOLOGIES', 'MIREMBE EVA', 'SCIENCE', 'BSC IT I', 45, 'ONLINE', 'emirembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['MATHEMATHICAL STATISTICS II', 'LOKOLIMOI JOHN BOSCO', 'SCIENCE', 'BSC ECON & STAT I', 12, 'BLENDED',
             'jblokolimoi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['TIME SERIES & REGRESSION ANALYSIS ', 'MUJUNI PEREZ', 'SCIENCE', 'BSC FM II,BSC GEN II', 3, 'BLENDED',
             'pmujuni@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA 3201 SAMPLING THEORY', 'MUJUNI PEREZ', 'SCIENCE', 'BSC GEN III', 7, 'BLENDED', 'pmujuni@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS1204 DISCOVER I NETWORKING BASICS', 'NAIGENDE DUNCAN', 'SCIENCE', 'DIP CS I', 25, 'BLENDED',
             'dnaigende@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 1203 DATABASE MANAGEMENT SYSTEMS', 'KALEMA PETER', 'SCIENCE', 'BSC IT I,BSC CS I', 65, 'ONLINE',
             'pkalema@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 2203 RESEARCH METHODS IN IT', 'DR. SHEBA NYAKAISIKI', 'SCIENCE', 'BSC IT II,BSC CS II', 27, 'ONLINE',
             'snyakaisiki@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['COC 2201 RESEARCH METHODOLOGY  & DATA ANALYSIS', 'DR. MBABAZI FULGENSIA', 'SCIENCE',
             'BSC ECON & STAT II,BSC GEN II', 12, 'ONLINE', 'fmbabazi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO 3203 MONEY, BANKING & PUBLIC FINANCE', 'KADDU MILLY', 'SCIENCE', 'BSC GEN III', 7, 'BLENDED',
             'mkaddu@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO3203 MONETARY ECONOMICS', 'KADDU MILLY', 'SCIENCE', 'BSC ECON & STAT III', 11, 'BLENDED',
             'mkaddu@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS 2203 ELECTRONIC COMMERCE & ELECTRONIC BUSINESS FUNDAMENTALS ', 'xxxx', 'SCIENCE', 'DIP CS II', 10,
             'BLENDED', 'not available',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA 1201 TIME SERIES & INDEX NUMBERS', 'MUJUNI PEREZ', 'SCIENCE', 'BSC ECON & STAT II,BSC GEN II', 12,
             'BLENDED', 'pmujuni@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['LITERATURE & COMPOSITION', 'NAKYEJJWE CHRISTINE', 'SCIENCE',
             'BSC IT I,BSC ECON & STAT I,BSC GEN I,BSC CS I', 68, 'BLENDED', 'cnakyejjwe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO 2202 ECONOMETRICS', 'MUBIINZI GEOFFREY', 'SCIENCE', 'BSC ECON & STAT II,BSC GEN II', 13, 'BLENDED',
             'gmubiinzi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 3204  SCIENCE, TECHNOLOGY  & ETHICS', 'DR. WILLIAM KAGGWA', 'SCIENCE',
             'BSC IT III,BSC GEN III,BSC CS III', 40, 'BLENDED', 'mwkaggwa@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA3203 STATISTICAL METHODS', 'NAMAGEMBE CHARLOTTEE', 'SCIENCE', 'BSC ECON & STAT III', 11, 'BLENDED',
             'cnamagembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS1203 COMPUTER MAINTANANCE & TROUBLE SHOOTING', 'NAGAWA VIOLET', 'SCIENCE', 'DIP CS I', 25, 'BLENDED',
             'vnagawa@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO 1201 MACROECONOMICS I', 'KIMONO PAUL', 'SCIENCE', 'BSC ECON & STAT I,BSC GEN I', 13, 'BLENDED',
             'paulkimono@yahoo.com',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 2204 MOBILE COMPUTING & NET WORKS', 'DR. SANYA RAHMAN', 'SCIENCE', 'BSC IT II,BSC GEN II,BSC CS II',
             28, 'ONLINE', 'rsanya@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA3201 ECONOMETRICS II', 'MUBIINZI GEOFFREY', 'SCIENCE', 'BSC ECON & STAT III', 11, 'BLENDED',
             'gmubiinzi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS 2202 COMPUTER GRAPHICS & ANNIMATIONS', 'MUCHAKE BRIAN', 'SCIENCE', 'DIP CS II', 10, 'BLENDED',
             'bmuchake@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['NUMERICAL METHODS', 'SSEMBATYA FRANCIS', 'SCIENCE', 'BSC CS I', 20, 'BLENDED', 'fssembatya@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 2205 LINEAR PROGRAMMING', 'NAMAGEMBE CHARLOTTEE', 'SCIENCE', 'BSC CS II', 7, 'BLENDED',
             'cnamagembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['MTC 2202 LENEAR PROGRAMMING', 'NAMAGEMBE CHARLOTTEE', 'SCIENCE', 'BSC FM II,BSC GEN II', 3, 'BLENDED',
             'cnamagembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['COC 3201 SCIENCE, ECONOMICS & ETHICS', 'DR. WILLIAM KAGGWA', 'SCIENCE', 'BSC ECON & STAT III,BSC GEN III',
             18, 'BLENDED', 'mwkaggwa@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS  2201 DEVELOPMENT RESEARCH (INDIVIDUAL PROJECT)', 'KALEMA PETER', 'SCIENCE', 'DIP CS II', 10,
             'BLENDED', 'pkalema@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 1206 DIGITAL ELECTRONICS', 'xxxx', 'SCIENCE', 'BSC CS I', 20, 'BLENDED', 'not available',"http://meet.google.com/ysn-ixek-ibk"],
            ['STA 1202 ELEMENTS OF PROBABILITY', 'LOKOLIMOI JOHN BOSCO', 'SCIENCE', 'BSC GEN I', 1, 'BLENDED',
             'jblokolimoi@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['PEF 2201 ETHICS IN FOCUS', 'ENZAMA REMIJO', 'SCIENCE',
             'BSC IT II,BSC FM II,BSC ECON & STAT II,BSC GEN II,BSC CS II', 41, 'BLENDED', 'renzama@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['DIPS1201 INTRODUCTION TO COMPUTER SCIENCE & TECHNOLOGY II', 'BABIRYE NANTEZA LUCY', 'SCIENCE', 'DIP CS I',
             25, 'BLENDED', 'nbabirye@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['CSC 2202 WEB BASED SYSTEMS PROGRAMMING', 'MIREMBE EVA', 'SCIENCE', 'BSC IT II,BSC GEN II,BSC CS II', 28,
             'BLENDED', 'emirembe@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"],
            ['MTF 2201 LIFE & NON LIFE INSSURANCE MATHEMATHICS', 'xxxx', 'SCIENCE', 'BSC FM II', 2, 'BLENDED',
             'not available',"http://meet.google.com/ysn-ixek-ibk"],
            ['ECO 2203 ECONOMICS OF AGRICULTURE', 'NABASUMBA SYLVIA', 'SCIENCE', 'BSC ECON & STAT II,BSC GEN II', 12,
             'BLENDED', 'snabasumba@umu.ac.ug',"http://meet.google.com/ysn-ixek-ibk"]
            ]
