"""
This python script acts as a resource for all datastructures and entities
that might be needed inorder to implement a multi level feedback queue.
"""

class Process():
    name = None
    burst_time = None
    wait_time = None
    context_switches = None
    remaining_burst_time = None
    is_complete = None

    def __init__(self, name, burst_time) -> None:
        """
        Initializes the process properties, that are unique to each process.
        """
        self.name = name
        self.burst_time = burst_time
        self.wait_time = 0
        self.context_switches = 0
        self.remaining_burst_time = self.burst_time
        self.is_complete = False

    def increase_wait_time(self) -> None:
        """
        Increases the total_wait_time of the process by 1
        """
        self.wait_time = self.wait_time + 1

    def get_remaining_time(self) -> int():
        """
        Returns the total remaining burst time of the process.
        """
        return self.remaining_burst_time

    def set_remaining_time(self, time) -> None:
        """
        Reduces the total waiting time by given time.
        """
        self.remaining_burst_time = self.remaining_burst_time - time
        if self.remaining_burst_time <= 0:
            self.remaining_burst_time = 0
            self.is_complete = True
        

class Queue_A():
    __NAME = None
    __front = None
    __rear = None
    __TIME_QUANTUM = None
    __waiting = list()

    
    def __init__(self) -> None:
        """
        This is the constructor that initializes the Queue pointers.
        """
        try:
            #lets define the time_quantum for the queue.
            self.__TIME_QUANTUM = 5
            self.__NAME = "A"
        except Exception as e:
            print("[ERR] The following error occured while trying to initialize a new Queue: "+str(e))

    def is_empty(self) -> bool:
        """
        Returns a boolean value, 
        True if there are no elements within the list waiting.
        False, otherwise.
        """
        if len(self.__waiting) == 0:
            return True
        else:
            return False

    
