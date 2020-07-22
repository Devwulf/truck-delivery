import math
from src.borg import Borg
from collections import deque
from src.constantarray import ConstantArray

# Note: We cannot use the A* algorithm because all the nodes are connected
# to each other. Since A* always chooses the good enough path to the end
# point, it will always choose the direct path from the start to end, even
# if there are other better paths. We have to use the Dijkstra's algorithm
# to find the absolute best path between two points.
class Pathfinder(Borg):
    def __init__(self, distance_matrix=None):
        Borg.__init__(self)
        if distance_matrix is not None:
            self.distance_matrix = distance_matrix
            self.node_amount = len(distance_matrix)
            self.calculated_paths_matrix = [[PathNode(j, 0, []) for j in range(len(distance_matrix[0]))] for i in range(len(distance_matrix))]
            self._calculate_paths()

    def get_path(self, from_node, to_node):
        return self.calculated_paths_matrix[from_node][to_node]

    def _calculate_paths(self):
        for i in range(self.node_amount):
            self._dijkstra(i)

    def _dijkstra(self, start_node):
        """
        Use the Dijkstra's algorithm to find the best paths between
        any two nodes. The time complexity of this is O(n^2).

        :param start_node: The node of the graph to start from.
        :return: N/A
        """
        array = ConstantArray(self.node_amount)
        for i in range(self.node_amount):
            if i == start_node:
                array[start_node] = PathNode(start_node, 0, [])
                continue
            array[i] = PathNode(i, math.inf, [])

        while len(array) > 0:
            # Find the closest node in array
            min = math.inf
            min_index = 0
            for i, node in enumerate(array):
                if node is None:
                    continue
                if node.distance < min:
                    min = node.distance
                    min_index = i

            current_node = array.pop(min_index)
            adjacent_nodes = self.distance_matrix[current_node.index]
            for i, adj in enumerate(adjacent_nodes):
                adjacent_node = array[i]
                new_distance = adj + current_node.distance
                if adjacent_node is not None and new_distance < adjacent_node.distance:
                    curr_path_node = self.calculated_paths_matrix[start_node][current_node.index]
                    adj_path_node = self.calculated_paths_matrix[start_node][adjacent_node.index]
                    if current_node.index != start_node:
                        shortest_path = curr_path_node.path.copy()
                        shortest_path.append(current_node.index)
                        adj_path_node.path = shortest_path
                    adj_path_node.distance = new_distance
                    adjacent_node.distance = new_distance

class PathNode:
    def __init__(self, index, distance, path):
        self.index = index
        self.distance = distance
        self.time = distance / 18 * 60 * 60
        self.path = path

    def __eq__(self, other):
        return self.index == other.index

    def __ne__(self, other):
        return self.index != other.index

    def __lt__(self, other):
        return self.distance < other.distance

    def __le__(self, other):
        return self.distance <= other.distance

    def __gt__(self, other):
        return self.distance > other.distance

    def __ge__(self, other):
        return self.distance >= other.distance

    def __str__(self):
        return "Index: %s\nDistance: %s\nPath: %s\n" % (self.index, self.distance, self.path)

    def __repr__(self):
        return "%s: %s (%s)" % (self.index, self.distance, self.path)

    def _get_distance(self):
        return self._distance

    def _set_distance(self, value):
        self._distance = value
        self.time = value / 18 * 60 * 60

    distance = property(_get_distance, _set_distance)

class Node:
    def __init__(self, value):
        self.next = None
        self.value = value