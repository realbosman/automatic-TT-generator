from Models.Listener import Listener
from Models.TimeDimension import TimeDimension


class TimetableMetaData:
    """
    This TimetableMetaData holds all the information about the created time table project
    such as :
    -time table name
    -creator
    -days in a week
    -preferences
    """

    instance = None
    isInfoSet = False
    time_table_name = "Timetbale Name"
    creator_name = ""
    institute_name = ""
    creators_email = " "
    preferences_list_ = list()

    # This makes sure that the is only one instance of the TimetableMetaData at a time.
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self, cls=None):
        self.timeDimension__ = cls

    def set_timetable_information(self,
                                  is_set: bool
                                  , time_table_name_: str
                                  , creator_name: str
                                  , institute_name: str
                                  , creators_email: str
                                  , days_list: list
                                  , preferences_list: list):
        TimetableMetaData.isInfoSet = is_set
        TimetableMetaData.time_table_name = time_table_name_
        TimetableMetaData.creator_name = creator_name
        TimetableMetaData.institute_name = institute_name
        TimetableMetaData.creators_email = creators_email
        TimetableMetaData.preferences_list_ = preferences_list
        self.timeDimension__.set_from_metadata_thread(days_list)
        Listener.timeTableNameListener = time_table_name_
        # print("From the class", TimetableMetaData.isInfoSet)
        # self.days_list=self.timeDimension__.refresh_list_Home_timetable_metadata()

    @staticmethod
    def get_is_info_set(self) -> bool:
        return TimetableMetaData.isInfoSet

    @staticmethod
    def get_timetable_name(self):
        return TimetableMetaData.time_table_name

    def clean_print(self):
        print(">>>>>.", self.days_list)

    def save_instance_(self):
        Listener.saveInstanceDict["TimetableMetaData"] = {
            "isInfoSet": TimetableMetaData.isInfoSet,
            "time_table_name": TimetableMetaData.time_table_name,
            "creator_name": TimetableMetaData.creator_name,
            "institute_name": TimetableMetaData.institute_name,
            "creators_email": TimetableMetaData.creators_email,
            "preferences_list_": TimetableMetaData.preferences_list_
        }

    # Reset every variable to pepare new file
    def new_file_(self):
        TimetableMetaData.isInfoSet = False
        TimetableMetaData.time_table_name = "Timetbale Name"
        TimetableMetaData.creator_name = ""
        TimetableMetaData.institute_name = ""
        TimetableMetaData.creators_email = " "
        TimetableMetaData.preferences_list_ = list()

    def save_instance_reload(self):
        TimetableMetaData.isInfoSet = Listener.saveInstanceDict["TimetableMetaData"]["isInfoSet"]
        TimetableMetaData.time_table_name = Listener.saveInstanceDict["TimetableMetaData"]["time_table_name"]
        TimetableMetaData.creator_name = Listener.saveInstanceDict["TimetableMetaData"]["creator_name"]
        TimetableMetaData.institute_name = Listener.saveInstanceDict["TimetableMetaData"]["institute_name"]
        TimetableMetaData.creators_email = Listener.saveInstanceDict["TimetableMetaData"]["creators_email"]
        TimetableMetaData.preferences_list_ = Listener.saveInstanceDict["TimetableMetaData"]["preferences_list_"]
