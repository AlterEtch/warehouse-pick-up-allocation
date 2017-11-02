class Task:
    def __init__(self, canvas, gridSize, pos, cost=10, isStation=False):
        self.pos = pos
        self.canvas = canvas
        self.size = gridSize * 0.5
        self.cost = cost
        self.isStation = isStation
        if not self.isStation:
            self.id = self.canvas.create_oval(self.pos[0]*gridSize + 0.5*(gridSize-self.size), self.pos[1]*(gridSize) + 0.5*(gridSize-self.size), (self.pos[0]+1)*gridSize - 0.5*(gridSize-self.size), (self.pos[1]+1)*gridSize - 0.5*(gridSize-self.size), fill="white")
        self.progress = 0
        self.timer = 0
        self.assigned = False

    def setAssignStatus(self, status):
        self.assigned = status
        self.canvas.itemconfig(self.id, fill="red")

    def addProgress(self):
        self.setProgress(self.progress + 1)

    def setProgress(self, progress):
        self.progress = progress
        if self.progress == 0:
            if self.assigned == True:
                self.canvas.itemconfig(self.id, fill="red")
            else:
                self.canvas.itemconfig(self.id, fill="white")
        elif self.progress >= self.cost:
            self.canvas.itemconfig(self.id, fill="blue")
        else:
            self.canvas.itemconfig(self.id, fill="yellow")

    def resetProgress(self):
        self.setProgress(0)

    def getCost(self):
        return self.cost
