import csv
import Package

packages = []
with open('assets/packages.csv', encoding="utf-8-sig") as csv_file:
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
            package = Package.Package(package_id, address_id, delivery_time, has_truck_req, truck_req, is_delayed, delay_time, has_package_req, package_req)
            packages.append(package)
        except ValueError as e:
            print(e)

for package in packages:
    package.print()