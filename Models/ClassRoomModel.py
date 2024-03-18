class ClassRoomModel:
    classRoomName = ""
    classRoomFaculty = ""

    def __init__(self, class_room_name, class_room_faculty):
        self.classRoomName = class_room_name
        self.classRoomFaculty = class_room_faculty

    def __getitem__(self, item):
        return item

    def getClassRoomDetails(self):
        return [self.classRoomName, self.classRoomFaculty]

    def printClassRoomDetails(self):
        print(f'This is {self.classRoomName}  and Faculty {self.classRoomFaculty}')
