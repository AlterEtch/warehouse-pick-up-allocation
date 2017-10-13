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
        if not world.isBlocked([x+1,y]):
            possible.append(Actions.E)
        if not world.isBlocked([x-1,y]):
            possible.append(Actions.W)
        if not world.isBlocked([x,y+1]):
            possible.append(Actions.S)
        if not world.isBlocked([x,y-1]):
            possible.append(Actions.N)

        if world.directional and not override:
            for i in range(1, world.width/world.gridSize-1):
                if world.layout[i][y-1] and not world.layout[i][y+1] and Actions.W in possible:
                    possible.remove(Actions.W)
                    break
                elif world.layout[i][y+1] and not world.layout[i][y-1] and Actions.E in possible:
                    possible.remove(Actions.E)
                    break
            for j in range(1, world.height/world.gridSize-1):
                if world.layout[x-1][j] and not world.layout[x+1][j] and Actions.S in possible:
                    possible.remove(Actions.S)
                    break
                elif world.layout[x+1][j] and not world.layout[x-1][j] and Actions.N in possible:
                    possible.remove(Actions.N)
                    break

        return possible
