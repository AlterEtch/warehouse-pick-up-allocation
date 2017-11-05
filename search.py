from actions import Actions
from util import *
import heapq


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
        self.goals = [Node(self.robot.task.pos)]
        self.toNeighbours = False

    def performAStarSearch(self, toNeighbours=False):
        if toNeighbours:
            self.toNeighbours = toNeighbours
            self.goals = self.getSuccessors(self.goal.pos)

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

            for goal in self.goals:
                if self.current.pos == goal.pos:
                    return self.reconstructPath(self.current)

            successors = self.getRobotSuccessors(self.current.pos)

            for node in successors:
                if self.checkNodeInSet(node, closedSet):
                    continue

                if not self.checkNodeInSet(node, openSet):
                    openSet.append(node)

                tentativeTravelCost = self.current.getTravelCost() + util.calculateEuclideanDistance(self.current.pos,
                                                                                                     node.pos)
                if tentativeTravelCost >= node.getTravelCost():
                    continue

                node.setPreviousNode(self.current)
                node.setTravelCost(tentativeTravelCost)
                node.setTotalCost(node.getTravelCost() + self.getHeuristicCost(node))

    def reconstructPath(self, current):
        path = [current.pos]
        dirPath = []
        while current.getPreviousNode().pos != current.pos:
            current = current.getPreviousNode()
            path.insert(0, current.pos)

        for i in range(len(path) - 1):
            dirPath.append([path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]])

        return path, dirPath

    def checkNodeInSet(self, node, set):
        for setNode in set:
            if node.pos == setNode.pos:
                return True
        return False

    def getRobotSuccessors(self, pos):
        possible = []
        possible = Actions.possibleActions(pos, self.robot.world)
        if possible == [Actions.STOP]:
            possible = Actions.possibleActions(pos, self.robot.world)
        successor = []
        for direction in possible:
            x = pos[0] + direction[0]
            y = pos[1] + direction[1]
            successor.append(Node([x, y]))
        return successor

    def getMinCostNode(self, set):
        minVal = 1000000
        for node in set:
            if node.getTotalCost() < minVal:
                minVal = node.getTotalCost()
                minNode = node
        return minNode

    def getHeuristicCost(self, node):
        minDist = 1000000
        for goal in self.goals:
            dist = util.calculateManhattanDistance(node.pos, goal.pos)
            if dist < minDist:
                minDist = dist
        return minDist


"""
    ------------------------------------------------------------------------
    |                                                                       |
    |   The codes below mainly include Clarke and Wright savings algorithm  |
    |                                                                       |
    -------------------------------------------------------------------------
"""


class Graph:
    """
    Class Graph based on the graph theory
    """

    def __init__(self, nodes):
        self.__vertices = []
        self.__graph_group = []  # (list)[[group 0],[group 1]...] elements linked together are put in the same group
        for i in range(nodes):
            self.__vertices.append(i)
            self.__graph_group.append([i])

    def location(self, vert):
        """
        Find out where the vert is in the self.__graph_group
        :param vert
        :return: i,j i_th group, j_th element
        """
        i = 0
        for group in self.__graph_group:
            j = 0
            for item in group:
                if vert == item:
                    return i, j
                j += 1
            i += 1

    def is_head(self, loc):
        """
        Whether the vert is the 1st element in the group
        :param loc: from self.location()
        :return: boolean
        """
        (i, j) = loc
        if j == 0:
            return True
        else:
            return False

    def is_tail(self, loc):
        """
        Whether the vert is the last element in the group
        :param loc: from self.location()
        :return:
        """
        (i, j) = loc
        if j == len(self.__graph_group[i]) - 1:
            return True
        else:
            return False

    def set_edge(self, vert1, vert2):
        """
        Set the edge of two vertex, updating the self.__graph_group
        :param vert1:
        :param vert2:
        :return: True for success, False for fail
        """
        loc1 = self.location(vert1)
        loc2 = self.location(vert2)
        if loc1[0] == loc2[0]:
            return False
        if self.is_tail(loc1):
            if self.is_head(loc2):
                self.__graph_group[loc1[0]] = self.__graph_group[loc1[0]] + self.__graph_group[loc2[0]]
                self.__graph_group.pop(loc2[0])
                return True
            elif self.is_tail(loc2):
                self.__graph_group[loc1[0]] = self.__graph_group[loc1[0]] + self.__graph_group[loc2[0]][::-1]
                self.__graph_group.pop(loc2[0])
                return True
        elif self.is_head(loc1):
            if self.is_head(loc2):
                self.__graph_group[loc1[0]] = self.__graph_group[loc2[0]][::-1] + self.__graph_group[loc1[0]]
                self.__graph_group.pop(loc2[0])
                return True
            elif self.is_tail(loc2):
                self.__graph_group[loc1[0]] = self.__graph_group[loc2[0]] + self.__graph_group[loc1[0]]
                self.__graph_group.pop(loc2[0])
                return True

    def load(self, vert):
        """

        :param vert:
        :return: (int) amount of the tasks
        """
        loc = self.location(vert)
        load = len(self.__graph_group[loc[0]])
        return load

    def gen_link(self):
        """

        :return: (list)
        """
        if self.__graph_group:
            link = max(self.__graph_group, key=lambda x: len(x))
            return link
        return None

    def try_gen_link(self):
        """

        :return: (list)link or None
        """
        for link in self.__graph_group:
            if len(link) == ROBOT_CAPACITY:
                return link
        return None


class PriorityQueue:
    """
    Class PriorityQueue used for A* algorithm
    """

    def __init__(self):
        self.element = []

    def empty(self):
        return len(self.element) == 0

    def put(self, item, priority):
        heapq.heappush(self.element, (priority, item))

    def get(self):
        return heapq.heappop(self.element)[1]


def heuristic(pos1, pos2):
    """

    :param pos1:
    :param pos2:
    :return: heuristic distance between pos1 and pos2
    """
    (x1, y1) = pos1
    (x2, y2) = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_planning(world, start, goal):
    """
    Calculate distance cost of each point and show from which parent point the current point comes from
    :param world:
    :param start:
    :param goal:
    :return: (dict) (came_from, cost_so_far)
    """
    start = tuple(start)
    goal = tuple(goal)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next_pos in world.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(goal, next_pos)
                frontier.put(next_pos, priority)
                came_from[next_pos] = current

    return came_from, cost_so_far[current]


def path_generate(world, start, goal):
    """
    Generate a list indicate direction including:E,W,N,S
    :param world:
    :param start:
    :param goal:
    :return: (list) path
    """
    start = tuple(start)
    goal = tuple(goal)
    came_from = a_star_planning(world, start, goal)[0]
    path = []
    position = goal
    (x, y) = position
    while position != start:
        if came_from[position] == (x - 1, y):
            path.insert(0, Actions.E)
        elif came_from[position] == (x + 1, y):
            path.insert(0, Actions.W)
        elif came_from[position] == (x, y - 1):
            path.insert(0, Actions.S)
        elif came_from[position] == (x, y + 1):
            path.insert(0, Actions.N)
        position = came_from[position]
        [x, y] = position
    return path


def saving_dist_table(world):
    """
    Calculate distance cost saving between each two task positions
    and sort the saving decreasingly
    :param world:
    :return: (list)saving_table
    """
    task_pos_list = []
    task_num = int(ROBOT_CAPACITY * TEMPORAL_PRIORITY_RATIO)
    for item in world.taskCache[:task_num]:
        task_pos_list.append(item.pos)
    task_num = len(task_pos_list)
    distance_table = {}
    for index, task in enumerate(task_pos_list):
        cost = a_star_planning(world, START_POINT, task)[1]
        distance_table[(-1, index)] = cost
    for index1 in range(0, len(task_pos_list) - 1):
        for index2 in range(index1 + 1, len(task_pos_list)):
            cost = a_star_planning(world, task_pos_list[index1], task_pos_list[index2])[1]
            distance_table[(index1, index2)] = cost
    saving_table = {}
    for (task1, task2) in distance_table:
        if task1 != -1:
            saving_table[(task1, task2)] = \
                distance_table[(-1, task1)] + distance_table[(-1, task2)] - distance_table[(task1, task2)]
    saving_table = sorted(saving_table.items(), key=lambda x: x[1], reverse=True)
    # convert to list with decreasing order as[((task0,task1),cost),...]
    # print saving_table
    return saving_table, task_num


def sort_task(world):
    """
    Generate separated sequences according to the saving_table.
    :param world:
    :return:(list)[[task00,task01,...],[task10,task11,...],...]
    """
    (saving_table, task_num) = saving_dist_table(world)
    task_index_list = range(task_num)
    g = Graph(len(task_index_list))
    for item in saving_table:
        (task1, task2) = item[0]
        if len(task_index_list) == 0:
            break
        if g.try_gen_link():
            return g.try_gen_link()
        if g.load(task1) + g.load(task2) <= ROBOT_CAPACITY:
            if g.set_edge(task1, task2):
                try:
                    task_index_list.remove(task1)
                except ValueError:
                    pass
                try:
                    task_index_list.remove(task2)
                except ValueError:
                    pass
    return g.gen_link()
