import os
import os
import time


class Listener:
    # Static variables to store state and timetable name
    stateHome = False
    timeTableNameListener = "Timetbale Name"
    timeZone=str(time.tzname[0])
    isTimeTableCreated = False
    isWeekendInclusive = False
    iswarningOnSession = False
    ispdf_generated=False
    tutor_with_highest_session_=0
    get_time_slot_count=0
    isOptionsUpdated = False
    preferenceList = ["TimeSlots", "Groups", "Classroom/Room/Space", "Course/Class/Session",
                      "Instructor/Lecturer/Tutor"]
    saveInstanceDict = {

    }

    @staticmethod
    def get_app_path_docs():
        # Static method to get the path to the app's documents folder
        documents_folder = os.path.join(os.environ["USERPROFILE"], "Documents")
        app_documents_folder = os.path.join(documents_folder, "Automated TimeTable Generator/Generated timetables")
        if not os.path.exists(app_documents_folder):
            os.makedirs(app_documents_folder)
        return app_documents_folder

    @staticmethod
    def get_app_path_files():
        # Static method to get the path to the app's Recent files folder
        documents_folder = os.path.join(os.environ["USERPROFILE"], "Documents")
        app_recent_files_folder = os.path.join(documents_folder, r"Automated TimeTable Generator\\Recent files")
        if not os.path.exists(app_recent_files_folder):
            os.makedirs(app_recent_files_folder)
        return app_recent_files_folder

    @staticmethod
    def get_state_home():
        # Static method to get the state of home
        return Listener.stateHome

    @staticmethod
    def set_state_home(state):
        # Static method to set the state of home
        Listener.stateHome = state

    @staticmethod
    def set_time_table_name(name):
        # Static method to set the timetable name
        Listener.timeTableNameListener = name

    @staticmethod
    def get_time_table_name():
        # Static method to get the timetable name
        return Listener.timeTableNameListener

    @staticmethod
    def save_instance_():
        Listener.saveInstanceDict["Listener"] = {
            "stateHome": Listener.stateHome,
            "timeTableNameListener": Listener.timeTableNameListener,
            "isTimeTableCreated": Listener.isTimeTableCreated,
            "isWeekendInclusive": Listener.isWeekendInclusive,
            "isOptionsUpdated": Listener.isOptionsUpdated,
            "preferenceList": Listener.preferenceList
        }

    # Reset every variable to pepare new file
    @staticmethod
    def new_file_():
        Listener.stateHome = False
        Listener.timeTableNameListener = "Timetbale Name"
        Listener.isTimeTableCreated = False
        Listener.isWeekendInclusive = False
        Listener.isOptionsUpdated = False
        Listener.preferenceList = ["TimeSlots", "Groups", "Classroom/Room/Space", "Course/Class/Session",
                                   "Instructor/Lecturer/Tutor"]
        Listener.saveInstanceDict = {

        }

    @staticmethod
    def save_instance_reload():

        Listener.stateHome = Listener.saveInstanceDict["Listener"]["stateHome"]
        Listener.timeTableNameListener = Listener.saveInstanceDict["Listener"]["timeTableNameListener"]
        Listener.isTimeTableCreated = Listener.saveInstanceDict["Listener"]["isTimeTableCreated"]
        Listener.isWeekendInclusive = Listener.saveInstanceDict["Listener"]["isWeekendInclusive"]
        Listener.isOptionsUpdated = Listener.saveInstanceDict["Listener"]["isOptionsUpdated"]
        Listener.preferenceList = Listener.saveInstanceDict["Listener"]["preferenceList"]
