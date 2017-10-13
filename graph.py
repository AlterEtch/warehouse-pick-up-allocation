class Graph():
    def __init__(self, notes):
        self.__graph_dict = dict()
        self.__vertices = range(1,notes+1)
        self.__complete_tag=dict()
        for key in self.__vertices:
            self.__graph_dict[key] = []
            self.__complete_tag[key]=False

    def set_edge(self, pair):
        (vert1, vert2) = pair
        if (not(self.__complete_tag[vert1] or self.__complete_tag[vert2]))\
                and(self.is_head(vert1) and self.is_head(vert2)) \
                and (not self.is_reachable(vert1, vert2)):
            self.__graph_dict[vert1].append(vert2)
            self.__graph_dict[vert2].append(vert1)
            return True
        else:
            return False

    def one_path_complete(self,vert):
        self.__complete_tag[vert]=True

    def is_reachable(self, vert1, vert2):
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
        if len(self.__graph_dict[vert]) == 2:
            return False
        else:
            return True

    def gen_link(self):
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
            tmp_link.append(0)
            tmp_link.insert(0,0)
            link.append(tmp_link)
            tmp_link = []
        return link
