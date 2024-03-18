import random

from Algorithm.Algo import TtGenerator
from Models.ClassRoomModel import ClassRoomModel
from Models.CourseUnitModel import CourseUnitModel
from Models.Manager import Manager
from Models.CreatedLectures import CreatedLecture, CreatedLectures
from Models.Lecturer_Model import Lecturer_Model
from tabulate import tabulate

from Models.TimeDimension import TimeDimension

if __name__ == '__main__':
    '''
    classRoom = ClassRoomModel("Room 11", "Science")
    Lecturer = Lecturer_Model("Mr.Kasozi Brian", "Science")
    CourseUnit = CourseUnitModel("Programming", "Science")
    Lecturer1 = Lecturer_Model("Mr.Anthony", "Science")
    CourseUnit1 = CourseUnitModel("OOP", "Science")

    CUL = CourseUnit_Lecturer_Model()
    CUL.Add_to_courseUnit_list(CourseUnit.getCourseUnitDetails())
    CUL.Add_to_lecture_list(Lecturer.getLecturerDetails())
    CUL.Add_to_courseUnit_list(CourseUnit1.getCourseUnitDetails())
    CUL.Add_to_lecture_list(Lecturer1.getLecturerDetails())
   

    print(CUL.get_lecture_list())
    print(CUL.get_courseUnit_list())
    print(df['Room Number'][0])
     '''
    '''manager = Manager()
    manager.load_data('./files/ROOMS.xlsx', "ClassRoom", 'Room Number')
    manager.load_data('./files/LECTURER DETAILS.xlsx', "CourseUnit", 'Course Unit Name')
    manager.load_data('./files/LECTURER DETAILS.xlsx', "Lecturer", 'Name')

    print(manager.get_courseUnit_list())
    print(manager.get_class_room_list())
    print(manager.get_lecturer_list())'''

    """lectures = CreatedLectures()
    for i in range(10):
        lecture = CreatedLecture()
        lecture["hshgs", 'sjgg', "jhgsjd", "hsgdjsg", "hdgha"]
        lectures.Add_to_CreatedLecturesSet(lecture.getCreatedLectureDetails() + str(i))
        print(lecture.getCreatedLectureDetails())
    print(lectures.get_created_lectures_set())

    table = [
        
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 3, 4, 5, 6, 7]

    ]"""

    """headers = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    print(tabulate(table, headers, tablefmt="grid"))

    time_dimension = TimeDimension()
    res = key, val = random.choice(list(time_dimension.get_time_slots().items()))
    time_dimension.get_time_slots()["MON"].append("4")
    print(str(res))
    print(time_dimension.get_time_slots())
    print(time_dimension.get_time_slots().keys())
    print(time_dimension.get_time_slots().get("MON"))"""

    manager = Manager()
    manager.load_data('./files/ROOMS.xlsx', "ClassRoom", 'Room Number')
    manager.load_data('./files/LECTURER DETAILS.xlsx', "CourseUnit", 'Course Unit Name')
    manager.load_data('./files/LECTURER DETAILS.xlsx', "Lecturer", 'Name')

    # print(manager.get_courseUnit_list()[:5])
    # print(manager.get_class_room_list())
    # print(manager.get_lecturer_list())

    time_slots = TimeDimension().get_time_slots()
    Algo = TtGenerator(time_slots, manager.get_courseUnit_list()[:10])
    Algo.cleanPrint()
