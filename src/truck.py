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
        self.location_clusters = []
        self.delivery_queue = deque()
        self.eta = -1
        self.odometer = 0
        self.data = Data()
        self.printed = False

    def add_delivery(self, location_id, package_id):
        self.deliveries.append(Delivery(location_id, package_id))

    def space_left(self):
        return self.deliveries.space_left()

    def plan_drive(self):
        location_clusters = Warehouse().location_clusters
        packages = Data().get_packages()
        print(self.deliveries)
        location_only = deque()
        timed_locations_only = deque()
        timed_location_clusters = []
        for delivery in self.deliveries:
            if delivery is None:
                continue
            if location_clusters[delivery.location_id]._earliest_time < 86399.0:
                # Add the locations with time-sensitive packages later
                if location_clusters[delivery.location_id] not in timed_location_clusters:
                    timed_location_clusters.append(location_clusters[delivery.location_id])
                continue
            if delivery.location_id not in location_only:
                location_only.append(delivery.location_id)
        timed_location_clusters = sorted(timed_location_clusters, key=lambda location: location._earliest_time)
        for cluster in timed_location_clusters:
            if cluster._location_id not in timed_locations_only:
                timed_locations_only.append(cluster._location_id)
        print(location_only)
        print(timed_locations_only)
        final_arr = [0]
        shortest_distance = 0
        start = 0
        while len(location_only) > 0:
            current_loc = location_only.popleft()
            shortest = math.inf
            shortest_path = []
            for i in range(len(final_arr)):
                array = final_arr.copy()
                array.insert(i + 1, current_loc)
                distance = self.overall_distance(array)
                if distance <= shortest:
                    shortest = distance
                    shortest_path = array
            shortest_distance = shortest
            final_arr = shortest_path
            print("%s: %s" % (shortest_distance, final_arr))

        print("Shortest path with distance %s: %s" % (shortest_distance, final_arr))

    def partial_distance(self, location_array, start, end):
        print(location_array[start:end+1])
        return self.overall_distance(location_array[start:end])

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
        if len(self.deliveries) <= 0:
            if self.printed == False:
                print("%s: Odometer for truck %s is at %s miles." % (current_time, self.id, self.odometer))
                self.printed = True
            return

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

        next_queue = self.delivery_queue[0]
        current_location = self.data.get_location(self.current_location)
        location = self.data.get_location(next_queue.location_id)
        if self.eta == -1:
            print("%s: Driving from location %s to location %s to deliver package no. %s" % (current_time, current_location.location_id - 1, location.location_id - 1, next_queue.package_id))
            path_node = path.get_path(self.current_location, next_queue.location_id)
            self.eta = path_node.distance / self.speed * 60 * 60 + current_seconds
            self.odometer += path_node.distance
        if current_seconds >= self.eta:
            while len(self.delivery_queue) > 0 and self.delivery_queue[0].location_id == next_queue.location_id:
                next_delivery = self.delivery_queue.popleft()
                #print("%s: Delivered package no. %s at location %s." % (current_time, next_delivery.package_id, location.address))
            self.eta = -1
            self.current_location = next_queue.location_id

# What do we need to calculate and what do we need to give?
# Calculate: best path between nodes, how long that path is, which nodes to go through
# Give: from node, to node
class Delivery:
    def __init__(self, location_id, package_id):
        self.location_id = location_id
        self.package_id = package_id

    def __repr__(self):
        return "%s: %s" % (self.location_id, self.package_id)
