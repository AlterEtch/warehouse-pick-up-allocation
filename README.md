# Warehouse Multi-Robot Automation System Simulation

This is a simple python simulation for warehouse multi-robot automation system.

## Getting Started

### Prerequisites
[Python 2.7](https://www.python.org/download/releases/2.7/)

### Packages/Modules Used
The following is a list of packages and modules used in this project. The corresponding documentation can be accessed through the hyperlink of each item.
1.  [TKinter](https://docs.python.org/2/library/tkinter.html)
2.  [heapq](https://docs.python.org/2/library/heapq.html)
3.  [random](https://docs.python.org/2/library/random.html)
4.  [math](https://docs.python.org/2/library/math.html#module-math)
5.  [argparse](https://docs.python.org/2/howto/argparse.html)
6.  [copy](https://docs.python.org/2/library/copy.html)
7.  [atexit](https://docs.python.org/2/library/atexit.html)

### Running the Project
The project can be run in terminal using the following command:
```
python main.py
```

####Command Line Arguments
Command line arguments are supported to modify some of the simulation parameters. The available arguments and the corresponding default values and description are listed below:

| Arguments | Type     | Default | Description                           |
| ----------|:---------|:--------|:--------------------------------------|
| -rr       | Int      | 0       | Number of initial robots in the world, randomly generated in stations. Only applicable for layouts with multiple stations |
| -fr       | Int      | 3       | Number of initial robots in the world, at a fixed station |
| -t        | Int      | 10      | Number of initial tasks in the world  |
| -l        | Int/Char | 2       | Layout selection, not recommended to change |
| -g        | Int      | 1       | Graphics Option: Full Graphics=1, Partial Graphics=0 |
| -st       | Int      | 2000    | Total Simulation Time                 |
| -tr       | Int      | 100     | Task Rewards                          |
| -df       | Float    | 0.999   | Discounting Factor                    |
| -tpf      | Int      | 3       | Temporal Priority Factor              |
| -tg       | Int      | 10      | Task Generation Time Interval         |
| -rc       | Int      | 5       | Robot Capacity (Maximum Task per Robot) |


The other command line arguments found in the code are for internal testing only and are not recommended to be used.
