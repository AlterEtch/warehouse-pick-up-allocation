from graphics import MainGraphics
from world import WorldState
from search import *
from layout import *
from util import *
import sys
import argparse
import atexit


LAYOUT_MAP = {'1': getLayout1,
              '2': getLayout2,
              '3': getLayout3}

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-rr', type=int, default=0, help="number of randomized robots")
parser.add_argument('-fr', type=int, default=3, help="number of fixed robots")
parser.add_argument('-t', type=int, default=10, help="number of tasks")
parser.add_argument('-d', type=bool, default=False, help="directional layout")
parser.add_argument('-l', default='2', choices=sorted(LAYOUT_MAP.keys()), help="layout selection")
parser.add_argument('-m', type=int, default=10, help="task allocation mode")
args = parser.parse_args()

getLayout = LAYOUT_MAP[args.l]
width, height, gridSize, layout, stations = getLayout()

# if args.m == 1 and args.r > len(stations):
#     print 'Number of robots exceeds maxmimum limit'
#     sys.exit()

world = WorldState(width=width, height=height, gridSize=gridSize, layout=layout, stations=stations, directional=args.d, mode=args.m)
graphics = MainGraphics(world=world)
world.set_graphics(graphics)


# TaskPosList = [[1, 4], [5, 3], [9, 6], [6, 9], [14, 15], [9, 19], [15, 19]]
# for pos in TaskPosList:
#    world.add_task(pos=pos)


# world.add_random_task(10)

# Main loop for window
def setup():
    if args.rr:
        world.add_random_robot(args.rr)
    for i in range(args.fr):
        world.add_robot(world.stations[8].pos)
    world.add_random_task(args.t)

    if args.m == 0:
        for i in range(len(world.robots)):
            if i < len(world.tasks):
                world.robots[i].add_task(world.tasks[i])

    graphics.createRobotStatusBar()
    graphics.createTaskStatusBar()

    if args.m == 0:
        for robot in world.robots:
            if robot.task != []:
                robot.update_path_finder()
                try:
                    path, dirPath = robot.pathfinder.perform_a_star_search()
                except TypeError:
                    print 'restarting'
                    setup()
                else:
                    robot.set_path(dirPath)


setup()

text = time.strftime("%Y-%m-%d %H:%M:%S\n******************START******************\n", time.localtime())
write_log(text, 'w')
write_log("There are " + str(len(world.robots)) + " robots with capacity of " + str(ROBOT_CAPACITY) + ".\n" +
          "Every " + str(TASK_TIME_INTERVAL) + " units of time, a task is generated randomly \n")
while True:
    if world.timer % TASK_TIME_INTERVAL == 0 and world.mode == 10:
        world.add_random_task(1)
    world.update()
    for robot in world.robots:
        robot.follow_path()
    graphics.root_window.after(10)
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
