import re
from datetime import datetime
import src.timeutil as timeutil

num_arr_regex = "^((\d*, ?)*(\d+)|\[(\d*, ?)*(\d+)\])$"

class Package:
    def __init__(self, package_id, address_id, delivery_time, has_truck_req, truck_req, is_delayed, delay_time, has_package_req, package_req):
        self.package_id = package_id
        self.address_id = address_id
        self.delivery_time = delivery_time
        self.has_truck_req = has_truck_req
        self.truck_req = truck_req
        self.is_delayed = is_delayed
        self.delay_time = delay_time
        self.has_package_req = has_package_req
        self.package_req = package_req

    def _get_package_id(self):
        return self._package_id

    def _set_package_id(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Id cannot be a negative value!")
        self._package_id = val

    def _get_address_id(self):
        return self._address_id

    def _set_address_id(self, value):
        val = int(value)
        if val < 0:
            raise ValueError("Address Id cannot be a negative value!")
        self._address_id = val

    def _get_delivery_time(self, is_seconds=False):
        if is_seconds:
            return self._delivery_time
        return timeutil.to_time(self._delivery_time)

    def _set_delivery_time(self, value):
        val = "11:59:59 PM" if value == "EOD" else value
        self._delivery_time = timeutil.to_seconds(val)

    def _get_has_truck_req(self):
        return self._has_truck_req

    def _set_has_truck_req(self, value):
        val = True if value == "1" else False
        self._has_truck_req = val

    def _get_truck_req(self):
        return self._truck_req

    def _set_truck_req(self, value):
        val = int(value)
        self._truck_req = val

    def _get_is_delayed(self):
        return self._is_delayed

    def _set_is_delayed(self, value):
        val = True if value == "1" else False
        self._is_delayed = val

    def _get_delay_time(self, is_seconds=False):
        if is_seconds:
            return self._delivery_time
        return timeutil.to_time(self._delay_time)

    def _set_delay_time(self, value):
        val = "11:59:59 PM" if value == "-1" else value
        self._delay_time = timeutil.to_seconds(val)

    def _get_has_package_req(self):
        return self._has_package_req

    def _set_has_package_req(self, value):
        val = True if value == "1" else False
        self._has_package_req = val

    def _get_package_req(self):
        return self._package_req

    # Example of expected value: "13, 19", "[13, 19]"
    def _set_package_req(self, value):
        match = re.search(num_arr_regex, value)
        val = value
        if match is None:
            if value == "-1":
                val = "[]"
            else:
                raise ValueError("The given value has to be an array of numbers, like so: 13, 19 or [13, 19]")
        if val[0] == '[':
            no_brackets = val[1:len(val) - 1]
        else:
            no_brackets = val
        no_spaces = no_brackets.replace(' ', '')
        num_arr = [] if len(no_spaces) <= 0 else [int(s) for s in no_spaces.split(',')]
        self._package_req = num_arr

    package_id = property(_get_package_id, _set_package_id)
    address_id = property(_get_address_id, _set_address_id)
    delivery_time = property(_get_delivery_time, _set_delivery_time)
    has_truck_req = property(_get_has_truck_req, _set_has_truck_req)
    truck_req = property(_get_truck_req, _set_truck_req)
    is_delayed = property(_get_is_delayed, _set_is_delayed)
    delay_time = property(_get_delay_time, _set_delay_time)
    has_package_req = property(_get_has_package_req, _set_has_package_req)
    package_req = property(_get_package_req, _set_package_req)

    def __repr__(self):
        message = ""
        message += "Package %s" % self.package_id
        message += "\tAddress Id: %s\n\tDelivery Time: %s" % (self.address_id, self.delivery_time)
        if self.has_truck_req == True:
            message += "\tTruck Req: %s" % self.truck_req
        if self.is_delayed == True:
            message += "\tDelay Time: %s" % self.delay_time
        if self.has_package_req == True:
            message += "\tPackage Req: %s" % self.package_req
        message += "\n"
        return message
