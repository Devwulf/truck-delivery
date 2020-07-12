from src.data import Data
from src.clock import Clock
from src.pathfinder import Pathfinder
from src.truck import Truck
from src.warehouse import Warehouse

def main():
    # Initialize all singletons below
    Data(initialize=True)
    Clock(initialize=True)
    Warehouse(initialize=True)

    data = Data()
    packages = data.get_packages()
    locations = data.get_locations()
    location_matrix = data.get_locations_matrix()
    path = Pathfinder(location_matrix)
    #print(path.get_path(0, 7))
    print(Warehouse().group_by_truck_req(2))
    print(Warehouse().group_by_package_req())
    print(Warehouse().group_by_location_cluster())
    truck = Truck(1)
    truck.add_delivery(7, 36)
    truck2 = Truck(2)
    truck2.add_delivery(20, 14)
    truck2.add_delivery(26, 22)
    clock = Clock()
    clock.onTick += truck.drive
    clock.onTick += truck2.drive
    #clock.start("8:00 AM", "8:30 AM", 0.01, 20)

def run_on_tick(sender, current_time):
    print("Current time is: %s" % current_time)

if __name__ == "__main__":
    main()