from graphics import MainGraphics

class WorldState():
    def __init__(self, gridSize=40):
        self.gridSize = gridSize
        self.layout = self.initWallLayout(width=800, height=640, gridSize=self.gridSize)
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

    def setWallLayout(self, layout):
        self.layout = layout

    def addRobot(self, robot):
        self.robots.append(robot)

    def addTask(self, task):
        self.tasks.append(task)

    def isBlocked(self, pos):
        x = pos[0]
        y = pos[1]
        if self.layout[x][y] == 1:
            return True
        for robot in self.robots:
            if robot.pos[0] == x and robot.pos[1] == y:
                return True
        return False
