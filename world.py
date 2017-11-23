from robotAgent import RobotAgent
from task import Task
from task import TaskAllocation
from random import randint
import util
import search
import Tkinter
from actions import Actions


class WorldState():
    def __init__(self, width, height, gridSize, layout, stations, mode, directional=False):
        """
        Initialize the WorldState
        :param width:
        :param height:
        :param gridSize:
        :param layout:
        :param stations:
        :param mode:
        :param directional:
        """
        self.gridSize = gridSize
        self.width = width
        self.height = height
        self.layout = layout
        self.stations = stations
        self.robots = []
        self.taskCache = []
        self.tasks = []
        self.timer = 0
        self.totalMileage = 0
        self.completedTask = 0
        self.directional = directional
        self.graphics = []
        self.canvas = []
        self.mode = mode
        self.completedOrder = 0
        self.taskRewards = 0

    def set_graphics(self, graphics):
        """
        Set the world graphics
        :param graphics:
        """
        self.graphics = graphics
        self.canvas = self.graphics.canvas

    def set_wall_layout(self, layout):
        """
        Set the grid world layout
        :param layout:
        """
        self.layout = layout
        if self.graphics:
            self.graphics.delete("all")
            self.graphics.drawWalls()
            self.graphics.drawGrids()
            self.graphics.canvas.pack()
            self.graphics.canvas.update()

    def add_completed_order(self, order):
        """
        Increment the completed order counter
        :param order:
        """
        self.completedOrder += order

    def add_robot(self, pos):
        """
        Add a robot to the world at pos
        :param pos: position of the robot to be added
        """
        robot = RobotAgent(world=self, canvas=self.canvas, size=self.gridSize, pos=pos)
        self.robots.append(robot)
        robot.id_task = self.canvas.create_text(self.width + 55, 110 + 20 * robot.id_text, fill="white",
                                                anchor=Tkinter.W)

    def add_task(self, pos):
        """
        Add a task to the world at pos
        :param pos: position of the task to be added
        """
        task_index = len(self.tasks) + self.completedTask
        task = Task(world=self, canvas=self.canvas, pos=pos, index=task_index)
        self.taskCache.append(task)
        self.tasks.append(task)

    def add_random_robot(self, num):
        """
        Randomly add robots to the world
        :param num: number of robots to be added
        """
        for x in range(num):
            if self.stations is not None:
                self.add_robot(util.generate_random_station(self))
            else:
                self.add_robot(util.generate_random_position(self))

    def add_random_task(self, num):
        """
        Randomly add tasks to the world
        :param num: number of tasks to be added
        """
        for x in range(num):
            self.add_task(util.generate_random_position(self))

    def has_robot_at(self, pos):
        """
        Check whether there is a robot at a position
        :param pos: position to be checked
        :return: boolean
        """
        return self.find_robot_at(pos) != 0

    def has_task_at(self, pos):
        """
        Check whether there is a task at a position
        :param pos: position to be checked
        :return: boolean
        """
        return self.find_task_at(pos) != 0

    def has_station_at(self, pos):
        """
        Check whether there is a station at a position
        :param pos: position to be checked
        :return: boolean
        """
        return self.find_station_at(pos) != 0

    def has_robot_next_to(self, pos):
        """
        Check whether there is a robot next to a position
        :param pos: position to be checked
        :return: boolean
        """
        neighbours = Actions.get_nearby_locations(pos, self)
        for neighbour in neighbours:
            if self.has_robot_at(neighbour):
                return True
        return False

    def find_robot_at(self, pos):
        """
        Return the robot at a position, if any
        :param pos: position to be checked
        :return: robot
        """
        for robot in self.robots:
            if robot.pos == pos:
                return robot
        return 0

    def find_task_at(self, pos):
        """
        Return the task at a position, if any
        :param pos: position to be checked
        :return: task
        """
        for task in self.taskCache:
            if task.pos == pos:
                return task
        return 0

    def find_station_at(self, pos):
        """
        Return the station at a position, if any
        :param pos: position to be checked
        :return: station
        """
        for station in self.stations:
            if station.pos == pos:
                return station
        return 0

    def find_robot_with_task(self, task):
        """
        Return the robot with a task, if any
        :param task: target task
        :return: robot
        """
        for robot in self.robots:
            if task in robot.task:
                return robot
        return 0

    def find_robot_next_to_with_task(self, pos, task):
        """
        Return the robot next to a position with a task, if any
        :param pos: position to be checked
        :param task: target task
        :return: robot
        """
        if not self.has_robot_next_to(pos):
            return 0
        locations = Actions.get_nearby_locations(pos, self)
        for location in locations:
            robot = self.find_robot_at(location)
            if robot:
                for robot_task in robot.task:
                    if robot_task.pos == pos:
                        return robot
        return 0

    def is_wall(self, pos):
        """
        Check whether a position is wall
        :param pos: position to be checked
        :return: boolean
        """
        x, y = pos
        if x > self.width / self.gridSize or y > self.height / self.gridSize or x < 0 or y < 0:
            return False
        if self.layout[x][y] == 1:
            return True
        return False

    def is_blocked(self, pos):
        """
        Check whether a position is blocked by wall or robot
        :param pos: position to be checked
        :return: boolean
        """
        x, y = pos
        if pos == util.START_POINT:
            return False
        if x > self.width / self.gridSize or y > self.height / self.gridSize or x < 0 or y < 0:
            return True
        if self.is_wall(pos) or self.has_robot_at(pos):
            return True
        return False

    def neighbors(self, pos):
        """
        Return the available neighbors of a position to move to
        :param pos: position to be checked
        :return: (list)position
        """
        (x, y) = pos
        result = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        result = filter(lambda r: not self.is_blocked(r), result)
        return result

    def timer_click(self):
        """
        Increment the world timer
        """
        self.timer += 1
        self.canvas.itemconfig(self.graphics.timerLabel, text=str(self.timer))

    def check_tasks_status(self):
        """
        Check and handle any matter related to tasks at each time step
        """
        self.canvas.itemconfig(self.graphics.taskCountLabel, text=str(len(self.tasks)))

        unassigned_task = []
        for task in self.tasks:
            if not self.find_robot_with_task(task):
                unassigned_task.append(task)
        self.taskCache = unassigned_task

        # Fully randomized mode
        if self.mode == 0:
            for robot in self.robots:
                for task in robot.task:
                    if task.progress < task.timeCost:
                        if not self.has_robot_at(task.pos):
                            task.reset_progress()
                        elif task not in self.find_robot_at(task.pos).task:
                            task.reset_progress()
                        if task.pos == robot.pos and len(robot.path) == 0:
                            task.add_progress()
                    else:
                        task.timer += 1
                        if task.timer >= 10:
                            r = self.find_robot_with_task(task)
                            if r != 0:
                                r.delete_task(task)

        # First Algorithm Mode
        if self.mode == 1:
            for task in self.tasks:
                task.timer_click()
                task.check_order()
                if not self.find_robot_with_task(task):
                    task.set_assign_status(False)

                if self.has_robot_next_to(task.pos) or self.has_robot_at(task.pos):
                    robot = self.find_robot_next_to_with_task(task.pos, task)
                    if not robot:
                        robot = self.find_robot_with_task(task)
                    if robot:
                        if robot.pos == task.pos:
                            robot.set_status("Arrived Task Location")
                            load = min(robot.capacity - robot.load, task.order)
                            robot.add_load(load)
                            task.set_order(task.order - load)
                            task.update_time_left(load)
                            if task.progress < task.timeCost:
                                task.add_progress()
                            else:
                                if robot.task:
                                    robot.delete_task(task)
                        else:
                            task.reset_progress()

            for i in range(len(self.tasks)):
                task = TaskAllocation.get_most_needed_unassigned_task(self)
                if task:
                    print 'most needed: ', task.index
                    robot = TaskAllocation.get_closest_available_robot(self, task.pos)
                    if robot:
                        if robot.assignable:
                            robot.set_task(task)

        # Clarke and Wright Savings Algorithm Mode
        if self.mode == 10:
            for robot in self.robots:
                for task in robot.task:
                    if task.progress < task.timeCost:
                        if not self.has_robot_at(task.pos):
                            task.reset_progress()
                        elif task not in self.find_robot_at(task.pos).task:
                            task.reset_progress()
                        if task.pos == robot.pos and len(robot.path) == 0:
                            task.add_progress()
                    else:
                        task.timer += 1
                        if task.timer >= 10:
                            r = self.find_robot_with_task(task)
                            if r != 0:
                                if r.pos == task.pos:
                                    r.delete_task(task)

    def try_allocate_rob(self):
        """
        When finding a free robot in the station, assign task to the robot. Only used in Clarke and Wright Algorithm.
        :return:None
        """
        if self.has_robot_at(util.START_POINT[:]):
            r = self.find_robot_at(util.START_POINT[:])
            if not r.task:
                r.capacityCount = 0
                task = search.sort_task(self)
                tmp_task = []
                if task:
                    for index in task:
                        tmp_task.append(self.taskCache[index])
                        r.add_task(tmp_task[-1])
                    for i in tmp_task:
                        self.taskCache.remove(i)

    def update_robot_path(self):
        """
        setpath from current position to the next task position
        :return: None
        """
        for robot in self.robots:
            if self.mode == 10:
                par = robot.capacityCount
            else:
                par = robot.load
            if True:
                if robot.task:
                    if par < util.ROBOT_CAPACITY:
                        rand = randint(0, 100)
                        if not len(robot.path):
                            robot.update_path_finder()
                        elif rand > 50:
                            robot.update_path_finder()
                        if not TaskAllocation.is_task_station(robot.task):
                            robot.set_status("Fetching Order")
                    else:
                        robot.task = []
                        robot.assignable = False
                        robot.update_path_finder()
                        robot.set_status("Return to Station")
                else:
                    robot.task = []
                    robot.update_path_finder()
                    robot.set_status("Return to Station")

    def check_robot_status(self):
        """
        Check and handle any matter related to robots at each time step
        """
        for robot in self.robots:
            if robot.task:
                if robot.task[0].isStation and robot.at_station():
                    robot.charge_battery()
            if robot.at_station():
                robot.load = 0
                robot.capacityCount = 0
                robot.assignable = True

    def update(self):
        """
        Update the world at each time step
        """
        self.timer_click()
        self.check_tasks_status()
        self.check_robot_status()
        self.graphics.update_status_bar()
        if self.mode == 10:
            self.try_allocate_rob()
        self.update_robot_path()
