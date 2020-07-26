# Mark Christian Malabanan, Student ID #001233960

from src.data import Data
from src.clock import Clock
from src.pathfinder import Pathfinder
from src.truck import TimedTruck, DelayedTruck
from src.warehouse import Warehouse
from src.package import DeliveryStatus
import src.timeutil as timeutil

class Main:
    def __init__(self):
        # Initialize all singletons below
        Data(initialize=True)
        Clock(initialize=True)
        Warehouse(initialize=True)
        Pathfinder(Data().get_locations_matrix())

        self.truck = TimedTruck(1)
        self.truck2 = DelayedTruck(2)

    def run(self):
        clock = Clock()
        clock.on_tick += self.truck.on_update
        clock.on_tick += self.truck2.on_update
        clock.on_stop += self.on_clock_stop
        clock.start("8:00 AM", "11:59:59 PM", 0.01, 20)

    def on_clock_stop(self, sender, current_seconds):
        print("%s: The day has ended!" % (timeutil.to_time(current_seconds)))
        packages = Data().get_packages().values()
        packages = sorted(packages, key=lambda package: package.package_id)
        success_count = 0
        failed_count = 0
        for package in packages:
            if package.delivery_status == DeliveryStatus.Delivered:
                success_count += 1
            else:
                failed_count += 1
            print(package)
        print("Total truck mileage: %s miles\nSuccessfully delivered: %s\nFailed to deliver (late or not delivered): %s" % (self.truck.odometer + self.truck2.odometer, success_count, failed_count))

if __name__ == "__main__":
    Main().run()
