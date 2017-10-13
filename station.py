class Station():
    def __init__(self, pos):
        self.pos = pos
        self.available = True

    def setAvailability(self, state):
        self.available = state

    def getAvailability(self):
        return self.available
