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

    def set_timetable_information(self, time_table_name: str
                                  , creator_name: str
                                  , institute_name: str
                                  , creators_email: str
                                  , days_list: list
                                  , preferences_list: list):
        self.time_table_name = time_table_name
        self.creator_name = creator_name
        self.institute_name = institute_name
        self.days_list = days_list
        self.creators_email = creators_email
        self.preferences_list = preferences_list
        self.timeDimension = TimeDimension()
        self.timeDimension.set_from_metadata(self.days_list)



    def clean_print(self):
        print(">>>>>.", self.days_list)
