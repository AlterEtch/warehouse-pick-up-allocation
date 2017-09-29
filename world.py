from graphics import MainGraphics
from robotAgent import RobotAgent
from task import Task

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
            if robot.pos[0] == pos[0] and robot.pos[1] == pos[1]:
                return True

    def isBlocked(self, pos):
        x = pos[0]
        y = pos[1]
        if self.layout[x][y] == 1 or self.hasRobotAt(pos):
            return True
        return False

    def checkTasksStatus(self):
        for task in self.tasks:
            for robot in self.robots:
                if not self.hasRobotAt(task.pos):
                    task.resetProgress()
                if robot.task == task:
                    if robot.pos == task.pos and len(robot.path) == 0:
                        task.addProgress()
