import re
import textwrap

state_regex = "^([A-Z][A-Z])$"
class Location:
    def __init__(self, location_id, name, address, city, state, zip_code):
        """
        Space: O(1) Time: O(1)

        :param location_id: The location id of this location.
        :param name: The name of this location.
        :param address: The address associated with this location.
        :param city: The city this location is in.
        :param state: The state this location is in.
        :param zip_code: The zip code where this location is in.
        """
        self.location_id = location_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def _get_location_id(self):
        """
        Space: O(1) Time: O(1)

        :return: The id associated with this location.
        """
        return self._location_id

    def _set_location_id(self, value):
        """
        Space: O(1) Time: O(1)

        :param value: The id to assign to this location. Can be an integer string.
        :return: N/A
        """
        val = int(value)
        if (val < 0):
            raise ValueError("The given location id cannot be a negative number")
        self._location_id = val

    def _get_name(self):
        """
        Space: O(1) Time: O(1)

        :return: The name of this location.
        """
        return self._name

    def _set_name(self, value):
        """
        Space: O(1) Time: O(1)

        :param value: The name to assign to this location.
        :return: N/A
        """
        self._name = value

    def _get_address(self):
        """
        Space: O(1) Time: O(1)

        :return: The address of this location.
        """
        return self._address

    def _set_address(self, value):
        """
        Space: O(1) Time: O(1)

        :param value: The address to assign to this location.
        :return: N/A
        """
        self._address = value

    def _get_city(self):
        """
        Space: O(1) Time: O(1)

        :return: The city that this location is in.
        """
        return self._city

    def _set_city(self, value):
        """
        Space: O(1) Time: O(1)

        :param value: The city to assign to this location
        :return: N/A
        """
        self._city = value

    def _get_state(self):
        """
        Space: O(1) Time: O(1)

        :return: The state that this location is in.
        """
        return self._state

    def _set_state(self, value):
        """
        Space: O(1) Time: O(1)

        :param value: The state to assign to this location. Must be two capital letters (e.g. UT)
        :return: N/A
        """
        match = re.search(state_regex, value)
        if match is None:
            raise ValueError("The given state value is invalid: %s\nUse only two capital letters for states." % value)
        self._state = value

    def _get_zip_code(self):
        """
        Space: O(1) Time: O(1)

        :return: The zip code of this location.
        """
        return self._zip_code

    def _set_zip_code(self, value):
        """
        Space: O(1) Time: O(1)

        :param value: The zip code to assign to this location. Can be an integer string.
        :return: N/A
        """
        val = int(value)
        self._zip_code = val

    location_id = property(_get_location_id, _set_location_id)
    name = property(_get_name, _set_name)
    address = property(_get_address, _set_address)
    city = property(_get_city, _set_city)
    state = property(_get_state, _set_state)
    zip_code = property(_get_zip_code, _set_zip_code)