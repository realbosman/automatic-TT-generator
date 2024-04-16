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
    time_table_name = "_"
    creator_name = ""
    institute_name = ""
    creators_email = " "
    preferences_list_ = list()

    # This makes sure that the is only one instance of the TimetableMetaData at a time.
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self,cls=None):
        self.timeDimension__ = cls




    def set_timetable_information(self,
                                  is_set:bool
                                  ,time_table_name_: str
                                  , creator_name: str
                                  , institute_name: str
                                  , creators_email: str
                                  , days_list: list
                                  , preferences_list: list):
        TimetableMetaData.isInfoSet=is_set
        TimetableMetaData.time_table_name = time_table_name_
        TimetableMetaData.creator_name = creator_name
        TimetableMetaData.institute_name = institute_name
        TimetableMetaData.creators_email = creators_email
        TimetableMetaData.preferences_list_ = preferences_list
        self.timeDimension__.set_from_metadata_thread(days_list)
        Listener.timeTableNameListener=time_table_name_
        print("From the class",TimetableMetaData.isInfoSet)
        # self.days_list=self.timeDimension__.refresh_list_Home_timetable_metadata()

    @staticmethod
    def get_is_info_set(self)->bool:
        return TimetableMetaData.isInfoSet

    @staticmethod
    def get_timetable_name(self):
        return TimetableMetaData.time_table_name


    def clean_print(self):
        print(">>>>>.", self.days_list)
