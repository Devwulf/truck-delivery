import math
from src.pathfinder import Pathfinder
from src.warehouse import LocationCluster
import src.timeutil as timeutil

# Best to use a deque for locations
def solve(locations, start_id, end_id):
    start_node = LocationCluster(start_id)
    final_arr = [start_node]
    shortest_distance = 0
    shortest_time = 0
    while len(locations) > 0:
        current_loc = locations.popleft()
        if current_loc is None:
            continue

        short_dist = math.inf
        short_time = 0
        shortest_path = []
        for i in range(len(final_arr)):
            array = final_arr.copy()
            array.insert(i + 1, current_loc)
            distance = overall_distance(array, lambda location: location._location_id)
            time = overall_time(array, lambda location: location._location_id)
            if distance <= short_dist:
                short_dist = distance
                short_time = time
                shortest_path = array
        shortest_distance = short_dist
        shortest_time = short_time
        final_arr = shortest_path
    if end_id >= 0:
        last_to_start = Pathfinder().get_path(final_arr[-1]._location_id, end_id)
        shortest_distance += last_to_start.distance
        shortest_time += last_to_start.time
        final_arr.append(LocationCluster(end_id))
    return [shortest_distance, timeutil.to_time(shortest_time), final_arr]

def overall_distance(location_array, get_id):
    path = Pathfinder()
    i = 0
    distance_sum = 0
    while i < len(location_array) - 1:
        current_loc = get_id(location_array[i])
        next_loc = get_id(location_array[i + 1])
        path_node = path.get_path(current_loc, next_loc)
        distance_sum += path_node.distance
        i += 1
    return distance_sum

def overall_time(location_array, get_id):
    path = Pathfinder()
    i = 0
    time_sum = 0
    while i < len(location_array) - 1:
        current_loc = get_id(location_array[i])
        next_loc = get_id(location_array[i + 1])
        path_node = path.get_path(current_loc, next_loc)
        time_sum += path_node.time
        i += 1
    return time_sum