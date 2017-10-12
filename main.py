from graphics import MainGraphics
from robotAgent import RobotAgent
from world import WorldState
from actions import Actions
from task import Task
from search import *
from layout import *
import sys
import argparse

LAYOUT_MAP = {'1' : getLayout1,
              '2' : getLayout2,
              '3' : getLayout3}

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-r', type=int, default=5, help="number of robots")
parser.add_argument('-t', type=int, help="number of tasks")
parser.add_argument('-d', type=bool, default=False, help="directional layout")
parser.add_argument('-l', default='1', choices=sorted(LAYOUT_MAP.keys()), help="layout selection")
args = parser.parse_args()
getLayout = LAYOUT_MAP[args.l]
width, height, gridSize, layout = getLayout()

world = WorldState(width=width, height=height, gridSize=gridSize, layout=layout, oneWay=args.d)
graphics = MainGraphics(world=world)
world.setGraphics(graphics)

def setup():
    world.addRandomRobot(args.r)
    world.addRandomTask(args.t or args.r)

    for i in range(len(world.robots)):
        if i < len(world.tasks):
            world.robots[i].setTask(world.tasks[i])

    for robot in world.robots:
        if robot.task != []:
            robot.updatePathFiner()
            try:
                path, dirPath = robot.pathfinder.performAStarSearch()
            except TypeError:
                print 'restarting'
                setup()
            else:
                robot.setPath(dirPath)
                graphics.drawPath(path)

setup()
# Main loop for window
while True:
    world.update()
    for robot in world.robots:
        robot.followPath()
    #graphics.root_window.after(50)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
