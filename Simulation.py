"""
This is the main script file, that has the class Simulation that is responsible for execution of this task.
"""
from Resources import Process
from Resources import Queue_A
from Resources import CPU  
#We need a global Console object that can be used to maintain a log of all acitivity.
from Console import Console


class Simulation():
    __file_handler = None
    __dispatch_ratio = None
    __demotion_criteria = None
    __data = None
    def __init__(self) -> None:
        self.console = Console()
        self.cpu = CPU(self.console)
        self.qa = Queue_A(self.console)
    
    def convert_data(self) -> None:
        """
        Converts the input file text, into useful readable format.
        """
        try:
            self.data = self.data.split("\n")
            data = list()
            for value in self.data:
                try:
                    data.append(int(value))
                except:
                    data.append(-1)
            self.data = data
        except Exception as e:
            print("[ERR] The following error occured while trying to read job file: "+str(e))

        

    def run(self) -> None:
        """
        Starting point of the Simulation for this Multi level queue.
        """
        try:

            #Get user inputs.
            self.console.note_activity("[I/O] Asking user for job file name.")
            file_name = "TestCase.txt" #input("Please enter the job file name: ")
            self.console.note_activity("[I/O] User entered the following string for job file name: " +file_name)
            self.console.note_activity("[I/O] Asking user for Dispatch Ratio.")
            self.__dispatch_ratio = 4 #int(input("Please enter dispatch ratio: "))
            self.console.note_activity("[I/O] User entered the following value for Dispatch Ratio: "+str(self.__dispatch_ratio))
            self.console.note_activity("[I/O] Asking user for Demotion Criteria.")
            self.__demotion_criteria = 5 #int(input("Please enter demotion criteria: "))
            self.console.note_activity("[I/O] User entered the following value for Demotion Criteria: "+str(self.__demotion_criteria))
            self.__file_handler = open(file_name, "r", encoding="UTF-8")
            self.data = self.__file_handler.read()
            self.console.note_activity("[I/O] Reading file: " +file_name)
            self.convert_data()
            self.console.note_activity("[I/O] Converting data within file:" +file_name)
            print(self.data)

            #Begin Execution.
            for i in range(10):
                self.cpu.update_clock_cycle(i)
                process = Process(name= "P"+str(i+1), burst_time=i+1, console=self.console)
                self.qa.add_process_to_waiting(process= process)
                previous_process = self.cpu.held_by
                
                process = self.qa.pick_process()
                
                self.cpu.give_access(process)
                if previous_process!=None:
                    self.qa.add_process_to_waiting(previous_process)
        except Exception as e:
            print("[ERR] The following error occured while execution: "+str(e))

    def __del__(self) -> None:
        self.console.flush()

OBJ = Simulation()
OBJ.run()