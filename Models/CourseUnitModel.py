'''
This is a Cousre Unit Model that holds all the information
about a Couurse Unit Model
'''

class CourseUnitModel:
    CourseUnitName = ""
    CourseUnitFaculty = ""

    def __init__(self, course_unit_name, course_unit_faculty):
        self.CourseUnitName = course_unit_name
        self.CourseUnitFaculty = course_unit_faculty

    def __getitem__(self, item):
        return item

    def getCourseUnitDetails(self):
        return [self.CourseUnitName, self.CourseUnitFaculty]

    def printLecturerDetails(self):
        print(f'Lecturer {self.CourseUnitName}  and Faculty {self.CourseUnitFaculty}')
