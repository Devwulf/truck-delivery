# A constant length array, where remove simply sets the value to none
# search: O(n), access: O(1), remove: O(1), add: N/A, insert: O(1)
class ConstantArray:
    def __init__(self, size):
        self._array = [None] * size
        self.max_size = size
        self._size = 0
        self._counter = 0
        self._popleft_counter = 0

    def pop(self, index):
        """
        :param index: The index of the value to remove and return from the list.
        :return: The value removed from the list.
        """
        item = self.__getitem__(index)
        self.__delitem__(index)
        return item

    def popleft(self):
        """
        Removes and returns the leftmost item in the list.

        :return: The leftmost item in the list.
        """
        while self.__getitem__(self._popleft_counter) is None and self._popleft_counter < self.max_size:
            self._popleft_counter += 1
        item = self.__getitem__(self._popleft_counter)
        if item is None:
            return
        self.__delitem__(self._popleft_counter)
        self._popleft_counter += 1
        return item

    def peekleft(self):
        """
        Returns the leftmost item in the list without removing it from the list.

        :return: The leftmost item in the list.
        """
        return self.__getitem__(self._popleft_counter)

    def append(self, item):
        """
        Adds the item to the rightmost part of the list, regardless of if there are spaces in the list.

        :param item: The item to be added to the list.
        :return: N/A
        """
        if item is None:
            raise ValueError("Cannot set the value None at index '%s'. Use this instead: del array[key]." % self._size)
        if self._size >= self.max_size:
            raise ValueError("Array is full, cannot add any more values.")
        self._array[self._size] = item
        self._size += 1

    def space_left(self):
        """
        :return: The current size of the list based on how many valid items are in it.
        """
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