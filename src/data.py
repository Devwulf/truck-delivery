import csv
from src.package import Package
from src.location import Location
from src.borg import Borg


class Data(Borg):
    _assets_path = "assets/"
    _packages_file = "packages.csv"
    _locations_file = "locations.csv"
    _location_weights_file = "location-weights.csv"

    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
            self.__packages = []
            self.__locations = []
            self.__locations_matrix = []

    # TODO: Eventually use hashmap to store these data
    def get_packages(self):
        if len(self.__packages) > 0:
            return self.__packages

        with open(self._assets_path + self._packages_file, encoding="utf-8-sig") as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                if (len(row) != 9):
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

                try:
                    package = Package(package_id, address_id, delivery_time, has_truck_req, truck_req, is_delayed, delay_time, has_package_req, package_req)
                    self.__packages.append(package)
                except ValueError as e:
                    print(e)

        return self.__packages

    def get_locations(self):
        if len(self.__locations) > 0:
            return self.__locations

        with open(self._assets_path + self._locations_file, encoding="utf-8-sig") as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')
            for row in read_csv:
                if (len(row) != 6):
                    raise ValueError("The given input data for a location may have too little or too many columns.")

                location_id = row[0]
                name = row[1]
                address = row[2]
                city = row[3]
                state = row[4]
                zip_code = row[5]

                try:
                    location = Location(location_id, name, address, city, state, zip_code)
                    self.__locations.append(location)
                except ValueError as e:
                    print(e)

        return self.__locations

    def get_locations_matrix(self):
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

    def get_package(self, id):
        packages = self.get_packages()
        return packages[id - 1]

    def get_location(self, id):
        locations = self.get_locations()
        return locations[id]

    packages = property(get_packages)
    locations = property(get_locations)
    locations_matrix = property(get_locations_matrix)