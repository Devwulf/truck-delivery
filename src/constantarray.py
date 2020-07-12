# A constant length array, where remove simply sets the value to none
# search: O(n), access: O(1), remove: O(1), add: N/A, insert: O(1)
class ConstantArray:
    def __init__(self, size):
        self._array = [None] * size
        self.max_size = size
        self._size = 0
        self._counter = 0

    def pop(self, key):
        item = self.__getitem__(key)
        self.__delitem__(key)
        return item

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, value):
        if value is None:
            raise ValueError("Cannot set the value None at index '%s'. Use this instead: del array[key]." % key)
        self._array[key] = value
        self._size += 1

    def __delitem__(self, key):
        self._array[key] = None
        self._size -= 1

    def __len__(self):
        return self._size

    def __repr__(self):
        return self._array.__repr__()

    def __iter__(self):
        return self._array.__iter__()