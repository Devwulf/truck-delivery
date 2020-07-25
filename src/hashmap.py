from typing import List
import math

class HashMap:
    def __init__(self, size):
        """
        Space: O(n^2) Time: O(n)

        :param size: The max size of this hashmap.
        """
        size = math.ceil(size * 1.5)
        self.__map:List[List[KeyValuePair]] = [[] for i in range(size)]
        self.__size = 0
        self.__max_size = size

    def append(self, key, value):
        """
        Appends the given key and value pair to the hashmap by hashing
        the given key. If new keys have the same hash key as the older
        ones, they are both placed in the same array under the hash key.

        Space: O(n) Time: O(n)

        :param key: The key used to identify the value.
        :param value: The value of the given key.
        :return: N/A
        """
        key_hash = self.__get_hash(key)
        pair = KeyValuePair(key, value)

        for kv in self.__map[key_hash]:
            if kv.key == key:
                raise ValueError("Can't have similar keys in the map: %s (similar to %s)" % (pair, kv))
        self.__map[key_hash].append(pair)
        self.__size += 1

    def pop(self, key):
        """
        Removes the key-value pair from the map and returns the value.

        Space: O(n) Time: O(n)

        :param key: The key of the value to be removed and returned.
        :return: The value removed from the map.
        """
        key_hash = self.__get_hash(key)

        for i, kv in enumerate(self.__map[key_hash]):
            if kv.key == key:
                self.__size -= 1
                return self.__map[key_hash].pop(i)
        return None

    def to_array(self):
        """
        Creates and returns an array of the key-value pairs in this
        map.

        Space: O(n^2) Time: O(n^2)

        :return: An array of the key-value pairs in this map.
        """
        result = []
        for kv_arr in self.__map:
            for kv in kv_arr:
                result.append(kv)
        return result

    def keys(self):
        """
        Creates and returns an array of only the keys in this map.

        Space: O(n^2) Time: O(n^2)

        :return: An array of only the keys in this map.
        """
        result = []
        for kv_arr in self.__map:
            for kv in kv_arr:
                result.append(kv.key)
        return result

    def values(self):
        """
        Creates and returns an array of only the values in this map.

        Space: O(n^2) Time: O(n^2)

        :return: An array of only the values in this map.
        """
        result = []
        for kv_arr in self.__map:
            for kv in kv_arr:
                result.append(kv.value)
        return result

    def __get_hash(self, key):
        """
        Hashes the key to (hopefully) create a unique enough index
        to store the key-value pair into.

        Space: O(n) Time: O(n)

        :param key: The key to be hashed.
        :return: The hashed key.
        """
        input = str(key)
        hash = 7
        for char in input:
            hash = hash * 31 + ord(char)
        return int(hash % self.__max_size)

    def __getitem__(self, key):
        """
        Looks up a key in the map and returns the value associated to it.

        Space: O(n) Time: O(n)

        :param key: The key of the value to be looked up.
        :return: The value looked up in map.
        """
        key_hash = self.__get_hash(key)

        for kv in self.__map[key_hash]:
            if kv.key == key:
                return kv.value
        return None

    def __delitem__(self, key):
        """
        Space: O(n) Time: O(n)

        :param key: The key of the value to be removed from the map.
        :return: N/A
        """
        self.pop(key)

    def __len__(self):
        """
        Space: O(1) Time: O(1)

        :return: The amount of the key-value pairs in this map.
        """
        return self.__size

    def __iter__(self):
        """
        Space: O(1) Time: O(1)

        :return: The iterator of the map itself.
        """
        return self.__map.__iter__()

class KeyValuePair:
    def __init__(self, key, value):
        """
        Space: O(1) Time: O(1)

        :param key: The key in this pair.
        :param value: The value in this pair.
        """
        self.key = key
        self.value = value