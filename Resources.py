"""
This python script acts as a resource for all datastructures and entities
that might be needed inorder to implement a multi level feedback queue.
    -Harsha Vardhan, Khurdula 2023.
"""

class Process():
    name = None
    burst_time = None
    wait_time = None
    context_switches = None
    remaining_burst_time = None
    is_complete = None

    def __init__(self, name: str(), burst_time: float()) -> None:
        """
        Initializes the process properties, that are unique to each process.
        """
        try:
            #check if the new process name and burst_times are valid. If not raise exceptions.
            if name == None or len(name.strip()) ==0:
                raise Exception("Process name cannot be empty!")
            elif burst_time < 0 or burst_time == 0:
                raise Exception("Invalid burst time provided for new Process: %s."%(name))
            
            #If the process data is correct then initialize the other Process attributes.
            self.name = name
            self.burst_time = burst_time
            self.wait_time = 0
            self.context_switches = 0
            self.remaining_burst_time = self.burst_time
            self.is_complete = False
        except Exception as e:
            print("[ERR] The following error occured while trying to create a new process: "+str(e))

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

    def set_remaining_time(self, time: float()) -> None:
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

    """
    Note: The waiting list is a queue, that is implemented from right to left. Meaning the right end of the queue has the rear pointer.
    And the left end would be the front.
    e.x. the 0 index will always be the front from where we can pick processes. And the n'th index would be the rear where new processes can be added to the queue.

    Front (pick process from here) -  [p1, p2, p5, ...] - Rear (adds processes here).
    """
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

    def add_process_to_waiting(self, process: Process()) -> bool:
        """
        This method receives a process and then adds it to the waiting list.
        """
        try:
            self.__waiting.append(process)
        except Exception as e:
            print("[ERR] The following error occured while trying to add the new process to the Queue A waiting list: %s"%(str(e)))
