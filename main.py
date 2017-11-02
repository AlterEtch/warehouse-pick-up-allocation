from graphics import MainGraphics
from world import WorldState
from search import *
from layout import *
import sys
import argparse
import atexit

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

if args.r > len(stations):
    print 'Number of robots exceeds maximum limit'
    sys.exit()

world = WorldState(width=width, height=height, gridSize=gridSize, layout=layout, stations=stations, directional=args.d)
graphics = MainGraphics(world=world)
world.setGraphics(graphics)

world.addRobot(pos=START_POINT[:])
world.addRobot(pos=START_POINT[:])
world.addRobot(pos=START_POINT[:])

# TaskPosList = [[1, 4], [5, 3], [9, 6], [6, 9], [14, 15], [9, 19], [15, 19]]
# for pos in TaskPosList:
#    world.addTask(pos=pos)

world.addRandomTask(20)

# Main loop for window
while True:
    if world.timer % 20 == 0:
        world.addRandomTask(1)
    world.update()
    for robot in world.robots:
        robot.followPath()
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
    if world.timer == 1000:
        break


def exit_handler():
    text = time.strftime("\n%Y-%m-%d %H:%M:%S\n******END******\n", time.localtime())
    write_log(text)
    write_log("Current time: " + str(world.timer) + "\n"
              + "Unassigned task: " + str(len(world.taskCache)) + "\n")


atexit.register(exit_handler)
