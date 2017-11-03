from math import *
from random import randint
import os
import time
import re
import numpy

"""CONST"""
# station position as start point and end point
START_POINT = [29, 1]
# capacity of each robot
ROBOT_CAPACITY = 5
# TBD, whatever it is
TEMPORAL_PRIORITY_RATIO = 2.5
# the time interval between two added task
TASK_TIME_INTERVAL = 10
# log file name
FILE_NAME = os.getcwd() + time.strftime("\\log\\%Y-%m-%d %H_%M_%S.txt", time.localtime())


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
    """
    Open file and write log
    :param text:
    :param mode:
    :return: None
    """
    f = open(FILE_NAME, mode)
    f.write(text)
    f.close()


def output_log(world):
    """
    When program is terminated raise this function
    :param world:
    :return:
    """
    text = time.strftime("\n%Y-%m-%d %H:%M:%S\n******************END******************\n", time.localtime())
    write_log(text)
    write_log("Current time: " + str(world.timer) + "\n"
              + "Unassigned task: " + str(len(world.taskCache)) + "\n"
              + "Completed task: " + str(world.completedTask) + "\n"
              + "Total Mileage: " + str(world.totalMileage) + "\n")
    write_analysis(world)


def write_analysis(world):
    """
    Calculate some statistical data
    :return: None
    """
    with open(FILE_NAME) as f:
        task_begin = dict()
        task_cycle = list()
        for line1 in f:
            if line1.startswith("At time:"):
                try:
                    line2 = f.next()
                except StopIteration:
                    line2 = ''
                line = line1 + line2
                m = re.search('.*:(.*)\n\t<(.*)>', line)
                time_val = int(m.group(1))
                instance = m.group(2)
                if instance.startswith("task.Task"):
                    if "added" in line:
                        task_begin[instance] = time_val
                    if "consumed" in line:
                        task_cycle.append(time_val - task_begin[instance])
    write_log("\ntask life cycle data:\n" + str(task_cycle) + "\n")
    text = "Latency: -AVG " + str(numpy.mean(task_cycle)) + " -MAX " + str(max(task_cycle)) + " -VARIANCE " + \
           str(numpy.var(task_cycle)) + "\n" + "Throughput: " + str(world.completedTask * 1.0 / world.timer) + "\n"
    write_log("\n******************ANALYSIS******************\n" + text)
    print text
