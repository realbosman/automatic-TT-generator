class ClassRooms:
    '''
    This class holds all the class rooms
    '''
    instance = None

    def __init__(self):
        self.ClassRooms_ = {
            "Room A": [30],
            "Room B": [30],
            "Room C": [30],
            "Room D": [30],
            "Room E": [30],
            "Room F": [30],
            "Room G": [30],
            "Room H": [30],
            "Room I": [30],
            "Room J": [30],
            "Room K": [30],
            "Room L": [30],
            "Room M": [30],
            "Room N": [30],
            "Room O": [30],
            "Room P": [30],
            "Room  ONLINE": ["ANY"],
        }

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    # This takes in a dictionary that holds classes with their specifics
    def __getitem__(self, items):
        self.ClassRooms_.clear()
        for i in range(len(items)):
            key = list(items[i].keys())
            val = list(items[i].values())
            print(f'key {key} {val}')
            self.ClassRooms_[key[0]] = val[0]

    def edit_class_rooms(self, new_clas_room):
        pass
        # self.ClassRooms_.clear()
        # key = list(new_clas_room.keys())
        # val = list(new_clas_room.values())
        # self.ClassRooms_[key[0]] = val[0]

    def get_classrooms_list(self):
        return self.ClassRooms_


class ClassRoomModel:
    '''
     This class creates  a class room
    '''

    def __init__(self, class_room_name, class_room_capacity):
        # self.classRoomModel_dict.clear()
        self.classRoomModel_dict = dict()
        self.classRoomName = class_room_name
        self.classRoomCapacity = class_room_capacity
        self.classRoomModel_dict[self.classRoomName] = self.classRoomCapacity
        # print(self.classRoomModel_dict)

    def getClassRoomDetails(self):
        return self.classRoomModel_dict

# mylist = [ClassRoomModel("Room AAAAAA", "3000").getClassRoomDetails(),
#           ClassRoomModel("Room AAAAAA2", "3000").getClassRoomDetails(),
#           ClassRoomModel("Room AAAAAA3", "3000").getClassRoomDetails()]
#
# classRoomz = ClassRooms()
# # TODO how to do [for i in ranae] in a list
# classRoomz[mylist]
#
# print(classRoomz.get_classrooms_list())
# # my_list = [i for i in range(10)]
# print(list(classRoomz.ClassRooms_.keys()))
#
