import os


class Listener:

    instance = None
    countInstance = 0

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
            cls.countInstance += 1
            print(cls.countInstance)
        else:
            print(cls.countInstance)

        return cls.instance

    def __init__(self, * args):
        self.stateHome: bool = False
        self.timeTableNameListener="Listener time Name";
        # Get the path to the Documents folder
        self.documents_folder = os.path.join(os.environ["USERPROFILE"], "Documents")

        # Create a directory within the Documents folder to store your app's documents
        self.app_documents_folder = os.path.join(self.documents_folder, "Automated TimeTable Generator")

        # Check if the app_documents_folder already exists
        if not os.path.exists(self.app_documents_folder):
            # If it doesn't exist, create it
            os.makedirs(self.app_documents_folder)

    def getStateHome(self):
        return self.stateHome

    def setStateHome(self, state):
        self.stateHome = state

    def get_app_path(self):
        return self.app_documents_folder


