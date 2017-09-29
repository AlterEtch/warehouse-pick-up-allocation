class Actions:
    E = [1,0]
    S = [0,1]
    W = [-1,0]
    N = [0,-1]
    STOP = [0,0]

    @staticmethod
    def possibleActions(pos, states):
        x = pos[0]
        y = pos[1]
        possible = [Actions.STOP]
        if not states.isBlocked([x+1,y]):
            possible.append(Actions.E)
        if not states.isBlocked([x-1,y]):
            possible.append(Actions.W)
        if not states.isBlocked([x,y+1]):
            possible.append(Actions.S)
        if not states.isBlocked([x,y-1]):
            possible.append(Actions.N)
        return possible
