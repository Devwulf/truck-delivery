from src.borg import Borg
from src.constantarray import ConstantArray
from src.data import Data
from src.clustering import clustering
import math

class Warehouse(Borg):
    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
            packages = Data().get_packages().copy()
            self.__packages = ConstantArray(len(packages))
            for i, package in enumerate(packages):
                if package is None:
                    continue
                self.__packages[i] = package
            self.__n_clusters = 16
            self.__clustered_packages = [[] for i in range(self.__n_clusters)]
            self._calculate_clusters()
            self.left_packages = []
            self.location_clusters = self.group_by_same_location()

    def load_trucks(self, trucks):
        # Should return a list of packages already grouped

        # Grouping should be hierarchical. From most basic criteria to more complex:
        # 1. Group by same location
        # 2. Group by truck req
        # 3. Group by package req
        # For all these, keep track of the earliest delivery time req for each group

        # What if instead of grouping, packages are strung together?
        # On what criteria can they be strung together?
        # - Same location
        # - Package req
        # - Light strung on location cluster

        # NOOOO! Scratch everything above! Use insertion sort for planning!
        # Basically how it will work is the trucks will be given a set of
        # grouped packages, kinda like what I already did below.
        # But in the truck, it can plan its own path around the city as long
        # as it delivers the time-sensitive packages on time.
        # We can do that planning kinda like the SortedLinkedList I made,
        # where each package in the deliveries are tried to be inserted
        # on each index of the array and see at which insert will result
        # in an overall short path
        truck_ids = [truck.id for truck in trucks]
        array = self.group_location_truck_package_reqs(truck_ids)
        for item in array:
            for truck in trucks:

                if isinstance(item, list):
                    len_sum = 0
                    for loc_cluster in item:
                        len_sum += len(loc_cluster)
                    if truck.space_left() < len_sum:
                        continue
                    for loc_cluster in item:
                        if loc_cluster._truck_req != -1 and loc_cluster._truck_req != truck.id:
                            continue
                        for i, package in enumerate(loc_cluster):
                            truck.add_delivery(loc_cluster._location_id, package.package_id)
                        loc_cluster.clear()
                elif isinstance(item, LocationCluster):
                    if truck.space_left() < len(item):
                        continue
                    if item._truck_req != -1 and item._truck_req != truck.id:
                        continue
                    for i, package in enumerate(item):
                        truck.add_delivery(item._location_id, package.package_id)
                    item.clear()
        self.left_packages = array

    def group_by_same_location(self):
        # TODO: Possibly use a hashmap if location ids are not consecutive
        array = ConstantArray(len(Data().get_locations()))
        packages = self.__packages
        for package in packages:
            if array[package.address_id] is None:
                array[package.address_id] = LocationCluster(package.address_id)
            array[package.address_id].append(package)

        '''
        none_less = ConstantArray(len(array))
        for arr in array:
            if arr is None:
                continue
            none_less.append(arr)
        #return sorted(none_less, key=lambda location: location._earliest_time)
        '''
        return array

    def group_by_same_location_and_truck_req(self, truck_ids):
        location_arr = self.group_by_same_location()
        for truck_id in truck_ids:
            truck_arr = self.group_by_truck_req(truck_id)
            first_match_index = -1
            for i, item in enumerate(location_arr):
                for package in item:
                    if package.package_id in truck_arr:
                        if first_match_index == -1:
                            first_match_index = i
                            location_arr[first_match_index] = TruckReqCluster([location_arr[first_match_index]], truck_id)
                            break
                        else:
                            location_arr[first_match_index].append(item)
                            del location_arr[i]
                            break
        return location_arr

    def group_location_truck_package_reqs(self, truck_ids):
        #location_truck_arr = self.group_by_same_location_and_truck_req(truck_ids)
        location_truck_arr = self.group_by_same_location()
        package_arr = self.group_by_package_req()
        first_match_index = -1
        for i, item in enumerate(location_truck_arr):
            if item is None:
                continue
            if isinstance(item, TruckReqCluster):
                for loc_cluster in item:
                    for package in loc_cluster:
                        if package.package_id in package_arr:
                            if first_match_index == -1:
                                first_match_index = i
                                location_truck_arr[first_match_index] = [location_truck_arr[first_match_index]]
                                break
                            else:
                                location_truck_arr[first_match_index].append(item)
                                del location_truck_arr[i]
                                break
            else:
                for package in item:
                    if package.package_id in package_arr:
                        if first_match_index == -1:
                            first_match_index = i
                            # location_truck_arr[first_match_index] = AllCluster(location_truck_arr[first_match_index])
                            location_truck_arr[first_match_index] = [location_truck_arr[first_match_index]]
                            break
                        else:
                            location_truck_arr[first_match_index].append(item)
                            del location_truck_arr[i]
                            break
        return location_truck_arr

    def group_all(self, truck_id):
        all_arr = self.group_location_truck_package_reqs(truck_id)
        clusters = self.__clustered_packages
        for cluster in clusters:
            first_match_index = -1
            for i, arr in enumerate(all_arr):
                if arr is None:
                    continue
                for package in arr:
                    if package.package_id in cluster:
                        if first_match_index == -1:
                            first_match_index = i
                            all_arr[first_match_index] = [all_arr[first_match_index]]
                            break
                        else:
                            all_arr[first_match_index].append(arr)
                            del all_arr[i]
                            break
        return all_arr

    # Will always take n time
    def group_by_truck_req(self, truck_id):
        packages = []
        for i, package in enumerate(self.__packages):
            if package is None:
                continue
            if package.has_truck_req and package._truck_req == truck_id:
                packages.append(i + 1)
        return packages

    def group_by_package_req(self):
        packages = []
        for i, package in enumerate(self.__packages):
            if package is None:
                continue
            if not package.has_package_req:
                continue

            # TODO: Use DFS to find islands in the adjacency matrix of related packages
            if i + 1 not in packages:
                packages.append(i + 1)
            for id in package.package_req:
                if id not in packages:
                    packages.append(id)
        return packages

    def group_by_location_cluster(self):
        return self.__clustered_packages

    def sort_by_delivery_time(self):
        return

    def _calculate_clusters(self):
        location_matrix = Data().get_locations_matrix()
        clusters = clustering(location_matrix, self.__n_clusters)
        for package in self.__packages:
            if package is None:
                continue
            for i, cluster in enumerate(clusters):
                if package.address_id in cluster:
                    self.__clustered_packages[i].append(package.package_id)

class LocationCluster:
    def __init__(self, id):
        self._array = []
        self._location_id = id
        self._earliest_time = math.inf
        self._truck_req = -1

    def __len__(self):
        return len(self._array)

    def __getitem__(self, key):
        return self._array[key]

    def __repr__(self):
        return "%s-%s: %s" % (self._location_id, self._earliest_time, self._array.__repr__())

    def __iter__(self):
        return self._array.__iter__()

    def __delitem__(self, key):
        self._array.__delitem__(key)

    def clear(self):
        self._array.clear()

    def append(self, item):
        if item._get_delivery_time(True) < self._earliest_time:
            self._earliest_time = item._get_delivery_time(True)
        if item.has_truck_req:
            if self._truck_req != -1 and item.truck_req != self._truck_req:
                return False
            self._truck_req = item.truck_req
        self._array.append(item)
        return True

class TruckReqCluster:
    def __init__(self, arr, truck_id):
        self._array = arr # this will be an array of locationclusters
        self._truck_req = truck_id

    def __len__(self):
        len_sum = 0
        for item in self._array:
            len_sum += len(item)
        return len_sum

    def __getitem__(self, key):
        return self._array[key]

    def __repr__(self):
        return "%s: %s" % (self._truck_req, self._array.__repr__())

    def __iter__(self):
        return self._array.__iter__()

    def append(self, arr):
        self._array.append(arr)
