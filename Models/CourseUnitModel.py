
from  Models.Lecturer_Model import TutorsManager
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
        self.Headers = {
            "headers": ["Name","Tutor", "Faculty","Group"]
        }

        self.Session_List = [

            ["OOP",  "Mr.Kasozi","Science",],
            ["PYTHON",  "Mr.TONY","Science"],
            ["POP", "Mr.REAGAN","Science"],
            ["WEB",  "Madam MIREMBE","Science"]

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
                if Name==new_session[1]:
                    # TODO if at all a lecture teaches more than one
                    break
            else:
                lst_ = [f'{new_session[1]}', f'{new_session[0]}', '--------']
                self.tutor.add_new_tutor(lst_,index=-1)






    def delete_session(self, index):
        self.Session_List.pop(index)

    def add_new_session(self, new_session):
        self.Session_List.append(new_session)
        lst=[f'{new_session[1]}',f'{new_session[0]}','--------']
        self.tutor.add_new_tutor(lst)

    def get_algo_reources(self) -> list:
        algo_list = list()
        for lst in self.Session_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'<{lst[0]}><{lst[1]}>')
        return algo_list
