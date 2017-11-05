import Tkinter


class MainGraphics():
    def __init__(self, world, bgColor="black", title="Warehouse Simulation"):
        self.world = world
        self.width = world.width
        self.height = world.height
        self.bgColor = bgColor
        self.title = title
        self.gridSize = world.gridSize
        self.layout = world.layout

        self.createWindow()
        self.initStatusBar()

    def createWindow(self):
        self.root_window = Tkinter.Tk()
        self.root_window.title(self.title)
        self.root_window.resizable(0, 0)

        self.statusBarWidth = 600
        self.canvas = Tkinter.Canvas(self.root_window, bg=self.bgColor, width=self.width + self.statusBarWidth, height=self.height)

        self.drawWalls()
        self.drawGrids()
        self.drawStations()
        self.drawButtons()
        self.canvas.pack()
        self.canvas.update()

    def drawPath(self, path):
        for i in range(0,len(path)-1):
            x1 = path[i][0] * self.gridSize + 0.5 * self.gridSize
            y1 = path[i][1] * self.gridSize + 0.5 * self.gridSize
            x2 = path[i + 1][0] * self.gridSize + 0.5 * self.gridSize
            y2 = path[i + 1][1] * self.gridSize + 0.5 * self.gridSize
            self.canvas.create_line([x1, y1], [x2, y2], fill="yellow")

    def drawGrids(self):
        for x in range(0, self.width, self.gridSize):
            self.canvas.create_line([x, 0], [x, self.height], fill="red")
        for y in range(0, self.height, self.gridSize):
            self.canvas.create_line([0, y], [self.width, y], fill="red")
        self.numberAxis()

    def drawStations(self):
        for s in self.world.stations:
            self.fillCell(s.pos, "blue", "rect")

    def drawButtons(self):
        buttonWidth = 120
        buttonHeight = 50
        leadingSpace = (self.statusBarWidth - 2 * buttonWidth) / 3
        bottomSpace = 50
        self.startButton = self.createRoundRectangle(self.width + leadingSpace, self.height - (bottomSpace + buttonHeight), self.width + leadingSpace + buttonWidth, self.height - bottomSpace, radius=0, outline="#6E6E6E", width=3)
        self.canvas.create_text(self.width + leadingSpace + buttonWidth / 2, self.height - (bottomSpace + buttonHeight / 2), anchor=Tkinter.CENTER, fill="#6E6E6E", text="Start")
        self.resetButton = self.createRoundRectangle(self.width + leadingSpace * 2 + buttonWidth, self.height - (bottomSpace + buttonHeight), self.width + 2 * (leadingSpace + buttonWidth), self.height - bottomSpace, radius=0, outline="#6E6E6E", width=3)
        self.canvas.create_text(self.width + (2 * leadingSpace + 3 * buttonWidth / 2), self.height - (bottomSpace + buttonHeight / 2), anchor=Tkinter.CENTER, fill="#6E6E6E", text="Reset")

    def createRoundRectangle(self, x1, y1, x2, y2, radius=20, **kwargs):
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

    def fillCell(self, pos, color, shape, percent=100):
        x, y = pos
        if shape == "rect":
            self.canvas.create_rectangle(x * self.gridSize, y * self.gridSize, (x + 1) * self.gridSize, (y + 1) * self.gridSize, fill=color)

    def drawWalls(self):
        for x in range(0, self.width / self.gridSize):
            for y in range(0, self.height / self.gridSize):
                if self.layout[x][y]:
                    self.fillCell([x, y], "red", "rect")

    def numberAxis(self):
        for x in range(1, self.width / self.gridSize - 1):
            self.canvas.create_text((x + 0.5) * self.gridSize, 0.5 * self.gridSize, text=str(x))
            self.canvas.create_text((x + 0.5) * self.gridSize, self.height - 0.5 * self.gridSize, text=str(x))
        for y in range(1, self.height / self.gridSize - 1):
            self.canvas.create_text(0.5 * self.gridSize, (y + 0.5) * self.gridSize, text=str(y))
            self.canvas.create_text(self.width - 0.5 * self.gridSize, (y + 0.5) * self.gridSize, text=str(y))

    def initStatusBar(self):
        self.canvas.create_text(self.width + 20, 50, anchor=Tkinter.W, fill="white", text="Current Time: ")
        self.timerLabel = self.canvas.create_text(self.width + 220, 50, anchor=Tkinter.W, fill="white", text="0")
        self.canvas.create_text(self.width + 20, 70, anchor=Tkinter.W, fill="white", text="Total Task Locations: ")
        self.taskCountLabel = self.canvas.create_text(self.width + 220, 70, anchor=Tkinter.W, fill="white", text="0")
        self.canvas.create_text(self.width + 20, 90, anchor=Tkinter.W, fill="white", text="Total Order Completed:")
        self.taskCompletedLabel = self.canvas.create_text(self.width + 220, 90, anchor=Tkinter.W, fill="white", text="0")
        self.canvas.create_text(self.width + 20, 110, anchor=Tkinter.W, fill="white", text="Average Time Per Order:")
        self.taskCompletionSpeedLabel = self.canvas.create_text(self.width + 220, 110, anchor=Tkinter.W, fill="white", text="0")

    def createRobotStatusBar(self):
        self.robotStatusBarY = 160
        self.robotPosLabels = []
        self.robotStatusLabels = []
        self.robotLoadLabels = []
        self.robotAssignedLabels = []
        self.robotPowerLabels = []

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

    def createTaskStatusBar(self):
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

    def updateStatusBar(self):
        self.canvas.itemconfig(self.taskCompletedLabel, text=str(self.world.completedOrder))
        if not self.world.completedOrder:
            self.canvas.itemconfig(self.taskCompletionSpeedLabel, text="N/A")
        else:
            self.canvas.itemconfig(self.taskCompletionSpeedLabel, text=str(float(self.world.timer) / float(self.world.completedOrder)))

        for i in range(len(self.world.robots)):
            self.canvas.itemconfig(self.robotPosLabels[i], text=str(self.world.robots[i].pos))
            self.canvas.itemconfig(self.robotStatusLabels[i], text=str(self.world.robots[i].status))
            self.canvas.itemconfig(self.robotLoadLabels[i], text=str(self.world.robots[i].load))
            self.canvas.itemconfig(self.robotPowerLabels[i], text=str(self.world.robots[i].power))
            if self.world.robots[i].task:
                if not self.world.robots[i].task.isStation:
                    self.canvas.itemconfig(self.robotAssignedLabels[i], text=str(self.world.robots[i].task.index))
                else:
                    self.canvas.itemconfig(self.robotAssignedLabels[i], text="Base")
            else:
                self.canvas.itemconfig(self.robotAssignedLabels[i], text="None")

        for i in range(len(self.taskOrderLabels)):
            self.canvas.itemconfig(self.taskOrderLabels[i], text=str(self.world.tasks[i].order))
            self.canvas.itemconfig(self.taskTimeLabels[i], text=str(self.world.tasks[i].timeleft))
