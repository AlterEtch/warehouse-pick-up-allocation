"""
this file include A* algorithm and Clarke and Wright savings algorithm
"""

import heapq
import graph

from actions import Actions


class PriorityQueue:
    """
    Priority queue used for A* algorithm
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
    cost_so_far = {}
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


def saving_dist_table(world, start):
    """
    Calculate distance cost saving between each two task positions
    and sort the saving decreasingly
    :param world:
    :param start:
    :return: (list)saving_table
    """
    task_pos_list = []
    for item in world.taskCache:
        task_pos_list.append(item.pos)
    task_pos_list.insert(0, start)
    distance_table = {}
    for i in range(len(task_pos_list)):
        for j in range(i + 1, len(task_pos_list)):
            cost = a_star_planning(world, task_pos_list[i], task_pos_list[j])[1]
            distance_table[(i, j)] = cost
    saving_table = {}
    for (task1, task2) in distance_table:
        if task1 != 0:
            saving_table[(task1, task2)] = distance_table[(0, task1)] + distance_table[(0, task2)] - distance_table[(task1, task2)]
    saving_table = sorted(saving_table.items(), key=lambda x: x[1], reverse=True)
    # convert to list with decreasing order as[((task1,task2),cost),...]
    return saving_table


def sort_task(saving_table, task_num, capacity=4):
    """

    :param saving_table:
    :param task_num:
    :param capacity:
    :return:(list)[[task11,task12,...],[task21,task22,...],...]
    """
    task_list = range(1, task_num + 1)
    g = graph.Graph(len(task_list))
    for item in saving_table:
        (task1, task2) = item[0]
        if len(task_list) == 0:
            break
        else:
            if g.load(task1) + g.load(task2) <= capacity:
                if g.set_edge(task1, task2):
                    try:
                        task_list.remove(task1)
                    except ValueError:
                        pass
                    try:
                        task_list.remove(task2)
                    except ValueError:
                        pass
    return g.gen_link()
