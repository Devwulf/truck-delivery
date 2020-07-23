from src.borg import Borg
from src.data import Data
from src.hashmap import HashMap
from typing import List

class Warehouse(Borg):
    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
            hashmap:HashMap = Data().get_packages()
            self.__packages:List[int] = sorted(hashmap.keys())

    def __get_packages(self):
        """
        :return: The list of package ids currently in this warehouse.
        """
        return self.__packages

    def __set_packages(self, value):
        """
        :param value: The list of packages to set the warehouse packages to.
        :return: N/A
        """
        self.__packages = value

    packages = property(__get_packages, __set_packages)
