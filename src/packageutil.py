from src.package import Package
from src.locationcluster import LocationCluster
from src.data import Data
from typing import Callable
from typing import List

def get_packages_and(packages:List[int], is_timed, is_delayed):
    return get_packages_with_predicate(packages, lambda package: (is_timed == package.is_timed) and (is_delayed == package.is_delayed))

def get_packages_or(packages:List[int], is_timed, is_delayed):
    return get_packages_with_predicate(packages, lambda package: (is_timed == package.is_timed) or (is_delayed == package.is_delayed))

def get_timed_packages_only(packages:List[int], is_not=False):
    return get_packages_with_predicate(packages, lambda package: is_not != package.is_timed)

def get_delayed_packages_only(packages:List[int], is_not=False):
    return get_packages_with_predicate(packages, lambda package: is_not != package.is_delayed)

def get_packages_with_predicate(packages:List[int], predicate: Callable[[Package], bool]):
    result = []
    non_result = []
    for package_id in packages:
        package = Data().get_package(package_id)
        if predicate(package):
            result.append(package_id)
        else:
            non_result.append(package_id)
    packages[:] = non_result
    return result

def get_package_ids_with_same_package_req(packages:List[int]):
    result = []
    for package_id in packages:
        package = Data().get_package(package_id)
        if not package.has_package_req:
            continue
        for req in package.package_req:
            if req not in result:
                result.append(req)
        result.append(package.package_id)
    return result

def to_location_clusters(packages:List[int]) -> List[LocationCluster]:
    array = [None] * 27
    for package_id in packages:
        package = Data().get_package(package_id)
        if array[package.address_id] is None:
            array[package.address_id] = LocationCluster(package.address_id)
        array[package.address_id].append(package)
    result = []
    for cluster in array:
        if cluster is None:
            continue
        result.append(cluster)
    return result

def to_packages(location_clusters:List[LocationCluster]):
    result = []
    cluster: LocationCluster
    for cluster in location_clusters:
        if cluster is None:
            continue
        package: Package
        for package in cluster:
            result.append(package.package_id)
    return result

def fill_up(first_arr:List[int], second_arr:List[int], amount:int, significant_only=False):
    result = []
    for package1_id in first_arr:
        package1 = Data().get_package(package1_id)
        if amount <= 0:
            break
        non_result = []
        for package2_id in second_arr:
            package2 = Data().get_package(package2_id)
            if amount > 0 and package1.address_id == package2.address_id:
                result.append(package2.package_id)
                amount -= 1
            else:
                non_result.append(package2.package_id)
        second_arr[:] = non_result
    if amount > 0 and not significant_only:
        if len(second_arr) <= 0:
            return result
        result2 = [second_arr[0]]
        for package1_id in result2:
            package1 = Data().get_package(package1_id)
            if amount <= 0:
                break
            non_result = []
            for package2_id in second_arr:
                package2 = Data().get_package(package2_id)
                if amount > 0 and package1.address_id == package2.address_id:
                    result.append(package2.package_id)
                    amount -= 1
                else:
                    non_result.append(package2.package_id)
            second_arr[:] = non_result
            if len(second_arr) <= 0:
                break
            result2.append(second_arr[0])
    return result

def fill_with_same_package_req(first_arr:List[int], second_arr:List[int], packages_with_same_package_req:List[int]):
    # Check how many packages in the same package req are already here
    same_package_req_count = 0
    for package1_id in first_arr:
        package1 = Data().get_package(package1_id)
        if package1.package_id in packages_with_same_package_req:
            same_package_req_count += 1
    same_package_req_needed = len(packages_with_same_package_req) - same_package_req_count
    if same_package_req_needed <= 0:
        return [] # Nothing more needs to be done if they're all in the truck already

    result = []
    non_result = []
    for package2_id in second_arr:
        package2 = Data().get_package(package2_id)
        if same_package_req_needed > 0 and package2.package_id in packages_with_same_package_req:
            result.append(package2.package_id)
        else:
            non_result.append(package2.package_id)
    second_arr[:] = non_result
    return result
