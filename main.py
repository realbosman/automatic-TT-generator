import random

from Algorithm.Algo import TtGenerator
from Models.ClassRoomModel import ClassRoomModel, ClassRooms
from Models.CourseUnitModel import CourseUnitModel
from Models.Manager import Manager
from Models.CreatedLectures import CreatedLecture, CreatedLectures
from Models.Lecturer_Model import Lecturer_Model
from tabulate import tabulate

from Models.TimeDimension import TimeDimension

if __name__ == '__main__':

    manager = Manager()
    manager.load_data('./files/ROOMS.xlsx', "ClassRoom", 'Room Number')
    manager.load_data('./files/LECTURER DETAILS.xlsx', "CourseUnit", 'Course Unit Name')
    manager.load_data('./files/LECTURER DETAILS.xlsx', "Lecturer", 'Name')
    # print(manager.get_lecturer_list()[:10])
    lect_cu_details=manager.get_lecture_courseUnit_dict(manager.get_courseUnit_list()[:10] ,manager.get_lecturer_list()[:10])
    class_roomZ=ClassRooms()
    # print(manager.get_lecture_courseUnit_dict(manager.get_courseUnit_list()[:10] ,manager.get_lecturer_list()[:10]))


    # print(manager.get_courseUnit_list()[:5])
    # print(manager.get_class_room_list())
    # print(manager.get_lecturer_list())

    time_slots = TimeDimension().get_time_slots()
    Algo = TtGenerator(time_slots, manager.get_courseUnit_list()[:10],class_roomZ.get_classrooms_list(),lect_cu_details)
    Algo.cleanPrint()
