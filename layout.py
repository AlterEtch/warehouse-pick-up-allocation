from station import Station
import util


def get_layout1():
    width, height, grid_size = 1000, 1000, 50
    wall_layout = [[0 for row in range(0, height / grid_size + 1)] for col in range(0, width / grid_size + 1)]
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if x == 0 or y == 0 or x == width / grid_size - 1 or y == height / grid_size - 1:
                wall_layout[x][y] = 1

    stations = []

    for i in range(width / (2 * grid_size) - 2, width / (2 * grid_size) + 2):
        for j in range(1, 3):
            stations.append(Station([i, j]))

    grid_cost = dict()
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if wall_layout[x][y] == 0:
                E = 1 if wall_layout[x + 1][y] == 0 else float('inf')
                W = 1 if wall_layout[x - 1][y] == 0 else float('inf')
                S = 1 if wall_layout[x][y + 1] == 0 else float('inf')
                N = 1 if wall_layout[x][y - 1] == 0 else float('inf')
                grid_cost[x, y, x + 1, y] = E
                grid_cost[x, y, x - 1, y] = W
                grid_cost[x, y, x, y + 1] = S
                grid_cost[x, y, x, y - 1] = N

    return width, height, grid_size, wall_layout, stations, grid_cost


def get_layout2():
    width, height, grid_size = 1180, 980, 20
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

    for m in range(1, width / grid_size - 2):
        for n in range(1, height / grid_size - 1, 7):
            wall_layout[m][n] = 0
            wall_layout[m + 1][n] = 0
            wall_layout[m][n + 1] = 0
            wall_layout[m][n + 2] = 0
            wall_layout[m + 1][n + 1] = 0

    stations = [Station(util.START_POINT[:])]

    # for p in range(1, width / grid_size - 2):
    #     if not (p + 1) % 6:
    #         stations.append(Station([p, 1]))
    #         stations.append(Station([p, height / grid_size - 2]))

    for s in stations:
        x, y = s.pos
        wall_layout[x][y] = 0

    grid_cost = dict()
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if wall_layout[x][y] == 0:
                E = 1 if wall_layout[x + 1][y] == 0 else float('inf')
                W = 1 if wall_layout[x - 1][y] == 0 else float('inf')
                S = 1 if wall_layout[x][y + 1] == 0 else float('inf')
                N = 1 if wall_layout[x][y - 1] == 0 else float('inf')
                grid_cost[x, y, x + 1, y] = E
                grid_cost[x, y, x - 1, y] = W
                grid_cost[x, y, x, y + 1] = S
                grid_cost[x, y, x, y - 1] = N

    for x in range(0, width / grid_size):
        if (x, 1, x - 1, 1) in grid_cost:
            grid_cost[x, 1, x - 1, 1] = float('inf')

    return width, height, grid_size, wall_layout, stations, grid_cost


def get_layout3():
    width, height, grid_size = 820, 620, 20
    wall_layout = [[0 for row in range(0, height / grid_size + 1)] for col in range(0, width / grid_size + 1)]
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if x in {0, 0, width / grid_size, width / grid_size - 1} or y in {0, 0, height / grid_size - 1,
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

    grid_cost = dict()
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if wall_layout[x][y] == 0:
                E = 1 if wall_layout[x + 1][y] == 0 else float('inf')
                W = 1 if wall_layout[x - 1][y] == 0 else float('inf')
                S = 1 if wall_layout[x][y + 1] == 0 else float('inf')
                N = 1 if wall_layout[x][y - 1] == 0 else float('inf')
                grid_cost[x, y, x + 1, y] = E
                grid_cost[x, y, x - 1, y] = W
                grid_cost[x, y, x, y + 1] = S
                grid_cost[x, y, x, y - 1] = N

    return width, height, grid_size, wall_layout, stations, grid_cost


def get_layout4():
    width, height, grid_size = 800, 580, 20
    wall_layout = [[0 for row in range(0, height / grid_size)] for col in range(0, width / grid_size)]
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if x in {0, 0, width / grid_size - 1, width / grid_size - 1} or y in {0, 0, height / grid_size - 1,
                                                                                  height / grid_size - 1}:
                wall_layout[x][y] = 1

    for i in range(1, width / (2 * grid_size) - 1):
        for j in range(1, height / grid_size):
            if i % 2:
                wall_layout[2 * i + 1][j] = 1
                wall_layout[2 * i + 2][j] = 1

    for m in range(1, width / grid_size - 2):
        wall_layout[m][1] = 0
        for n in range(2, height / grid_size - 1, 8):
            wall_layout[m][n] = 0
            wall_layout[m][n + 1] = 0

    stations = [Station(util.START_POINT[:])]

    for s in stations:
        x, y = s.pos
        wall_layout[x][y] = 0

    grid_cost = dict()
    for x in range(0, width / grid_size):
        for y in range(0, height / grid_size):
            if wall_layout[x][y] == 0:
                E = 1 if wall_layout[x + 1][y] == 0 else float('inf')
                W = 1 if wall_layout[x - 1][y] == 0 else float('inf')
                S = 1 if wall_layout[x][y + 1] == 0 else float('inf')
                N = 1 if wall_layout[x][y - 1] == 0 else float('inf')
                grid_cost[x, y, x + 1, y] = E
                grid_cost[x, y, x - 1, y] = W
                grid_cost[x, y, x, y + 1] = S
                grid_cost[x, y, x, y - 1] = N

    for x in range(0, width / grid_size):
        if (x, 1, x - 1, 1) in grid_cost and grid_cost[x, 1, x - 1, 1] == 1:
            grid_cost[x, 1, x - 1, 1] = float('inf')

    oppo_dir_cost=2
    for y in range(1,height/grid_size):
        for x in range(1,width /grid_size-1,4):
            if (x, y, x, y+1) in grid_cost and grid_cost[x, y, x, y+1] == 1:
                grid_cost[x, y, x, y+1]=oppo_dir_cost
        for x in range(2,width / grid_size-1,4):
            if (x, y, x, y-1) in grid_cost and grid_cost[x, y, x, y-1] == 1:
                grid_cost[x, y, x, y-1]=oppo_dir_cost

    for x in range(1,width/grid_size):
        for y in range(2,height/grid_size-1,8):
            if (x, y, x-1,y) in grid_cost and grid_cost[x, y, x-1,y] ==1:
                grid_cost[x, y, x-1,y]=oppo_dir_cost
        for y in range(3,height/grid_size-1,8):
            if (x, y, x+1,y) in grid_cost and grid_cost[x, y, x+1,y] ==1:
                grid_cost[x, y, x+1,y]=oppo_dir_cost

    return width, height, grid_size, wall_layout, stations, grid_cost
