from station import *

# One base station
def getLayout1():
    width, height, gridSize = 1040, 800, 40
    wallLayout = [[0 for row in range(0,height/gridSize+1)] for col in range(0,width/gridSize+1)]
    for x in range(0, width/gridSize):
        for y in range(0, height/gridSize):
            if x == 0 or y == 0 or x == width/gridSize-1 or y == height/gridSize-1:
                wallLayout[x][y] = 1

    stations = []

    for i in range(11,15):
        for j in range(1,3):
            stations.append(Station([i, j]))
    return width, height, gridSize, wallLayout, stations


def getLayout2():
    width, height, gridSize = 1180, 840, 20
    wallLayout = [[0 for row in range(0, height / gridSize)] for col in range(0, width / gridSize)]
    for x in range(0, width / gridSize):
        for y in range(0, height / gridSize):
            if x in {0, 0, width / gridSize - 1, width / gridSize - 1} or y in {0, 0, height / gridSize - 1,
                                                                                height / gridSize - 1}:
                wallLayout[x][y] = 1

    for i in range(1, width / (3 * gridSize) - 1):
        for j in range(1, height / gridSize):
            if i % 2:
                wallLayout[3 * i + 1][j] = 1
                wallLayout[3 * i + 2][j] = 1
                wallLayout[3 * i + 3][j] = 1

    for m in range(2, width / gridSize - 2):
        for n in range(2, height / gridSize - 1, 7):
            wallLayout[m][n] = 0
            wallLayout[m + 1][n] = 0
            wallLayout[m][n + 1] = 0
            wallLayout[m][n + 2] = 0
            wallLayout[m + 1][n + 1] = 0

    stations = []

    for p in range(1, width / gridSize - 2):
        if not (p + 1) % 6:
            stations.append(Station([p, 1]))
            stations.append(Station([p, height / gridSize - 2]))

    for s in stations:
        x, y = s.pos
        wallLayout[x][y] = 0

    return width, height, gridSize, wallLayout, stations


def getLayout3():
    width, height, gridSize = 1300, 940, 20
    wallLayout = [[0 for row in range(0, height / gridSize)] for col in range(0, width / gridSize)]
    for x in range(0, width / gridSize):
        for y in range(0, height / gridSize):
            if x in {0, 0, width / gridSize - 1, width / gridSize - 1} or y in {0, 0, height / gridSize - 1,
                                                                                height / gridSize - 1}:
                wallLayout[x][y] = 1

    for i in range(1, width / (3 * gridSize) - 1):
        for j in range(1, height / gridSize):
            if i % 2:
                wallLayout[3 * i + 1][j] = 1
                wallLayout[3 * i + 2][j] = 1
                wallLayout[3 * i + 3][j] = 1

    for m in range(2, width / gridSize - 2):
        for n in range(2, height / gridSize - 1, 8):
            wallLayout[m][n] = 0
            wallLayout[m + 1][n] = 0
            wallLayout[m][n + 1] = 0
            wallLayout[m][n + 2] = 0
            wallLayout[m + 1][n + 1] = 0

    stations = []

    for p in range(1, width / gridSize - 2):
        if not (p + 1) % 6:
            stations.append(Station([p, 1]))
            stations.append(Station([p, height / gridSize - 2]))

    for s in stations:
        x, y = s.pos
        wallLayout[x][y] = 0

    return width, height, gridSize, wallLayout, stations
