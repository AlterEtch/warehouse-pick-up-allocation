from graphics import MainGraphics
from world import WorldState
from layout import *
import util
import argparse
import atexit

LAYOUT_MAP = {'1': get_layout1,
              '2': get_layout2,
              '3': get_layout3,
              '4': get_layout4}

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-rr', type=int, default=0, help="number of randomized robots")
parser.add_argument('-fr', type=int, default=20, help="number of fixed robots")
parser.add_argument('-t', type=int, default=10, help="number of tasks")
parser.add_argument('-d', type=bool, default=False, help="directional layout")
parser.add_argument('-l', default='4', choices=sorted(LAYOUT_MAP.keys()), help="layout selection")
parser.add_argument('-m', type=int, default=10, help="task allocation mode")
parser.add_argument('-g', type=int, default=1, help="graphics")
parser.add_argument('-st', type=int, default=2000, help="simulation time")
parser.add_argument('-tr', type=int, default=100, help="task rewards")
parser.add_argument('-df', type=float, default=0.999, help="discounting factor")
parser.add_argument('-tpf', type=float, default=5, help="temporal priority factor")
parser.add_argument('-tg', type=int, default=40, help="task generation time interval")
parser.add_argument('-rc', type=int, default=10, help="robot capacity")

args = parser.parse_args()

util.INITIAL_TASK = args.t
util.GRAPHICS_ON = args.g
util.SIMULATION_TIME = args.st
util.TASK_REWARD = args.tr
util.DISCOUNTING_FACTOR = args.df
util.TEMPORAL_PRIORITY_FACTOR = args.tpf
util.TASK_TIME_INTERVAL = args.tg
util.ROBOT_CAPACITY = args.rc

getLayout = LAYOUT_MAP[args.l]
width, height, gridSize, layout, stations, gridCost = getLayout()

world = WorldState(width=width, height=height, gridSize=gridSize, layout=layout, stations=stations, gridCost=gridCost, directional=args.d, mode=args.m)
graphics = MainGraphics(world=world)
world.set_graphics(graphics)


# Main loop for window
def setup():
    if args.rr:
        world.add_random_robot(args.rr)
    for i in range(args.fr):
        world.add_robot(world.stations[0].pos)
    world.add_random_task(util.INITIAL_TASK)

    if args.m == 0:
        for i in range(len(world.robots)):
            if i < len(world.tasks):
                world.robots[i].add_task(world.tasks[i])

    graphics.create_robot_status_bar()

    if args.m != 10:
        graphics.create_task_status_bar()


setup()

while True:
    if world.timer % util.TASK_TIME_INTERVAL == 0 and world.mode == 10:
        world.add_random_task(14)
    world.update()
    for robot in world.robots:
        robot.follow_path()
    graphics.root_window.after(0)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
    if world.timer == util.SIMULATION_TIME:
        break


def exit_handler():
    """
    When program exits, raise the handler
    :return:None
    """
    print 'Task Reward: ', world.taskRewards
    print 'Energy Cost: ', float(world.totalMileage)
    print 'Total Reward: ', world.taskRewards - float(world.totalMileage)
    print 'Task Completed: ', world.completedTask


atexit.register(exit_handler)
