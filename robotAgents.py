from time import sleep

class RobotAgent():
    def __init__(self, canvas, size, pos):
        self.pos = pos
        self.canvas = canvas
        self.size = size
        self.id = self.canvas.create_oval(self.pos[0]*self.size, self.pos[1]*self.size, (self.pos[0]+1)*self.size, (self.pos[1]+1)*self.size, fill="green")
        self.task = [1,1]
        self.path = []
        self.possibleActions = [[0,0],[1,0],[0,1],[-1,0],[0,-1]]

    def move(self, direction, possibleActions=[[0,0],[1,0],[0,1],[-1,0],[0,-1]]):
        if direction in possibleActions:
            self.pos[0] += direction[0]
            self.pos[1] += direction[1]
            # Animate the movement of robot
            for x in range(0,self.size):
                self.canvas.move(self.id, direction[0], direction[1])
                self.canvas.update()
        print self.pos

    def setTask(self, pos):
        self.task = pos

    def setPath(self, path):
        self.path = path

    def followPath(self):
        if len(self.path) != 0:
            self.move(self.path[0])
            self.path.pop(0)
