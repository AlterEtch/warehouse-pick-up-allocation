from math import *
import util
import random
import copy

class Task():
    def __init__(self, canvas, world, pos, index=0, cost=1, isStation=False, mean=0.05, timeout=300):
        self.pos = pos
        self.canvas = canvas
        self.world = world
        self.size = self.world.gridSize * 0.5
        self.cost = cost
        self.index = index
        self.isStation = isStation
        self.mean = mean
        self.timeout = copy.deepcopy(timeout)
        self.timeleft = copy.deepcopy(timeout)
        if not self.isStation:
            self.shape = self.canvas.create_oval(self.pos[0]*self.world.gridSize + 0.5*(self.world.gridSize-self.size), self.pos[1]*(self.world.gridSize) + 0.5*(self.world.gridSize-self.size), (self.pos[0]+1)*self.world.gridSize - 0.5*(self.world.gridSize-self.size), (self.pos[1]+1)*self.world.gridSize - 0.5*(self.world.gridSize-self.size), fill="white")
            self.text = self.canvas.create_text((self.pos[0]+0.5)*self.world.gridSize, (self.pos[1]+0.5)*self.world.gridSize, fill="blue", text=self.index)
        self.progress = 0
        self.timer = 0
        self.order = 0
        self.assigned = False
        self.p = [0,0,0,0,0,0,0,0,0,0,0]
        self.records = []
        self.initProbability()

    def initProbability(self):
        for k in range(11):
            self.p[k] = exp(-self.mean) * pow(self.mean, k) / factorial(k)
            #print "p(", k, ") = ", self.p[k]

    def checkOrder(self):
        r = random.uniform(0.0, 1.0)
        #print "r = ", r
        p = self.p[0]
        for k in range(0, 11):
            if r <= p:
                self.order += k
                self.records.append([copy.deepcopy(self.world.timer), self.order])
                break
            elif k != 10:
                p += self.p[k+1]

    def setAssignStatus(self, status):
        self.assigned = status
        if not self.isStation:
            if status:
                self.canvas.itemconfig(self.shape, fill="yellow")
            else:
                self.canvas.itemconfig(self.shape, fill="white")

    def updateTimeLeft(self, order):
        for record in self.records:
            if record[1] >= order:
                self.timeleft = self.timeout - (self.world.timer - record[0])
                if self.order == 0:
                    self.timeleft = self.timeout
                break
        recordsToDelete = []
        for record in self.records:
            record[1] = record[1] - order
            if record[1] <= 0:
                recordsToDelete.append(record)
        for record in recordsToDelete:
            self.records.remove(record)

    def timeClick(self):
        if self.order:
            self.timeleft -= 1

    def setOrder(self, order):
        self.order = order

    def addProgress(self):
        self.setProgress(self.progress + 1)

    def setProgress(self, progress):
        self.progress = progress
        if self.progress == 0:
            if self.assigned == True:
                self.canvas.itemconfig(self.shape, fill="red")
            else:
                self.canvas.itemconfig(self.shape, fill="white")
        elif self.progress >= self.cost:
            self.canvas.itemconfig(self.shape, fill="blue")
        else:
            self.canvas.itemconfig(self.shape, fill="yellow")

    def resetProgress(self):
        self.setProgress(0)

    def getCost(self):
        return self.cost


class TaskAllocation():

    @staticmethod
    def getClosestObject(world, pos, obj):
        minDist = 100000
        result = 0
        if obj == "Robot":
            objects = world.robots
        elif obj in ["Station", "AvailableStation"] :
            objects = world.stations

        for item in objects:
            dist = util.calculateManhattanDistance(item.pos, pos)
            if dist < minDist:
                if obj == "AvailableStation":
                    if not item.getAvailability():
                        continue
                minDist = dist
                result = item
        return result

    @staticmethod
    def getClosestRobot(world, pos):
        return TaskAllocation.getClosestObject(world, pos, "Robot")

    @staticmethod
    def getClosestStation(world, pos):
        return TaskAllocation.getClosestObject(world, pos, "Station")

    @staticmethod
    def getClosestAvailableStation(world, pos):
        return TaskAllocation.getClosestObject(world, pos, "AvailableStation")

    @staticmethod
    def getClosestAvailableRobot(world, pos, radius=1000):
        minDist = 100000
        result = 0
        for robot in world.robots:
            dist = util.calculateManhattanDistance(robot.pos, pos)
            if dist < minDist and robot.capacity > robot.load and robot.assignable:
                if robot.task:
                    if not robot.task.isStation or dist > radius:
                        continue
                minDist = dist
                result = robot
        return result

    @staticmethod
    def getMostNeededTask(world):
        minVal = 100000
        result = []
        for task in world.tasks:
            if task.timeleft <= minVal:
                result = task
                minVal = task.timeleft
        return result

    @staticmethod
    def getMostNeededUnassignedTask(world):
        minVal = 100000
        result = 0
        tasks = copy.copy(world.tasks)
        for task in tasks:
            if task.order and task.timeleft <= minVal and not task.assigned:
                result = task
                minVal = task.timeleft
        return result
