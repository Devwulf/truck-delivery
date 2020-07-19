from src.package import Package
from typing import List
import math

class LocationCluster:
    def __init__(self, id:int):
        self.__packages:List[Package] = []
        self.__location_id = id
        self.__earliest_time = math.inf
        self.__truck_req = -1
        self.__delay_time = -1

    def __get_packages(self):
        return self.__packages

    def __get_location_id(self):
        return self.__location_id

    def __get_earliest_time(self):
        return self.__earliest_time

    def __get_truck_req(self):
        return self.__truck_req

    def __get_delay_time(self):
        return self.__delay_time

    packages = property(__get_packages)
    location_id = property(__get_location_id)
    earliest_time = property(__get_earliest_time)
    truck_req = property(__get_truck_req)
    delay_time = property(__get_delay_time)

    def __len__(self):
        return len(self.__packages)

    def __getitem__(self, key:int):
        return self.__packages[key]

    def __repr__(self):
        return "%s-%s: %s" % (self.location_id, self.earliest_time, self.__packages.__repr__())

    def __iter__(self):
        return self.__packages.__iter__()

    def __delitem__(self, key:int):
        self.__packages.__delitem__(key)

    def clear(self):
        self.__packages.clear()

    def append(self, item:Package):
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