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

    # This makes sure that the is only one instance of the TimetableMetaData at a time.
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self,cls=None):
        self.isInfoSet=False
        self.time_table_name="_"
        self.creator_name = ""
        self.institute_name = ""
        self.timeDimension__=cls
        self.creators_email = " "
        self.preferences_list =list()



    def set_timetable_information(self,
                                  is_set:bool
                                  ,time_table_name_: str
                                  , creator_name: str
                                  , institute_name: str
                                  , creators_email: str
                                  , days_list: list
                                  , preferences_list: list):
        self.isInfoSet=is_set
        self.time_table_name = time_table_name_
        self.creator_name = creator_name
        self.institute_name = institute_name
        self.creators_email = creators_email
        self.preferences_list = preferences_list
        self.timeDimension__.set_from_metadata_thread(days_list)
        # self.days_list=self.timeDimension__.refresh_list_Home_timetable_metadata()


    def get_is_info_set(self)->bool:
        return self.isInfoSet

    def get_timetable_name(self):
        return self.time_table_name


    def clean_print(self):
        print(">>>>>.", self.days_list)
