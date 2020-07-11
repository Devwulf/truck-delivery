from collections import deque
from pathfinder import Pathfinder
import timeutil

class Truck:
    def __init__(self, speed=18):
        self.speed = speed
        self.current_location = 0
        self.deliveries = deque()
        self.eta = -1

    def add_delivery(self, location_id, package_id):
        # Enqueue to the back
        self.deliveries.append(Delivery(location_id, package_id))

    def drive(self, sender, current_seconds):
        path = Pathfinder()
        if len(self.deliveries) <= 0:
            return
        delivery = self.deliveries[-1]
        current_time = timeutil.to_time(current_seconds)
        if self.eta == -1:
            path_node = path.get_path(self.current_location, delivery.location_id)
            self.eta = path_node.distance / self.speed * 60 * 60 + current_seconds

        if current_seconds % 300 == 0:
            print("%s: Driving to location %s to deliver package no. %s" % (current_time, delivery.location_id, delivery.package_id))

        if current_seconds >= self.eta:
            delivery = self.deliveries.popleft()
            print("%s: Delivered package no. %s at location %s." % (current_time, delivery.package_id, delivery.location_id))
            self.eta = -1

# What do we need to calculate and what do we need to give?
# Calculate: best path between nodes, how long that path is, which nodes to go through
# Give: from node, to node
class Delivery:
    def __init__(self, location_id, package_id):
        self.location_id = location_id
        self.package_id = package_id
