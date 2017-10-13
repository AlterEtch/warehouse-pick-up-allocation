from graphics import MainGraphics
from robotAgent import RobotAgent
from task import Task
from util import *

class WorldState():
    def __init__(self, width, height, gridSize, layout, stations, directional = False):
        self.gridSize = gridSize
        self.width = width
        self.height = height
        self.layout = layout
        self.stations = stations
        self.robots = []
        self.tasks = []
        self.timer = 0
        self.directional = directional
        self.graphics = []

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
        station = pos
        robot = RobotAgent(world=self, canvas=self.canvas, size=self.gridSize, pos=pos)
        self.robots.append(robot)

    def addTask(self, pos):
        task = Task(canvas=self.canvas, gridSize=self.gridSize, pos=pos)
        self.tasks.append(task)

    def addRandomRobot(self, num):
        for x in range(num):
            self.addRobot(generateRandomStation(self))

    def addRandomTask(self, num):
        for x in range(num):
            self.addTask(generateRandomPosition(self))

    def hasRobotAt(self, pos):
        return self.findRobotAt(pos) != 0

    def hasTaskAt(self, pos):
        return self.findTaskAt(pos) != 0

    def hasStationAt(self, pos):
        return self.findStationAt(pos) != 0

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

    def findStationAt(self, pos):
        for station in self.stations:
            if station.pos == pos:
                return station
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

    def neighbors(self,pos):
        (x,y)=pos
        result=[(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
        result = filter(lambda r: not self.isBlocked(r),result)
        return result

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
                    r = self.findRobotWithTask(task)
                    if r != 0:
                        r.returnToStation()
                    self.canvas.delete(task.id)
                    self.tasks.remove(task)

    def update(self):
        self.timerClick()
        self.checkTasksStatus()

    def cost(self,fromPos1,toPos2):
        return 1
