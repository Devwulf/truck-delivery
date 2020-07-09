import csv
from package import Package
from location import Location

assets_path = "assets/"
packages_file = "packages.csv"
locations_file = "locations.csv"
location_weights_file = "location-weights.csv"

def get_packages():
    packages = []
    with open(assets_path + packages_file, encoding="utf-8-sig") as csv_file:
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
                packages.append(package)
            except ValueError as e:
                print(e)

    return packages

def get_locations():
    locations = []
    with open(assets_path + locations_file, encoding="utf-8-sig") as csv_file:
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
                locations.append(location)
            except ValueError as e:
                print(e)

    return locations

def get_locations_matrix():
    matrix = []
    with open(assets_path + location_weights_file) as csvFile:
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

    return matrix