class Station:
    def __init__(self, pos, charging_rate=100):
        """
        Initialize stations
        :param pos:
        :param charging_rate:
        """
        self.pos = pos
        self.available = True
        self.chargingRate = charging_rate

    def set_availability(self, state):
        """
        Set the availability of the station
        :param state:
        """
        self.available = state

    def get_availability(self):
        """
        Get the availability of the station
        :return: boolean
        """
        return self.available
