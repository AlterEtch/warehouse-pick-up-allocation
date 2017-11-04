from task import *
from search import *
import copy


class RobotAgent():
    def __init__(self, world, canvas, size, pos, index, capacity=200):
        self.pos = copy.deepcopy(pos)
        self.world = world
        self.canvas = canvas
        self.size = size
        self.id_num = len(world.robots)
        self.id = self.canvas.create_oval(self.pos[0] * self.size, self.pos[1] * self.size,
                                          (self.pos[0] + 1) * self.size, (self.pos[1] + 1) * self.size, fill="green")
        self.status = "Waiting for Order"
        self.id_label = self.canvas.create_text((self.pos[0] + 0.5) * self.size, (self.pos[1] + 0.5) * self.size,
                                                text=str(self.id_num))
        self.task = []
        self.path = []
        self.station = Task(world=self.world, canvas=self.canvas, gridSize=self.world.gridSize,
                            pos=copy.deepcopy(self.pos),
                            isStation=True)
        self.capacityCount = 0

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
                self.canvas.move(self.id_label, direction[0] * self.size / 2, direction[1] * self.size / 2)
                self.canvas.update()
                self.world.totalMileage += 1
                self.canvas.itemconfig(self.world.mileageLabel, text=str(self.world.totalMileage))

        else:
            if len(self.path):
                print 'recalculating path'
                self.updatePathFiner()
                try:
                    path, dirPath = self.pathfinder.performAStarSearch(override=True)
                except TypeError:
                    self.path.insert(0, [0, 0])
                else:
                    self.path = dirPath
                    #self.world.graphics.drawPath(path)

    def getPossibleActions(self, override=False):
        return Actions.possibleActions(self.pos, self.world, override)

    def setTask(self, task):
        self.task.append(task)
        task.setAssignStatus(True)

    def delete_task(self, task):
        self.task.remove(task)
        write_log("\nAt time:" + str(self.world.timer) + "\n\t" +
                  str(task) + " at " + str(task.pos) + " is consumed")
        self.capacityCount += 1
        self.world.completedTask += 1
        self.world.canvas.itemconfig(self.world.completedLabel, text=str(self.world.completedTask))
        self.world.canvas.delete(task.id)
        self.world.canvas.delete(task.id_label)

    def setPath(self, path):
        self.path += path

    def setStatus(self, status):
        self.status = status

    def addLoad(self, load):
        self.load += load

    def followPath(self):
        if len(self.path) != 0:
            self.move(self.path[0])
            self.path.pop(0)
            if not len(self.path) and self.task:
                if self.task.isStation:
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
            #self.world.graphics.drawPath(path)
        except TypeError:
            print 'error1'
