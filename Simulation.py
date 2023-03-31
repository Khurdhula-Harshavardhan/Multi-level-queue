"""
This is the main script file, that has the class Simulation that is responsible for execution of this task.
"""
from Resources import Process
from Resources import Queue_A
from Resources import CPU  
#We need a global Console object that can be used to maintain a log of all acitivity.
from Console import Console


class Simulation():
    def __init__(self) -> None:
        self.console = Console()
        self.cpu = CPU(self.console)
        self.qa = Queue_A(self.console)
        

        

    def run(self) -> None:
        """
        Starting point of the Simulation for this Multi level queue.
        """
        try:
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