"""
This python script acts as a resource for all datastructures and entities
that might be needed inorder to implement a multi level feedback queue.
"""

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
