import Tkinter

class MainGraphics():
    def __init__(self, width=800, height=640, bgColor="black", title="Warehouse Simulation", gridSize=40, layout=0):
        self.width = width
        self.height = height
        self.bgColor = bgColor
        self.title = title
        self.gridSize = gridSize
        self.layout = layout

        self.createWindow()

    def createWindow(self):
        self._root_window = Tkinter.Tk()
        self._root_window.title(self.title)
        self._root_window.resizable(0, 0)

        self._canvas = Tkinter.Canvas(self._root_window, bg=self.bgColor, width=self.width, height=self.height)

        self.drawWalls()
        self.drawGrids()
        self._canvas.pack()
        self._canvas.update()

    def drawGrids(self):
        for x in range(0, self.width, self.gridSize):
            self._canvas.create_line([x,0],[x,self.height], fill="red")
        for y in range(0, self.height, self.gridSize):
            self._canvas.create_line([0,y],[self.width,y], fill="red")

    def fillCell(self, x, y, color, shape):
        if shape == "rect":
            self._canvas.create_rectangle(x*self.gridSize, y*self.gridSize, (x+1)*self.gridSize, (y+1)*self.gridSize, fill=color)
        else:
            self._canvas.create_oval(x*self.gridSize, y*self.gridSize, (x+1)*self.gridSize, (y+1)*self.gridSize, fill=color)

    def drawWalls(self):
        for x in range(0, self.width/self.gridSize):
            for y in range(0, self.height/self.gridSize):
                if self.layout[x][y]:
                    self.fillCell(x,y, "red", "rect")
