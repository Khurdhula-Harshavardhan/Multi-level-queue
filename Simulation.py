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
    __total_processes = None
    __completed_processes = list()

    def __init__(self) -> None:
        self.console = Console()
        self.cpu = CPU(self.console)
        self.qa = Queue_A(self.console)
        self.__total_processes =0
    
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

    def data_is_empty(self) -> bool:
        """
        Checks if there are no new jobs incoming:
        """
        if len(self.data) == 0:
            return True
        else:
            return False
        
    def should_yield(self, process) -> bool:
        """
        Checks if the current process has ran out of its assigned time quantum, we must swap only then.
        Returns true if the process has used its time quantum,
        false otherwise.
        """
        if process.is_complete:
            self.console.note_activity("[PROCESS] Process "+process.name +" is now fulfilled.")
            return True
        elif process.time_spent_in_cpu % process.quantum == 0:
            self.console.note_activity("[PROCESS] Process "+ process.name + " has used up its time quantum.")
            return True
        else:
            self.console.note_activity("[PROCESS] Process "+ process.name + " has not used up its time quantum.")
            return False
        
    def view_statistics(self) -> None:
        """
        This method, is called after all process have been completed.
        """
        try:
            print("-"*75)
            print("The following are the process statistics in the order of their completion:")
            for process in self.__completed_processes:
                stars = " *"*5
                print(stars+" Process Name: "+process.name+stars)
                print("Arrived at: "+str(process.get_arrival_time()))
                print("Burst Time: "+str(process.burst_time))
                print("Total waiting time: "+str(process.wait_time))


        except Exception as e:
            print("[ERR] The following error occured while trying to display statistics: "+str(e))

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

            clock = 0
            self.__total_processes = 0
            #Begin Execution.
            while not self.data_is_empty() or not self.qa.is_empty() or not self.cpu.is_idle():
                self.cpu.update_clock_cycle(clock)
                
                #check for processes that have been completed in previous cycles and remove them completely.
                self.qa.clean_up()

                #check for incoming new processes.
                if not self.data_is_empty():
                    self.console.note_activity("[I/O] Checking for any incoming jobs at current clock.")
                    new_process_burst_time = self.data[0]
                    self.data.pop(0)

                    if new_process_burst_time!=-1:
                        process = Process("P"+str(self.__total_processes+1), new_process_burst_time, clock, self.console)
                        self.__total_processes = self.__total_processes+1
                        self.qa.add_process_to_waiting(process=process) #add a process to queue if there is a process coming in.
                    else:
                        self.console.note_activity("[I/O] No process has arrived at current clock cycle.")
                
                self.console.note_activity("[CPU] Checking if CPU is idle.")
                #Check if CPU is currently IDLE.
                if self.cpu.is_idle():
                    self.console.note_activity("[CPU] CPU IS IDLE.")
                    process = self.qa.pick_process()
                    self.cpu.give_access(process=process)
                else:
                    #CPU is not idle.
                    
                    current_process = self.cpu.get_current_user()
                    self.console.note_activity("[CPU] CPU is not idle, and is held by process: "+current_process.name)
                    current_process.set_remaining_time(1)
                    current_process.increase_time_in_cpu()

                    
                    
                    self.console.note_activity("[PROCESS] Checking if the process "+ current_process.name+ " has used its current time quantum.")
                    if self.should_yield(current_process):
                        process = self.qa.pick_process()
                            
                        self.cpu.give_access(process)
                        if current_process!=None and current_process.is_complete:
                            self.__completed_processes.append(current_process)
                            self.console.note_activity("[M-Q] Process "+current_process.name+" has been added to list of finished processes.")
                        else:
                            self.qa.add_process_to_waiting(current_process)
                        
                
                #update clock
                clock = clock + 1
            self.view_statistics()
        except Exception as e:
            print("[ERR] The following error occured while execution: "+str(e))

    def __del__(self) -> None:
        self.console.flush()

OBJ = Simulation()
OBJ.run()