from Models.Listener import Listener


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

    Tutor_List = [

        # ["Mr.Kasozi", "OOP", "Science"],
        # ["Mr.TONY", "PYTHON", "Science"],
        # ["Mr.REAGAN", "POP", "Science"],
        # ["Madam MIREMBE", "WEB", "Science"]

    ]


    @staticmethod
    def get_column_headers():
        return TutorsManager.Headers["headers"]

    @staticmethod
    def get_tutors() -> list:
        return TutorsManager.Tutor_List

    @staticmethod
    def get_tutors_length() -> int:
        return int(len(TutorsManager.Tutor_List))

    @staticmethod
    def edit_tutors(index, new_session):
        TutorsManager.Tutor_List[index] = new_session

    @staticmethod
    def delete_tutor(index):
        TutorsManager.Tutor_List.pop(index + 1)

    @staticmethod
    def add_new_tutor(new_session, index=None):
        if index is None:
            TutorsManager.Tutor_List.append(new_session)
        else:
            TutorsManager.Tutor_List[index] = new_session

    @staticmethod
    def get_algo_reources() -> list:
        algo_list = list()
        for lst in TutorsManager.Tutor_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'{lst[0]}')
        return algo_list

    @staticmethod
    def  save_instance_():
        Listener.saveInstanceDict["TutorsManager"]={
            "Space_List": TutorsManager.Tutor_List
        }

    # Reset every variable to pepare new file
    @staticmethod
    def new_file_():
        TutorsManager.Headers = {
            "headers": ["Name", "Program", "Faculty"]
        }

        TutorsManager.Tutor_List = [

            ["--------", "--------", "--------"],

        ]

    @staticmethod
    def save_instance_reload():
        TutorsManager.Tutor_List=Listener.saveInstanceDict["TutorsManager"]["Space_List"]





