import os
import os


class Listener:
    # Static variables to store state and timetable name
    stateHome = False
    timeTableNameListener = "Timetbale Name"
    isTimeTableCreated = False
    isOptionsUpdated=False
    preferenceList = ["TimeSlots", "Groups", "Classroom/Room/Space", "Course/Class/Session",
                      "Instructor/Lecturer/Tutor"]

    @staticmethod
    def get_app_path():
        # Static method to get the path to the app's documents folder
        documents_folder = os.path.join(os.environ["USERPROFILE"], "Documents")
        app_documents_folder = os.path.join(documents_folder, "Automated TimeTable Generator")
        if not os.path.exists(app_documents_folder):
            os.makedirs(app_documents_folder)
        return app_documents_folder

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


class TimeTableManager:
    # Static variable to store the timetable name
    timeTableNameListener = ""

    @staticmethod
    def set_time_table_name(name):
        # Setter method to update the timetable name
        TimeTableManager.timeTableNameListener = name

    @staticmethod
    def get_time_table_name():
        # Getter method to retrieve the timetable name
        return TimeTableManager.timeTableNameListener
