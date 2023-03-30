"""
This python script acts as a resource for all datastructures and entities
that might be needed inorder to implement a multi level feedback queue.
"""

class Queue():
    __front = None
    __rear = None
    
    def __init__(self) -> None:
        """
        This is the constructor that initializes the Queue pointers.
        """
        try:
            pass
        except Exception as e:
            print("[ERR] The following error occured while trying to initialize a new Queue: "+str(e))