from Models.Lecturer_Model import TutorsManager


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

        self.tutor = TutorsManager()
        self.Groups_set = set()
        self.faculty_set = set()

        self.Headers = {
            "headers": ["Name", "Tutor", "Faculty", "Group"]
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
            ["CSC 1204 COMPUTATIONAL STATISTICS", "NAMAGEMBE OLIVIA ", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["WEB DEVELOPMENT TECHNOLOGIES", "MIREMBE EVA", "SCIENCE", "BSC IT 1"],
            ["CSC 1202 OBJECTORIENTED PROGRAMMING", "Mr. KASAAZI George William", "SCIENCE", "BSC IT 1"],
            ["COMPUTER 1 CSC 1203 DATABASE MANAGEMENT SYSTEMS", "KALEMA PETER", "SCIENCE", "BSC IT 1,BSC CS 1"],
            ["CSC 1201 SYSTEM ANALYSIS & DESIGN", "LUBOWA SAMUEL", "SCIENCE", "BSC CS 1,BSC IT 1"],
            ["CSC1104 PRINCIPLES OF PROGRAMMING", "KASOZI BRIAN", "SCIENCE", "BSC IT 1"]
        ]

        # self.set_groups_cu()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
            cls.countInstance += 1
            print(cls.countInstance)
        else:

            print(cls.countInstance)

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
        for lst in self.tutor.get_tutors():
            for i, Name in enumerate(lst):
                if Name == new_session[1]:
                    # TODO if at all a lecture teaches more than one
                    break
            else:
                lst_ = [f'{new_session[1]}', f'{new_session[0]}', '--------']
                self.tutor.add_new_tutor(lst_, index=-1)

    def set_groups_cu(self):
        for index, lst in enumerate(self.Session_List):
            d = lst[3].split(',')
            if len(d) > 1:
                for i, sub_group in enumerate(d):
                    self.Groups_set.add(f'<{lst[2]}><{d[i]}>')
            else:
                self.Groups_set.add(f'<{lst[2]}><{lst[3]}>')
        # print(self.Groups_set)
        # print(self.get_faculty_cu())

    def get_faculty_cu(self):
        for index, lst in enumerate(self.Session_List):
            self.faculty_set.add(lst[2])
        return self.faculty_set

    def get_sub_groups(self):
        self.set_groups_cu()
        return self.Groups_set

    def delete_session(self, index):
        self.Session_List.pop(index + 1)

    def add_new_session(self, new_session):
        self.Session_List.append(new_session)
        lst = [f'{new_session[1]}', f'{new_session[0]}', '--------']
        self.tutor.add_new_tutor(lst)

    def get_algo_reources(self) -> list:
        algo_list = list()
        for lst in self.Session_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'<{lst[2]}><{lst[3]}><{lst[0]}><{lst[1]}>')
        return algo_list
