from graphics import MainGraphics
from robotAgent import RobotAgent
from world import WorldState
from actions import Actions
from task import Task
from search import *
import sys
import argparse

# Keyboard events for testing
def leftKey(event):
    world.robots[0].move([-1,0])

def rightKey(event):
    world.robots[0].move([1,0])

def upKey(event):
    world.robots[0].move([0,-1])

def downKey(event):
    world.robots[0].move([0,1])

parser = argparse.ArgumentParser(description="Test")
parser.add_argument('-r', type=int)
parser.add_argument('-t', type=int)
parser.add_argument('-o', type=int)
parser.add_argument('-s', type=int)
args = parser.parse_args()

world = WorldState(width=1040, height=800, gridSize=20, oneWay=args.o or False)
graphics = MainGraphics(world=world)
world.setGraphics(graphics)

def setup():
    world.addRandomRobot(args.r or 5)
    world.addRandomTask(args.t or args.r or 5)

    for i in range(len(world.robots)):
        if i < len(world.tasks):
            world.robots[i].setTask(world.tasks[i])

    # Key binding for testing
    graphics.root_window.bind( "<Left>", leftKey )
    graphics.root_window.bind( "<Right>", rightKey )
    graphics.root_window.bind( "<Up>", upKey )
    graphics.root_window.bind( "<Down>", downKey )

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
