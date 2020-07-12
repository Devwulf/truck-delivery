from src.borg import Borg
from src.constantarray import ConstantArray
from src.data import Data
from src.clustering import clustering

class Warehouse(Borg):
    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
            packages = Data().get_packages()
            self.__packages = ConstantArray(len(packages))
            for i, package in enumerate(packages):
                if package is None:
                    continue
                self.__packages[i] = package
            self.__n_clusters = 4
            self.__clustered_packages = [[] for i in range(self.__n_clusters)]
            self._calculate_clusters()

    def get_packages(self, truck_id):
        # Should return a list of packages already grouped

        # Grouping should be hierarchical. From most basic criteria to more complex:
        # 1. Group by same location
        # 2. Group by truck req
        # 3. Group by package req
        # 4. Group by location cluster
        # For all these, keep track of the earliest delivery time req for each group
        return

    # Will always take n time
    def group_by_truck_req(self, truck_id):
        packages = []
        for i, package in enumerate(self.__packages):
            if package is None:
                continue
            if package.has_truck_req and package.truck_req == truck_id:
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

        return

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
                    self.__clustered_packages[i].append(package)
