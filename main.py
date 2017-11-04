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
parser.add_argument('-rr', type=int, default=5, help="number of randomized robots")
parser.add_argument('-fr', type=int, default=0, help="number of fixed robots")
parser.add_argument('-t', type=int, default=5, help="number of tasks")
parser.add_argument('-d', type=bool, default=False, help="directional layout")
parser.add_argument('-l', default='1', choices=sorted(LAYOUT_MAP.keys()), help="layout selection")
parser.add_argument('-m', type=int, default=1, help="task allocation mode")
args = parser.parse_args()

getLayout = LAYOUT_MAP[args.l]
width, height, gridSize, layout, stations = getLayout()

# if args.m == 1 and args.r > len(stations):
#     print 'Number of robots exceeds maxmimum limit'
#     sys.exit()

print args.m
world = WorldState(width=width, height=height, gridSize=gridSize, layout=layout, stations=stations, directional=args.d, mode=args.m)
graphics = MainGraphics(world=world)
world.setGraphics(graphics)

def setup():
    if args.rr:
        world.addRandomRobot(args.rr)
    for i in range(args.fr):
        world.addRobot(world.stations[0].pos)
    world.addRandomTask(args.t)

    if args.m == 0:
        for i in range(len(world.robots)):
            if i < len(world.tasks):
                world.robots[i].setTask(world.tasks[i])

    graphics.createRobotStatusBar()
    graphics.createTaskStatusBar()

    if args.m == 0:
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
                    #graphics.drawPath(path)

setup()
# Main loop for window
while True:
    world.update()
    if args.m == 1:
        if not world.timer % 1:
            for task in world.tasks:
                task.checkOrder()
    for robot in world.robots:
        robot.followPath()
        if len(robot.path):
            if robot.status != "Returning to Base":
                robot.setStatus("Fetching Order")
    graphics.root_window.after(5)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
