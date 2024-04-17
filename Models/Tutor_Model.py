


class Lecturer_Model:
    '''
      This is a class shows a list Tutors with the necessary info about them
    '''

    def __init__(self, lecturer_name, lecturer_course_unit):
        self.lecturer_dict = dict()
        self.lecturer_dict = lecturer_name
        self.lecturer_course_unit = lecturer_course_unit
        self.lecturer_dict[self.lecturer_dict] = self.lecturer_course_unit
        # print(self.classRoomModel_dict)

    def getlecturerDetails(self):
        return self.lecturer_dict


class TutorsManager:
    '''
       This class manages the space
       '''

    instance = None
    countInstance = 0


    Headers = {
        "headers": ["Name", "Session", "Faculty"]
    }

    Space_List = [

        ["Mr.Kasozi", "OOP", "Science"],
        ["Mr.TONY", "PYTHON", "Science"],
        ["Mr.REAGAN", "POP", "Science"],
        ["Madam MIREMBE", "WEB", "Science"]

    ]


    @staticmethod
    def get_column_headers():
        return TutorsManager.Headers["headers"]

    @staticmethod
    def get_tutors() -> list:
        return TutorsManager.Space_List

    @staticmethod
    def get_tutors_length() -> int:
        return int(len(TutorsManager.Space_List))

    @staticmethod
    def edit_tutors(index, new_session):
        TutorsManager.Space_List[index] = new_session

    @staticmethod
    def delete_tutor(index):
        TutorsManager.Space_List.pop(index + 1)

    @staticmethod
    def add_new_tutor(new_session, index=None):
        if index is None:
            TutorsManager.Space_List.append(new_session)
        else:
            TutorsManager.Space_List[index] = new_session

    @staticmethod
    def get_algo_reources() -> list:
        algo_list = list()
        for lst in TutorsManager.Space_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'{lst[0]}')
        return algo_list
