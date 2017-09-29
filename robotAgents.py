from time import sleep
from actions import Actions

class RobotAgent():
    def __init__(self, world, canvas, size, pos):
        self.pos = pos
        self.world = world
        self.canvas = canvas
        self.size = size
        self.id = self.canvas.create_oval(self.pos[0]*self.size, self.pos[1]*self.size, (self.pos[0]+1)*self.size, (self.pos[1]+1)*self.size, fill="green")
        self.task = []
        self.path = []

    def move(self, direction):
        possibleActions = self.getPossibleActions()
        if direction in possibleActions:
            self.pos[0] += direction[0]
            self.pos[1] += direction[1]
            # Animate the movement of robot
            for x in range(0,self.size):
                self.canvas.move(self.id, direction[0], direction[1])
                self.canvas.update()
        print self.pos

    def getPossibleActions(self):
        return Actions.possibleActions(self.pos, self.world)

    def setTask(self, task):
        self.task = task
        task.setStatus("assigned")

    def setPath(self, path):
        self.path = path

    def followPath(self):
        if len(self.path) != 0:
            self.move(self.path[0])
            self.path.pop(0)
