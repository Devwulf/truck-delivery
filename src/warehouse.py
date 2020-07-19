from src.borg import Borg
from src.data import Data
from src.hashmap import HashMap

class Warehouse(Borg):
    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
            hashmap:HashMap = Data().get_packages()
            self.__packages = sorted(hashmap.keys())

    def get_packages(self):
        return self.__packages

    def set_packages(self, value):
        self.__packages = value

    packages = property(get_packages, set_packages)
