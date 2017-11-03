from graphics import MainGraphics
from robotAgent import RobotAgent
from task import Task
from task import TaskAllocation
from util import *

class WorldState():
    def __init__(self, width, height, gridSize, layout, stations, mode, directional = False):
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
        self.mode = mode
        self.completedOrder = 0

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

    def addCompletedOrder(self, order):
        self.completedOrder += order

    def addRobot(self, pos):
        station = pos
        robot = RobotAgent(world=self, canvas=self.canvas, size=self.gridSize, pos=pos, index=len(self.robots) + 1)
        self.robots.append(robot)

    def addTask(self, pos):
        task = Task(canvas=self.canvas, world=self, pos=pos, index=len(self.tasks) + 1)
        self.tasks.append(task)

    def addRandomRobot(self, num):
        for x in range(num):
            if self.stations is not None:
                self.addRobot(generateRandomStation(self))
            else:
                self.addRobot(generateRandomPosition(self))

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

    def isWall(self, pos):
        x,y = pos
        if x > self.width/self.gridSize or y > self.height/self.gridSize or x < 0 or y < 0:
            return False
        if self.layout[x][y] == 1:
            return True
        return False

    def isBlocked(self, pos):
        x,y = pos
        if x > self.width/self.gridSize or y > self.height/self.gridSize or x < 0 or y < 0:
            return False
        if self.isWall(pos) or self.hasRobotAt(pos):
            return True
        return False

    def isBlockedAtRow(self, row):
        for x in range(2, self.width/self.gridSize - 2):
            if self.isBlocked([x,row]):
                return True
        return False

    def isBlockedAtColumn(self, col):
        for y in range(2, self.height/self.gridSize - 2):
            if self.isBlocked([col,y]):
                return True
        return False

    def timerClick(self):
        self.timer += 1
        self.canvas.itemconfig(self.graphics.timerLabel, text=str(self.timer))

    def checkTasksStatus(self):
        self.canvas.itemconfig(self.graphics.taskCountLabel, text=str(len(self.tasks)))

        # Fully randomized mode
        if self.mode == 0:
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
                            print self.mode
                        self.canvas.delete(task.id)
                        self.tasks.remove(task)
        # First Algorithm Mode
        if self.mode == 1:
            for task in self.tasks:
                task.timeoutClick()
                if task.order and not task.assigned:
                    r = TaskAllocation.getClosestAvailableRobot(self, task.pos)
                    if r:
                        r.setTask(task)
                        r.updatePathFiner()

                if self.hasRobotAt(task.pos):
                    r = self.findRobotAt(task.pos)
                    if r.task.pos == task.pos:
                        r.setStatus("Arrived Task Location")
                        r.addLoad(task.order)
                        task.setOrder(0)
                        task.setAssignStatus(False)
                        r.returnToStation()
                        r.setStatus("Returning to Base")

    def update(self):
        self.timerClick()
        self.checkTasksStatus()
        self.graphics.updateStatusBar()
