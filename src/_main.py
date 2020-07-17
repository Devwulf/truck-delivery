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
    print(Warehouse().group_by_same_location())
    '''
    print(path.calculated_paths_matrix[3])
    print(Warehouse().group_by_same_location())
    print(Warehouse().group_by_same_location_and_truck_req([1, 2]))
    print(Warehouse().group_location_truck_package_reqs([1, 2]))
    print(Warehouse().group_by_package_req())
    print(Warehouse().group_by_truck_req(2))
    print(Warehouse().group_by_package_req())
    print(Warehouse().group_by_location_cluster())
    print(Warehouse().group_all(2))
    '''
    truck = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)
    Warehouse().load_trucks([truck, truck2])
    truck.plan_drive()
    truck2.plan_drive()
    Warehouse().load_trucks([truck3])
    truck3.plan_drive()

    clock = Clock()
    clock.onTick += truck.drive
    #clock.onTick += truck2.drive
    #clock.start("8:00 AM", "11:59:59 PM", 0.01, 20)

def run_on_tick(sender, current_time):
    print("Current time is: %s" % current_time)

if __name__ == "__main__":
    main()
