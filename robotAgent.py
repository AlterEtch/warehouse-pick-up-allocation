from actions import Actions
from task import Task
from search import PathFind
from random import randint
import util
import copy


class RobotAgent():
    def __init__(self, world, canvas, size, pos, capacity=util.ROBOT_CAPACITY, power=100000):
        """
        Initilize the robot
        :param world:
        :param canvas:
        :param size:
        :param pos:
        :param capacity:
        :param power:
        """
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
        self.station = Task(canvas=self.canvas, world=self.world, pos=self.world.stations[0].pos[:], isStation=True)
        self.assignable = True
        self.capacityCount = 0
        self.pathfinder = PathFind(self)

    def move(self, direction):
        """
        Move the robot in the direction
        :param direction:
        """
        possible_actions = self.get_possible_actions()
        if direction in possible_actions and self.power:
            self.pos[0] += direction[0]
            self.pos[1] += direction[1]
            self.power -= 1
            self.world.totalMileage += 1
            # Animate the movement of robot
            if util.GRAPHICS_ON:
                for x in range(0, 2):
                    for obj in self.canvas.find_withtag("robot" + str(self.index)):
                        self.canvas.move(obj, direction[0] * self.size / 2, direction[1] * self.size / 2)
                        self.canvas.update()
        elif not self.power:
            self.set_status("Out of Power")
        else:
            print 'collision'
            rand = randint(1, 100)
            if rand>50:
                self.update_path_finder()
            self.path.insert(0,[Actions.STOP])

    def get_possible_actions(self):
        """
        Return the possition actions at the current state
        :return: (list)directions
        """
        return Actions.get_possible_actions(self.pos, self.world)

    def set_task(self, task):
        """
        Set the current task of the robot
        :param task:
        """
        self.task = [task]
        task.set_assign_status(True)

    def add_task(self, task):
        """
        Append a task to be current task list
        :param task:
        """
        self.task.append(task)
        task.set_assign_status(True)

    def delete_task(self, task):
        """
        Complete and delete a task from task list
        :param task:
        """
        if not task.isStation:
            if task in self.task:
                self.task.remove(task)
            if not task.isStation:
                self.capacityCount += 1
                self.load += 1
                self.world.completedTask += 1
                if task.index <= util.INITIAL_TASK:
                    self.world.taskRewards += util.TASK_REWARD * pow(util.DISCOUNTING_FACTOR, self.world.timer)
                else:
                    self.world.taskRewards += util.TASK_REWARD * pow(util.DISCOUNTING_FACTOR, (self.world.timer - (task.index - util.INITIAL_TASK) * util.TASK_TIME_INTERVAL))
            if self.world.mode == 10:
                if not task.isStation:
                    self.world.canvas.delete(task.id_shape)
                    self.world.canvas.delete(task.id_text)
                if task in self.world.tasks:
                    self.world.tasks.remove(task)

    def set_path(self, path):
        """
        Set the current path of the robot
        :param path:
        """
        self.path = path

    def set_status(self, status):
        """
        Set the status of the robot
        :param status:
        """
        self.status = status

    def add_load(self, load):
        """
        Increment the robot load
        :param load:
        """
        self.load += load

    def at_station(self):
        """
        Check whether the robot is at a station
        :return: boolean
        """
        return self.world.find_station_at(self.pos)

    def charge_battery(self):
        """
        Charge battery and increment the power of robot
        """
        station = self.world.find_station_at(self.station.pos)
        if station:
            self.power = min(self.power + station.chargingRate, self.maxPower)

    def follow_path(self):
        """
        Follow the current path of the robot
        """
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
        """
        Update the path finder and find a new path
        """
        if not self.task or self.task[0].isStation:
            self.line_up_at(self.station.pos)

        self.pathfinder = PathFind(self)
        try:
            dir_path = self.pathfinder.perform_a_star_search()[1]
        except TypeError:
            print 'error:destination is occupied'
            dir_path = [Actions.STOP]
            dir_path.append(self.path)
        self.set_path(dir_path)

    def line_up_at(self, pos):
        x, y = pos
        if self.world.has_robot_at([x, y]):
            if self is not self.world.find_robot_at([x, y]):
                self.line_up_at([x - 1, y])
            else:
                self.task = [Task(canvas=self.canvas, world=self.world, pos=[x, y], isStation=True)]
        elif self.world.has_robot_at([x-1,y]):
            if self is not self.world.find_robot_at([x-1, y]):
                self.line_up_at([x-2,y])
            else:
                self.task = [Task(canvas=self.canvas, world=self.world, pos=[x, y], isStation=True)]
        else:
            self.task = [Task(canvas=self.canvas, world=self.world, pos=[x, y], isStation=True)]

    def return_to_station(self):
        """
        Return the station
        """
        self.set_task(self.station)

