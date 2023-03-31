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
        Qa = Queue_A(self.console)
        cpu = CPU(self.console)

        for i in range(10):
            cpu.update_clock_cycle(i)
            process = Process(name= "P"+str(i+1), burst_time=i+1, console=self.console)
            cpu.give_access(process)
            Qa.add_process_to_waiting(process= process)

    def __del__(self) -> None:
        self.console.flush()

OBJ = Simulation()