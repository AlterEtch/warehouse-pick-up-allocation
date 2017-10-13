from graphics import MainGraphics
from robotAgent import RobotAgent
from world import WorldState
from actions import Actions
from task import Task
from search import *
from layout import *
from routing import *
import graph
import sys
import argparse


# Keyboard events for testing
def leftKey(event):
    world.robots[0].move([-1, 0])


def rightKey(event):
    world.robots[0].move([1, 0])


def upKey(event):
    world.robots[0].move([0, -1])


def downKey(event):
    world.robots[0].move([0, 1])


world = WorldState(width=880, height=680, gridSize=20)
graphics = MainGraphics(world=world)
world.setGraphics(graphics)

# Key binding for testing
graphics.root_window.bind("<Left>", leftKey)
graphics.root_window.bind("<Right>", rightKey)
graphics.root_window.bind("<Up>", upKey)
graphics.root_window.bind("<Down>", downKey)

world.addRobot(pos=[1, 1], label='0')
world.addRobot(pos=[2, 1], label='1')
TaskPosList = [[1, 4], [5, 3], [9, 6], [6, 9],[14,15],[33,18],[37,18]]
for pos in TaskPosList:
    world.addTask(pos=pos)

table = saving_dist_table(world, [1, 1])

SortTask = sort_task(table, len(TaskPosList))
print SortTask


# Main loop for window
while True:
    world.update()
    for robot in world.robots:
        robot.followPath()
    graphics.root_window.after(500)
    graphics.root_window.update_idletasks()
    graphics.root_window.update()
