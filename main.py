from graphics import MainGraphics
from robotAgent import RobotAgent
from world import WorldState
from actions import Actions
from task import Task
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
world.addRobot(pos=[2,1])

world.addTask(pos=[10,10])

# Key binding for testing
graphics.root_window.bind( "<Left>", leftKey )
graphics.root_window.bind( "<Right>", rightKey )
graphics.root_window.bind( "<Up>", upKey )
graphics.root_window.bind( "<Down>", downKey )

#world.robots[0].setPath([Actions.E,Actions.E,Actions.E,Actions.N,Actions.N,Actions.E,Actions.S])
#world.robots[1].setPath([Actions.S,Actions.N,Actions.W,Actions.S,Actions.N,Actions.E,Actions.S])

world.robots[0].setTask(world.tasks[0])

# Main loop for window
while True:
    for robot in world.robots:
        robot.followPath()
    world.checkTasksStatus()
    graphics.root_window.after(250)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
