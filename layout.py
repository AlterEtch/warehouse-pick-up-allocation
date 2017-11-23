from station import Station
import util

def getLayout1():
    width, height, gridSize = 1000, 1000, 50
    wall_layout = [[0 for row in range(0, height / gridSize + 1)] for col in range(0, width / gridSize + 1)]
    for x in range(0, width / gridSize):
        for y in range(0, height / gridSize):
            if x == 0 or y == 0 or x == width/gridSize-1 or y == height/gridSize-1:
                wall_layout[x][y] = 1

    stations = []

    for i in range(width / (2 * gridSize) - 2, width / (2 * gridSize) + 2):
        for j in range(1,3):
            stations.append(Station([i, j]))
    return width, height, gridSize, wall_layout, stations


def getLayout2():
    width, height, grid_size = 1180, 980, 20
    wall_layout = [[0 for row in range(0, height / grid_size)] for col in range(0, width / grid_size)]
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if x in {0, 0, width / grid_size - 1, width / grid_size - 1} or y in {0, 0, height / grid_size - 1, height / grid_size - 1}:
                wall_layout[x][y] = 1

    for i in range(1, width / (3 * grid_size) - 1):
        for j in range(1, height / grid_size):
            if i % 2:
                wall_layout[3 * i + 1][j] = 1
                wall_layout[3 * i + 2][j] = 1
                wall_layout[3 * i + 3][j] = 1

    for m in range(1, width / grid_size - 2):
        for n in range(1, height / grid_size - 1, 7):
            wall_layout[m][n] = 0
            wall_layout[m + 1][n] = 0
            wall_layout[m][n + 1] = 0
            wall_layout[m][n + 2] = 0
            wall_layout[m + 1][n + 1] = 0

    stations = [Station(util.START_POINT)]

    # for p in range(1, width / grid_size - 2):
    #     if not (p + 1) % 6:
    #         stations.append(Station([p, 1]))
    #         stations.append(Station([p, height / grid_size - 2]))

    for s in stations:
        x, y = s.pos
        wall_layout[x][y] = 0

    return width, height, grid_size, wall_layout, stations


def getLayout3():
    width, height, grid_size = 1300, 940, 20
    wall_layout = [[0 for row in range(0, height / grid_size)] for col in range(0, width / grid_size)]
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if x in {0, 0, width / grid_size - 1, width / grid_size - 1} or y in {0, 0, height / grid_size - 1,
                                                                                height / grid_size - 1}:
                wall_layout[x][y] = 1

    for i in range(1, width / (3 * grid_size) - 1):
        for j in range(1, height / grid_size):
            if i % 2:
                wall_layout[3 * i + 1][j] = 1
                wall_layout[3 * i + 2][j] = 1
                wall_layout[3 * i + 3][j] = 1

    for m in range(2, width / grid_size - 2):
        for n in range(2, height / grid_size - 1, 8):
            wall_layout[m][n] = 0
            wall_layout[m + 1][n] = 0
            wall_layout[m][n + 1] = 0
            wall_layout[m][n + 2] = 0
            wall_layout[m + 1][n + 1] = 0

    stations = []

    for p in range(1, width / grid_size - 2):
        if not (p + 1) % 6:
            stations.append(Station([p, 1]))
            stations.append(Station([p, height / grid_size - 2]))

    for s in stations:
        x, y = s.pos
        wall_layout[x][y] = 0

    return width, height, grid_size, wall_layout, stations
