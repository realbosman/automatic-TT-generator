class CreatedLecture:


    def __init__(self):
        print("a lecture has been created")

    def __getitem__(self, items):
        self.lectureID = items[0]
        self.lectureName = items[1]
        self.lectureInstructor = items[2]
        self.lectureLocation = items[3]
        self.lectureTime = items[4]

    # By default, lectureTime is "" unless the lecturer wants specific time
    def getCreatedLectureDetails(self):
        return f'{self.lectureID}/{self.lectureName}/' \
               f'{self.lectureInstructor}/' \
               f'{self.lectureLocation}/' \
               f'{self.lectureTime}'


class CreatedLectures:
    instance = None
    createdLectureSet = set()

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def Add_to_CreatedLecturesSet(self, created_lecture_object):
        self.createdLectureSet.add(created_lecture_object)

    def get_created_lectures_set(self):
        mySet = self.createdLectureSet
        return mySet
