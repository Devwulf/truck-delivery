from src.data import Data
from src.clock import Clock
from src.pathfinder import Pathfinder
from src.truck import TimedTruck, DelayedTruck
from src.warehouse import Warehouse

def main():
    # Initialize all singletons below
    Data(initialize=True)
    Clock(initialize=True)
    Warehouse(initialize=True)

    location_matrix = Data().get_locations_matrix()
    Pathfinder(location_matrix)

    truck = TimedTruck(1)
    truck2 = DelayedTruck(2)

    clock = Clock()
    clock.onTick += truck.on_update
    clock.onTick += truck2.on_update
    clock.start("8:00 AM", "11:59:59 PM", 0.01, 20)

if __name__ == "__main__":
    main()
