import src.tspsolver as tsp
from src.data import Data
from src.warehouse import LocationCluster
from src.warehouse import Warehouse
from src.pathfinder import Pathfinder
from src.constantarray import ConstantArray
from src.package import Package
import src.timeutil as timeutil
from collections import deque
from typing import Callable
import math

def main():
    Data(initialize=True)
    Warehouse(initialize=True)
    Pathfinder(Data().get_locations_matrix())

    '''
    locations = Warehouse().flatten_group_by_same_location(False)
    print(locations)
    timed_locations = get_timed_locations(locations)
    timed_locations2 = get_timed_delayed_locations(locations)
    truck_2_locations = get_truck_specific_locations(locations, 2)
    print(timed_locations)
    print(timed_locations2)
    print(truck_2_locations)
    print(locations)
    print()
    solved_timed_locations = tsp.solve(deque(timed_locations), 0, 0)
    print(solved_timed_locations)
    solved_timed_locations2 = tsp.solve(deque(timed_locations2), 0, -1)
    print(solved_timed_locations2)
    solved_truck_2_locations = tsp.solve(deque(truck_2_locations), solved_timed_locations2[-1][-1]._location_id, 0)
    print(solved_truck_2_locations)
    solved_locations = tsp.solve(deque(locations), 0, 0)
    print(solved_locations)
    solved_locations1 = tsp.solve(deque(locations[:5] + locations[8:11]), 0, 0)
    print(solved_locations1)
    solved_locations2 = tsp.solve(deque(locations[5:8] + locations[11:]), 0, 0)
    print(solved_locations2)
    '''

    packages = Data().get_packages()
    no_delayed_packages = get_delayed_packages_only(packages, is_not=True)
    print(no_delayed_packages)
    timed_packages_only = get_timed_packages_only(no_delayed_packages)
    print(timed_packages_only)
    print(no_delayed_packages)

    print()
    if len(timed_packages_only) < 16:
        # Check if there are package reqs first, then fill it up
        timed_packages_only.extend(fill_up(timed_packages_only, no_delayed_packages, 16 - len(timed_packages_only)))
    print(timed_packages_only)
    print(no_delayed_packages)
    timed_packages_only_clustered = to_location_clusters(timed_packages_only)
    print(timed_packages_only_clustered)
    print()

    timed_delayed_packages = get_packages_or(packages, is_timed=True, is_delayed=True)
    print(timed_delayed_packages)
    current_time = timeutil.to_seconds("9:05 AM")
    current_delayed_packages = get_packages_with_predicate(timed_delayed_packages, lambda package: package._get_delay_time(is_seconds=True) == current_time)
    print(current_delayed_packages)
    print()

    if len(current_delayed_packages) < 16:
        print(fill_up(current_delayed_packages, no_delayed_packages, 16 - len(current_delayed_packages)))
    print(current_delayed_packages)
    current_delayed_packages_clustered = to_location_clusters(current_delayed_packages)
    print(current_delayed_packages_clustered)
    print(no_delayed_packages)

def get_packages_and(packages:list, is_timed, is_delayed):
    return get_packages_with_predicate(packages, lambda package: (is_timed == package.is_timed) and (is_delayed == package.is_delayed))

def get_packages_or(packages:list, is_timed, is_delayed):
    return get_packages_with_predicate(packages, lambda package: (is_timed == package.is_timed) or (is_delayed == package.is_delayed))

def get_timed_packages_only(packages:list, is_not=False):
    return get_packages_with_predicate(packages, lambda package: is_not != package.is_timed)

def get_delayed_packages_only(packages:list, is_not=False):
    return get_packages_with_predicate(packages, lambda package: is_not != package.is_delayed)

def get_packages_with_predicate(packages:list, predicate: Callable[[Package], bool]):
    result = []
    non_result = []
    package: Package
    for package in packages:
        if predicate(package):
            result.append(package)
        else:
            non_result.append(package)
    packages[:] = non_result
    return result

def to_location_clusters(packages:list):
    array = ConstantArray(27)
    for package in packages:
        if array[package.address_id] is None:
            array[package.address_id] = LocationCluster(package.address_id)
        array[package.address_id].append(package)
    result = []
    for cluster in array:
        if cluster is None:
            continue
        result.append(cluster)
    return result

def to_packages(location_clusters:list):
    result = []
    for cluster in location_clusters:
        if cluster is None:
            continue
        for package in cluster:
            result.append(package)
    return result

def fill_up(first_arr:list, second_arr:list, amount:int):
    package1: Package
    package2: Package
    result = []
    for package1 in first_arr:
        if amount <= 0:
            break
        non_result = []
        for package2 in second_arr:
            if amount > 0 and package1.address_id == package2.address_id:
                result.append(package2)
                amount -= 1
            else:
                non_result.append(package2)
        second_arr[:] = non_result
    if amount > 0:
        if len(second_arr) <= 0:
            return result
        result2 = [second_arr[0]]
        for package1 in result2:
            if amount <= 0:
                break
            non_result = []
            for package2 in second_arr:
                if amount > 0 and package1.address_id == package2.address_id:
                    result.append(package2)
                    amount -= 1
                else:
                    non_result.append(package2)
            second_arr[:] = non_result
            if len(second_arr) <= 0:
                break
            result2.append(second_arr[0])
    return result

def get_timed_locations(locations):
    result = []
    for location in locations:
        if location is None:
            continue
        if (location._earliest_time < 86399.0 or location._location_id == 4) and location._delay_time == -1:
            result.append(location)
    locations[:] = [location for location in locations if not (location is not None and (location._earliest_time < 86399.0 or location._location_id == 4) and location._delay_time == math.inf)]
    return result

def get_timed_delayed_locations(locations):
    result = []
    for location in locations:
        if location is None:
            continue
        if location._earliest_time < 86399.0:
            result.append(location)
    locations[:] = [location for location in locations if not (location is not None and location._earliest_time < 86399.0)]
    return result

def get_truck_specific_locations(locations, truck_id):
    result = []
    for location in locations:
        if location is None:
            continue
        if location._truck_req == truck_id:
            result.append(location)
    locations[:] = [location for location in locations if not (location is not None and location._truck_req == truck_id)]
    return result

if __name__ == "__main__":
    main()