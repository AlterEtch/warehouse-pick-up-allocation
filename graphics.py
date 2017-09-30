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

        self.canvas = Tkinter.Canvas(self.root_window, bg=self.bgColor, width=self.width + 200, height=self.height)

        self.drawWalls()
        self.drawGrids()
        self.canvas.pack()
        self.canvas.update()

    def drawGrids(self):
        for x in range(0, self.width, self.gridSize):
            self.canvas.create_line([x,0],[x,self.height], fill="red")
        for y in range(0, self.height, self.gridSize):
            self.canvas.create_line([0,y],[self.width,y], fill="red")

    def fillCell(self, x, y, color, shape):
        self.canvas.create_rectangle(x*self.gridSize, y*self.gridSize, (x+1)*self.gridSize, (y+1)*self.gridSize, fill=color)

    def drawWalls(self):
        for x in range(0, self.width/self.gridSize):
            for y in range(0, self.height/self.gridSize):
                if self.layout[x][y]:
                    self.fillCell(x,y, "red", "rect")

    def initStatusBar(self):
        self.canvas.create_text(self.width + 10, 50, anchor=Tkinter.W, fill="white", text="Current Time: ")
        self.world.timerLabel = self.canvas.create_text(self.width + 150, 50, anchor=Tkinter.W, fill="white", text="0")
        self.canvas.create_text(self.width + 10, 70, anchor=Tkinter.W, fill="white", text="Remaining Tasks: ")
        self.world.taskCountLabel = self.canvas.create_text(self.width + 150, 70, anchor=Tkinter.W, fill="white", text="0")
