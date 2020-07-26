# Mark Christian Malabanan, Student ID #001233960

import math
from src.borg import Borg
from src.constantarray import ConstantArray

# Note: We cannot use the A* algorithm because all the nodes are connected
# to each other. Since A* always chooses the good enough path to the end
# point, it will always choose the direct path from the start to end, even
# if there are other better paths. We have to use the Dijkstra's algorithm
# to find the absolute best path between two points.
class Pathfinder(Borg):
    def __init__(self, distance_matrix=None):
        """
        Space: O(n^2) Time: O(n^2)

        :param distance_matrix: The distance matrix of the locations.
        """
        Borg.__init__(self)
        if distance_matrix is not None:
            self.distance_matrix = distance_matrix
            self.node_amount = len(distance_matrix)
            self.calculated_paths_matrix = [[PathNode(j, 0, []) for j in range(len(distance_matrix[0]))] for i in range(len(distance_matrix))]
            self._calculate_paths()

    def get_path(self, from_node, to_node):
        return self.calculated_paths_matrix[from_node][to_node]

    def _calculate_paths(self):
        """
        Calculates the best path for each locations.

        Space: O(n^2) Time: O(n^2)

        :return: N/A
        """
        for i in range(self.node_amount):
            self._dijkstra(i)

    def _dijkstra(self, start_node):
        """
        Use the Dijkstra's algorithm to find the best paths between
        any two nodes. The time complexity of this is O(n^2).

        Space: O(n^2) Time: O(n^2)

        :param start_node: The node of the graph to start from.
        :return: N/A
        """
        # Fill the array with nodes of distance 0 for the start node,
        # and infinite for the other nodes.
        array = ConstantArray(self.node_amount)
        for i in range(self.node_amount):
            if i == start_node:
                array[start_node] = PathNode(start_node, 0, [])
                continue
            array[i] = PathNode(i, math.inf, [])

        while len(array) > 0:
            # Find and get the closest node in array
            min = math.inf
            min_index = 0
            for i, node in enumerate(array):
                if node is None:
                    continue
                if node.distance < min:
                    min = node.distance
                    min_index = i
            closest_node = array.pop(min_index)

            # Get the adjacent location distances of the closest node.
            # Since we have a fully connected graph, all locations
            # are adjacent to each other.
            adjacent_nodes = self.distance_matrix[closest_node.index]
            for i, adj in enumerate(adjacent_nodes):
                adjacent_node = array[i]
                new_distance = adj + closest_node.distance
                # If the distance of this adjacent node is greater than
                # the distance of the closest node plus the distance of
                # the adjacent node to the closest node, then update
                # the distance of this adjacent node.
                if adjacent_node is not None and new_distance < adjacent_node.distance:
                    curr_path_node = self.calculated_paths_matrix[start_node][closest_node.index]
                    adj_path_node = self.calculated_paths_matrix[start_node][adjacent_node.index]
                    if closest_node.index != start_node:
                        shortest_path = curr_path_node.path.copy()
                        shortest_path.append(closest_node.index)
                        adj_path_node.path = shortest_path
                    adj_path_node.distance = new_distance
                    adjacent_node.distance = new_distance

class PathNode:
    def __init__(self, index, distance, path):
        """
        Space: O(1) Time: O(1)

        :param index: The index of the location that this node is associated to.
        :param distance: The overall distance of the path.
        :param path: An array of location ids showing the best path.
        """
        self.index = index
        self.distance = distance
        self.time = distance / 18 * 60 * 60
        self.path = path

    def __eq__(self, other):
        """
        Space: O(1) Time: O(1)

        :param other: The other path node to compare this to.
        :return: True if the node indices are equal, False otherwise.
        """
        return self.index == other.index

    def __ne__(self, other):
        """
        Space: O(1) Time: O(1)

        :param other: The other path node to compare this to.
        :return: True if the node indices are not equal, False otherwise.
        """
        return self.index != other.index

    def __lt__(self, other):
        """
        Space: O(1) Time: O(1)

        :param other: The other path node to compare this to.
        :return: True if this node distance is less than the other node distance, False otherwise.
        """
        return self.distance < other.distance

    def __le__(self, other):
        """
        Space: O(1) Time: O(1)

        :param other: The other path node to compare this to.
        :return: True if this node distance is less than or equal to the other node distance, False otherwise.
        """
        return self.distance <= other.distance

    def __gt__(self, other):
        """
        Space: O(1) Time: O(1)

        :param other: The other path node to compare this to.
        :return: True if this node distance is greater than the other node distance, False otherwise.
        """
        return self.distance > other.distance

    def __ge__(self, other):
        """
        Space: O(1) Time: O(1)

        :param other: The other path node to compare this to.
        :return: True if this node distance is greater than or equal to the other node distance, False otherwise.
        """
        return self.distance >= other.distance

    def _get_distance(self):
        """
        Space: O(1) Time: O(1)

        :return: The total distance of this path.
        """
        return self._distance

    def _set_distance(self, value):
        """
        Space: O(1) Time: O(1)

        :param value: The value to set the distance of this path to.
        :return: N/A
        """
        self._distance = value
        self.time = value / 18 * 60 * 60

    distance = property(_get_distance, _set_distance)