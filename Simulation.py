"""
This is the main script file, that has the class Simulation that is responsible for execution of this task.
"""
from Resources import Process
from Resources import Queue_A
from Resources import CPU  
from Resources import Queue_B
#We need a global Console object that can be used to maintain a log of all acitivity.
from Console import Console


class Simulation():
    __file_handler = None
    __dispatch_ratio = None
    __demotion_criteria = None
    __total_dispatches = None
    __data = None
    __total_processes = None
    __completed_processes = list()
    qb = None
    console = None
    qa = None
    __current_processs = None

    def __init__(self) -> None:
        self.console = Console()
        self.cpu = CPU(self.console)
        self.qa = Queue_A(self.console)
        self.__total_processes =0
        self.qb = Queue_B(self.console)
        self.__total_dispatches = 0
    
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
            self.update_total_dispatches()
            return True
        elif process.time_spent_in_cpu == process.quantum:
            self.console.note_activity("[PROCESS] Process "+ process.name + " has used up its time quantum.")
            self.update_total_dispatches()  
            return True
        else:
            self.console.note_activity("[PROCESS] Process "+ process.name + " has not used up its time quantum.")
            return False
        
    def view_statistics(self, clock) -> None:
        """
        This method, is called after all process have been completed.
        """
        try:
            
            print("-"*75)
            
            longest_wait = 0
            total_wait = 0
            print("[STATS] The following are the process statistics in the order of their completion:")
            print("Demotion Criteria: "+str(self.__demotion_criteria))
            print("Dispatch Ratio: "+str(self.__dispatch_ratio))
            for process in self.__completed_processes:
               
                stars = " *"*5
                if process.wait_time >= longest_wait:
                    longest_wait = process.wait_time
                total_wait = total_wait + process.wait_time
               
            
            
            print("Total CPU idles: "+str(self.cpu.total_idle//2))
            print("End Time: " +str(clock+1))
            print("Processes Completed: "+str(len(self.__completed_processes)))
            print("longest wait time: "+str(longest_wait))
            print("Total Wait Time: "+str(total_wait))
            print("Average Wait time: "+str((total_wait/len(self.__completed_processes))))

        except Exception as e:
            print("[ERR] The following error occured while trying to display statistics: "+str(e))

    def check_dispatch_ratio(self) -> bool:
        """
        Check if the dispatch ratio has been met,
        returns true in case if it is met,
        false otherwise.
        """
        if self.__total_dispatches == self.__dispatch_ratio:
            self.__total_dispatches = 0
            return True
        else:
            return False

    def update_total_dispatches(self) -> None:
        """
        Increments the total_dispatches by 1.
        """
        self.__total_dispatches = self.__total_dispatches + 1
        self.console.note_activity("[MUL-Q] Total dispatches updated to: "+str(self.__total_dispatches))

    def should_be_demoted(self, process) -> bool:
        """
        Checks if the process has met demotion criteria,
        returns True if yes,
        False otherwise.
        """
        self.console.note_activity("[MUL-Q] Checking if Process "+process.name+" must be demoted to Queue B.")
        if process.chances==0:
            return True
        else:
            return False

    def run(self) -> None:
        """
        Starting point of the Simulation for this Multi level queue.
        """
        try:
            
            #Get user inputs.
            self.console.note_activity("[I/O] Asking user for job file name.")
            file_name = input("Please enter the job file name: ")
            self.console.note_activity("[I/O] User entered the following string for job file name: " +file_name)
            self.console.note_activity("[I/O] Asking user for Dispatch Ratio.")
            self.__dispatch_ratio = int(input("Please enter dispatch ratio: "))
            self.console.note_activity("[I/O] User entered the following value for Dispatch Ratio: "+str(self.__dispatch_ratio))
            self.console.note_activity("[I/O] Asking user for Demotion Criteria.")
            self.__demotion_criteria = int(input("Please enter demotion criteria: "))
            self.console.note_activity("[I/O] User entered the following value for Demotion Criteria: "+str(self.__demotion_criteria))
            self.__file_handler = open(file_name, "r", encoding="UTF-8")
            self.data = self.__file_handler.read()
            self.console.note_activity("[I/O] Reading file: " +file_name)
            self.convert_data()
            self.console.note_activity("[I/O] Converting data within file:" +file_name)
            #print(self.data)

            clock = 0
            self.__total_processes = 0
            #Begin Execution.
            while not self.data_is_empty() or not self.qa.is_empty() or not self.cpu.is_idle() or not self.qb.is_empty():
                self.cpu.update_clock_cycle(clock)
                
                

                self.console.note_activity("[CPU] Checking if CPU is idle.")
                #Check if CPU is currently IDLE.
                if self.cpu.is_idle() and self.__total_processes!=0:
                    
                    self.console.note_activity("[CPU] CPU is IDLE, we must schedule a process now!")
                    
                    if self.qa.is_empty() and not self.qb.is_empty(): #in the case that Queue A is completely empty, then we must keep picking processes from Queue B.
                        self.console.note_activity("[MUL-Q] Picking a process from Queue B since Queue A is now empty")
                        process = self.qb.pick_process()
                        
                        
                    elif not self.qa.is_empty() and not self.check_dispatch_ratio():
                        self.console.note_activity("[MUL-Q] Picking a process from Queue A.")
                        process = self.qa.pick_process()
                        
                    
                    elif not self.qb.is_empty() and self.check_dispatch_ratio():
                        self.console.note_activity("[MUL-Q] Dispatch Ratio has been met! Picking a Process from Queue B")
                        process = self.qb.pick_process()
                    
                    elif self.qb.is_empty() and not self.qa.is_empty() and self.check_dispatch_ratio():
                        self.console.note_activity("[MUL-Q] Picking a process from Queue A because Queue B is empty, and the dispatch ratio has been met.")
                        process = self.qa.pick_process()

                   
                        
                    if process!=None:
                        self.cpu.give_access(process=process)
                        process.increase_time_in_cpu()
                        process.set_remaining_time(1, clock=clock)

                elif self.__total_processes!=0:
                    #CPU is not idle.
                    
                    current_process = self.cpu.get_current_user()
                    self.__current_processs = current_process
                    self.console.note_activity("[CPU] CPU is not idle, and is held by process: "+current_process.name)
                    current_process.set_remaining_time(1, clock=clock)
                    current_process.increase_time_in_cpu()

                    
                    
                    self.console.note_activity("[PROCESS] Checking if the process "+ current_process.name+ " has used its current time quantum.")
                    if self.should_yield(current_process):
                        
                        #we must now decide which process has to be scheduled, if we have met the total processes scheduled ratio we must now then
                        if self.check_dispatch_ratio() and not self.qb.is_empty():
                            self.console.note_activity("[MUL-Q] The dispatch ratio has been met. Picking a process from Queue B")
                            process = self.qb.pick_process()
                        else:
                            process = self.qa.pick_process()
                            
                        self.cpu.give_access(process)
                        
                        if current_process!=None and current_process.is_complete:
                            #current_process.set_completion_time(clock=clock) #Note the time of completion for the process.
                            self.__completed_processes.append(current_process) #Add the process to the list of completed processes.
                            self.console.note_activity("[M-Q] Process "+current_process.name+" has been added to list of finished processes.")
                        else:
                            if self.should_be_demoted(current_process):
                                self.qb.add_process_to_waiting(current_process)
                            else:
                                self.qa.add_process_to_waiting(current_process)
                            self.__current_processs = current_process
                #check for incoming new processes.
                if not self.data_is_empty():
                    self.console.note_activity("[I/O] Checking for any incoming jobs at current clock.")
                    new_process_burst_time = self.data[0]
                    self.data.pop(0)

                    if new_process_burst_time!=-1:
                        process = Process("P"+str(self.__total_processes+1), new_process_burst_time, clock, self.console, self.__demotion_criteria)
                        self.__total_processes = self.__total_processes+1
                        self.qa.add_process_to_waiting(process=process) #add a process to queue if there is a process coming in.
                    else:
                        self.console.note_activity("[I/O] No process has arrived at current clock cycle.")
                
                
                        
                #check for processes that have been completed in previous cycles and remove them completely.
                self.qa.clean_up()
                self.qb.clean_up()
                #update clock
                clock = clock + 1
            self.view_statistics(clock)
        except Exception as e:
            print("[ERR] The following error occured while execution: "+str(e))

    def __del__(self) -> None:
        self.console.flush()

OBJ = Simulation()
OBJ.run()