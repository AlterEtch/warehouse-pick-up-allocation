from math import *
from random import randint
import os
import time


START_POINT = [29, 1]

ROBOT_CAPACITY = 4

FileName = os.getcwd()+time.strftime("\\log\\%Y-%m-%d %H_%M_%S.txt", time.localtime())

def generateRandomPosition(world):
    pos = [randint(2, world.width / world.gridSize - 3), randint(3, world.height / world.gridSize - 4)]
    if world.isBlocked(pos) or world.hasStationAt(pos) or len(world.neighbors(pos)) == 4:
        return generateRandomPosition(world)
    return pos


def generateRandomStation(world):
    stationSet = []
    for s in world.stations:
        if not world.isBlocked(s.pos):
            stationSet.append(s)
    pos = stationSet[randint(0, len(stationSet) - 1)].pos
    if world.isBlocked(pos):
        return generateRandomStation(world)
    return pos


def calculateManhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def calculateEuclideanDistance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def write_log(text, mode='a'):
    f = open(FileName, mode)
    f.write(text)
    f.close()


