from station import *

def getLayout1():
    width, height, gridSize = 1040, 800, 20
    wallLayout = [[0 for row in range(0,height/gridSize)] for col in range(0,width/gridSize)]
    for x in range(0, width/gridSize):
        for y in range(0, height/gridSize):
            if x == 0 or y == 0 or x == width/gridSize-1 or y == height/gridSize-1:
                wallLayout[x][y] = 1

    for i in range(0, width/(2*gridSize)-1):
        for j in range(1, height/gridSize):
            if i % 2:
                wallLayout[2*i+1][j] = 1
                wallLayout[2*i+2][j] = 1

    for m in range(1, width/gridSize-2):
        for n in range(1, height/gridSize-1, 6):
            wallLayout[m][n] = 0
            wallLayout[m+1][n] = 0
            wallLayout[m][n+1] = 0
            wallLayout[m+1][n+1] = 0

    stations = (Station([1,1]), Station([10,1]), Station([20,1]), Station([30,1]),
                Station([51,1]), Station([51,10]))

    return width, height, gridSize, wallLayout, stations

def getLayout2():
    width, height, gridSize = 1060, 800, 20
    wallLayout = [[0 for row in range(0,height/gridSize)] for col in range(0,width/gridSize)]
    for x in range(0, width/gridSize):
        for y in range(0, height/gridSize):
            if x == 0 or y == 0 or x == width/gridSize-1 or y == height/gridSize-1:
                wallLayout[x][y] = 1

    for i in range(1, width/(3*gridSize)-1):
        for j in range(1, height/gridSize):
            if i % 2:
                wallLayout[3*i+1][j] = 1
                wallLayout[3*i+2][j] = 1
                wallLayout[3*i+3][j] = 1

    for m in range(1, width/gridSize-2):
        for n in range(1, height/gridSize-1, 7):
            wallLayout[m][n] = 0
            wallLayout[m][n] = 0
            wallLayout[m+1][n] = 0
            wallLayout[m][n+1] = 0
            wallLayout[m][n+2] = 0
            wallLayout[m+1][n+1] = 0

    stations = (Station([1,1]), Station([10,1]), Station([20,1]), Station([30,1]), Station([40,1]),
                Station([51,1]), Station([51,10]))

    return width, height, gridSize, wallLayout, stations

def getLayout3():
    width, height, gridSize = 1040, 800, 20
    wallLayout = [[0 for row in range(0,height/gridSize)] for col in range(0,width/gridSize)]
    for x in range(0, width/gridSize):
        for y in range(0, height/gridSize):
            if x == 0 or y == 0 or x == width/gridSize-1 or y == height/gridSize-1:
                wallLayout[x][y] = 1

    for i in range(0, width/(2*gridSize)-1):
        for j in range(1, height/gridSize):
            if i % 2:
                wallLayout[2*i+1][j] = 1
                wallLayout[2*i+2][j] = 1

    for m in range(1, width/gridSize-2):
        for n in range(1, height/gridSize-1, 6):
            wallLayout[m][n] = 0
            wallLayout[m+1][n] = 0
            wallLayout[m][n+1] = 0
            wallLayout[m+1][n+1] = 0

    stations = (Station([1,1]), Station([10,1]), Station([20,1]), Station([30,1]),
                Station([51,1]), Station([51,10]))

    return width, height, gridSize, wallLayout, stations
