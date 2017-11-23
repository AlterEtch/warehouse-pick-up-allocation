# Warehouse Multi-Robot Automation System Simulation

This is a simple python simulation for warehouse multi-robot automation system.

## Getting Started

### Prerequisites
[Python 2.7](https://www.python.org/download/releases/2.7/)

### Packages/Modules Used
1.  [TKinter](https://docs.python.org/2/library/tkinter.html)
2.  [heapq](https://docs.python.org/2/library/heapq.html)
3.  [random](https://docs.python.org/2/library/random.html)
4.  [math](https://docs.python.org/2/library/math.html#module-math)
5.  [argparse](https://docs.python.org/2/howto/argparse.html)
6.  [copy](https://docs.python.org/2/library/copy.html)

### Running the Project
The project can be run in terminal using the following command:
```
python main.py
```

Command line arguments are supported to modify the simulation parameters. The available arguments and the corresponding default values and description are listed below:
####Command Line Arguments
| Arguments | Type     | Default | Description                           |
| ----------|:---------|:--------|:--------------------------------------|
| -rr       | Int      | 0       | Number of initial robots in the world, randomly generated in stations. Only applicable with multiple stations |
| -fr       | Int      | 3       | Number of initial robots in the world, at a fixed station |
| -t        | Int      | 10      | Number of initial tasks in the world  |
| -l        | Int/Char | 2       | Layout selection                      |
| -g        | Int      | 1       | Graphics Option: Full Graphics=1, Partial Graphics=0 |
