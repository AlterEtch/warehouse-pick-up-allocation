from graphics import MainGraphics
from robotAgents import RobotAgent
from world import WorldState
from actions import Actions
import sys

def leftKey(event):
    world.robots[0].move([-1,0])

def rightKey(event):
    world.robots[0].move([1,0])

def upKey(event):
    world.robots[0].move([0,-1])

def downKey(event):
    world.robots[0].move([0,1])

world = WorldState(gridSize=20)
graphics = MainGraphics(layout=world.layout, gridSize=world.gridSize)

world.addRobot(RobotAgent(world=world, canvas=graphics._canvas, size=world.gridSize, pos=[5,6]))

graphics._root_window.bind( "<Left>", leftKey )
graphics._root_window.bind( "<Right>", rightKey )
graphics._root_window.bind( "<Up>", upKey )
graphics._root_window.bind( "<Down>", downKey )

world.robots[0].setPath([Actions.E,Actions.E,Actions.E,Actions.N,Actions.N,Actions.E,Actions.S])

# Main loop for window
while True:
    world.robots[0].followPath()
    graphics._root_window.update_idletasks()
    graphics._root_window.update()
