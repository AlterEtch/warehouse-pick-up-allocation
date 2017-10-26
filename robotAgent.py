from time import sleep
from actions import Actions
from task import *
from search import *
import copy
import routing


class RobotAgent():
    def __init__(self, world, canvas, size, pos):
        self.pos = pos
        self.world = world
        self.canvas = canvas
        self.size = size
        self.id = self.canvas.create_oval(self.pos[0] * self.size, self.pos[1] * self.size,
                                          (self.pos[0] + 1) * self.size, (self.pos[1] + 1) * self.size, fill="green")
        self.task = []
        self.path = []
        self.station = Task(canvas=self.canvas, gridSize=self.world.gridSize, pos=copy.deepcopy(self.pos),
                            isStation=True)

    def move(self, direction):
        possibleActions = self.getPossibleActions()
        if possibleActions == [Actions.STOP] and len(self.path):
            possibleActions = self.getPossibleActions(override=True)
        if direction in possibleActions:
            self.pos[0] += direction[0]
            self.pos[1] += direction[1]
            # Animate the movement of robot
            for x in range(0, self.size / (self.size / 2)):
                self.canvas.move(self.id, direction[0] * self.size / 2, direction[1] * self.size / 2)
                self.canvas.update()
        else:
            if len(self.path):
                print 'recalculating path'
                self.updatePathFiner()
                try:
                    path, dirPath = self.pathfinder.performAStarSearch(override=True)
                except TypeError:
                    self.path.insert(0,[0,0])
                else:
                    self.path = dirPath
                    self.world.graphics.drawPath(path)

    def getPossibleActions(self, override=False):
        return Actions.possibleActions(self.pos, self.world, override)

    def setTask(self, task):
        self.task.append(task)
        task.setAssignStatus(True)

    def setPath(self, path):
        self.path += path

    def followPath(self):
        if len(self.path) != 0:
            self.move(self.path[0])
            self.path.pop(0)

    def updatePathFiner(self):
        self.pathfinder = PathFind(self)

    def returnToStation(self):
        self.task = self.station
        self.updatePathFiner()
        try:
            path, dirPath = self.pathfinder.performAStarSearch()
            self.setPath(dirPath)
            self.world.graphics.drawPath(path)
        except TypeError:
            print 'error1'
            # try:
            #     path, dirPath = self.pathfinder.performAStarSearch(override)
            #     self.setPath(dirPath)
            #     self.world.graphics.drawPath(path)
            # except TypeError:
            #     print 'error2'

    def allocation(self, index, destination=None):
        """
        Generate path sequence by gen_rob_path(),
        Move robot to location by setPath().
        If destination is not set,
        robot returns to starting point.
        :param index: a sequence whose elements representing tasks in the world
        :param destination: the point that the robot will go to after finish tasks
        :return: None
        """
        if destination is None:
            destination = self.pos
        for i in range(len(index)):
            task=self.world.tasks[index[i] - 1]
            self.setTask(task)
        path = self.gen_rob_path(destination)
        self.setPath(path)

    def gen_rob_path(self, destination):
        """
        Generate a path moving to each task in turn, according to the order of the task,
        :param destination: the point that the robot will go to after finish tasks
        :return: list (with element of E,W,N,S)
        """
        tmp_task = []
        task_amount = len(self.task)
        for i in range(task_amount):
            position = self.task[i].pos
            tmp_task.append(position)
        self.task=[]
        tmp_task.append(destination)
        tmp_task.insert(0, self.pos)
        path = []
        for i in range(task_amount + 1):
            path += routing.path_generate(self.world, tmp_task[i], tmp_task[i + 1])
        return path
