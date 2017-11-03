from robotAgent import RobotAgent
from task import Task
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
        self.taskCache = []
        self.timer = 0
        self.directional = directional
        self.graphics = []
        self.taskAllocationIndex = []

    def setGraphics(self, graphics):
        self.graphics = graphics
        self.canvas = self.graphics.canvas

    def setWallLayout(self, layout):
        self.layout = layout
        if self.graphics:
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
        write_log("\nAt time:" + str(self.timer) + "\n" +
                  str(task) + " at " + str(task.pos) + " is added\n")
        self.taskCache.append(task)

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
        for task in self.taskCache:
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
        for x in range(2, self.width / self.gridSize - 2):
            if self.isBlocked([x, row]):
                return True
        return False

    def isBlockedAtColumn(self, col):
        for y in range(2, self.height / self.gridSize - 2):
            if self.isBlocked([col, y]):
                return True
        return False

    def timerClick(self):
        self.timer += 1
        self.canvas.itemconfig(self.timerLabel, text=str(self.timer))

    def checkTasksStatus(self):
        self.canvas.itemconfig(self.taskCountLabel, text=str(len(self.taskCache)))
        for robot in self.robots:
            for task in robot.task:
                if task.progress < task.cost:
                    if not self.hasRobotAt(task.pos):
                        task.resetProgress()
                    elif task not in self.findRobotAt(task.pos).task:
                        task.resetProgress()
                    if task.pos == robot.pos and len(robot.path) == 0:
                        task.addProgress()
                else:
                    task.timer += 1
                    if task.timer >= 10:
                        r = self.findRobotWithTask(task)
                        if r != 0:
                            r.task.remove(task)
                            write_log("\nAt time:" + str(self.timer) + "\n" +
                                      str(task) + " at " + str(task.pos) + " is consumed\n")
                            r.capacityCount += 1
                        self.canvas.delete(task.id)
                        self.canvas.delete(task.id_label)

    def allocate_rob(self):
        """
        Assign task to the free robot.
        :return:None
        """
        if self.hasRobotAt(START_POINT[:]):
            r = self.findRobotAt(START_POINT[:])
            if not r.task:
                task = sort_task(self)
                tmp_task = []
                write_log("\nAt time:" + str(self.timer) + "\n" +
                          str(r) + " labeled as Robot " + str(r.id_num) + " accepts the task:" + str(task) + " at pos:")
                if task:
                    for index in task:
                        tmp_task.append(self.taskCache[index])
                        r.setTask(tmp_task[-1])
                        text = str(tmp_task[-1].pos)
                        write_log(text)
                    write_log("\n")
                    for i in tmp_task:
                        self.taskCache.remove(i)
                    self.refresh_task_label()

    def update_robot_path(self):
        """
        setpath from current position to the next task position
        :return: None
        """
        for r in self.robots:
            if not r.path:
                path = []
                if r.task:
                    if r.capacityCount < r.capacity:
                        path = routing.path_generate(self, r.pos, r.task[0].pos)
                    else:
                        path = routing.path_generate(self, r.pos, START_POINT[:])
                        r.capacityCount = 0
                if not r.task:
                    path = routing.path_generate(self, r.pos, START_POINT[:])
                r.setPath(path)

    def refresh_task_label(self):
        i = 0
        for task in self.taskCache:
            self.canvas.itemconfig(task.id_label,text=str(i))
            i += 1



    def update(self):
        self.timerClick()
        self.checkTasksStatus()
        self.allocate_rob()
        self.update_robot_path()
