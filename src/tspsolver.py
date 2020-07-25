import math
from src.pathfinder import Pathfinder
from src.locationcluster import LocationCluster
import src.timeutil as timeutil
from typing import Deque

def solve(locations:Deque[LocationCluster], start_id:int, end_id:int):
    """
    Solves the Traveling Salesman Problem for a given list of locations.
    This uses a similar concept to insertion sort, and runs like so,
    given a queue of locations to move through and the best paths between
    each of those locations:
        1. A location is removed from the queue and added to a path list.
        2. The path list is passed through the overall_distance() method to
            calculate the distance travelled if that path was taken
        3. Keep track of the shortest distance and path list.
        4. Repeat this until the queue is empty.
    This has a time complexity of O(n^3), although an optimization can be
    implemented on calculating the overall distance to make it O(n^2) instead.

    Space: O(n^2) Time: O(n^3)

    :param locations: A queue of locations (as LocationCluster) to solve the TSP problem for.
    :param start_id: The id of the starting location.
    :param end_id: The id of the ending location.
    :return: An array of the shortest distance, the shortest time, and the shortest path.
    """
    start_node = LocationCluster(start_id)
    shortest_path = [start_node]
    shortest_distance = 0
    shortest_time = 0
    while len(locations) > 0:
        current_loc = locations.popleft()
        if current_loc is None:
            continue

        short_dist = math.inf
        short_time = 0
        short_path = []
        for i in range(len(shortest_path)):
            array = shortest_path.copy()
            array.insert(i + 1, current_loc)
            distance = overall_distance(array, lambda location: location.location_id)
            #time = overall_time(array, lambda location: location.location_id)
            if distance <= short_dist:
                short_dist = distance
                #short_time = time
                short_path = array
        shortest_distance = short_dist
        #shortest_time = short_time
        shortest_path = short_path
    if end_id >= 0:
        last_to_start = Pathfinder().get_path(shortest_path[-1].location_id, end_id)
        shortest_distance += last_to_start.distance
        #shortest_time += last_to_start.time
        shortest_path.append(LocationCluster(end_id))
    if shortest_path[0].location_id == shortest_path[-1].location_id and len(shortest_path) == 2:
        return [0, 0, []]
    return [shortest_distance, timeutil.to_time(shortest_time), shortest_path[1:]]

def overall_distance(path_array, get_id) -> float:
    """
    Calculates the overall distance of the given path.

    Space: O(n) Time: O(n)

    :param path_array: The path to calculate the distance for.
    :param get_id: The conversion function used to convert the package to id.
    :return: The overall distance of the given path.
    """
    i = 0
    distance_sum = 0
    while i < len(path_array) - 1:
        current_loc = get_id(path_array[i])
        next_loc = get_id(path_array[i + 1])
        path_node = Pathfinder().get_path(current_loc, next_loc)
        distance_sum += path_node.distance
        i += 1
    return distance_sum

def overall_time(path_array, get_id) -> float:
    """
    Calculates the overall time spent taking the given path.

    Space: O(n) Time: O(n)

    :param path_array: The path to calculate the time for.
    :param get_id: The conversion function used to convert the package to id.
    :return: The overall time of the given path.
    """
    i = 0
    time_sum = 0
    while i < len(path_array) - 1:
        current_loc = get_id(path_array[i])
        next_loc = get_id(path_array[i + 1])
        path_node = Pathfinder().get_path(current_loc, next_loc)
        time_sum += path_node.time
        i += 1
    return time_sum