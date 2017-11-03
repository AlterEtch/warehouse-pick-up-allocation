from math import *
from random import randint
import os
import time
import re

START_POINT = [29, 1]

ROBOT_CAPACITY = 4

TEMPORAL_PRIORITY_RATIO = 2.5

FileName = os.getcwd() + time.strftime("\\log\\%Y-%m-%d %H_%M_%S.txt", time.localtime())


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


def output_log(world):
    text = time.strftime("\n%Y-%m-%d %H:%M:%S\n******************END******************\n", time.localtime())
    write_log(text)
    write_log("Current time: " + str(world.timer) + "\n"
              + "Unassigned task: " + str(len(world.taskCache)) + "\n")
    write_analysis()


def write_analysis():
    with open(FileName) as f:
        task_begin = dict()
        task_cycle = dict()
        for line1 in f:
            if line1.startswith("At time:"):
                try:
                    line2 = f.next()
                except StopIteration:
                    line2 = ''
                line = line1 + line2
                m = re.search('.*:(.*)\n<(.*)>', line)
                time_val = int(m.group(1))
                instance = m.group(2)
                if instance.startswith("task.Task"):
                    if "added" in line:
                        task_begin[instance] = time_val
                    if "consumed" in line:
                        task_cycle[instance] = time_val - task_begin[instance]
    write_log("\nAnalysis:\n" +
              "task remain time -AVG " + str(mean(task_cycle.values())) + " -MAX " + str(max(task_cycle.values()))+"\n")


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
