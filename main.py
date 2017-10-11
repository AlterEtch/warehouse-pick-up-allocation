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
world.setGraphics(graphics)
#world.setCanvas(graphics.canvas)

# world.addRobot(pos=[1,1])
# world.addRobot(pos=[15,1])
# world.addRobot(pos=[26,24])
#
# world.addTask(pos=[3,7])
# world.addTask(pos=[14,16])
# world.addTask(pos=[22,21])

if len(sys.argv) == 2:
    world.addRandomRobot(int(sys.argv[1]))
    world.addRandomTask(int(sys.argv[1]))
elif len(sys.argv) == 3:
    world.addRandomRobot(int(sys.argv[1]))
    world.addRandomTask(int(sys.argv[2]))
else:
    world.addRandomRobot(6)
    world.addRandomTask(6)

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
        path, dirPath = robot.pathfinder.performAStarSearch()
        robot.setPath(dirPath)
        graphics.drawPath(path)

# Main loop for window
while True:
    world.update()
    for robot in world.robots:
        robot.followPath()
    graphics.root_window.after(50)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
