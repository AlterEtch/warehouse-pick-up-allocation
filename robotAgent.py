from actions import Actions
from task import Task
from search import PathFind
from util import *
import copy


class RobotAgent():
    def __init__(self, world, canvas, size, pos, capacity=ROBOT_CAPACITY, power=100000):
        self.pos = copy.deepcopy(pos)
        self.world = world
        self.canvas = canvas
        self.size = size
        self.index = len(world.robots)+1
        self.capacity = capacity
        self.maxPower = power
        self.power = copy.deepcopy(power)
        self.load = 0
        self.status = "Waiting for Order"
        self.id_shape = self.canvas.create_oval(self.pos[0] * self.size, self.pos[1] * self.size, (self.pos[0] + 1) * self.size, (self.pos[1] + 1) * self.size, fill="green", tag="robot" + str(self.index))
        self.id_text = self.canvas.create_text((self.pos[0] + 0.5) * self.size, (self.pos[1] + 0.5) * self.size, fill="black", text=self.index, tag="robot" + str(self.index))
        self.task = []
        self.path = []
        self.station = Task(canvas=self.canvas, world=self.world, pos=copy.deepcopy(self.pos), isStation=True)
        self.assignable = True
        self.capacityCount = 0

    def move(self, direction):
        possibleActions = self.getPossibleActions()
        if possibleActions == [Actions.STOP] and len(self.path):
            possibleActions = self.getPossibleActions(override=True)
        if direction in possibleActions and self.power:
            self.pos[0] += direction[0]
            self.pos[1] += direction[1]
            self.power -= 1
            self.world.totalMileage += 1
            # Animate the movement of robot
            for x in range(0, 2):
                for obj in self.canvas.find_withtag("robot" + str(self.index)):
                    self.canvas.move(obj, direction[0] * self.size / 2, direction[1] * self.size / 2)
                    self.canvas.update()
        elif not self.power:
            self.setStatus("Out of Power")
        else:
            if len(self.path):
                self.updatePathFiner()
                try:
                    path, dirPath = self.pathfinder.performAStarSearch(override=True)
                except TypeError:
                    self.path.insert(0, [0, 0])
                else:
                    self.path = dirPath
                    if False:
                        self.world.graphics.drawPath(path)

    def getPossibleActions(self):
        return Actions.possibleActions(self.pos, self.world)

    def setTask(self, task):
        self.task.append(task)
        task.setAssignStatus(True)

    def delete_task(self, task):
        self.task.remove(task)
        write_log("\nAt time:" + str(self.world.timer) + "\n\t" +
                  str(task) + " at " + str(task.pos) + " is consumed")
        self.capacityCount += 1
        self.world.completedTask += 1
        self.world.canvas.delete(task.id_shape)
        self.world.canvas.delete(task.id_text)

    def setPath(self, path):
        self.path += path

    def setStatus(self, status):
        self.status = status

    def addLoad(self, load):
        self.load += load

    def atStation(self):
        return self.world.findStationAt(self.pos)

    def chargeBattery(self):
        station = self.world.findStationAt(self.station.pos)
        if station:
            self.power = min(self.power + station.chargingRate, self.maxPower)

    def followPath(self):
        if len(self.path) != 0:
            self.move(self.path[0])
            self.path.pop(0)
            if not len(self.path) and self.task:
                if self.task[0].isStation:
                    self.setStatus("Waiting for Order")
                    self.world.addCompletedOrder(self.load)
                    self.load = 0
                    self.task = []

    def updatePathFiner(self):
        self.pathfinder = PathFind(self)
        try:
            path, dirPath = self.pathfinder.performAStarSearch()
            self.setPath(dirPath)
        except TypeError:
            self.setStatus("Error")

    def returnToStation(self):
        self.task = self.station
        self.updatePathFiner()
        try:
            path, dirPath = self.pathfinder.performAStarSearch()
            self.setPath(dirPath)
            if False:
                self.world.graphics.drawPath(path)
        except TypeError:
            print 'error1'
