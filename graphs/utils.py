
import logging

from fraud_detection.settings import FILE_DIRS

logger = logging.getLogger(__name__)


class DuplicateEdgeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NodeDoesntExistError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Graph(object):

    def __init__(self, structure=None):

        if structure is None:
            structure = dict()

        self.__structure = structure

    def __node(self, *args):

        for n in args:
            if not self.node_exist(n):
                self.__structure[n] = set()

    def add_node(self, **kwargs):
        """
        Adding new node on graph
        :param n: New node to adding a graph
        :return: None
        """

        logger.info("Adding new node on graph")
        if 'nodes' in kwargs:
            nodes = [n for n in kwargs.get('nodes')]
            apply(self.__node, nodes)

        elif 'node' in kwargs:
            self.__node(kwargs.get('node'))

    def __edge(self, e):
        """
        
        :param e: An edge compound by two nodes
        :return: 
        """
        if self.node_exist(e[0]) and self.node_exist(e[1]) and not self.edge_exist(e) and e[0] != e[1]:
            self.__structure[e[0]].add(e[1])
            self.__structure[e[1]].add(e[0])

        elif self.edge_exist(e):
            logger.error("Edge already exist")
            raise DuplicateEdgeError("Edge already exist")

        else:
            logger.error("Node doesn't exist")
            raise NodeDoesntExistError("Node(s) doesn't exist")

    def add_edge(self, **kwargs):
        """
        Connecting two nodes
        :param e: A edge will be connected
        :return: None
        """

        logger.info("Adding new edge on graph")
        if 'edge' in kwargs:
            e = kwargs.get('edge')
            self.__edge(e)

        elif 'edges' in kwargs:
            for e in kwargs.get('edges'):
                self.__edge(e)

    def node_exist(self, n):
        """
        Check if node already exist in graph
        :param n: An Node
        :return: True if node already exist
        """
        logger.info("Checking if node already exist")
        return self.__structure.get(n) is not None

    def edge_exist(self, e):
        """
        Test if edge exist in graph
        :param e: Tuple representing a edge
        :return: True if edge exist or False if edge not exist
        """

        logger.info("Checking if edge exist (if two nodes already connected)")
        return self.is_connected(e[0], e[1])

    def get_all_node(self):
        """
        List all nodes
        :return: A list representing all nodes on graph
        """
        return self.__structure.keys()

    def is_connected(self, n1, n2):
        """
        Base function to check if edge exist, or if two nodes are in 
        the same network collision
        :param n1: node 1
        :param n2: node 2
        :return: True if nodes are connected of false if not
        """

        logger.info("Checking if two nodes are connected")
        e1 = self.__structure.get(n1)
        e2 = self.__structure.get(n2)

        if n1 in e2 and n2 in e1:
            return True

        return False

    def same_network(self, e):

        """
        For answer if two nodes are in the same network collision, 
        not need know all network, only know if the nodes are connected

        :param e: A tuple representing an edge of graph 
        :return: True if two nodes are in the same network collision
        """

        logger.info("Checking if two nodes are in same network collision")
        if self.node_exist(e[0]) and self.node_exist(e[1]):
            if self.is_connected(e[0], e[1]):
                return True
            else:
                return UtilsService.any(self.__structure[e[1]], lambda x: x in self.__structure[e[0]])

        else:
            logger.error("Node doesn't exist")
            raise NodeDoesntExistError("Node doesn't exist")

    def __str__(self):
        return str(self.__structure)


class UtilsService(object):

    @staticmethod
    def load_graph():
        logger.info("Load file")

        nodes = list()
        edges = list()
        graph = Graph()

        with open(FILE_DIRS, "r") as f:
            lines = f.readlines()

            for line in lines:
                l = line.split(' ')
                nodes.extend(map(lambda x: int(x), l))
                edges.append(tuple([int(l[0]), int(l[1])]))

        graph.add_node(nodes=list(set(nodes)))
        graph.add_edge(edges=edges)

        return graph

    @staticmethod
    def store_graph(edge):
        logger.info("Wrinting new edge on graph")
        with open(FILE_DIRS, "a+") as f:
            f.write("\n{0} {1}".format(edge[0], edge[1]))

    @staticmethod
    def any(iterable, predicate):
        for iter in iterable:
            if predicate(iter):
                return True
        return False

    @staticmethod
    def all(iterable, predicate):
        result = False

        for iter in iterable:
            result = result and predicate(iter)

        return result
