class Actions:
    E = [1,0]
    S = [0,1]
    W = [-1,0]
    N = [0,-1]
    STOP = [0,0]

    @staticmethod
    def possibleActions(pos, world, override=False):
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
            if (not world.isBlocked([x+1,y])) or world.findStationAt(pos) != 0:
                possible.append(Actions.E)
            if (not world.isBlocked([x-1,y])) or world.findStationAt(pos) != 0:
                possible.append(Actions.W)
            if (not world.isBlocked([x,y+1])) or world.findStationAt(pos) != 0:
                possible.append(Actions.S)
            if (not world.isBlocked([x,y-1])) or world.findStationAt(pos) != 0:
                possible.append(Actions.N)

        if world.directional and not override:
            # for i in range(2, world.width/world.gridSize-2):
            #     if world.isBlockedAtRow(y-1) and not world.isBlockedAtRow(y) and not world.isBlockedAtRow(y+1) and Actions.W in possible:
            #         possible.remove(Actions.W)
            #         break
            #     elif world.isBlockedAtRow(y+1) and not world.isBlockedAtRow(y) and not world.isBlockedAtRow(y-1) and Actions.E in possible:
            #         possible.remove(Actions.E)
            #         break
            # for j in range(2, world.height/world.gridSize-2):
            #     if world.isBlockedAtColumn(x-1) and not world.isBlockedAtColumn(x) and not world.isBlockedAtColumn(x+1) and Actions.S in possible:
            #         possible.remove(Actions.S)
            #         break
            #     elif world.isBlockedAtColumn(x+1) and not world.isBlockedAtColumn(x) and not world.isBlockedAtColumn(x-1) and Actions.N in possible:
            #         possible.remove(Actions.N)
            #         break

            for i in range(2, world.width/world.gridSize-2):
                if world.layout[i][y-1] and not world.layout[i][y+1] and Actions.W in possible:
                    possible.remove(Actions.W)
                    break
                elif world.layout[i][y+1] and not world.layout[i][y-1] and Actions.E in possible:
                    possible.remove(Actions.E)
                    break
            for j in range(2, world.height/world.gridSize-2):
                if world.layout[x-1][j] and not world.layout[x+1][j] and Actions.S in possible:
                    possible.remove(Actions.S)
                    break
                elif world.layout[x+1][j] and not world.layout[x-1][j] and Actions.N in possible:
                    possible.remove(Actions.N)
                    break

        return possible
