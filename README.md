# CPU Scheduler Simulator

A Python implementation of various CPU scheduling algorithms with resource management. This simulator supports multiple processes with alternating CPU and resource bursts.

## Features

- Implemented algorithms:
  - First Come First Serve (FCFS)
  - Round Robin (RR)
  - Shortest Job First (SJF)
  - Shortest Remaining Time Next (SRTN)

## Usage

```bash
python scheduler.py input_file output_file algorithm_number [quantum]
```
**For example:**
```
python scheduler.py input.txt output.txt 1
```

### Parameters:
- `input_file`: Path to the input file containing process information
- `output_file`: Path where the output timelines will be written
- `algorithm_number`: Scheduling algorithm to use (1-4)
  - 1: FCFS
  - 2: Round Robin
  - 3: SJF
  - 4: SRTN
- `quantum`: Time quantum for Round Robin algorithm (optional, default=2)

## Input File Format

```
n
arrival_time cpu_burst1 io_burst1 cpu_burst2 io_burst2 ...
```

Where:
- First line contains the number of processes (n)
- Each subsequent line represents a process with:
  - Arrival time
  - Alternating CPU and I/O burst times
  - Last burst must be a CPU burst

Example:
```
3
0 5 2 3
2 4 1 2
4 3
```

## Output Format

The program generates two lines in the output file:
1. CPU timeline showing which process (by PID) is using the CPU at each time unit
2. Resource timeline showing which process is using the resource at each time unit

Example:
```
1 1 1 1 1 2 2 2 2 3 3 3
_ _ 1 1 2 _ _ _ _ _ _ _
```

## Process States

Each process can be in one of these states:
- Ready Queue: Waiting for CPU
- Running: Using CPU
- Resource Queue: Waiting for resource
- Using Resource: Currently using the resource
- Completed: Finished all bursts

## Implementation Details

- Processes are represented by the `Process` class containing:
  - Process ID (pid)
  - Arrival time
  - List of CPU and resource bursts
  - Remaining times
- The `Scheduler` class implements all scheduling algorithms
- Resource scheduling always uses FCFS policy
- Idle time is represented by '_' in the timeline