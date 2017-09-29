from graphics import MainGraphics
from robotAgents import RobotAgent
from world import WorldState
import sys

def leftKey(event):
    world.robots[0].move([-1,0],Actions.possibleActions(world.robots[0].pos, world))

def rightKey(event):
    world.robots[0].move([1,0],Actions.possibleActions(world.robots[0].pos, world))

def upKey(event):
    world.robots[0].move([0,-1],Actions.possibleActions(world.robots[0].pos, world))

def downKey(event):
    world.robots[0].move([0,1],Actions.possibleActions(world.robots[0].pos, world))

class Actions:
    E = [1,0]
    S = [0,1]
    W = [-1,0]
    N = [0,-1]
    STOP = [0,0]

    @staticmethod
    def possibleActions(pos, states):
        x = pos[0]
        y = pos[1]
        possible = [Actions.STOP]
        if not states.isBlocked([x+1,y]):
            possible.append(Actions.E)
        if not states.isBlocked([x-1,y]):
            possible.append(Actions.W)
        if not states.isBlocked([x,y+1]):
            possible.append(Actions.S)
        if not states.isBlocked([x,y-1]):
            possible.append(Actions.N)
        return possible

world = WorldState(gridSize=20)
graphics = MainGraphics(layout=world.layout, gridSize=world.gridSize)

world.addRobot(RobotAgent(canvas=graphics._canvas, size=world.gridSize, pos=[5,6]))

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
