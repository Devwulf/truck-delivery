class HashMap:
    def __init__(self, size):
        self.map = [None] * size

    def add(self, key, value):
        keyHash = self._get_hash(key)
        keyValuePair = [key, value]

        if self.map[keyHash] is None:
            self.map[keyHash] = keyValuePair
        else:
            raise ValueError("Can't have similar keys in the map.")

    def delete(self, key):
        keyHash = self._get_hash(key)

        if self.map[keyHash] is None:
            return None

        value = self.map[keyHash]
        self.map[keyHash] = None
        return value

    def _get_hash(self, value):
        input = str(value)
        hash = 7
        for char in input:
            hash = hash * 31 + ord(char)
        return hash % len(self.map)

    def __getitem__(self, key):
        keyHash = self._get_hash(key)

        if self.map[keyHash] is None:
            return None

        return self.map[keyHash][1]

    def __repr__(self):
        message = ""
        for i in range(0, len(self.map)):
            pair = self.map[i]
            if (pair is not None):
                message += "%s: [%s, %s]" % (i, pair[0], pair[1])
        return message