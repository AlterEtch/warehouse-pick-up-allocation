from graphics import MainGraphics
from robotAgent import RobotAgent
from task import Task
from util import *
from routing import *

import routing


class WorldState():
    def __init__(self, width, height, gridSize, layout, stations, directional=False):
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
            if task in robot.task:
                return robot
        return 0

    def isBlocked(self, pos):
        x, y = pos
        if self.layout[x][y] == 1:
            return True
        return False

    def neighbors(self, pos):
        (x, y) = pos
        result = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        result = filter(lambda r: not self.isBlocked(r), result)
        return result

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
        self.canvas.itemconfig(self.timerLabel, text=str(self.timer))

    def checkTasksStatus(self):
        self.canvas.itemconfig(self.taskCountLabel, text=str(len(self.tasks)))
        for task in self.tasks:
            if task.progress < task.cost:
                if not self.hasRobotAt(task.pos):
                    task.resetProgress()
                elif task not in self.findRobotAt(task.pos).task:
                    task.resetProgress()
                for robot in self.robots:

                    if task in robot.task:
                        if task.pos == robot.pos and len(robot.path) == 0:
                            task.addProgress()
            else:
                task.timer += 1
                if task.timer >= 10:
                    r = self.findRobotWithTask(task)
                    if r !=0:
                        r.task.remove(task)
                        r.capacityCount+=1
                    self.canvas.delete(task.id)
                    self.tasks.remove(task)

    def aloc_rob(self):
        """
        Calculate the distance saving by saving_dist_table()
        Divide tasks into several segments by sort_task()
        :return: None
        """
        table = saving_dist_table(self, [1, 1])
        #print table
        task_amount = len(self.tasks)
        aloc_task = sort_task(table, task_amount)
        print aloc_task
        for i in range(len(aloc_task)):
            task = aloc_task[i]
            num = i%len(self.robots)
            for j in range(len(task)):
                tmp_task = self.tasks[task[j] - 1]
                self.robots[num].setTask(tmp_task)

    def update_robot_path(self):
        """
        setpath from current position to the next task position
        :return: None
        """
        for robot_ in self.robots:
            if not robot_.path:
                if robot_.task:
                    if robot_.capacityCount<robot_.capacity:
                        path=routing.path_generate(self, robot_.pos, robot_.task[0].pos)
                    else:
                        path = routing.path_generate(self, robot_.pos, [1, 1])
                        robot_.capacityCount=0
                if not robot_.task:
                    path = routing.path_generate(self, robot_.pos, [1, 1])
                robot_.setPath(path)

    def update(self):
        self.timerClick()
        self.checkTasksStatus()
        self.update_robot_path()


