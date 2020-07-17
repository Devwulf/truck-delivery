from collections import deque
from src.pathfinder import Pathfinder
from src.data import Data
import src.timeutil as timeutil
from src.constantarray import ConstantArray
from src.warehouse import Warehouse
import math

class Truck:
    def __init__(self, id, speed=18):
        self.id = id
        self.speed = speed
        self.current_location = 0
        self.deliveries = ConstantArray(16)
        self.delivery_locations = []
        self.location_clusters = []
        self.delivery_queue = deque()
        self.eta = -1
        self.odometer = 0
        self.data = Data()
        self.printed = False

    def add_delivery(self, location_id, package_id, location_cluster):
        self.deliveries.append(Delivery(location_id, package_id))
        if location_cluster not in self.location_clusters:
            self.location_clusters.append(location_cluster)

    def space_left(self):
        return self.deliveries.space_left()

    def plan_drive(self):
        #print(self.deliveries)
        location_only = deque()
        timed_location_clusters = deque()

        for location_cluster in self.location_clusters:
            if location_cluster is None:
                continue
            if location_cluster._earliest_time < 86399.0:
                # Add the locations with time-sensitive packages later
                if location_cluster not in timed_location_clusters:
                    timed_location_clusters.append(location_cluster)
                continue
            if location_cluster not in location_only:
                location_only.append(location_cluster)
        timed_location_clusters = deque(sorted(timed_location_clusters, key=lambda location: location._earliest_time))
        #print(location_only)
        #print(timed_location_clusters)
        final_arr = [0]
        shortest_distance = 0
        while len(location_only) > 0:
            current_loc = location_only.popleft()
            shortest = math.inf
            shortest_path = []
            for i in range(len(final_arr)):
                array = final_arr.copy()
                array.insert(i + 1, current_loc._location_id)
                distance = self.overall_distance(array)
                if distance <= shortest:
                    shortest = distance
                    shortest_path = array
            shortest_distance = shortest
            final_arr = shortest_path
            #print("%s: %s" % (shortest_distance, final_arr))

        # For the timed locations, what if we also find the best path
        # for that, then merge the two final arrays?
        # We'll also make it so if a group of timed packages can't be
        # delivered on time, we can make the time req of the earlier
        # timed packages to be earlier than normal, kinda pushing the
        # earlier ones even earlier
        start_time = timeutil.to_seconds("8:00 AM")
        start = 0
        while len(timed_location_clusters) > 0:
            current_loc = timed_location_clusters.popleft()
            shortest = math.inf
            shortest_path = []
            shortest_index = 0
            for i in range(start, len(final_arr)):
                array = final_arr.copy()
                array.insert(i + 1, current_loc._location_id)
                distance = self.overall_distance(array)
                partial_distance = self.partial_distance(array, 0, i + 1)
                eta = partial_distance / self.speed * 60 * 60 + start_time
                if eta > current_loc._earliest_time:
                    #print("%s %s %s" % (eta, start, array))
                    break
                if distance <= shortest:
                    shortest = distance
                    shortest_path = array
                    shortest_index = i + 1
            shortest_distance = shortest
            final_arr = shortest_path
            start = shortest_index
            #print("%s: %s" % (shortest_distance, final_arr))

        shortest_distance += Pathfinder().get_path(final_arr[-1], 0).distance
        #print("Shortest path with distance %s: %s" % (shortest_distance, final_arr))

        location_clusters = Warehouse().location_clusters
        for i in final_arr:
            if location_clusters[i] is None:
                continue
            try:
                self.delivery_queue.append(location_clusters[i])
            except:
                print(i)

    def partial_distance(self, location_array, start, end):
        return self.overall_distance(location_array[start:end+1])

    def overall_distance(self, location_array):
        path = Pathfinder()
        i = 0
        distance_sum = 0
        while i < len(location_array) - 1:
            current_loc = location_array[i]
            next_loc = location_array[i + 1]
            path_node = path.get_path(current_loc, next_loc)
            distance_sum += path_node.distance
            i += 1
        return distance_sum

    def drive(self, sender, current_seconds):
        path = Pathfinder()

        current_time = timeutil.to_time(current_seconds)
        if len(self.delivery_queue) <= 0:
            if self.printed == False:
                print("%s: Odometer for truck %s is at %s miles." % (current_time, self.id, self.odometer))
                self.printed = True
            return

        '''
        if len(self.delivery_queue) <= 0:
            # Grab next one in deliveries
            delivery = self.deliveries.popleft()
            self.delivery_queue.appendleft(delivery)
            # Grab the next ones going to the same location
            while len(self.deliveries) > 0 and self.deliveries.peekleft() is not None and self.deliveries.peekleft().location_id == delivery.location_id:
                delivery = self.deliveries.popleft()
                self.delivery_queue.appendleft(delivery)
            path_node = path.get_path(self.current_location, delivery.location_id)
            for i in reversed(path_node.path):
                for j, delivery_item in enumerate(self.deliveries):
                    if delivery_item is None:
                        continue
                    if delivery_item.location_id == i:
                        self.delivery_queue.appendleft(delivery_item)
                        del self.deliveries[i]
        '''

        next_queue = self.delivery_queue[0]
        current_location = self.data.get_location(self.current_location)
        location = self.data.get_location(next_queue._location_id)
        if self.eta == -1:
            print("%s: Driving from location %s to location %s to deliver packages." % (current_time, current_location.location_id - 1, location.location_id - 1))
            path_node = path.get_path(self.current_location, next_queue._location_id)
            self.eta = path_node.distance / self.speed * 60 * 60 + current_seconds
            self.odometer += path_node.distance
        if current_seconds >= self.eta:
            next_delivery = self.delivery_queue.popleft()
            for package in next_delivery:
                print("%s: Delivered package no. %s at location %s." % (current_time, package.package_id, location.address))
            self.eta = -1
            self.current_location = next_queue._location_id

# What do we need to calculate and what do we need to give?
# Calculate: best path between nodes, how long that path is, which nodes to go through
# Give: from node, to node
class Delivery:
    def __init__(self, location_id, package_id):
        self.location_id = location_id
        self.package_id = package_id

    def __repr__(self):
        return "%s: %s" % (self.location_id, self.package_id)
