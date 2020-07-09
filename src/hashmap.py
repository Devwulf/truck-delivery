class HashMap:
    def __init__(self, size):
        self.map = [None] * size

    def _getHash(self, value):
        input = str(value)
        hash = 7
        for char in input:
            hash = hash * 31 + ord(char)
        return hash % len(self.map)

    def add(self, key, value):
        keyHash = self._getHash(key)
        keyValuePair = [key, value]

        if self.map[keyHash] is None:
            self.map[keyHash] = keyValuePair
            return True
        else:
            print("Can't have similar keys in the map")
            return False

    def get(self, key):
        keyHash = self._getHash(key)

        if self.map[keyHash] is None:
            return None

        return self.map[keyHash][1]

    def delete(self, key):
        keyHash = self._getHash(key)

        if self.map[keyHash] is None:
            return False

        self.map[keyHash] = None
        return True

    def print(self):
        for i in range(0, len(self.map)):
            pair = self.map[i]
            if (pair is not None):
                print("%s: [%s, %s]" % (i, pair[0], pair[1]))

map = HashMap(100)
map.add("Bob", "Cool Package")
map.add("Ming", "Cool Package 2")
map.add("some key", "Cool Package 3")
map.add("Min", "Cool Package 4")
map.add("Ankit", "Cool Package 4")
map.add("Aditya", "Cool Package 4")
map.add("Alicia", "Cool Package 4")
map.add("Mike", "Cool Package 4")

map.print()