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
    packages = sorted(packages, key=lambda package: package.package_id)
    print(packages)
    packages_with_same_package_req = get_package_ids_with_same_package_req(packages)
    print(packages_with_same_package_req)
    no_delayed_packages = get_delayed_packages_only(packages, is_not=True)
    print(no_delayed_packages)
    timed_packages_only = get_timed_packages_only(no_delayed_packages)
    print(timed_packages_only)
    print(no_delayed_packages)

    print()
    if len(timed_packages_only) < 16:
        # Check if there are package reqs first, then fill it up
        timed_packages_only.extend(fill_with_same_package_req(timed_packages_only, no_delayed_packages, packages_with_same_package_req))
    if len(timed_packages_only) < 16:
        timed_packages_only.extend(fill_up(timed_packages_only, no_delayed_packages, 16 - len(timed_packages_only)))
    print(timed_packages_only)
    print(no_delayed_packages)
    timed_packages_only_clustered = to_location_clusters(timed_packages_only)
    print(timed_packages_only_clustered)
    solved_timed_packages_only_clustered = tsp.solve(deque(timed_packages_only_clustered), start_id=0, end_id=0)
    print(solved_timed_packages_only_clustered)
    print()

    timed_delayed_packages = get_packages_or(packages, is_timed=True, is_delayed=True)
    print(timed_delayed_packages)
    current_time = timeutil.to_seconds("9:05 AM")
    current_delayed_packages = get_packages_with_predicate(timed_delayed_packages, lambda package: package._get_delay_time(is_seconds=True) == current_time and package.is_timed)
    print(current_delayed_packages)
    no_delayed_packages.extend(timed_delayed_packages)
    truck2_packages = get_packages_with_predicate(no_delayed_packages, predicate=lambda package: package.truck_req == 2)
    print(truck2_packages)
    print()

    extra_packages = []
    extra_nonsignificant_packages = []
    if len(current_delayed_packages) < 16:
        extra_packages = fill_up(current_delayed_packages, no_delayed_packages, 12 - len(current_delayed_packages), significant_only=True)
        extra_nonsignificant_packages = fill_up(current_delayed_packages, no_delayed_packages, 11 - len(current_delayed_packages))
    print(current_delayed_packages + extra_packages)
    print(extra_nonsignificant_packages + truck2_packages)
    current_delayed_packages_clustered = to_location_clusters(current_delayed_packages + extra_packages)
    print(current_delayed_packages_clustered)
    extra_packages_clustered = to_location_clusters(extra_nonsignificant_packages + truck2_packages)
    print(extra_packages_clustered)
    solved_current_delayed_packages_clustered = tsp.solve(deque(current_delayed_packages_clustered), start_id=0, end_id=-1)
    print(solved_current_delayed_packages_clustered)
    solved_extra_packages_clustered = tsp.solve(deque(extra_packages_clustered), solved_current_delayed_packages_clustered[-1][-1].location_id, 0)
    print(solved_extra_packages_clustered)
    print()

    print(no_delayed_packages)
    no_delayed_packages_clustered = to_location_clusters(no_delayed_packages)
    print(no_delayed_packages_clustered)
    solved_no_delayed_packages_clustered = tsp.solve(deque(no_delayed_packages_clustered), 0, 0)
    print(solved_no_delayed_packages_clustered)

if __name__ == "__main__":
    main()