from actions import Actions
from task import Task
from search import PathFind
from util import *
from random import randint
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
        self.pathfinder = PathFind(self)

    def move(self, direction):
        possible_actions = self.get_possible_actions()
        if direction in possible_actions and self.power:
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
            self.set_status("Out of Power")
        # Collision
        else:
            print 'collision'
            path = [Actions.STOP]
            path.append(self.path)
            self.set_path(path)

    def get_possible_actions(self):
        return Actions.possibleActions(self.pos, self.world)

    def set_task(self, task):
        self.task = [task]
        task.set_assign_status(True)

    def add_task(self, task):
        self.task.append(task)
        task.set_assign_status(True)

    def delete_task(self, task):
        if task in self.task:
            self.task.remove(task)
        write_log("\nAt time:" + str(self.world.timer) + "\n\t" +
                  str(task) + " at " + str(task.pos) + " is consumed")
        self.capacityCount += 1
        self.load += task.order
        self.world.completedTask += 1
        if self.world.mode == 10:
            if not task.isStation:
                self.world.canvas.delete(task.id_shape)
                self.world.canvas.delete(task.id_text)
            if task in self.world.tasks:
                self.world.tasks.remove(task)

    def set_path(self, path):
        self.path = path

    def set_status(self, status):
        self.status = status

    def add_load(self, load):
        self.load += load

    def at_station(self):
        return self.world.find_station_at(self.pos)

    def charge_battery(self):
        station = self.world.find_station_at(self.station.pos)
        if station:
            self.power = min(self.power + station.chargingRate, self.maxPower)

    def follow_path(self):
        if len(self.path) != 0:
            self.move(self.path[0])
            self.path.pop(0)
            if not len(self.path) and self.task:
                if self.task[0].isStation:
                    self.set_status("Waiting for Order")
                    self.world.add_completed_order(self.load)
                    self.load = 0
                    self.task = []

    def update_path_finder(self):
        if not self.task:
            self.task = [self.station]
        self.pathfinder = PathFind(self)
        try:
            dir_path = self.pathfinder.perform_a_star_search()[1]
        except TypeError:
            print 'error'
            dir_path = [Actions.STOP]
            dir_path.append(self.path)
        self.set_path(dir_path)


    def return_to_station(self):
        #self.task.append(self.station)
        self.set_task(self.station)
        #self.update_path_finder()
        # try:
        #     path, dirPath = self.pathfinder.perform_a_star_search()
        #     self.set_path(dirPath)
        #     if False:
        #         self.world.graphics.drawPath(path)
        # except TypeError:
        #     print 'error1'
