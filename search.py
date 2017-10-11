from math import *
from actions import Actions

class Node():
    def __init__(self, pos):
        self.pos = pos
        self.g = 100000
        self.f = 100000

    def setTravelCost(self, cost):
        self.g = cost

    def setTotalCost(self, cost):
        self.f = cost

    def getTravelCost(self):
        return self.g

    def getTotalCost(self):
        return self.f

class AStarSearch():
    def __init__(self, robot):
        self.robot = robot
        self.start = Node(self.robot.pos)
        self.current = Node(self.robot.pos)
        self.goal = Node(self.robot.task.pos)


    def performSearch(self):
        # The set of nodes already evaluated
        closedSet = []

        # The set of currently discovered nodes that are not evaluated yet.
        # Initially, only the start node is known.
        openSet = [self.start]

        print self.goal.pos

        self.start.setTravelCost(0)
        self.start.setTotalCost(self.getHeuristicCost(self.start))

        while len(openSet) > 0:
        #for i in range(5):
            self.current = self.getMinCostNode(openSet)
            #print 'current position:', self.current
            #print 'closedSet:', closedSet

            openSet.remove(self.current)

            closedSet.append(self.current)

            if self.current.pos == self.goal.pos:
                return closedSet

            successors = self.getSuccessors()
            for node in successors:
                #print 'node:', node
                if self.checkNodeInSet(node, closedSet):
                    #print 'closed'
                    continue

                if not self.checkNodeInSet(node, openSet):
                    openSet.append(node)

                node.setTravelCost(self.current.getTravelCost() + self.calculateEuclideanDistance(self.current.pos, node.pos))
                node.setTotalCost(node.getTravelCost() + self.getHeuristicCost(node))

    def reconstructPath(self, nodeSet):
        return nodeSet

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
        return self.calculateManhattanDistance(node.pos, self.goal.pos)

    def calculateManhattanDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def calculateEuclideanDistance(self, pos1, pos2):
        return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
