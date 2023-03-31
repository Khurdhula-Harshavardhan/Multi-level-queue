"""
I find the need to see what's happening in the backend while this simulation is running:
Hence I'd like to document each activity of the Simulation.
In-order to achieve this, I shall write a new Component/Class that will implement this idea of documentation: Console.
"""

class Console():
    __file_handler = None #object that will help us handle the file.
    __history: list() = list() #list that will store all activities.
    def __init__(self) -> None:
        try:
            self.FILE_NAME: str() = "log.txt"
            self.__file_handler = open(self.FILE_NAME, "w", encoding="UTF-8")
            
        except Exception as e:
            print("[ERR] FATAL ERROR, FAILED TO LOAD CONSOLE OBJECT: "+str(e))

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
    
    def flush(self) -> bool:
        """
        This method allows Console to flush out all the information stored within the __history list to an actual text file named: log.txt
        """
        try:
            print("[INFO] Trying to write all activity to log.txt")
            if len(self.__history) == 0:
                raise Exception("No previous activities found!")
            else:
                self.__file_handler.write("\n".join(self.__history))
                print("[INFO] log.txt updated successfully.")
        except Exception as e:
            print("[ERR] The following error occured while trying to flush history to a log file: %s"%(str(e)))
