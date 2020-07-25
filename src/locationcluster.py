from src.package import Package
from typing import List
import math

class LocationCluster:
    def __init__(self, id:int):
        """
        Space: O(n) Time: O(1)

        :param id: The id of the location that this cluster is associated to.
        """
        self.__packages:List[Package] = []
        self.__location_id = id
        self.__earliest_time = math.inf
        self.__truck_req = -1
        self.__delay_time = -1

    def __get_packages(self):
        """
        Space: O(n) Time: O(1)

        :return: The packages to be delivered to the associated location.
        """
        return self.__packages

    def __get_location_id(self):
        """
        Space: O(1) Time: O(1)

        :return: The location id of the associated location.
        """
        return self.__location_id

    def __get_earliest_time(self):
        """
        Space: O(1) Time: O(1)

        :return: The earliest delivery time among the packages.
        """
        return self.__earliest_time

    def __get_truck_req(self):
        """
        Space: O(1) Time: O(1)

        :return: The truck requirement based on the packages' truck requirement.
        """
        return self.__truck_req

    def __get_delay_time(self):
        """
        Space: O(1) Time: O(1)

        :return: The earliest delay time among the packages.
        """
        return self.__delay_time

    packages = property(__get_packages)
    location_id = property(__get_location_id)
    earliest_time = property(__get_earliest_time)
    truck_req = property(__get_truck_req)
    delay_time = property(__get_delay_time)

    def __len__(self):
        """
        Space: O(1) Time: O(1)

        :return: The length of the packages in this cluster.
        """
        return len(self.__packages)

    def __getitem__(self, index:int):
        """
        Space: O(1) Time: O(1)

        :param index: The index of the value to be returned.
        :return:
        """
        return self.__packages[index]

    def __iter__(self):
        """
        Space: O(1) Time: O(1)

        :return: The iterator of the internal package list.
        """
        return self.__packages.__iter__()

    def __delitem__(self, index:int):
        """
        Space: O(n) Time: O(n)

        :param index: The index of the value to be deleted.
        :return: N/A
        """
        self.__packages.__delitem__(index)

    def clear(self):
        """
        Removes all the packages associated to this cluster.

        Space: O(n) Time: O(n)

        :return: N/A
        """
        self.__packages.clear()

    def append(self, item:Package) -> bool:
        """
        Adds the package into the list of packages associated to this cluster.
        Also calculates the earliest time, truck requirement, and delay time
        based on the added packages.

        Space: O(1) Time: O(1)

        :param item: The package to be added to the packages list.
        :return: True if the item is successfully added to the list, False if the package conflicts with other packages based on truck requirement and delay time.
        """
        if item.delivery_time < self.earliest_time:
            self.__earliest_time = item.delivery_time
        if item.has_truck_req:
            if self.truck_req != -1 and item.truck_req != self.truck_req:
                return False
            self.__truck_req = item.truck_req
        if item.is_delayed:
            if self.delay_time != -1 and item.delay_time != self.delay_time:
                return False
            self.__delay_time = item.delay_time
        self.__packages.append(item)
        return True