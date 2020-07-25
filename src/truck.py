from collections import deque
from src.pathfinder import Pathfinder
from src.data import Data
import src.timeutil as timeutil
from src.warehouse import Warehouse
from src.package import Package, DeliveryStatus
from src.locationcluster import LocationCluster
import src.packageutil as packageutil
import src.tspsolver as tsp
import math
from abc import ABC, abstractmethod
from typing import List
from typing import Deque

class AbstractTruck(ABC):
    def __init__(self, truck_id, speed=18):
        """
        Space: O(n) Time: O(1)

        :param truck_id: The id of this truck.
        :param speed: The speed of this truck.
        """
        self.truck_id = truck_id
        self.speed = speed
        self.eta = -1
        self.odometer = 0
        self.current_location = 0
        self.delivery_path:Deque[LocationCluster] = deque()
        self.__sender = None

    def on_update(self, sender, current_seconds:int):
        """
        Runs on every tick of the clock.

        Space: O(n^2) Time: O(n^2)

        :param sender: The clock object that runs this.
        :param current_seconds: The current time in seconds.
        :return: N/A
        """
        if self.__sender is None:
            self.__sender = sender

        if self.load_packages_when(current_seconds):
            self.load_packages()
        else:
            self.drive(current_seconds)

    def end_update(self):
        """
        Ends the update lifecycle of this object.

        Space: O(1) Time: O(1)

        :return: N/A
        """
        if self.__sender is None:
            return
        self.__sender.on_tick -= self.on_update

    def drive(self, current_seconds:int):
        """
        Makes the truck drive and move from location to location to
        deliver the packages.

        Space: O(n) Time: O(n)

        :param current_seconds: The current time in seconds.
        :return: N/A
        """
        if len(self.delivery_path) <= 0:
            return

        # Convert the time in seconds to a time string of format HH:MM:SS [AM/PM]
        current_time:str = timeutil.to_time(current_seconds)

        # Grab next location cluster in our path and get the location
        # objects for the current and next location
        next_location = self.delivery_path[0]
        current_location = Data().get_location(self.current_location)
        location = Data().get_location(next_location.location_id)

        # If we're not moving to the next location yet, set the ETA
        if self.eta == -1:
            if next_location.location_id == current_location.location_id:
                self.delivery_path.popleft()
                return

            print("%s: Driving from location %s to location %s to deliver packages '%s'." % (current_time, current_location.address, location.address, next_location.packages))
            path_node = Pathfinder().get_path(self.current_location, next_location.location_id)
            self.eta = path_node.distance / self.speed * 60 * 60 + current_seconds
            self.odometer += path_node.distance

        # If we get to the next location, deliver and mark each package
        # as delivered if on time, delivered late otherwise. Then we set
        # our current location to this location.
        if current_seconds >= self.eta:
            next_delivery = self.delivery_path.popleft()
            for package in next_delivery:
                delivery_status = DeliveryStatus.DeliveredLate if package.is_timed and current_seconds > package.delivery_time else DeliveryStatus.Delivered
                package.delivery_status = delivery_status.value
                package.delivered_at = current_seconds
                print("%s: Delivered package no. %s at location %s." % (current_time, package.package_id, location.address))
            self.eta = -1
            self.current_location = next_location.location_id

    # What will be loaded into this truck
    @abstractmethod
    def load_packages(self):
        """
        Loads the packages into the truck by accessing the
        warehouse's package storage.

        Space: O(n^2) Time: O(n^2)
        """
        pass

    @abstractmethod
    def load_packages_when(self, current_seconds:int) -> bool:
        """
        This is called to determine when the packages should be
        loaded into the truck. Called in the on_update() method
        like so:
            ``if load_packages_when(current_seconds):``
                ``load_packages()``

        Space: O(1) Time: O(1)

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
        packages:List[int] = Warehouse().packages
        # End drive if no more packages in warehouse
        if len(packages) <= 0:
            print("Truck %s finished delivery! Odometer is: %s miles" % (self.truck_id, self.odometer))
            self.end_update()
            return

        # Grab necessary packages
        packages_with_same_package_req = packageutil.get_package_ids_with_same_package_req(packages)
        delayed_packages = packageutil.get_delayed_packages_only(packages)
        timed_packages = packageutil.get_timed_packages_only(packages)

        # Fill with packages with the same package requirement
        if len(timed_packages) < 16:
            timed_packages.extend(packageutil.fill_with_same_package_req(timed_packages, packages, packages_with_same_package_req))
        # Fill with packages with the truck requirement of this truck.
        if len(timed_packages) < 16:
            truck_req_packages = packageutil.get_packages_with_predicate(packages, predicate=lambda package: package.truck_req == self.truck_id)
            timed_packages.extend(truck_req_packages)
        # Fill with packages going to the same locations and other packages.
        if len(timed_packages) < 16:
            timed_packages.extend(packageutil.fill_up(timed_packages, packages, 16 - len(timed_packages)))

        # Convert the package ids to location clusters and solve for TSP
        timed_packages_cluster = packageutil.to_location_clusters(timed_packages)
        solved = tsp.solve(deque(timed_packages_cluster), 0, 0)
        self.delivery_path = deque(solved[2])
        # Mark all packages in this truck as En Route
        for loc_cluster in self.delivery_path:
            for package in loc_cluster:
                package.delivery_status = DeliveryStatus.EnRoute
        packages.extend(delayed_packages)

    def load_packages_when(self, current_seconds) -> bool:
        # Load packages only when in the warehouse and there are
        # no packages in the truck
        if self.current_location == 0 and len(self.delivery_path) <= 0:
            return True
        return False

class DelayedTruck(AbstractTruck):
    """
    Waits for and loads the earliest delayed packages
    """

    def __init__(self, id, speed=18):
        """
        Space: O(n) Time: O(n)

        :param id: The id of this truck.
        :param speed: The speed of this truck.
        """
        super().__init__(id, speed)
        self.earliest_delay_time = math.inf
        packages:List[int] = Warehouse().packages
        # Get the earliest time that delayed packages are arriving.
        for package_id in packages:
            package:Package = Data().get_package(package_id)
            if package.is_delayed and package.delay_time < self.earliest_delay_time:
                self.earliest_delay_time = package.delay_time

    def load_packages(self):
        packages:List[int] = Warehouse().packages
        # End drive if no more packages in warehouse
        if len(packages) <= 0:
            print("Truck %s finished delivery! Odometer is: %s miles" % (self.truck_id, self.odometer))
            self.end_update()
            return

        # Grab necessary packages
        packages_with_same_package_req = packageutil.get_package_ids_with_same_package_req(packages)
        delayed_packages = packageutil.get_delayed_packages_only(packages)

        # Fill with packages with the same package requirement
        if len(delayed_packages) < 16:
            delayed_packages.extend(packageutil.fill_with_same_package_req(delayed_packages, packages, packages_with_same_package_req))
        # Fill with packages with the truck requirement of this truck.
        if len(delayed_packages) < 16:
            truck_req_packages = packageutil.get_packages_with_predicate(packages, predicate=lambda package: package.truck_req == self.truck_id)
            delayed_packages.extend(truck_req_packages)
        # Fill with packages going to the same locations and other packages.
        if len(delayed_packages) < 16:
            delayed_packages.extend(packageutil.fill_up(delayed_packages, packages, 16 - len(delayed_packages)))

        delayed_packages_cluster = packageutil.to_location_clusters(delayed_packages)
        # Convert the package ids to location clusters and solve for TSP
        solved = tsp.solve(deque(delayed_packages_cluster), 0, 0)
        self.delivery_path = deque(solved[2])
        # Mark all packages in this truck as En Route
        for loc_cluster in self.delivery_path:
            for package in loc_cluster:
                package.delivery_status = DeliveryStatus.EnRoute

    def load_packages_when(self, current_seconds:int) -> bool:
        # Load packages only when the current time is at or after the
        # earliest delay time and if the truck is at the warehouse and
        # if there are no packages in the truck.
        if current_seconds >= self.earliest_delay_time and self.current_location == 0 and len(self.delivery_path) <= 0:
            return True
        return False