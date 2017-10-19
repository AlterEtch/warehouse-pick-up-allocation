"""
this file build a graph class based on graph theory
"""

class Graph():
    def __init__(self, notes):
        self.__graph_dict = dict()
        self.__vertices = range(1,notes+1)
        self.__complete_tag=dict()
        for key in self.__vertices:
            self.__graph_dict[key] = []
            self.__complete_tag[key]=False

    def set_edge(self, pair):
        """
        Set the edge between two vertices when
        robot is not full-loaded, vertices is not in the middle and two vertices is not reachable.

        :param pair: a list with two elements representing two vertices in graph
        :return: boolean True for linking successfully
        """
        (vert1, vert2) = pair
        if (not(self.__complete_tag[vert1] or self.__complete_tag[vert2]))\
                and(self.is_head(vert1) and self.is_head(vert2)) \
                and (not self.is_reachable(vert1, vert2)):
            self.__graph_dict[vert1].append(vert2)
            self.__graph_dict[vert2].append(vert1)
            return True
        else:
            return False

    def reset_edge(self,pair):
        """
        Cut the edge between two vertices


        :param pair:
        :return: None
        """
        (vert1, vert2) = pair
        self.__graph_dict[vert1].remove(vert2)
        self.__graph_dict[vert2].remove(vert1)

    def one_path_complete(self,vert):
        """
        Set tag true, when robot is full-loaded.
        That means a path going through several task positions is completed.

        :param vert:
        :return: None
        """
        self.__complete_tag[vert]=True

    def is_reachable(self, vert1, vert2):
        """
        find out whether these two vertices could be reached each other.

        :param vert1:
        :param vert2:
        :return: boolean
        """

        curr_vert = vert1
        old_vert = None
        while curr_vert is not None:
            if curr_vert is vert2:
                return True
            else:
                try:
                    next_vert = filter(lambda x: x != old_vert, self.__graph_dict[curr_vert])[0]
                    old_vert = curr_vert
                    curr_vert = next_vert
                except IndexError:
                    curr_vert = None
        return False

    def is_head(self, vert):
        """
        find out whether the vertex is at the end of path and has only one edge with neighbor vertex or has no edge
        :param vert:
        :return:boolean
        """
        if len(self.__graph_dict[vert]) == 2:
            return False
        else:
            return True

    def gen_link(self):
        """
        generate a set of sequences of vertex label indicating the sequences of
        task position that the robot visiting in turn.


        :return: (list)link
        """
        link = []
        tmp_link = []
        vert_list = list(self.__vertices)
        while len(vert_list) != 0:
            for curr_vert in vert_list:
                if self.is_head(curr_vert):
                    tmp_link.append(curr_vert)
                    break
            vert_list.remove(curr_vert)
            old_vert = None
            while curr_vert is not None:
                try:
                    next_vert = filter(lambda x: x != old_vert, self.__graph_dict[curr_vert])[0]
                    old_vert = curr_vert
                    curr_vert = next_vert
                    tmp_link.append(curr_vert)
                    vert_list.remove(curr_vert)
                except IndexError:
                    curr_vert = None
            link.append(tmp_link)
            tmp_link = []
        return link
