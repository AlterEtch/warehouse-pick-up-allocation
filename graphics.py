import Tkinter


class MainGraphics():
    def __init__(self, world, bgColor="black", title="Warehouse Simulation"):
        """
        Initialize the graphics
        :param world:
        :param bgColor:
        :param title:
        """
        self.world = world
        self.width = world.width
        self.height = world.height
        self.bgColor = bgColor
        self.title = title
        self.gridSize = world.gridSize
        self.layout = world.layout
        self.root_window = None
        self.canvas = None
        self.create_window()
        self.init_status_bar()

    def create_window(self):
        """
        Create the main window for the application
        """
        self.root_window = Tkinter.Tk()
        self.root_window.title(self.title)
        self.root_window.resizable(0, 0)
        self.root_window.protocol("WM_DELETE_WINDOW", self.exit_handler)

        self.statusBarWidth = 600
        self.canvas = Tkinter.Canvas(self.root_window, bg=self.bgColor, width=self.width + self.statusBarWidth, height=self.height)

        self.draw_walls()
        self.draw_grids()
        self.draw_stations()
        #self.draw_buttons()
        self.canvas.pack()
        self.canvas.update()

    def draw_path(self, path):
        """
        Draw the path on canvas
        :param path: path to be drawn
        """
        for i in range(0,len(path)-1):
            x1 = path[i][0] * self.gridSize + 0.5 * self.gridSize
            y1 = path[i][1] * self.gridSize + 0.5 * self.gridSize
            x2 = path[i + 1][0] * self.gridSize + 0.5 * self.gridSize
            y2 = path[i + 1][1] * self.gridSize + 0.5 * self.gridSize
            self.canvas.create_line([x1, y1], [x2, y2], fill="yellow")

    def draw_grids(self):
        """
        Draw the grid world
        """
        for x in range(0, self.width, self.gridSize):
            self.canvas.create_line([x, 0], [x, self.height], fill="red")
        for y in range(0, self.height, self.gridSize):
            self.canvas.create_line([0, y], [self.width, y], fill="red")
        self.number_axis()

    def draw_stations(self):
        """
        Draw the stations on canvas
        """
        for s in self.world.stations:
            self.fill_cell(s.pos, "blue", "rect")

    def draw_buttons(self):
        """
        Draw buttons
        """
        buttonWidth = 120
        buttonHeight = 50
        leadingSpace = (self.statusBarWidth - 2 * buttonWidth) / 3
        bottomSpace = 50
        self.startButton = self.create_round_rectangle(self.width + leadingSpace, self.height - (bottomSpace + buttonHeight), self.width + leadingSpace + buttonWidth, self.height - bottomSpace, radius=0, outline="#6E6E6E", width=3)
        self.canvas.create_text(self.width + leadingSpace + buttonWidth / 2, self.height - (bottomSpace + buttonHeight / 2), anchor=Tkinter.CENTER, fill="#6E6E6E", text="Start")
        self.resetButton = self.create_round_rectangle(self.width + leadingSpace * 2 + buttonWidth, self.height - (bottomSpace + buttonHeight), self.width + 2 * (leadingSpace + buttonWidth), self.height - bottomSpace, radius=0, outline="#6E6E6E", width=3)
        self.canvas.create_text(self.width + (2 * leadingSpace + 3 * buttonWidth / 2), self.height - (bottomSpace + buttonHeight / 2), anchor=Tkinter.CENTER, fill="#6E6E6E", text="Reset")

    def create_round_rectangle(self, x1, y1, x2, y2, radius=20, **kwargs):
        """
        Draw round rectangle
        :param x1: top left corner x
        :param y1: top left corner y
        :param x2: bottom right corner x
        :param y2: bottom right corner y
        :param radius: fillet radius
        :param kwargs: other arguments
        :return: polygon
        """
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def fill_cell(self, pos, color, shape):
        """
        Fill a cell with particular color and shape
        :param pos:
        :param color:
        :param shape:
        """
        x, y = pos
        if shape == "rect":
            self.canvas.create_rectangle(x * self.gridSize, y * self.gridSize, (x + 1) * self.gridSize,
                                         (y + 1) * self.gridSize, fill=color)

    def draw_walls(self):
        """
        Draw the walls on the canvas
        """
        for x in range(0, self.width / self.gridSize):
            for y in range(0, self.height / self.gridSize):
                if self.layout[x][y]:
                    self.fill_cell([x, y], "red", "rect")

    def number_axis(self):
        """
        Number the coordinate axis
        """
        for x in range(1, self.width / self.gridSize - 1):
            self.canvas.create_text((x + 0.5) * self.gridSize, 0.5 * self.gridSize, text=str(x))
            self.canvas.create_text((x + 0.5) * self.gridSize, self.height - 0.5 * self.gridSize, text=str(x))
        for y in range(1, self.height / self.gridSize - 1):
            self.canvas.create_text(0.5 * self.gridSize, (y + 0.5) * self.gridSize, text=str(y))
            self.canvas.create_text(self.width - 0.5 * self.gridSize, (y + 0.5) * self.gridSize, text=str(y))

    def init_status_bar(self):
        """
        Initialize the status bar
        """
        self.canvas.create_text(self.width + 20, 50, anchor=Tkinter.W, fill="white", text="Current Time: ")
        self.timerLabel = self.canvas.create_text(self.width + 220, 50, anchor=Tkinter.W, fill="white", text="0")

        self.canvas.create_text(self.width + 20, 70, anchor=Tkinter.W, fill="white", text="Total Task Locations: ")
        self.taskCountLabel = self.canvas.create_text(self.width + 220, 70, anchor=Tkinter.W, fill="white", text="0")

        self.canvas.create_text(self.width + 20, 90, anchor=Tkinter.W, fill="white", text="Total Order Completed:")
        self.taskCompletedLabel = self.canvas.create_text(self.width + 220, 90, anchor=Tkinter.W, fill="white", text="0")

        self.canvas.create_text(self.width + 20, 110, anchor=Tkinter.W, fill="white", text="Task Reward:")
        self.taskRewardLabel = self.canvas.create_text(self.width + 220, 110, anchor=Tkinter.W, fill="white", text="0")

        self.canvas.create_text(self.width + 300, 70, anchor=Tkinter.W, fill="white", text="Unassigned Tasks: ")
        self.unassignedLabel = self.canvas.create_text(self.width + 450, 70, anchor=Tkinter.W, fill="white",
                                                             text="0")
        self.canvas.create_text(self.width + 300, 90, anchor=Tkinter.W, fill="white", text="Completed Tasks: ")
        self.completedLabel = self.canvas.create_text(self.width + 450, 90, anchor=Tkinter.W, fill="white",
                                                      text="0")
        self.canvas.create_text(self.width + 300, 110, anchor=Tkinter.W, fill="white", text="Energy Cost: ")
        self.mileageLabel = self.canvas.create_text(self.width + 450, 110, anchor=Tkinter.W, fill="white",
                                                    text="0")

        self.canvas.create_text(self.width + 20, 130, anchor=Tkinter.W, fill="white", text="Total Rewards: ")
        self.totalRewardLabel = self.canvas.create_text(self.width + 220, 130, anchor=Tkinter.W, fill="white",
                                                        text="0")

    def create_robot_status_bar(self):
        """
        Create a status bar for robots
        """
        self.robotStatusBarY = 160
        self.robotPosLabels = []
        self.robotStatusLabels = []
        self.robotLoadLabels = []
        self.robotAssignedLabels = []
        self.robotPowerLabels = []
        self.robotTaskSequence = []

        self.canvas.create_text(self.width + 20, self.robotStatusBarY, anchor=Tkinter.W, fill="white", text="Robot")
        self.canvas.create_text(self.width + 80, self.robotStatusBarY, anchor=Tkinter.W, fill="white", text="Position")
        self.canvas.create_text(self.width + 160, self.robotStatusBarY, anchor=Tkinter.W, fill="white", text="Status")
        self.canvas.create_text(self.width + 300, self.robotStatusBarY, anchor=Tkinter.W, fill="white", text="Load")
        self.canvas.create_text(self.width + 360, self.robotStatusBarY, anchor=Tkinter.W, fill="white", text="Power")
        self.canvas.create_text(self.width + 420, self.robotStatusBarY, anchor=Tkinter.W, fill="white", text="Assigned To")

        for count in range(len(self.world.robots)):
            self.canvas.create_text(self.width + 20, self.robotStatusBarY + 20 * (count+1), anchor=Tkinter.W, fill="white", text=str(self.world.robots[count].index))
            self.robotPosLabels.append(self.canvas.create_text(self.width + 80, self.robotStatusBarY + 20 * (count + 1), anchor=Tkinter.W, fill="white", text=str(self.world.robots[count].pos)))
            self.robotStatusLabels.append(self.canvas.create_text(self.width + 160, self.robotStatusBarY + 20 * (count + 1), anchor=Tkinter.W, fill="white", text="Waiting for Order"))
            self.robotLoadLabels.append(self.canvas.create_text(self.width + 300, self.robotStatusBarY + 20 * (count + 1), anchor=Tkinter.W, fill="white", text=str(self.world.robots[count].load)))
            self.robotPowerLabels.append(self.canvas.create_text(self.width + 360, self.robotStatusBarY + 20 * (count + 1), anchor=Tkinter.W, fill="white", text="None"))
            self.robotAssignedLabels.append(self.canvas.create_text(self.width + 420, self.robotStatusBarY + 20 * (count + 1), anchor=Tkinter.W, fill="white", text="None"))
            self.robotTaskSequence.append(self.canvas.create_text(self.width + 450, self.robotStatusBarY + 20 * (count +1), fill="white",anchor=Tkinter.W))

    def create_task_status_bar(self):
        """
        Create a status bar for tasks
        """
        self.taskStatusBarY = self.robotStatusBarY + len(self.world.robots) * 20 + 50
        self.taskPosLabels = []
        self.taskTimeLabels = []
        self.taskOrderLabels = []

        self.canvas.create_text(self.width + 20, self.taskStatusBarY, anchor=Tkinter.W, fill="white", text="Task")
        self.canvas.create_text(self.width + 80, self.taskStatusBarY, anchor=Tkinter.W, fill="white", text="Position")
        self.canvas.create_text(self.width + 160, self.taskStatusBarY, anchor=Tkinter.W, fill="white", text="Remaining Time")
        self.canvas.create_text(self.width + 300, self.taskStatusBarY, anchor=Tkinter.W, fill="white", text="Order")

        for count in range(len(self.world.tasks)):
            self.canvas.create_text(self.width + 20, self.taskStatusBarY + 20 * (count+1), anchor=Tkinter.W, fill="white", text=str(self.world.tasks[count].index))
            self.taskPosLabels.append(self.canvas.create_text(self.width + 80, self.taskStatusBarY + 20 * (count+1), anchor=Tkinter.W, fill="white", text=str(self.world.tasks[count].pos)))
            self.taskTimeLabels.append(self.canvas.create_text(self.width + 160, self.taskStatusBarY + 20 * (count+1), anchor=Tkinter.W, fill="white", text=str(self.world.tasks[count].timeout)))
            self.taskOrderLabels.append(self.canvas.create_text(self.width + 300, self.taskStatusBarY + 20 * (count+1), anchor=Tkinter.W, fill="white", text=str(self.world.tasks[count].order)))

    def update_status_bar(self):
        """
        Update the status bar
        """
        self.canvas.itemconfig(self.taskCompletedLabel, text=str(self.world.completedOrder))
        # if not self.world.completedOrder:
        #     self.canvas.itemconfig(self.taskCompletionSpeedLabel, text="N/A")
        # else:
        #     self.canvas.itemconfig(self.taskCompletionSpeedLabel,
        #                            text=str(float(self.world.timer) / float(self.world.completedOrder)))
        self.canvas.itemconfig(self.taskRewardLabel, text=str(self.world.taskRewards)[:8])
        self.canvas.itemconfig(self.unassignedLabel, text=str(len(self.world.taskCache)))
        self.canvas.itemconfig(self.completedLabel, text=str(self.world.completedTask))
        self.canvas.itemconfig(self.mileageLabel, text=str(self.world.totalMileage))
        self.canvas.itemconfig(self.totalRewardLabel, text=str(self.world.taskRewards - self.world.totalMileage)[:8])

        for i in range(len(self.world.robots)):
            self.canvas.itemconfig(self.robotPosLabels[i], text=str(self.world.robots[i].pos))
            self.canvas.itemconfig(self.robotStatusLabels[i], text=str(self.world.robots[i].status))
            self.canvas.itemconfig(self.robotLoadLabels[i], text=str(self.world.robots[i].load))
            self.canvas.itemconfig(self.robotPowerLabels[i], text=str(self.world.robots[i].power))
            if self.world.robots[i].task:
                if not self.world.robots[i].task[0].isStation:
                    self.canvas.itemconfig(self.robotAssignedLabels[i], text=str(self.world.robots[i].task[0].index))
                else:
                    self.canvas.itemconfig(self.robotAssignedLabels[i], text="Base")
            else:
                self.canvas.itemconfig(self.robotAssignedLabels[i], text="None")
            task_plan = []
            for j in range(len(self.world.robots[i].task)):
                task_plan.append(self.world.robots[i].task[j].index)
            self.canvas.itemconfig(self.robotTaskSequence[i], text=str(task_plan))

        if self.world.mode in [0, 1]:
            for i in range(len(self.taskOrderLabels)):
                self.canvas.itemconfig(self.taskOrderLabels[i], text=str(self.world.tasks[i].order))
                self.canvas.itemconfig(self.taskTimeLabels[i], text=str(self.world.tasks[i].timeLeft))

    def exit_handler(self):
        """
        When windows closed, raise the handler
        :return: None
        """
        self.root_window.destroy()
