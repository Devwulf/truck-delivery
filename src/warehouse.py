# Mark Christian Malabanan, Student ID #001233960

from src.borg import Borg
from src.data import Data
from src.hashmap import HashMap
from typing import List

class Warehouse(Borg):
    def __init__(self, initialize=False):
        """
        Space: O(n^2) Time: O(n^2)

        :param initialize: If True, this singleton should be initialized.
        """
        Borg.__init__(self)
        if initialize:
            hashmap:HashMap = Data().get_packages()
            self.__packages:List[int] = sorted(hashmap.keys())

    def __get_packages(self):
        """
        Space: O(n) Time: O(1)

        :return: The list of package ids currently in this warehouse.
        """
        return self.__packages

    def __set_packages(self, value):
        """
        Space: O(n) Time: O(1)

        :param value: The list of packages to set the warehouse packages to.
        :return: N/A
        """
        self.__packages = value

    packages = property(__get_packages, __set_packages)
