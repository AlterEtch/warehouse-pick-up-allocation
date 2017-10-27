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

LAYOUT_MAP = {'1': getLayout1,
              '2': getLayout2,
              '3': getLayout3}

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


# test begin @Zheng
def leftKey(event):
    world.robots[0].move([-1, 0])


def rightKey(event):
    world.robots[0].move([1, 0])


def upKey(event):
    world.robots[0].move([0, -1])


def downKey(event):
    world.robots[0].move([0, 1])


graphics.root_window.bind("<Left>", leftKey)
graphics.root_window.bind("<Right>", rightKey)
graphics.root_window.bind("<Up>", upKey)
graphics.root_window.bind("<Down>", downKey)

world.addRobot(pos=[1, 1])
world.addRobot(pos=[2, 1])
world.addRobot(pos=[3, 1])

#TaskPosList = [[1, 4], [5, 3], [9, 6], [6, 9], [14, 15], [9, 19], [15, 19]]
#for pos in TaskPosList:
#    world.addTask(pos=pos)

world.addRandomTask(20)

world.aloc_rob()
# test end


# Main loop for window
while True:
    world.update()
    for robot in world.robots:
        robot.followPath()
    graphics.root_window.after(25)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
