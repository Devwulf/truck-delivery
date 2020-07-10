import math

# Pathfinder using the A* algorithm
# A* algorithm recap:
# TotalWeight (f): sum of StartWeight (g) and EndWeight (h)
# Steps:
# 1. Create two arrays for unprocessed and processed nodes
# 2. Place the starting node into the unprocessed nodes list
# 3.1. If the unprocessed list is not empty, pop from top of list
# 3.2.

# Note: We cannot use the A* algorithm because all the nodes are connected
# to each other. Since A* always chooses the good enough path to the end
# point, it will always choose the direct path from the start to end, even
# if there are other better paths. We have to use the Djikstra's algorithm.
class Pathfinder:
    def __init__(self, distance_matrix):
        self.node_amount = len(distance_matrix)
        self.distance_matrix = distance_matrix
        self.calculated_matrix = [[None] * len(distance_matrix[0]) for i in range(len(distance_matrix))]
        self._calculate_paths()

    def get_path(self, from_node, to_node):
        return self.calculated_matrix[from_node][to_node]

    def _calculate_paths(self):
        return None

    # Operations we need:
    def _dijkstra(self, start_node):
        array = SortedLinkedList()
        array.sorted_add(DistanceNode(start_node, 0))
        for i in range(self.node_amount):
            if i == start_node:
                continue
            array.sorted_add(DistanceNode(i, math.inf))

        result = SortedLinkedList()
        while len(array) > 0:
            closest_node = array.pop()
            adjacent_nodes = self.distance_matrix[closest_node.index]
            for i, adj in enumerate(adjacent_nodes):
                node = DistanceNode(i, adj)
                current_node = array.get(node)
                new_distance = adj + closest_node.distance
                if current_node is not None and new_distance < current_node.distance:
                    array.remove(current_node)
                    current_node.distance = new_distance
                    array.sorted_add(current_node)
            result.sorted_add(closest_node)
        print(result)

    # Adds the node into array with insertion sort by descending
    # This makes insertion sort perform at O(n) instead of o(n^2)
    # because the array is already nearly sorted
    # We want descending because popping by the last node is O(1)
    def _sorted_add(self, array, node):
        for i, n in enumerate(array):
            if node.distance > n.distance:
                array.insert(i, node)

class DistanceNode:
    def __init__(self, index, distance):
        self.index = index
        self.distance = distance

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

    def __repr__(self):
        return "%s: %s" % (self.index, self.distance)

class Node:
    def __init__(self, value):
        self.next = None
        self.value = value

# Singly linked list that automatically sorts in ascending order
class SortedLinkedList:
    def __init__(self):
        # Need a dummy node here so sorted add will still work when
        # adding at the front
        self.head = Node(None)
        self.size = 0

    def sorted_add(self, value):
        if self.size <= 0:
            self.head.next = Node(value)
            self.size += 1
            return

        new_node = Node(value)
        current = self.head.next
        prev_node = self.head
        while current is not None:
            if new_node.value <= current.value:
                # Add before this element
                prev_node.next = new_node
                new_node.next = current
                self.size += 1
                return

            prev_node = current
            current = current.next

        # If it's still not added, it must be the last node
        prev_node.next = new_node
        self.size += 1

    def pop(self):
        node = self.head.next
        self.head.next = node.next
        self.size -= 1
        return node.value

    # This seems weird, but basically, this can return the node with
    # the same index as the item, even if they both have different values
    def get(self, item):
        current = self.head.next
        while current is not None:
            if current.value == item:
                return current.value
            current = current.next
        return None

    def remove(self, item):
        current = self.head.next
        prev_node = self.head
        while current is not None:
            if current.value == item:
                value = current.value
                prev_node.next = current.next
                self.size -= 1
                return value
            prev_node = current
            current = current.next
        return None

    def __repr__(self):
        message = "Size: %s\n" % self.size
        current = self.head.next
        while current is not None:
            message += "%s\n" % current.value
            current = current.next
        return message

    def __len__(self):
        return self.size

    def __contains__(self, item):
        current = self.head.next
        while current is not None:
            if current.value == item:
                return True
            current = current.next
        return False