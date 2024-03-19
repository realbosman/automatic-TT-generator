import pandas as pd


class Manager:
    instance = None

    def __init__(self):

        self.lecturer_list = list()
        self.classRoom_list = list()
        self.course_unit_list = list()
        self.lecture_courseUnit_dict = dict()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def Add_to_lecture_list(self, lecturer_object):
        self.lecturer_list.append(lecturer_object)

    def Add_to_courseUnit_list(self, course_object):
        self.course_unit_list.append(course_object)

    def Add_to_classRoom_list(self, class_room_object):
        self.classRoom_list.append(class_room_object)

    def get_lecturer_list(self):
        return self.lecturer_list

    def get_class_room_list(self):
        return self.classRoom_list

    def get_lecture_courseUnit_dict(self, func_l_list, func_cu_list):

        for i in range(len(func_l_list)):

            self.lecture_courseUnit_dict[func_cu_list[i]] = func_l_list[i]
        return self.lecture_courseUnit_dict

    def get_courseUnit_list(self):
        return self.course_unit_list

    def load_data(self, data_path, destination, targetcolumn):
        df = pd.read_excel(data_path)
        # print(len(df[targetcolumn]))
        col_length = len(df[targetcolumn])
        if destination == 'ClassRoom':
            for i in range(col_length):
                self.Add_to_classRoom_list(str(df[targetcolumn][i]))
        if destination == 'CourseUnit':
            for i in range(col_length):
                self.Add_to_courseUnit_list(str(df[targetcolumn][i]))
        if destination == 'Lecturer':
            for i in range(col_length):
                self.Add_to_lecture_list(str(df[targetcolumn][i]))
        # print("done")
