class TimeDimension:
    instance = None

    # TOD Make this  dynamic for the user (timeslots)
    '''
    This is a default timeslots dictionary
    '''
    TimeSlotsDict = {
        "MON": [" 7:30-9:30", " 10:00-13:00", " 2:00-16:00"],
        "TUE": [" 7:30-9:30", " 10:00-13:00", " 2:00-16:00"],
        "WED": [" 7:30-9:30", " 10:00-13:00", " 2:00-16:00"],
        "THUR": [" 7:30-9:30", " 10:00-13:00", " 2:00-16:00"],
        "FRI": [" 7:30-9:30", " 10:00-13:00", " 2:00-16:00"],
        "SAT": [" 7:30-9:30", " 10:00-13:00", " 2:00-16:00"],
        "SUN": [" 7:30-9:30", " 10:00-13:00", " 2:00-16:00"],
    }

    def __init__(self):
        print("Hey am time dimension")

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
        return cls.instance

    def edit_time_slots(self, new_time_slots_object):
        self.TimeSlotsDict = new_time_slots_object

    def get_time_slots(self):
        return self.TimeSlotsDict
