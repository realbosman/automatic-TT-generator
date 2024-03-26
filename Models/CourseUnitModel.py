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

class CourseUnits:
    '''
       This is a class shows a Curse units with the necessary info about them
       '''
    instance = None
    def __init__(self):
        self.CourseUnits_ = {

        }


    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    # This takes in a dictionary that holds CourseUnits with their specifics
    def __getitem__(self, items):
        self.CourseUnits_.clear()
        for i in range(len(items)):
            key = list(items[i].keys())
            val = list(items[i].values())
            print(f'key {key} {val}')
            self.CourseUnits_[key[0]] = val[0]

    def edit_CourseUnits_dict(self, new_lecturer_object):
        pass
        # self.Lecturers_.clear()
        # key = list(new_clas_room.keys())
        # val = list(new_clas_room.values())
        # self.Lecturers_[key[0]] = val[0]

    def get_CourseUnits_list(self):
        return self.CourseUnits_



