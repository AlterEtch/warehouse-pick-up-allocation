from math import *
from random import randint

def generateRandomPosition(world):
    pos = [randint(1, world.width/world.gridSize-2),randint(1, world.height/world.gridSize-2)]
    if world.isBlocked(pos):
        return generateRandomPosition(world)
    return pos

def generateRandomStation(world):
    pos = world.stations[randint(0, len(world.stations)-1)].pos
    if world.isBlocked(pos):
        return generateRandomStation(world)
    return pos

def calculateManhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def calculateEuclideanDistance(pos1, pos2):
    return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
