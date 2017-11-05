class Station():
    def __init__(self, pos, chargingRate=100):
        self.pos = pos
        self.available = True
        self.chargingRate = chargingRate

    def setAvailability(self, state):
        self.available = state

    def getAvailability(self):
        return self.available
