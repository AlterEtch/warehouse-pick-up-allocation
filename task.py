class Task():
    def __init__(self, canvas, gridSize, pos, cost=0):
        self.pos = pos
        self.canvas = canvas
        self.size = gridSize * 0.5
        self.cost = cost
        self.id = self.canvas.create_oval(self.pos[0]*gridSize + 0.5*(gridSize-self.size), self.pos[1]*(gridSize) + 0.5*(gridSize-self.size), (self.pos[0]+1)*gridSize - 0.5*(gridSize-self.size), (self.pos[1]+1)*gridSize - 0.5*(gridSize-self.size), fill="white")

    def setStatus(self, status):
        self.status = status
        if status == "assigned":
            self.canvas.itemconfig(self.id, fill="yellow")
        elif status == "completed":
            self.canvas.itemconfig(self.id, fill="blue")
        else:
            self.canvas.itemconfig(self.id, fill="white")

    def getCost(self):
        return self.cost
