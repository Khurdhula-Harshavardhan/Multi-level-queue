"""
This python script acts as a resource for all datastructures and entities
that might be needed inorder to implement a multi level feedback queue.
"""

class Queue():
    __NAME = None
    __front = None
    __rear = None
    __TIME_QUANTUM = None
    __waiting = list()

    
    def __init__(self, name, time_quantum) -> None:
        """
        This is the constructor that initializes the Queue pointers.
        """
        try:
            #lets define the time_quantum for the queue.
            self.__TIME_QUANTUM = time_quantum
            self.__NAME = name
        except Exception as e:
            print("[ERR] The following error occured while trying to initialize a new Queue: "+str(e))