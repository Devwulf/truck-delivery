import csv
from src.package import Package
from src.location import Location
from src.borg import Borg
from src.hashmap import HashMap

class Data(Borg):
    _assets_path = "assets/"
    _packages_file = "packages.csv"
    _locations_file = "locations.csv"
    _location_weights_file = "location-weights.csv"

    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
            self.__packages = HashMap(40)
            self.__locations = HashMap(27)
            self.__locations_matrix = []
            self.get_packages()
            self.get_locations()
            self.get_locations_matrix()

    def get_packages(self) -> HashMap:
        """
        Reads the packages from the .csv file (if the packages hashmap
        is not initialized) and returns the hashmap where the packages
        are stored.

        :return: The hashmap where the packages are stored.
        """
        if len(self.__packages) > 0:
            return self.__packages

        with open(self._assets_path + self._packages_file, encoding="utf-8-sig") as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                if len(row) != 11:
                    raise ValueError("The given input data for a package may have too little or too many columns.")

                package_id = row[0]
                address_id = row[1]
                delivery_time = row[2]
                has_truck_req = row[3]
                truck_req = row[4]
                is_delayed = row[5]
                delay_time = row[6]
                has_package_req = row[7]
                package_req = row[8]
                mass = row[9]
                delivery_status = row[10]

                try:
                    package = Package(package_id, address_id, delivery_time, has_truck_req, truck_req, is_delayed, delay_time, has_package_req, package_req, mass, delivery_status)
                    self.__packages.append(package.package_id, package)
                except ValueError as e:
                    print(e)

        return self.__packages

    def get_locations(self) -> HashMap:
        """
        Reads the locations from the .csv file (if the locations hashmap
        is not initialized) and returns the hashmap where the locations
        are stored.

        :return: The hashmap where the locations are stored.
        """

        if len(self.__locations) > 0:
            return self.__locations

        with open(self._assets_path + self._locations_file, encoding="utf-8-sig") as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                if len(row) != 6:
                    raise ValueError("The given input data for a location may have too little or too many columns.")

                location_id = row[0]
                name = row[1]
                address = row[2]
                city = row[3]
                state = row[4]
                zip_code = row[5]

                try:
                    location = Location(location_id, name, address, city, state, zip_code)
                    self.__locations.append(location.location_id, location)
                except ValueError as e:
                    print(e)

        return self.__locations

    def get_locations_matrix(self):
        """
        Reads the distance matrix of the locations from the .csv file
        (if the locations_matrix 2D array is not initialized) and returns
        the 2D float array of the distance matrix.

        :return: A 2D float array of the distance matrix of the locations
        """
        if len(self.__locations_matrix) > 0:
            return self.__locations_matrix

        matrix = self.__locations_matrix
        with open(self._assets_path + self._location_weights_file) as csvFile:
            readCSV = csv.reader(csvFile, delimiter=',')
            for row in readCSV:
                for i, str in enumerate(row):
                    row[i] = float(row[i] if row[i] else 0)
                matrix.append(row)

        # Making the matrix a redundant distance matrix with both the bottom
        # left and top right filled with data, so it's easier to use
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                matrix[i][j] = matrix[j][i]

        return self.__locations_matrix

    def get_package(self, id:int) -> Package:
        """
        :param id: The id of the package to be looked up from the hashmap.
        :return: The package that was looked up using the given id.
        """
        return self.packages[id]

    def get_location(self, id:int) -> Location:
        """
        :param id: The id of the location to be looked up from the hashmap.
        :return: The location that was looked up using the given id.
        """
        return self.locations[id]

    packages = property(get_packages)
    locations = property(get_locations)
    locations_matrix = property(get_locations_matrix)