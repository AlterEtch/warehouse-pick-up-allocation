"""
this file build a graph class based on graph theory
"""


class Graph:
    def __init__(self, nodes):
        self.__vertices = []
        self.__graph_group = []  # (list)[[group 0],[group 1]...] elements linked together are put in the same group
        for i in range(1, nodes + 1):
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
        return self.__graph_group
