from graphics import MainGraphics
from robotAgent import RobotAgent
from task import Task
from util import *

class WorldState():
    def __init__(self, width=800, height=640, gridSize=40):
        self.gridSize = gridSize
        self.width = width
        self.height = height
        self.layout = self.initWallLayout(width=self.width, height=self.height, gridSize=self.gridSize)
        self.robots = []
        self.tasks = []

    def initWallLayout(self, width, height, gridSize):
        wallLayout = [[0 for row in range(0,height/gridSize)] for col in range(0,width/gridSize)]
        for x in range(0, width/gridSize):
            for y in range(0, height/gridSize):
                if x == 0 or y == 0 or x == width/gridSize-1 or y == height/gridSize-1:
                    wallLayout[x][y] = 1
        wallLayout[3][5] = 1
        wallLayout[3][6] = 1
        return wallLayout

    def setCanvas(self, canvas):
        self.canvas = canvas

    def setWallLayout(self, layout):
        self.layout = layout

    def addRobot(self, pos):
        robot = RobotAgent(self, canvas=self.canvas, size=self.gridSize, pos=pos)
        self.robots.append(robot)

    def addTask(self, pos):
        task = Task(canvas=self.canvas, gridSize=self.gridSize, pos=pos)
        self.tasks.append(task)

    def hasRobotAt(self, pos):
        for robot in self.robots:
            if robot.pos == pos:
                return True
        return False

    def hasTaskAt(self, pos):
        for task in self.tasks:
            if task.pos == pos:
                return True
        return False

    def findRobotAt(self, pos):
        for robot in self.robots:
            if robot.pos == pos:
                return robot
        return 0

    def findTaskAt(self, pos):
        for task in self.tasks:
            if task.pos == pos:
                return task
        return 0

    def findRobotWithTask(self, task):
        for robot in self.robots:
            if robot.task == task:
                return robot
        return 0

    def isBlocked(self, pos):
        x = pos[0]
        y = pos[1]
        if self.layout[x][y] == 1 or self.hasRobotAt(pos):
            return True
        return False

    def checkTasksStatus(self):
        for task in self.tasks:
            if task.progress < task.cost:
                if not self.hasRobotAt(task.pos):
                    task.resetProgress()
                elif self.findRobotAt(task.pos).task != task:
                    task.resetProgress()
                for robot in self.robots:
                    if robot.task == task:
                        if task.pos == robot.pos and len(robot.path) == 0:
                            task.addProgress()
            else:
                task.timer += 1
                if task.timer >= 10:
                    if self.findRobotWithTask(task) != 0:
                        self.findRobotWithTask(task).task = []
                    self.canvas.delete(task.id)
                    self.tasks.remove(task)
