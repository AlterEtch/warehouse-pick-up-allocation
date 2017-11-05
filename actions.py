class Actions:
    E = [1,0]
    S = [0,1]
    W = [-1,0]
    N = [0,-1]
    STOP = [0,0]

    @staticmethod
    def possibleActions(pos, world):
        x,y = pos
        possible = [Actions.STOP]
        if world.mode == 1:
            if not world.isWall([x+1,y]):
                possible.append(Actions.E)
            if not world.isWall([x-1,y]):
                possible.append(Actions.W)
            if not world.isWall([x,y+1]):
                possible.append(Actions.S)
            if not world.isWall([x,y-1]):
                possible.append(Actions.N)
        else:
            if (not world.isBlocked([x+1,y])) or world.findStationAt([x+1,y]) != 0:
                possible.append(Actions.E)
            if (not world.isBlocked([x-1,y])) or world.findStationAt([x-1,y]) != 0:
                possible.append(Actions.W)
            if (not world.isBlocked([x,y+1])) or world.findStationAt([x,y+1]) != 0:
                possible.append(Actions.S)
            if (not world.isBlocked([x,y-1])) or world.findStationAt([x,y-1]) != 0:
                possible.append(Actions.N)

        return possible

    @staticmethod
    def nearbyLocation(pos, world):
        location = []
        possible = Actions.possibleActions(pos, world)
        for action in possible:
            location.append([pos[0] + action[0], pos[1] + action[1]])
        return location
