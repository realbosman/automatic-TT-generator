class Lecturer_Model:
    lecturerName = ""
    lecturerFaculty = ""

    # TODO Add a dict

    def __init__(self, lecturerName, lecturerFaculty):
        self.lecturerName = lecturerName
        self.lecturerFaculty = lecturerFaculty

    def __getitem__(self, item):
        return item

    def getLecturerDetails(self) -> object:
        return [self.lecturerName, self.lecturerFaculty]

    def printLecturerDetails(self):
        print(f'Lecturer {self.lecturerName}  and Faculty {self.lecturerFaculty}')
