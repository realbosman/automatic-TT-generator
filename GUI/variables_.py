from queue import Queue

from queue import Queue
from enum import Enum, auto
class  Global_variables:
    instance = None
    countInstance = 0
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            cls.instance = object.__new__(cls)
            cls.countInstance += 1
            print(cls.countInstance)
        else:

            print(cls.countInstance)

    def __init__(self,parent):
        self.parent = parent
        self.queue_message = Queue()

    def put_message(self,msg):
        self.queue_message.put(msg)
        self.parent.event_generate("<<CheckQueue>>", when="tail")

    def Check_Queue(self, e):
        """
       Read the queue
        """
        msg: Ticket


        msg = self.queue_message.get()
        if msg.ticket_type == TicketPurpose.UPDATE_PROGRESS_TEXT:
            pass
        if msg.ticket_type == TicketPurpose.UPDATE_PROGRESS_HEADING:
            pass

# Ticketing system call
class TicketPurpose(Enum):
    UPDATE_PROGRESS_TEXT = auto()
    UPDATE_PROGRESS_HEADING = auto()


class Ticket:
    def __init__(self, ticket_type: TicketPurpose,
                 ticket_value: list):
        self.ticket_type = ticket_type
        self.ticket_value = ticket_value