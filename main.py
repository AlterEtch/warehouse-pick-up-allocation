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

for i in range(3):
    world.addRobot(pos=START_POINT[:])

# TaskPosList = [[1, 4], [5, 3], [9, 6], [6, 9], [14, 15], [9, 19], [15, 19]]
# for pos in TaskPosList:
#    world.addTask(pos=pos)

text = time.strftime("%Y-%m-%d %H:%M:%S\n******************START******************\n", time.localtime())
write_log(text, 'w')
write_log("There are " + str(len(world.robots)) + " robots with capacity of " + str(ROBOT_CAPACITY) + ".\n" +
          "Every " + str(TASK_TIME_INTERVAL) + " units of time, a task is generated randomly \n")
# world.addRandomTask(10)

# Main loop for window
while True:
    if world.timer % TASK_TIME_INTERVAL == 0:
        world.addRandomTask(1)
    world.update()
    for robot in world.robots:
        robot.followPath()
    # graphics.root_window.after(25)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
    if world.timer == 2000:
        break


def exit_handler():
    """
    When program exits, raise the handler
    :return:None
    """
    output_log(world)


atexit.register(exit_handler)
