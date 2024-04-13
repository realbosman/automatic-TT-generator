class ClassRoomModel:
    '''
    This is ClassRoomModel ,on initialization is takes classRoom data
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


class SpaceManager:
    '''
       This class manages the space/Class Room
       '''

    instance = None
    countInstance = 0

    def __init__(self):
        self.Headers = {
            "headers": ["Name", "Faculty", "Capacity"]
        }

        self.Space_List = [

            ["Room A", "Science", "50"],
            ["Room B", "Science", "50"],
            ["Room C", "Science", "50"],
            ["Room D", "Science", "50"],
            ["Room E", "Science", "50"],
            ["Room F", "Science", "50"],
            ["Room G", "Science", "50"],
            ["Room H", "Science", "50"],
            ["Room I", "Science", "50"],
            ["Room J", "Science", "50"],
            ["Room A", "Science", "50"],
            ["Room B", "Science", "50"],
            ["Room C", "Science", "50"],
            ["Room D", "Science", "50"],
            ["Room E", "Science", "50"],
            ["Room F", "Science", "50"],
            ["Room G", "Science", "50"],
            ["Room H", "Science", "50"],
            ["Room I", "Science", "50"],
            ["Room J", "Science", "50"],
            ["Room A", "Science", "50"],
            ["Room B", "Science", "50"],
            ["Room C", "Science", "50"],
            ["Room D", "Science", "50"],
            ["Room E", "Science", "50"],
            ["Room F", "Science", "50"],
            ["Room G", "Science", "50"],
            ["Room H", "Science", "50"],
            ["Room I", "Science", "50"],
            ["Room J", "Science", "50"],
            ["Room A", "Science", "50"],
            ["Room B", "Science", "50"],
            ["Room C", "Science", "50"],
            ["Room D", "Science", "50"],
            ["Room E", "Science", "50"],
            ["Room F", "Science", "50"],
            ["Room G", "Science", "50"],
            ["Room H", "Science", "50"],
            ["Room I", "Science", "50"],
            ["Room J", "Science", "50"]

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

    def get_sessions(self) -> list:
        return self.Space_List

    def get_sessions_length(self) -> int:
        return int(len(self.Space_List))

    def edit_session(self, index, new_session):
        self.Space_List[index] = new_session

    def delete_session(self, index):
        self.Space_List.pop(index+1)

    def add_new_session(self, new_session):
        self.Space_List.append(new_session)

    def get_algo_reources(self) -> list:
        algo_list = list()
        for lst in self.Space_List:
            if lst[0] == '--------':
                pass
            else:
                algo_list.append(f'{lst[0]}')
        return algo_list
