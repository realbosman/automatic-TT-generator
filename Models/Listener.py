class Listener:
    '''
           This class this class listens for any incoming GUI events from other classes,
           helps to make execution on the Main Thread
           '''

    instance = None
    countInstance = 0

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
            cls.countInstance += 1
            print(cls.countInstance)
        else:
            print(cls.countInstance)

    def __init__(self):
        stateHome: bool = False

    def getStateHome(self):
        return self.stateHome

    def setStateHome(self, state):
        self.stateHome = state
