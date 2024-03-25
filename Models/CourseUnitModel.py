class CourseUnitModel:
    '''
    This class creates a new CourseUnitModel
    '''
    instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance



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



