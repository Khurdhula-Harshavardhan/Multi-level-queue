"""
I find the need to see what's happening in the backend while this simulation is running:
Hence I'd like to document each activity of the Simulation.
In-order to achieve this, I shall write a new Component/Class that will implement this idea of documentation: Console.
"""

class Console():
    __file_handler = None #object that will help us handle the file.
    __history: list() = None #list that will store all activities.
    def __init__(self) -> None:
        try:
            self.FILE_NAME: str() = "log.txt"
            self.__file_handler = open(file= self.FILE_NAME, OpenTextMode = "w", encoding="UTF-8")
        except Exception as e:
            print("[ERR] FATAL ERROR, FAILED TO LOAD CONSOLE OBJECT.")

    def note_activity(self, activity: str()) -> None:
        """
        This method adds certain action/activity to the List of History which maintains a record of previous and current operations.
        """
        try:
            if len(activity.strip()) == 0 or activity is None:
                raise Exception("Invalid log provided!")
            else:
                self.__history.append(activity)
        except Exception as e:
            print("[ERR] The following error occured while trying to take note of the activity: "+str(e))