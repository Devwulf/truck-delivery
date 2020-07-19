from typing import List

class HashMap:
    def __init__(self, size):
        self.__map:List[KeyValuePair] = [None] * size
        self.__size = 0
        self.__max_size = size

    def append(self, key, value):
        key_hash = self.__get_hash(key)
        pair = KeyValuePair(key, value)

        if self.__map[key_hash] is None:
            self.__map[key_hash] = pair
            self.__size += 1
        else:
            raise ValueError("Can't have similar keys in the map: %s:%s\nSimilar to %s" % (key_hash, value, self.__map[key_hash]))

    def pop(self, key):
        keyHash = self.__get_hash(key)

        if self.__map[keyHash] is None:
            return None

        value = self.__map[keyHash]
        self.__map[keyHash] = None
        self.__size -= 1
        return value

    # Array of key-value pairs
    def to_array(self):
        result = []
        item: KeyValuePair
        for item in self.__map:
            if item is None:
                continue
            result.append(item)
        return result

    # Array of keys only
    def keys(self):
        result = []
        item: KeyValuePair
        for item in self.__map:
            if item is None:
                continue
            result.append(item.key)
        return result

    # Array of values only
    def values(self):
        result = []
        item: KeyValuePair
        for item in self.__map:
            if item is None:
                continue
            result.append(item.value)
        return result

    def __get_hash(self, value):
        input = str(value)
        hash = 7
        for char in input:
            hash = hash * 31 + ord(char)
        return int(hash % self.__max_size)

    def __getitem__(self, key):
        keyHash = self.__get_hash(key)

        if self.__map[keyHash] is None:
            return None

        return self.__map[keyHash].value

    def __delitem__(self, key):
        self.pop(key)

    def __len__(self):
        return self.__size

    def __iter__(self):
        return self.__map.__iter__()

    def __repr__(self):
        message = ""
        for i in range(0, len(self.__map)):
            pair:KeyValuePair = self.__map[i]
            if (pair is not None):
                message += "%s: [%s, %s]" % (i, pair.key, pair.value)
        return message

class KeyValuePair:
    def __init__(self, key, value):
        self.key = key
        self.value = value