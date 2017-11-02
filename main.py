from graphics import MainGraphics
from world import WorldState
from search import *
from layout import *
import sys
import argparse
import time

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
    print 'Number of robots exceeds maxmimum limit'
    sys.exit()

world = WorldState(width=width, height=height, gridSize=gridSize, layout=layout, stations=stations, directional=args.d)
graphics = MainGraphics(world=world)
world.setGraphics(graphics)

text = time.strftime("%Y-%m-%d %H:%M:%S\n***START***\n", time.gmtime())
write_log(text, 'w')

world.addRobot(pos=[1, 1])
world.addRobot(pos=[1, 1])
world.addRobot(pos=[1, 1])

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
    graphics.root_window.after(5)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
