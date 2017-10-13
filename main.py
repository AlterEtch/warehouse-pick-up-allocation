from graphics import MainGraphics
from robotAgent import RobotAgent
from world import WorldState
from actions import Actions
from task import Task
from search import *
from layout import *
from routing import *
import graph
import sys
import argparse

LAYOUT_MAP = {'1' : getLayout1,
              '2' : getLayout2,
              '3' : getLayout3}

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-r', type=int, default=5, help="number of robots")
parser.add_argument('-t', type=int, help="number of tasks")
parser.add_argument('-d', type=bool, default=False, help="directional layout")
parser.add_argument('-l', default='2', choices=sorted(LAYOUT_MAP.keys()), help="layout selection")
args = parser.parse_args()
getLayout = LAYOUT_MAP[args.l]
width, height, gridSize, layout, stations = getLayout()

world = WorldState(width=width, height=height, gridSize=gridSize, layout=layout, stations=stations, directional=args.d)
graphics = MainGraphics(world=world)
world.setGraphics(graphics)

world.addRobot(pos=[1, 1])
world.addRobot(pos=[2, 1])
TaskPosList = [[1, 4], [5, 3], [9, 6], [6, 9],[14,15],[33,18],[37,18]]
for pos in TaskPosList:
    world.addTask(pos=pos)

table = saving_dist_table(world, [1, 1])

SortTask = sort_task(table, len(TaskPosList))
print SortTask


# Main loop for window
while True:
    world.update()
    for robot in world.robots:
        robot.followPath()
    graphics.root_window.after(500)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
