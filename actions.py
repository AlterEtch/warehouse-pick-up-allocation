class Actions:
    E = [1, 0]
    S = [0, 1]
    W = [-1, 0]
    N = [0, -1]
    STOP = [0, 0]

    @staticmethod
    def get_possible_actions(pos, world):
        """
        Return the possible actions available for a position
        :param pos: position to be checked
        :param world:
        :return: (list)actions
        """
        x,y = pos
        possible = [Actions.STOP]
        if world.mode == 1:
            if not world.is_wall([x+1, y]):
                possible.append(Actions.E)
            if not world.is_wall([x-1, y]):
                possible.append(Actions.W)
            if not world.is_wall([x, y+1]):
                possible.append(Actions.S)
            if not world.is_wall([x, y-1]):
                possible.append(Actions.N)
        else:
            if (not world.is_blocked([x+1, y])) or world.find_station_at([x+1, y]) != 0:
                possible.append(Actions.E)
            if (not world.is_blocked([x-1, y])) or world.find_station_at([x-1, y]) != 0:
                possible.append(Actions.W)
            if (not world.is_blocked([x, y+1])) or world.find_station_at([x, y+1]) != 0:
                possible.append(Actions.S)
            if (not world.is_blocked([x, y-1])) or world.find_station_at([x, y-1]) != 0:
                possible.append(Actions.N)

        return possible

    @staticmethod
    def get_nearby_locations(pos, world):
        """
        Return the nearby locations of a position
        :param pos: position to be checked
        :param world:
        :return: (list)locations
        """
        location = []
        possible = Actions.get_possible_actions(pos, world)
        for action in possible:
            location.append([pos[0] + action[0], pos[1] + action[1]])
        return location
