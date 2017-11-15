from robotAgent import RobotAgent
from task import Task
from task import TaskAllocation
from util import *
import search
import Tkinter
from actions import Actions


class WorldState():
    def __init__(self, width, height, gridSize, layout, stations, mode, directional=False):
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
        self.mode = mode
        self.completedOrder = 0

    def set_graphics(self, graphics):
        self.graphics = graphics
        self.canvas = self.graphics.canvas

    def set_wall_layout(self, layout):
        self.layout = layout
        if self.graphics:
            self.graphics.delete("all")
            self.graphics.drawWalls()
            self.graphics.drawGrids()
            self.graphics.canvas.pack()
            self.graphics.canvas.update()

    def add_completed_order(self, order):
        self.completedOrder += order

    def add_robot(self, pos):
        robot = RobotAgent(world=self, canvas=self.canvas, size=self.gridSize, pos=pos)
        self.robots.append(robot)
        robot.id_task = self.canvas.create_text(self.width + 55, 110 + 20 * robot.id_text, fill="white",
                                                anchor=Tkinter.W)

    def add_task(self, pos):
        task = Task(world=self, canvas=self.canvas, pos=pos)
        write_log("\nAt time:" + str(self.timer) + "\n\t" +
                  str(task) + " at " + str(task.pos) + " is added")
        self.taskCache.append(task)
        self.tasks.append(task)

    def add_random_robot(self, num):
        for x in range(num):
            if self.stations is not None:
                self.add_robot(generate_random_station(self))
            else:
                self.add_robot(generate_random_position(self))

    def add_random_task(self, num):
        for x in range(num):
            self.add_task(generate_random_position(self))

    def has_robot_at(self, pos):
        return self.find_robot_at(pos) != 0

    def has_task_at(self, pos):
        return self.find_task_at(pos) != 0

    def has_station_at(self, pos):
        return self.find_station_at(pos) != 0

    def has_robot_next_to(self, pos):
        neighbours = Actions.nearbyLocation(pos, self)
        for neighbour in neighbours:
            if self.has_robot_at(neighbour):
                return True
        return False

    def find_robot_at(self, pos):
        for robot in self.robots:
            if robot.pos == pos:
                return robot
        return 0

    def find_task_at(self, pos):
        for task in self.taskCache:
            if task.pos == pos:
                return task
        return 0

    def find_station_at(self, pos):
        for station in self.stations:
            if station.pos == pos:
                return station
        return 0

    def find_robot_with_task(self, task):
        for robot in self.robots:
            if task in robot.task:
                return robot
        return 0

    def find_robot_next_to_with_task(self, pos, task):
        if not self.has_robot_next_to(pos):
            return 0
        locations = Actions.nearbyLocation(pos, self)
        for location in locations:
            robot = self.find_robot_at(location)
            if robot:
                for robot_task in robot.task:
                    if robot_task.pos == pos:
                        return robot
        return 0

    def is_wall(self, pos):
        x, y = pos
        if x > self.width / self.gridSize or y > self.height / self.gridSize or x < 0 or y < 0:
            return False
        if self.layout[x][y] == 1:
            return True
        return False

    def is_blocked(self, pos):
        x, y = pos
        if pos == START_POINT:
            return False
        if x > self.width / self.gridSize or y > self.height / self.gridSize or x < 0 or y < 0:
            return True
        if self.is_wall(pos) or self.has_robot_at(pos):
            return True
        return False

    def neighbors(self, pos):
        (x, y) = pos
        result = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        result = filter(lambda r: not self.is_blocked(r), result)

        return result

    def is_blocked_at_row(self, row):
        for x in range(2, self.width / self.gridSize - 2):
            if self.is_blocked([x, row]):
                return True
        return False

    def is_blocked_at_column(self, col):
        for y in range(2, self.height / self.gridSize - 2):
            if self.is_blocked([col, y]):
                return True
        return False

    def timer_click(self):
        self.timer += 1
        self.canvas.itemconfig(self.graphics.timerLabel, text=str(self.timer))

    def check_tasks_status(self):
        self.canvas.itemconfig(self.graphics.taskCountLabel, text=str(len(self.tasks)))

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
                            # else:
                            #     robot.return_to_station()
                            #     robot.set_status("Returning to Base")

            for i in range(len(self.tasks)):
                task = TaskAllocation.get_most_needed_unassigned_task(self)
                if task:
                    robot = TaskAllocation.get_closest_available_robot(self, task.pos, radius=50)
                    if robot:
                        if robot.assignable:
                            robot.add_task(task)

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
                                r.delete_task(task)

    def try_allocate_rob(self):
        """
        When finding a free robot in the station, assign task to the robot.
        :return:None
        """
        if self.has_robot_at(START_POINT[:]):
            r = self.find_robot_at(START_POINT[:])
            if not r.task:
                r.capacityCount = 0
                task = search.sort_task(self)
                tmp_task = []
                if task:
                    write_log("\nAt time:" + str(self.timer) + "\n\t" +
                              str(r) + " labeled as Robot " + str(r.index) + " accepts the task:" + str(
                        task) + " at pos:")
                    for index in task:
                        tmp_task.append(self.taskCache[index])
                        r.add_task(tmp_task[-1])
                        text = str(tmp_task[-1].pos)
                        write_log(text)
                    for i in tmp_task:
                        self.taskCache.remove(i)
                    self.refresh_task_label()

    def update_robot_path(self):
        """
        setpath from current position to the next task position
        :return: None
        """
        for robot in self.robots:
            #if not robot.path:
            if True:
                path = []
                if robot.task:
                    if self.mode == 10:
                        par = robot.capacityCount
                    else:
                        par = robot.load
                    if par < ROBOT_CAPACITY:
                        # path = search.path_generate(self, robot.pos, robot.task[0].pos)
                        # robot.set_path(path)
                        robot.update_path_finder()
                    else:
                        robot.task = []
                        robot.assignable = False
                        robot.update_path_finder()
                        # path = search.path_generate(self, robot.pos, START_POINT[:])
                        # robot.set_path(path)

                if not robot.task:
                    robot.task = []
                    robot.update_path_finder()
                    # path = search.path_generate(self, robot.pos, START_POINT[:])
                    # robot.set_path(path)

    def refresh_task_label(self):
        """
        Refresh the label of the task.
        label 0 represents the earliest task.
        :return: None
        """
        i = 0
        for task in self.taskCache:
            self.canvas.itemconfig(task.id_text, text=str(i))
            i += 1

    def check_robot_status(self):
        for robot in self.robots:
            if robot.task:
                if robot.task[0].isStation and robot.at_station():
                    robot.charge_battery()
            if robot.at_station():
                robot.load = 0
                robot.capacityCount = 0
                robot.assignable = True

    def update(self):
        self.timer_click()
        self.check_tasks_status()
        self.check_robot_status()
        self.graphics.updateStatusBar()
        if self.mode == 10:
            self.try_allocate_rob()
        self.update_robot_path()
