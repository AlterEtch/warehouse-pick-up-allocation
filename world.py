from graphics import MainGraphics
from robotAgent import RobotAgent
from task import Task
from util import *

class WorldState():
    def __init__(self, width, height, gridSize, oneWay = False):
        self.gridSize = gridSize
        self.width = width
        self.height = height
        self.initWallLayout()
        self.robots = []
        self.tasks = []
        self.timer = 0
        self.oneWay = oneWay
        self.graphics = []

    def initWallLayout(self):
        wallLayout = [[0 for row in range(0,self.height/self.gridSize)] for col in range(0,self.width/self.gridSize)]
        for x in range(0, self.width/self.gridSize):
            for y in range(0, self.height/self.gridSize):
                if x == 0 or y == 0 or x == self.width/self.gridSize-1 or y == self.height/self.gridSize-1:
                    wallLayout[x][y] = 1

        for i in range(0, self.width/(2*self.gridSize)-1):
            for j in range(1, self.height/self.gridSize):
                if i % 2:
                    wallLayout[2*i+1][j] = 1
                    wallLayout[2*i+2][j] = 1

        for m in range(1, self.width/self.gridSize-2):
            for n in range(1, self.height/self.gridSize-1, 7):
                wallLayout[m][n] = 0
                wallLayout[m+1][n] = 0
                wallLayout[m][n+1] = 0
                wallLayout[m][n+2] = 0
                wallLayout[m+1][n+1] = 0

        self.layout = wallLayout

    def setGraphics(self, graphics):
        self.graphics = graphics
        self.canvas = self.graphics.canvas

    def setWallLayout(self, layout):
        self.layout = layout
        if self.graphics != []:
            self.graphics.delete("all")
            self.graphics.drawWalls()
            self.graphics.drawGrids()
            self.graphics.canvas.pack()
            self.graphics.canvas.update()

    def addRobot(self, pos):
        robot = RobotAgent(world=self, canvas=self.canvas, size=self.gridSize, pos=pos)
        self.robots.append(robot)

    def addTask(self, pos):
        task = Task(canvas=self.canvas, gridSize=self.gridSize, pos=pos)
        self.tasks.append(task)

    def addRandomRobot(self, num):
        for x in range(num):
            self.addRobot(generateRandomPosition(self))

    def addRandomTask(self, num):
        for x in range(num):
            self.addTask(generateRandomPosition(self))

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
        x,y = pos
        if self.layout[x][y] == 1 or self.hasRobotAt(pos):
            return True
        return False

    def timerClick(self):
        self.timer += 1
        self.canvas.itemconfig(self.timerLabel, text=str(self.timer))

    def checkTasksStatus(self):
        self.canvas.itemconfig(self.taskCountLabel, text=str(len(self.tasks)))
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

    def update(self):
        self.timerClick()
        self.checkTasksStatus()
