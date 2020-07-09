import data
from clock import Clock

def main():
    packages = data.get_packages()
    locations = data.get_locations()
    location_matrix = data.get_locations_matrix()
    clock = Clock()
    clock.onTick += run_on_tick
    clock.start("8:00 AM", "9:00 PM", 0.01, 5)

def run_on_tick(sender, current_time):
    print("Current time is: %s" % current_time)

if __name__ == "__main__":
    main()