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

    def __init__(self):
        self.Headers = {
            "headers": ["Name","Session", "Faculty" ]
        }

        self.Space_List = [

            [ "Mr.Kasozi", "OOP","Science"],
            [ "Mr.TONY","PYTHON", "Science"],
            [ "Mr.REAGAN","POP", "Science"],
            [ "Madam MIREMBE","WEB", "Science"]

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

    def get_tutors(self) -> list:
        return self.Space_List

    def get_tutors_length(self) -> int:
        return int(len(self.Space_List))

    def edit_tutors(self, index, new_session):
        self.Space_List[index] = new_session

    def delete_tutor(self, index):
        self.Space_List.pop(index+1)

    def add_new_tutor(self, new_session,index=None):
        if index is None:
            self.Space_List.append(new_session)
        else:
            self.Space_List[index]=new_session



    def get_algo_reources(self) -> list:
        algo_list = list()
        for lst in self.Space_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'{lst[0]}')
        return algo_list
