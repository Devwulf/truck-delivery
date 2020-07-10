import data
from clock import Clock
from pathfinder import Pathfinder

def main():
    packages = data.get_packages()
    locations = data.get_locations()
    location_matrix = data.get_locations_matrix()
    path = Pathfinder(location_matrix)
    path._dijkstra(0)
    clock = Clock()
    #clock.onTick += run_on_tick
    #clock.start("8:00 AM", "8:10 AM", 0.1, 20)

def run_on_tick(sender, current_time):
    print("Current time is: %s" % current_time)

if __name__ == "__main__":
    main()