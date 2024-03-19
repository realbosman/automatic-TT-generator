class Lecturers:
    instance = None



    def __init__(self):
        self.Lecturers_ = {

        }


    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    # This takes in a dictionary that holds lecturers with their specifics
    def __getitem__(self, items):
        self.Lecturers_.clear()
        for i in range(len(items)):
            key = list(items[i].keys())
            val = list(items[i].values())
            print(f'key {key} {val}')
            self.Lecturers_[key[0]] = val[0]

    def edit_Lecturers_dict(self, new_lecturer_object):
        pass
        # self.Lecturers_.clear()
        # key = list(new_clas_room.keys())
        # val = list(new_clas_room.values())
        # self.Lecturers_[key[0]] = val[0]

    def get_Lecturers_list(self):
        return self.Lecturers_


class Lecturer_Model:
    '''
     make the attributes in the  __init__ to be for only one class
    '''

    def __init__(self, lecturer_name, lecturer_course_unit):
        self.lecturer_dict = dict()
        self.lecturer_dict = lecturer_name
        self.lecturer_course_unit = lecturer_course_unit
        self.lecturer_dict[self.lecturer_dict] = self.lecturer_course_unit
        # print(self.classRoomModel_dict)

    def getlecturerDetails(self):
        return self.lecturer_dict
