from collections import deque
from src.pathfinder import Pathfinder
from src.data import Data
import src.timeutil as timeutil
from src.warehouse import Warehouse
from src.package import Package
from src.locationcluster import LocationCluster
import src.packageutil as packageutil
import src.tspsolver as tsp
import math
from abc import ABC, abstractmethod
from typing import List
from typing import Deque

class AbstractTruck(ABC):
    def __init__(self, truck_id, speed=18):
        self.truck_id = truck_id
        self.speed = speed
        self.eta = -1
        self.odometer = 0
        self.current_location = 0
        self.delivery_path:Deque[LocationCluster] = deque()
        self.__sender = None

    def on_update(self, sender, current_seconds:int):
        if self.__sender is None:
            self.__sender = sender

        if self.load_packages_when(current_seconds):
            self.load_packages()
        else:
            self.drive(current_seconds)

    def end_update(self):
        if self.__sender is None:
            return
        self.__sender.onTick -= self.on_update

    def drive(self, current_seconds:int):
        if len(self.delivery_path) <= 0:
            return

        current_time:str = timeutil.to_time(current_seconds)

        '''
        if len(self.delivery_queue) <= 0:
            if self.printed == False:
                print("%s: Odometer for truck %s is at %s miles." % (current_time, self.id, self.odometer))
                self.printed = True
            return
        '''

        next_location = self.delivery_path[0]
        current_location = Data().get_location(self.current_location)
        location = Data().get_location(next_location.location_id)
        if self.eta == -1:
            if next_location.location_id == current_location.location_id:
                self.delivery_path.popleft()
                return

            print("%s: Driving from location %s to location %s to deliver packages '%s'." % (current_time, current_location.address, location.address, next_location.packages))
            path_node = Pathfinder().get_path(self.current_location, next_location.location_id)
            self.eta = path_node.distance / self.speed * 60 * 60 + current_seconds
            self.odometer += path_node.distance
        if current_seconds >= self.eta:
            next_delivery = self.delivery_path.popleft()
            for package in next_delivery:
                print("%s: Delivered package no. %s at location %s." % (current_time, package.package_id, location.address))
            self.eta = -1
            self.current_location = next_location.location_id

    # What will be loaded into this truck
    @abstractmethod
    def load_packages(self):
        """
        Loads the packages into the truck by accessing the
        warehouse's package storage.
        """
        pass

    @abstractmethod
    def load_packages_when(self, current_seconds:int) -> bool:
        """
        This is called to determine when the packages should be
        loaded into the truck. Called in the on_update() method
        like so:

            if load_packages_when(current_seconds):
                load_packages()

        :param current_seconds: The current time in seconds
        :return: True if the packages should be loaded at the current second, False otherwise
        """
        pass

class TimedTruck(AbstractTruck):
    """
    Loads the time-sensitive packages and delivers them as soon as
    the simulation starts.
    """

    def __init__(self, id, speed=18):
        super().__init__(id, speed)

    def load_packages(self):
        packages:List[int] = Warehouse().get_packages()
        if len(packages) <= 0:
            print("Odometer of truck %s is: %s miles" % (self.truck_id, self.odometer))
            self.end_update()
            return

        packages_with_same_package_req = packageutil.get_package_ids_with_same_package_req(packages)
        delayed_packages = packageutil.get_delayed_packages_only(packages)
        timed_packages = packageutil.get_timed_packages_only(packages)

        if len(timed_packages) < 16:
            timed_packages.extend(packageutil.fill_with_same_package_req(timed_packages, packages, packages_with_same_package_req))
        if len(timed_packages) < 16:
            truck_req_packages = packageutil.get_packages_with_predicate(packages, predicate=lambda package: package.truck_req == self.truck_id)
            timed_packages.extend(truck_req_packages)
        if len(timed_packages) < 16:
            timed_packages.extend(packageutil.fill_up(timed_packages, packages, 16 - len(timed_packages)))

        timed_packages_cluster = packageutil.to_location_clusters(timed_packages)
        solved = tsp.solve(deque(timed_packages_cluster), 0, 0)
        self.delivery_path = deque(solved[2])
        packages.extend(delayed_packages)

    def load_packages_when(self, current_seconds) -> bool:
        if self.current_location == 0 and len(self.delivery_path) <= 0:
            return True
        return False

class DelayedTruck(AbstractTruck):
    """
    Waits for and loads the earliest delayed packages
    """

    def __init__(self, id, speed=18):
        super().__init__(id, speed)
        self.earliest_delay_time = math.inf
        packages:List[int] = Warehouse().get_packages()
        for package_id in packages:
            package:Package = Data().get_package(package_id)
            if package.is_delayed and package.delay_time < self.earliest_delay_time:
                self.earliest_delay_time = package.delay_time

    def load_packages(self):
        packages:List[int] = Warehouse().get_packages()
        if len(packages) <= 0:
            print("Odometer of truck %s is: %s miles" % (self.truck_id, self.odometer))
            self.end_update()
            return

        packages_with_same_package_req = packageutil.get_package_ids_with_same_package_req(packages)
        delayed_packages = packageutil.get_delayed_packages_only(packages)

        if len(delayed_packages) < 16:
            delayed_packages.extend(packageutil.fill_with_same_package_req(delayed_packages, packages, packages_with_same_package_req))
        if len(delayed_packages) < 16:
            truck_req_packages = packageutil.get_packages_with_predicate(packages, predicate=lambda package: package.truck_req == self.truck_id)
            delayed_packages.extend(truck_req_packages)
        if len(delayed_packages) < 16:
            delayed_packages.extend(packageutil.fill_up(delayed_packages, packages, 16 - len(delayed_packages)))

        delayed_packages_cluster = packageutil.to_location_clusters(delayed_packages)
        solved = tsp.solve(deque(delayed_packages_cluster), 0, 0)
        self.delivery_path = deque(solved[2])

    def load_packages_when(self, current_seconds:int) -> bool:
        if current_seconds >= self.earliest_delay_time and self.current_location == 0 and len(self.delivery_path) <= 0:
            return True
        return False