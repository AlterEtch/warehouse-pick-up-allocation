from util import *
from actions import Actions

class Node():
    def __init__(self, pos):
        self.pos = pos
        self.g = 100000
        self.f = 100000
        self.prev = self

    def setTravelCost(self, cost):
        self.g = cost

    def setTotalCost(self, cost):
        self.f = cost

    def setPreviousNode(self, node):
        self.prev = node

    def getTravelCost(self):
        return self.g

    def getTotalCost(self):
        return self.f

    def getPreviousNode(self):
        return self.prev

class PathFind():
    def __init__(self, robot):
        self.robot = robot
        self.start = Node(self.robot.pos)
        self.current = Node(self.robot.pos)
        self.goal = Node(self.robot.task.pos)

    def performAStarSearch(self):
        # The set of nodes already evaluated
        closedSet = []

        # The set of currently discovered nodes that are not evaluated yet.
        # Initially, only the start node is known.
        openSet = [self.start]

        self.start.setTravelCost(0)
        self.start.setTotalCost(self.getHeuristicCost(self.start))

        while len(openSet) > 0:
            self.current = self.getMinCostNode(openSet)
            openSet.remove(self.current)
            closedSet.append(self.current)

            if self.current.pos == self.goal.pos:
                return self.reconstructPath(self.current)

            successors = self.getSuccessors()

            for node in successors:
                if self.checkNodeInSet(node, closedSet):
                    continue

                if not self.checkNodeInSet(node, openSet):
                    openSet.append(node)

                tentativeTravelCost = self.current.getTravelCost() + calculateEuclideanDistance(self.current.pos, node.pos)
                if tentativeTravelCost >= node.getTravelCost():
                    continue

                node.setPreviousNode(self.current)
                node.setTravelCost(tentativeTravelCost)
                node.setTotalCost(node.getTravelCost() + self.getHeuristicCost(node))

    def reconstructPath(self, current):
        path = [current.pos]
        dirPath = [self.robot.pos]
        while current.getPreviousNode().pos != current.pos:
            current = current.getPreviousNode()
            path.insert(0, current.pos)

        for i in range(len(path)-1):
            dirPath.append([path[i+1][0] - path[i][0],path[i+1][1] - path[i][1]])
        return path, dirPath

    def checkNodeInSet(self, node, set):
        for setNode in set:
            if node.pos == setNode.pos:
                return True
        return False

    def getSuccessors(self):
        possible = []
        possible = Actions.possibleActions(self.current.pos, self.robot.world)
        successor = []
        for direction in possible:
            x = self.current.pos[0] + direction[0]
            y = self.current.pos[1] + direction[1]
            successor.append(Node([x,y]))
        return successor

    def getMinCostNode(self, set):
        minVal = 1000000
        for node in set:
            if node.getTotalCost() < minVal:
                minVal = node.getTotalCost()
                minNode = node
        return minNode

    def getHeuristicCost(self, node):
        return calculateManhattanDistance(node.pos, self.goal.pos)
