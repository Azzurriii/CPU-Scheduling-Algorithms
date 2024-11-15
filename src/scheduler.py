import sys
from collections import deque
from typing import List, Tuple

class Process:
    def __init__(self, pid: int, arrival_time: int, bursts: List[Tuple[int, int]]):
        self.pid = pid
        self.arrival_time = arrival_time
        self.bursts = deque(bursts)
        self.remaining_cpu_time = bursts[0][0] if bursts else 0
        self.original_cpu_time = bursts[0][0] if bursts else 0
        self.remaining_resource_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

class Scheduler:
    def __init__(self):
        self.ready_queue = deque()
        self.resource_queue = deque()
        self.current_time = 0
        self.cpu_timeline = []
        self.resource_timeline = []

    def fcfs(self, processes: List[Process]) -> Tuple[List[str], List[str]]:
        """First Come First Serve Algorithm"""
        current_process = None
        current_resource_process = None
        completed_processes = []
        
        while True:
            # Check for new arrivals
            for process in processes:
                if process.arrival_time == self.current_time and process not in completed_processes:
                    self.ready_queue.append(process)
            
            # Handle CPU scheduling
            if not current_process and self.ready_queue:
                current_process = self.ready_queue.popleft()
            
            if current_process:
                self.cpu_timeline.append(str(current_process.pid))
                current_process.remaining_cpu_time -= 1
                
                if current_process.remaining_cpu_time == 0:
                    if current_process.bursts[0][1] > 0:  # Has resource requirement
                        current_process.remaining_resource_time = current_process.bursts[0][1]
                        self.resource_queue.append(current_process)
                    current_process.bursts.popleft()
                    if current_process.bursts:
                        current_process.remaining_cpu_time = current_process.bursts[0][0]
                        self.ready_queue.append(current_process)
                    else:
                        completed_processes.append(current_process)
                    current_process = None
            else:
                self.cpu_timeline.append('_')
            
            # Handle Resource scheduling (FCFS)
            if not current_resource_process and self.resource_queue:
                current_resource_process = self.resource_queue.popleft()
            
            if current_resource_process:
                self.resource_timeline.append(str(current_resource_process.pid))
                current_resource_process.remaining_resource_time -= 1
                
                if current_resource_process.remaining_resource_time == 0:
                    if current_resource_process.bursts:
                        current_resource_process.remaining_cpu_time = current_resource_process.bursts[0][0]
                        self.ready_queue.append(current_resource_process)
                    current_resource_process = None
            else:
                self.resource_timeline.append('_')
            
            self.current_time += 1
            
            # Check if all processes are complete
            if len(completed_processes) == len(processes) and not current_process and not current_resource_process:
                break
        
        return self.cpu_timeline, self.resource_timeline

    def round_robin(self, processes: List[Process], quantum: int = 2) -> Tuple[List[str], List[str]]:
        """Round Robin Algorithm"""
        current_process = None
        current_resource_process = None
        completed_processes = []
        time_in_cpu = 0
        
        while True:
            # Check for new arrivals
            for process in processes:
                if process.arrival_time == self.current_time and process not in completed_processes:
                    self.ready_queue.append(process)
            
            # Handle CPU scheduling
            if not current_process and self.ready_queue:
                current_process = self.ready_queue.popleft()
                time_in_cpu = 0
            
            if current_process:
                self.cpu_timeline.append(str(current_process.pid))
                current_process.remaining_cpu_time -= 1
                time_in_cpu += 1
                
                # Check if quantum expired or process completed
                if time_in_cpu == quantum or current_process.remaining_cpu_time == 0:
                    if current_process.remaining_cpu_time > 0:
                        self.ready_queue.append(current_process)
                    else:
                        if current_process.bursts[0][1] > 0:
                            current_process.remaining_resource_time = current_process.bursts[0][1]
                            self.resource_queue.append(current_process)
                        current_process.bursts.popleft()
                        if current_process.bursts:
                            current_process.remaining_cpu_time = current_process.bursts[0][0]
                            self.ready_queue.append(current_process)
                        else:
                            completed_processes.append(current_process)
                    current_process = None
            else:
                self.cpu_timeline.append('_')
            
            # Handle Resource scheduling (FCFS)
            if not current_resource_process and self.resource_queue:
                current_resource_process = self.resource_queue.popleft()
            
            if current_resource_process:
                self.resource_timeline.append(str(current_resource_process.pid))
                current_resource_process.remaining_resource_time -= 1
                
                if current_resource_process.remaining_resource_time == 0:
                    if current_resource_process.bursts:
                        current_resource_process.remaining_cpu_time = current_resource_process.bursts[0][0]
                        self.ready_queue.append(current_resource_process)
                    current_resource_process = None
            else:
                self.resource_timeline.append('_')
            
            self.current_time += 1
            
            if len(completed_processes) == len(processes) and not current_process and not current_resource_process:
                break
        
        return self.cpu_timeline, self.resource_timeline

    def sjf(self, processes: List[Process]) -> Tuple[List[str], List[str]]:
        """Shortest Job First Algorithm"""
        current_process = None
        current_resource_process = None
        completed_processes = []
        
        while True:
            # Check for new arrivals
            for process in processes:
                if process.arrival_time == self.current_time and process not in completed_processes:
                    self.ready_queue.append(process)
            
            # Sort ready queue by remaining CPU time
            if self.ready_queue:
                ready_list = list(self.ready_queue)
                ready_list.sort(key=lambda p: p.remaining_cpu_time)
                self.ready_queue = deque(ready_list)
            
            # Handle CPU scheduling
            if not current_process and self.ready_queue:
                current_process = self.ready_queue.popleft()
            
            if current_process:
                self.cpu_timeline.append(str(current_process.pid))
                current_process.remaining_cpu_time -= 1
                
                if current_process.remaining_cpu_time == 0:
                    if current_process.bursts[0][1] > 0:
                        current_process.remaining_resource_time = current_process.bursts[0][1]
                        self.resource_queue.append(current_process)
                    current_process.bursts.popleft()
                    if current_process.bursts:
                        current_process.remaining_cpu_time = current_process.bursts[0][0]
                        self.ready_queue.append(current_process)
                    else:
                        completed_processes.append(current_process)
                    current_process = None
            else:
                self.cpu_timeline.append('_')
            
            # Handle Resource scheduling (FCFS)
            if not current_resource_process and self.resource_queue:
                current_resource_process = self.resource_queue.popleft()
            
            if current_resource_process:
                self.resource_timeline.append(str(current_resource_process.pid))
                current_resource_process.remaining_resource_time -= 1
                
                if current_resource_process.remaining_resource_time == 0:
                    if current_resource_process.bursts:
                        current_resource_process.remaining_cpu_time = current_resource_process.bursts[0][0]
                        self.ready_queue.append(current_resource_process)
                    current_resource_process = None
            else:
                self.resource_timeline.append('_')
            
            self.current_time += 1
            
            if len(completed_processes) == len(processes) and not current_process and not current_resource_process:
                break
        
        return self.cpu_timeline, self.resource_timeline

    def srtn(self, processes: List[Process]) -> Tuple[List[str], List[str]]:
        """Shortest Remaining Time Next Algorithm"""
        current_process = None
        current_resource_process = None
        completed_processes = []
        
        while True:
            # Check for new arrivals
            for process in processes:
                if process.arrival_time == self.current_time and process not in completed_processes:
                    self.ready_queue.append(process)
            
            # If there's a current process, add it back to ready queue for comparison
            if current_process:
                self.ready_queue.append(current_process)
                current_process = None
            
            # Sort ready queue by remaining CPU time
            if self.ready_queue:
                ready_list = list(self.ready_queue)
                ready_list.sort(key=lambda p: p.remaining_cpu_time)
                self.ready_queue = deque(ready_list)
                current_process = self.ready_queue.popleft()
            
            if current_process:
                self.cpu_timeline.append(str(current_process.pid))
                current_process.remaining_cpu_time -= 1
                
                if current_process.remaining_cpu_time == 0:
                    if current_process.bursts[0][1] > 0:
                        current_process.remaining_resource_time = current_process.bursts[0][1]
                        self.resource_queue.append(current_process)
                    current_process.bursts.popleft()
                    if current_process.bursts:
                        current_process.remaining_cpu_time = current_process.bursts[0][0]
                    else:
                        completed_processes.append(current_process)
                    current_process = None
            else:
                self.cpu_timeline.append('_')
            
            # Handle Resource scheduling (FCFS)
            if not current_resource_process and self.resource_queue:
                current_resource_process = self.resource_queue.popleft()
            
            if current_resource_process:
                self.resource_timeline.append(str(current_resource_process.pid))
                current_resource_process.remaining_resource_time -= 1
                
                if current_resource_process.remaining_resource_time == 0:
                    if current_resource_process.bursts:
                        current_resource_process.remaining_cpu_time = current_resource_process.bursts[0][0]
                        self.ready_queue.append(current_resource_process)
                    current_resource_process = None
            else:
                self.resource_timeline.append('_')
            
            self.current_time += 1
            
            if len(completed_processes) == len(processes) and not current_process and not current_resource_process:
                break
        
        return self.cpu_timeline, self.resource_timeline

def read_input(filename: str) -> List[Process]:
    processes = []
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        for i in range(n):
            line = list(map(int, f.readline().strip().split()))
            arrival_time = line[0]
            bursts = []
            for j in range(1, len(line), 2):
                if j + 1 < len(line):
                    bursts.append((line[j], line[j + 1]))
                else:
                    bursts.append((line[j], 0))
            processes.append(Process(i + 1, arrival_time, bursts))
    return processes

def write_output(filename: str, cpu_timeline: List[str], resource_timeline: List[str]):
    with open(filename, 'w') as f:
        f.write(' '.join(cpu_timeline) + '\n')
        f.write(' '.join(resource_timeline) + '\n')

def main():
    if len(sys.argv) < 4:
        print("Usage: python scheduler.py input_file output_file algorithm [quantum]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    algorithm = int(sys.argv[3])
    quantum = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    
    processes = read_input(input_file)
    scheduler = Scheduler()
    
    if algorithm == 1:
        cpu_timeline, resource_timeline = scheduler.fcfs(processes)
    elif algorithm == 2:
        cpu_timeline, resource_timeline = scheduler.round_robin(processes, quantum)
    elif algorithm == 3:
        cpu_timeline, resource_timeline = scheduler.sjf(processes)
    elif algorithm == 4:
        cpu_timeline, resource_timeline = scheduler.srtn(processes)
    else:
        print("Invalid algorithm choice")
        return
    
    write_output(output_file, cpu_timeline, resource_timeline)

    print('Done!')

if __name__ == "__main__":
    main()