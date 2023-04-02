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
    quantum = None
    time_spent_in_cpu = None
    arrival_time = None
    time_of_completion = None

    def __init__(self, name: str(), burst_time: float(), arrival_time: float(),console) -> None:
        """
        Initializes the process properties, that are unique to each process.
        """
        try:
            self.console = console
            #check if the new process name and burst_times are valid. If not raise exceptions.
            if name == None or len(name.strip()) ==0:
                raise Exception("Process name cannot be empty!")
            elif burst_time <= 0:
                raise Exception("Invalid burst time provided for new Process: %s."%(name))
            
            #If the process data is correct then initialize the other Process attributes.
            self.name = name
            self.burst_time = burst_time
            self.wait_time = 0
            self.context_switches = 0
            self.remaining_burst_time = self.burst_time
            self.is_complete = False
            self.quantum = 5
            self.time_spent_in_cpu = 0
            self.arrival_time = arrival_time
            self.console.note_activity("[PROCESS] New process " + str(self.name) +" has arrived, with burst time: "+str(self.burst_time))
        except Exception as e:
            print("[ERR] The following error occured while trying to create a new process: "+str(e))

    def get_arrival_time(self) -> float:
        """
        Returns the arrival time of a process.
        """
        return self.arrival_time

    def increase_wait_time(self) -> None:
        """
        Increases the total_wait_time of the process by 1
        """
        self.wait_time = self.wait_time + 1
        self.console.note_activity("[PROCESS] wait time of process: " +str(self.name) + " has been increased by 1.")

    def increase_time_in_cpu(self) -> None:
        """
        Increases the time spent at CPU by 1.
        """
        self.time_spent_in_cpu = self.time_spent_in_cpu + 1

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
            self.console.note_activity("[PROCESS] Process : " +str(self.name) + " has completed its total execution.")
        self.console.note_activity("[PROCESS] Remaining burst time of process: " +str(self.name) + " has been updated to "+ str(self.remaining_burst_time))
    
    def increase_context_switches(self) -> None:
        """
        Increases the count of Context Switches of the process by 1, when it is granted with CPU access.
        """
        self.context_switches = self.context_switches + 1
        self.console.note_activity("[PROCESS] Process "+self.name+ " total context switches has been updated to: "+str(self.context_switches))

    def set_completion_time(self, clock) -> None:
        """
        Sets completion time to given period of clock cycle.
        """
        self.time_of_completion = clock  

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
    
    def __init__(self, console) -> None:
        """
        This is the constructor that initializes the Queue pointers.
        """
        try:
            #lets define the time_quantum for the queue.
            self.__TIME_QUANTUM = 5
            self.__NAME = "A"
            self.console = console
            self.console.note_activity("[Q-A] Queue A has been initialized successfully.")
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
        
    def get_waiting_process(self) -> str():
        """
        Returns a string of processes waiting within Queue A.
        """
        processes = [process.name for process in self.__waiting]
        return "[" + ", ".join(processes) +"]"
    
    def clean_up(self) -> None:
        """
        Clean up the waiting list, make sure there are no processes that are completed!
        """
        try:
            self.console.note_activity("[Q-A] Checking for processes that can be cleaned up.")
            if self.is_empty():
                self.console.note_activity("[Q-A] No process needs clean up in Queue A, as is it empty.")
                return #Do nothing, as the Queue is Empty.
            else:
                #if there are processes present within the queue, lets check for processes and remove them if necessary.
                for process in self.__waiting:
                    if process.is_complete:
                        self.console.note_activity("[Q-A] Process " + process.name + " has completed its execution, cleaning it up.")
                        self.__waiting.remove(process)
                        self.console.note_activity("[Q-A] Process clean up complete.")
                    else:
                        process.increase_wait_time()
                        
            
            self.console.note_activity("[Q-A] No process needs clean up in Queue A.")        
        except Exception as e:
            print("[ERR] The following error occured while trying to clean up Queue A: "+str(e))

    def add_process_to_waiting(self, process: Process) -> bool:
        """
        This method receives a process and then adds it to the waiting list.
        """
        try:
            self.__waiting.append(process)
            self.console.note_activity("[Q-A] Process " + process.name + " has been added to waiting list of Queue A successfully.")
            self.console.note_activity("[Q-A] The Queue A contains processes: "+self.get_waiting_process())
        except Exception as e:
            print("[ERR] The following error occured while trying to add the new process to the Queue A waiting list: %s"%(str(e)))

    def pick_process(self) -> Process:
        try:
            self.console.note_activity("[Q-A] Trying to Pick a new process from Queue A.")
            if self.is_empty():
                self.console.note_activity("[Q-A] The waiting list is empty, there is no process available in order to be picked.")
                self.held_by = None
            else:
                process = self.__waiting[0]
                
                self.__waiting.remove(process)
                self.console.note_activity("[Q-A] Process "+process.name+" has been picked from Queue A.")
                self.console.note_activity("[Q-A] The Queue A now contains processes: "+self.get_waiting_process())
                
                return process
                
        except Exception as e:
            print("[ERR] The following error occured while trying to pick a process from Queue A: "+str(e))

class CPU():
    held_by = None
    current_clock_cycle = None
    console = None
    def __init__(self, console) -> None:
        self.console = console
        self.console.note_activity("[CPU] CPU has been initialized successfully.")

    def is_held_by(self, process) -> bool:
        """
        Check if the CPU is currently in use by Process x,
        if it is, then returns true,
        returns false other wise.
        """
        if self.held_by is process:
            return True
        else:
            return False
        
    def get_current_user(self) -> Process:
        """
        Returns the current process that has access/is using the CPU.
        """
        return self.held_by
    
    def is_idle(self) -> bool:
        """
        Returns True if the CPU is currently idle.
        False otherwise.
        """
        if self.held_by is None:
            return True
        else:
            return False
        
    def set_idle(self) -> None:
        """
        Sets CPU to IDLE status.
        """
        self.held_by = None
        
    def give_access(self, process) -> None:
        """
        This method Provides access to the CPU.
        """
        if process == None:
            self.console.note_activity("[CPU] No process has been scheduled, has queues are empty.")
            self.set_idle()
            return
        if self.is_held_by(process=process):
            self.console.note_activity("[CPU-ERR] Process "+str(process.name)+" already has the CPU and is still requesting for CPU.")
        else:
            if self.held_by == None:
                self.console.note_activity("[CPU] Is currently idle.")
                self.held_by = process
                self.console.note_activity("[CPU] Process "+process.name+" is now using the CPU.")
                
            else:
                self.console.note_activity("[CPU] Process "+self.held_by.name+" has left the CPU.")
                self.held_by = process
                self.console.note_activity("[CPU] Process "+process.name+" is now using the CPU.")
            process.increase_context_switches()
              
    
    def update_clock_cycle(self, clock_cycle) -> None:
        self.current_clock_cycle = clock_cycle
        self.console.note_activity("-"*50 + "\n[CPU] Current Clock Cycle has been updated to: "+str(self.current_clock_cycle))


class Queue_B():
    __NAME = None
    __front = None
    __rear = None
    __TIME_QUANTUM = None

    def __init__(self) -> None:

        self.__TIME_QUANTUM = 40
        self.__NAME = "B"
    