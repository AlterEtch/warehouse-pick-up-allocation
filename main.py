from graphics import MainGraphics
from robotAgent import RobotAgent
from world import WorldState
from actions import Actions
from task import Task
from search import *
import sys

# Keyboard events for testing
def leftKey(event):
    world.robots[0].move([-1,0])

def rightKey(event):
    world.robots[0].move([1,0])

def upKey(event):
    world.robots[0].move([0,-1])

def downKey(event):
    world.robots[0].move([0,1])

world = WorldState(width=880, height=680, gridSize=20)
graphics = MainGraphics(world=world)
world.setCanvas(graphics.canvas)

world.addRobot(pos=[1,1])
#world.addRobot(pos=[2,1])

world.addTask(pos=[3,7])
world.addTask(pos=[14,16])

# Key binding for testing
graphics.root_window.bind( "<Left>", leftKey )
graphics.root_window.bind( "<Right>", rightKey )
graphics.root_window.bind( "<Up>", upKey )
graphics.root_window.bind( "<Down>", downKey )

world.robots[0].setPath([Actions.S,Actions.E,Actions.E,Actions.E,Actions.E,Actions.E,Actions.E,Actions.E,Actions.E,Actions.E,Actions.S,Actions.S,Actions.S,Actions.S,Actions.S,Actions.S,Actions.S,Actions.S])
#world.robots[1].setPath([Actions.E,Actions.E,Actions.W,Actions.S,Actions.N,Actions.E,Actions.S])

world.robots[0].setTask(world.tasks[0])

print '2'

pf = AStarSearch(world.robots[0])
path, dirPath = pf.performSearch()

world.robots[0].setPath(dirPath)

graphics.drawPath(path)

# Main loop for window
while True:
    world.update()
    for robot in world.robots:
        robot.followPath()
    graphics.root_window.after(500)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
