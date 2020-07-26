# Mark Christian Malabanan, Student ID #001233960

from src.package import Package
from src.locationcluster import LocationCluster
from src.data import Data
from typing import Callable
from typing import List

def get_packages_and(packages:List[int], is_timed, is_delayed):
    """
    Gets the packages based on the boolean criteria is_timed AND is_delayed.
    Example:
        is_timed = True AND is_delayed = True:
            Return the packages that are timed (time-sensitive) and delayed.
        is_timed = False AND is_delayed = True:
            Return the packages that are not timed but are delayed.

    Note: This also removes the filtered packages from the given packages list.

    Space: O(n) Time: O(n)

    :param packages: The list of packages to filter.
    :param is_timed: The boolean criteria determining whether the package is time-sensitive.
    :param is_delayed: The boolean criteria determining whether the package is delayed.
    :return: The list of packages matching the given criteria.
    """
    return get_packages_with_predicate(packages, lambda package: (is_timed == package.is_timed) and (is_delayed == package.is_delayed))

def get_packages_or(packages:List[int], is_timed, is_delayed):
    """
    Gets the packages based on the boolean criteria is_timed OR is_delayed.
    Example:
        is_timed = True OR is_delayed = True:
            Return the packages that are timed (time-sensitive) plus those that are delayed.
        is_timed = False OR is_delayed = True:
            Return the packages that are not timed plus those that are not delayed.

    Note: This also removes the filtered packages from the given packages list.

    Space: O(n) Time: O(n)

    :param packages: The list of packages to filter.
    :param is_timed: The boolean criteria determining whether the package is time-sensitive.
    :param is_delayed: The boolean criteria determining whether the package is delayed.
    :return: The list of packages matching the given criteria.
    """
    return get_packages_with_predicate(packages, lambda package: (is_timed == package.is_timed) or (is_delayed == package.is_delayed))

def get_timed_packages_only(packages:List[int], is_not=False):
    """
    Gets only the time-sensitive packages.

    Note: This also removes the filtered packages from the given packages list.

    Space: O(n) Time: O(n)

    :param packages: The list of packages to filter.
    :param is_not: The boolean criteria determining whether to get all the packages that are NOT time-sensitive instead.
    :return: The list of packages matching the given criteria.
    """
    return get_packages_with_predicate(packages, lambda package: is_not != package.is_timed)

def get_delayed_packages_only(packages:List[int], is_not=False):
    """
    Gets only the delayed packages.

    Note: This also removes the filtered packages from the given packages list.

    Space: O(n) Time: O(n)

    :param packages: The list of packages to filter.
    :param is_not: The boolean criteria determining whether to get all the packages that are NOT delayed instead.
    :return: The list of packages matching the given criteria.
    """
    return get_packages_with_predicate(packages, lambda package: is_not != package.is_delayed)

def get_packages_with_predicate(packages:List[int], predicate: Callable[[Package], bool]):
    """
    Gets the packages based on the given predicate that acts as a
    custom filter. Example:
        Grab only the packages with a truck requirement of truck 2:
            ``get_packages_with_predicate(packages, predicate=lambda package: package.truck_req == 2)``

    Note: This also removes the filtered packages from the given packages list.

    Space: O(n) Time: O(n)

    :param packages: The list of packages to filter.
    :param predicate: The predicate used to filter the packages.
    :return: The list of packages matching the given criteria.
    """
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
    """
    Gets only the package ids of the packages that need to be together
    based on their package requirements.

    Space: O(n) Time: O(n^2)

    :param packages: The list of packages to filter.
    :return: The package ids of the packages that need to be together based on their package requirements.
    """
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
    """
    Converts the list of package ids to a list of locations clusters
    with the packages going to the same locations being in the same
    cluster.

    Space: O(n) Time: O(n)

    :param packages: The list of package ids to make into location clusters.
    :return: The list of location clusters containing the package objects.
    """
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
    """
    Converts the list of location clusters to a flattened list of
    package ids not grouped together.

    Space: O(n) Time: O(n^2)

    :param location_clusters: The list of location clusters to make into package ids.
    :return: The list of package ids contained in the given location clusters.
    """
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
    """
    Fills up the given first array package ids with package ids from
    the second array based on the similarity of the locations. If the
    length of the first array still doesn't reach the given amount, it
    will add non-significant (no similarity in locations) ids from
    the second array.

    However, instead of filling up the first array, it returns the array
    of ids that will fill up the first array. The second array is still
    modified to not include the ids removed from it.

    Space: O(n) Time: O(n^2)

    :param first_arr: The array of package ids to fill up to.
    :param second_arr: The array of package ids to fill up from.
    :param amount: The amount that the length of the first array much reach.
    :param significant_only: If True, will return only the package ids going to the same location as any of those in the first array.
    :return: The array of ids to fill up the first array with.
    """
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
    """
    Fills up the given first array package ids with package ids from
    the second array based on the the package requirements. If the
    length of the first array still doesn't reach the given amount, it
    will add non-significant (no similarity in locations) ids from
    the second array.

    However, instead of filling up the first array, it returns the array
    of ids that will fill up the first array. The second array is still
    modified to not include the ids removed from it.

    Space: O(n) Time: O(n)

    :param first_arr: The array of package ids to fill up to.
    :param second_arr: The array of package ids to fill up from.
    :param packages_with_same_package_req: The list of package ids that belong together based on their package requirements.
    :return: The array of ids to fill up the first array with.
    """
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
