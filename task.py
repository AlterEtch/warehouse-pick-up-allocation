from math import *
from util import *
import random
import copy

class Task():
    def __init__(self, canvas, world, pos, index=0, cost=10, isStation=False, mean=0.05, timeout=300):
        self.pos = pos
        self.canvas = canvas
        self.world = world
        self.size = self.world.gridSize * 0.6
        self.timeCost = cost
        self.index = len(self.world.taskCache)
        self.isStation = isStation
        self.mean = mean
        self.timeout = copy.deepcopy(timeout)
        self.timeLeft = copy.deepcopy(timeout)
        if not self.isStation:
            self.id_shape = self.canvas.create_oval(self.pos[0]*self.world.gridSize + 0.5*(self.world.gridSize-self.size), self.pos[1]*(self.world.gridSize) + 0.5*(self.world.gridSize-self.size), (self.pos[0]+1)*self.world.gridSize - 0.5*(self.world.gridSize-self.size), (self.pos[1]+1)*self.world.gridSize - 0.5*(self.world.gridSize-self.size), fill="gray30")
            self.id_text = self.canvas.create_text((self.pos[0]+0.5)*self.world.gridSize, (self.pos[1]+0.5)*self.world.gridSize, fill="white", text=self.index)
        self.progress = 0
        self.timer = 0
        self.order = 0
        self.assigned = False
        self.p = [0,0,0,0,0,0,0,0,0,0,0]
        self.records = []
        self.init_probability()

    def init_probability(self):
        for k in range(11):
            self.p[k] = exp(-self.mean) * pow(self.mean, k) / factorial(k)

    def check_order(self):
        r = random.uniform(0.0, 1.0)
        p = self.p[0]
        for k in range(0, 11):
            if r <= p:
                self.order += k
                self.records.append([copy.deepcopy(self.world.timer), self.order])
                break
            elif k != 10:
                p += self.p[k+1]

    def set_assign_status(self, status):
        self.assigned = status
        if status:
            self.canvas.itemconfig(self.id_shape, fill="red4")
            self.canvas.itemconfig(self.id_text, fill="green")
        else:
            self.canvas.itemconfig(self.id_text, fill="white")

    def update_time_left(self, order):
        for record in self.records:
            if record[1] >= order:
                self.timeLeft = self.timeout - (self.world.timer - record[0])
                if self.order == 0:
                    self.timeLeft = self.timeout
                break
        records_to_delete = []
        for record in self.records:
            record[1] = record[1] - order
            if record[1] <= 0:
                records_to_delete.append(record)
        for record in records_to_delete:
            self.records.remove(record)

    def timer_click(self):
        if self.order:
            self.timeLeft -= 1

    def set_order(self, order):
        self.order = order

    def add_progress(self):
        self.set_progress(self.progress + 1)

    def set_progress(self, progress):
        self.progress = progress
        # if self.progress == 0:
        #     if self.assigned:
        #         self.canvas.itemconfig(self.id_shape, fill="red4")
        #     else:
        #         self.canvas.itemconfig(self.id_shape, fill="white")
        # elif self.progress >= self.timeCost:
        #     self.canvas.itemconfig(self.id_shape, fill="blue")
        # else:
        #     self.canvas.itemconfig(self.id_shape, fill="yellow")

    def reset_progress(self):
        self.set_progress(0)

    def get_cost(self):
        return self.timeCost


class TaskAllocation():
    @staticmethod
    def get_closest_robot(world, pos):
        minDist = 100000
        result = 0
        for robot in world.robots:
            dist = calculate_manhattan_distance(robot.pos, pos)
            if dist < minDist:
                minDist = dist
                result = robot
        return result

    @staticmethod
    def get_closest_available_robot(world, pos, radius):
        min_dist = 100000
        result = 0
        for robot in world.robots:
            dist = calculate_manhattan_distance(robot.pos, pos)
            if dist < min_dist and robot.capacity > robot.load and dist <= radius and len(robot.task) < MAX_TASK_ASSIGNMENT:
                if robot.task:
                    for robot_task in robot.task:
                        if not robot_task.isStation or not robot.assignable:
                            continue
                min_dist = dist
                result = robot
        return result

    @staticmethod
    def get_most_needed_task(world):
        min_val = 100000
        result = []
        for task in world.tasks:
            if task.timeLeft <= min_val:
                result = task
                min_val = task.timeLeft
        return result

    @staticmethod
    def get_most_needed_unassigned_task(world):
        min_val = 100000
        result = 0
        tasks = copy.copy(world.tasks)
        for task in tasks:
            if task.order and task.timeLeft <= min_val and not task.assigned:
                result = task
                min_val = task.timeLeft
        return result
