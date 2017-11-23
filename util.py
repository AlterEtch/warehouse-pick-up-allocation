from math import *
from random import randint
import os
import time

"""CONST"""
# station position as start point and end point
START_POINT = [29, 1]
# capacity of each robot
ROBOT_CAPACITY = 5
# max number of task assigned to each robot
MAX_TASK_ASSIGNMENT = 5
# TBD, whatever it is
TEMPORAL_PRIORITY_RATIO = 1
# the time interval between two added task
TASK_TIME_INTERVAL = 10
# task reward
TASK_REWARD = 10
# discounting factor
DISCOUNTING_FACTOR = 0.999
# initial task
INITIAL_TASK = 10
# graphics on
GRAPHICS = False


def generate_random_position(world):
    """
    Randomly generate a position
    :param world:
    :return: position
    """
    pos = [randint(2, world.width/world.gridSize-3), randint(3, world.height/world.gridSize-4)]
    if world.is_blocked(pos) or world.has_station_at(pos) or len(world.neighbors(pos)) == 4 or world.has_task_at(pos):
        return generate_random_position(world)
    return pos


def generate_random_station(world):
    """
    Randomly generate a position from the stations
    :param world:
    :return: position
    """
    station_set = []
    for s in world.stations:
        if not world.is_blocked(s.pos):
            station_set.append(s)
    pos = station_set[randint(0, len(station_set) - 1)].pos
    if world.is_blocked(pos):
        return generate_random_station(world)
    return pos


def calculate_manhattan_distance(pos1, pos2):
    """
    Calculate the manhattan distance between two positions
    :param pos1:
    :param pos2:
    :return: manhattan_distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def calculate_euclidean_distance(pos1, pos2):
    """
    Calculate the Euclidean distance between two positions
    :param pos1:
    :param pos2:
    :return: euclidean_distance
    """
    return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
