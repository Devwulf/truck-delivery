# A constant length array, where remove simply sets the value to none
# search: O(n), access: O(1), remove: O(1), add: N/A, insert: O(1)
class ConstantArray:
    def __init__(self, size):
        """
        Space: O(n) Time: O(1)

        :param size: The max size that this list has.
        """
        self._array = [None] * size
        self.max_size = size
        self._size = 0
        self._counter = 0
        self._popleft_counter = 0

    def pop(self, index):
        """
        Removes and returns the item at the given index.

        Space: O(1) Time: O(1)

        :param index: The index of the value to remove and return from the list.
        :return: The value removed from the list.
        """
        item = self.__getitem__(index)
        self.__delitem__(index)
        return item

    def popleft(self):
        """
        Removes and returns the leftmost item in the list.

        Space: O(1) Time: O(n)

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

        Space: O(1) Time: O(1)

        :return: The leftmost item in the list.
        """
        return self.__getitem__(self._popleft_counter)

    def append(self, item):
        """
        Adds the item to the rightmost part of the list, regardless of if there are spaces in the list.

        Space: O(1) Time: O(1)

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
        Space: O(1) Time: O(1)

        :return: The current size of the list based on how many valid items are in it.
        """
        return self.max_size - self._size

    def __getitem__(self, index):
        """
        Space: O(1) Time: O(1)

        :param index: The index of the value to return.
        :return: The value to be returned.
        """
        return self._array[index]

    def __setitem__(self, index, value):
        """
        Space: O(1) Time: O(1)

        :param index: The index where the value should be stored.
        :param value: The value to be stored.
        :return: N/A
        """
        if value is None:
            raise ValueError("Cannot set the value None at index '%s'. Use this instead: del array[key]." % index)
        self._array[index] = value
        self._size += 1

    def __delitem__(self, index):
        """
        Space: O(1) Time: O(1)

        :param index: The index of the value to be deleted.
        :return: N/A
        """
        self._array[index] = None
        self._size -= 1

    def __len__(self):
        """
        Space: O(1) Time: O(1)

        :return: The amount of valid items in the list.
        """
        return self._size

    def __iter__(self):
        """
        Space: O(1) Time: O(1)

        :return: The iterator of the internal list.
        """
        return self._array.__iter__()