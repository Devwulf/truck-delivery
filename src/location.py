import re
import textwrap

state_regex = "^([A-Z][A-Z])$"
class Location:
    def __init__(self, location_id, name, address, city, state, zip_code):
        self.location_id = location_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def _get_location_id(self):
        return self._location_id

    def _set_location_id(self, value):
        val = int(value)
        if (val < 0):
            raise ValueError("The given location id cannot be a negative number")
        self._location_id = val

    def _get_name(self):
        return self._name

    def _set_name(self, value):
        self._name = value

    def _get_address(self):
        return self._address

    def _set_address(self, value):
        self._address = value

    def _get_city(self):
        return self._city

    def _set_city(self, value):
        self._city = value

    def _get_state(self):
        return self._state

    def _set_state(self, value):
        match = re.search(state_regex, value)
        if match is None:
            raise ValueError("The given state value is invalid: %s\nUse only two capital letters for states." % value)
        self._state = value

    def _get_zip_code(self):
        return self._zip_code

    def _set_zip_code(self, value):
        val = int(value)
        self._zip_code = val

    location_id = property(_get_location_id, _set_location_id)
    name = property(_get_name, _set_name)
    address = property(_get_address, _set_address)
    city = property(_get_city, _set_city)
    state = property(_get_state, _set_state)
    zip_code = property(_get_zip_code, _set_zip_code)

    def address_to_string(self):
        return "%s\n%s, %s %s" % (self.address, self.city, self.state, self.zip_code)

    def print(self):
        print("Location %s:\n\t%s\n%s\n" % (self.location_id, self.name, textwrap.indent(self.address_to_string(), "\t")))