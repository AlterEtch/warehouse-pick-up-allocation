from math import sqrt
from random import randint
import task

def generateRandomPosition(world):
    pos = [randint(1, world.width / world.gridSize - 2), randint(1, world.height / world.gridSize - 2)]
    if world.isBlocked(pos) or world.hasStationAt(pos):
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

def calculateEuclideanDistanceFromClosestStation(world, pos):
    station = task.TaskAllocation.getClosestAvailableStation(world, pos)
    return calculateEuclideanDistance(station.pos, pos)
