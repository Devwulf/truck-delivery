# A constant length array, where remove simply sets the value to none
# search: O(n), access: O(1), remove: O(1), add: N/A, insert: O(1)
class ConstantArray:
    def __init__(self, size):
        self._array = [None] * size
        self.max_size = size
        self._size = 0
        self._counter = 0
        self._popleft_counter = 0

    def pop(self, key):
        item = self.__getitem__(key)
        self.__delitem__(key)
        return item

    def popleft(self):
        while self.__getitem__(self._popleft_counter) is None and self._popleft_counter < self.max_size:
            self._popleft_counter += 1
        item = self.__getitem__(self._popleft_counter)
        if item is None:
            return
        self.__delitem__(self._popleft_counter)
        self._popleft_counter += 1
        return item

    def peekleft(self):
        return self.__getitem__(self._popleft_counter)

    def append(self, item):
        if item is None:
            raise ValueError("Cannot set the value None at index '%s'. Use this instead: del array[key]." % self._size)
        if self._size >= self.max_size:
            raise ValueError("Array is full, cannot add any more values.")
        self._array[self._size] = item
        self._size += 1

    def space_left(self):
        return self.max_size - self._size

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