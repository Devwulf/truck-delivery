import data
from clock import Clock
from pathfinder import Pathfinder
from truck import Truck

def main():
    packages = data.get_packages()
    locations = data.get_locations()
    location_matrix = data.get_locations_matrix()
    path = Pathfinder(location_matrix)
    #print(path.get_path(0, 7))
    truck = Truck()
    truck.add_delivery(7, 36)
    clock = Clock()
    clock.onTick += truck.drive
    clock.start("8:00 AM", "8:30 AM", 0.1, 20)

def run_on_tick(sender, current_time):
    print("Current time is: %s" % current_time)

if __name__ == "__main__":
    main()