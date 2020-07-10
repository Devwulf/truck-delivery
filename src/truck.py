class Truck:
    def __init__(self, speed):
        self.speed = speed
        self.deliveries = []

    # Pass min distance from one node to another, and the nodes to pass to get there
    def add_delivery(self, location_id, package_id, ):
        self.deliveries.append(Delivery(location_id, package_id))

# What do we need to calculate and what do we need to give?
# Calculate: best path between nodes, how long that path is, which nodes to go through
# Give: from node, to node
class Delivery:
    def __init__(self, location_id, package_id):
        self.location_id = location_id
        self.package_id = package_id
