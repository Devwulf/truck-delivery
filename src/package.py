import re
import src.timeutil as timeutil
from enum import IntEnum
import src.data as data

num_arr_regex = "^((\d*, ?)*(\d+)|\[(\d*, ?)*(\d+)\])$"

class DeliveryStatus(IntEnum):
    NotDelivered = 0
    EnRoute = 1
    Delivered = 2
    DeliveredLate = 3

class Package:
    def __init__(self, package_id, address_id, delivery_time, has_truck_req, truck_req, is_delayed, delay_time, has_package_req, package_req, mass, delivery_status):
        self.package_id = package_id
        self.address_id = address_id
        self.delivery_time = delivery_time
        self.has_truck_req = has_truck_req
        self.truck_req = truck_req
        self.is_delayed = is_delayed
        self.delay_time = delay_time
        self.has_package_req = has_package_req
        self.package_req = package_req
        self.mass = mass
        self.delivery_status = delivery_status
        self.delivered_at = 0

    def _get_package_id(self):
        """
        :return: The id of this package.
        """
        return self._package_id

    def _set_package_id(self, value):
        """
        :param value: The id that the package id should be set to. Can be an integer string.
        :return: N/A
        """
        val = int(value)
        if val < 0:
            raise ValueError("Id cannot be a negative value!")
        self._package_id = val

    def _get_address_id(self):
        """
        :return: The id of the address that this package is to be delivered to.
        """
        return self._address_id

    def _set_address_id(self, value):
        """
        :param value: The id of the address that this package should be delivered to. Can be an integer string.
        :return: N/A
        """
        val = int(value)
        if val < 0:
            raise ValueError("Address Id cannot be a negative value!")
        self._address_id = val

    def _get_is_timed(self):
        """
        :return: True if the package delivery time is below 86399 seconds (11:59:59 PM), False otherwise.
        """
        return self.delivery_time < 86399.0

    def _get_delivery_time(self):
        """
        :return: The time that this package is supposed to be delivered by.
        """
        return self._delivery_time

    def _set_delivery_time(self, value):
        """
        :param value: The time as a readable string. Has to be of the format HH:MM(:SS) [AM/PM] or set to EOD, which will be set to 11:59:59 PM.
        :return: N/A
        """
        val = "11:59:59 PM" if value == "EOD" else value
        self._delivery_time = timeutil.to_seconds(val)

    def _get_has_truck_req(self):
        """
        :return: True if the package has any truck requirements (e.g. should be delivered by truck 2), False otherwise.
        """
        return self._has_truck_req

    def _set_has_truck_req(self, value):
        """
        :param value: The boolean value to be set to has_truck_req. Has to be either 0 or 1. Can be an integer string.
        :return: N/A
        """
        int_val = int(value)
        val = True if int_val == 1 else False
        self._has_truck_req = val

    def _get_truck_req(self):
        """
        :return: The id of the truck that this package should be in.
        """
        return self._truck_req

    def _set_truck_req(self, value):
        """
        :param value: The id of the truck that this package should be in.
        :return: N/A
        """
        val = int(value)
        self._truck_req = val

    def _get_is_delayed(self):
        """
        :return: True if the package is delayed, False otherwise
        """
        return self._is_delayed

    def _set_is_delayed(self, value):
        """
        :param value: The boolean value to be set to is_delayed. Has to be either 0 or 1. Can be an integer string.
        :return: N/A
        """
        int_val = int(value)
        val = True if int_val == 1 else False
        self._is_delayed = val

    def _get_delay_time(self):
        """
        :return: The time, in seconds, that this delayed package will arrive at the warehouse.
        """
        return self._delay_time

    def _set_delay_time(self, value):
        """
        :param value: The time as a readable string. Has to be of the format HH:MM(:SS) [AM/PM] or set to -1, which will be set to 11:59:59 PM.
        :return: N/A
        """
        val = "11:59:59 PM" if value == "-1" else value
        self._delay_time = timeutil.to_seconds(val)

    def _get_has_package_req(self):
        """
        :return: True if the package has to be with other packages when being delivered, False otherwise.
        """
        return self._has_package_req

    def _set_has_package_req(self, value):
        """
        :param value: The boolean value to be set to has_package_req. Has to be either 0 or 1. Can be an integer string.
        :return: N/A
        """
        int_val = int(value)
        val = True if int_val == 1 else False
        self._has_package_req = val

    def _get_package_req(self):
        """
        :return: An array of the package ids that this package should be delivered with.
        """
        return self._package_req

    def _set_package_req(self, value):
        """
        :param value: An array, in string form, of package ids that this package should be delivered with. Examples of the different formats are: "13, 19" or "[13, 19]".
        :return: N/A
        """
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

    def _get_mass(self):
        """
        :return: The mass, in kilograms, of the package.
        """
        return self._mass

    def _set_mass(self, value):
        """
        :param value: The mass, in kilograms, that this package should be set to.
        :return: N/A
        """
        self._mass = int(value)

    def _get_delivery_status(self):
        """
        :return: The current delivery status of this package, as represented by the DeliveryStatus enum.
        """
        return self._delivery_status

    def _set_delivery_status(self, value):
        """
        :param value: The delivery status that this package should be set to.
        :return: N/A
        """
        self._delivery_status = DeliveryStatus(int(value))

    package_id = property(_get_package_id, _set_package_id)
    address_id = property(_get_address_id, _set_address_id)
    is_timed = property(_get_is_timed)
    delivery_time = property(_get_delivery_time, _set_delivery_time)
    has_truck_req = property(_get_has_truck_req, _set_has_truck_req)
    truck_req = property(_get_truck_req, _set_truck_req)
    is_delayed = property(_get_is_delayed, _set_is_delayed)
    delay_time = property(_get_delay_time, _set_delay_time)
    has_package_req = property(_get_has_package_req, _set_has_package_req)
    package_req = property(_get_package_req, _set_package_req)
    mass = property(_get_mass, _set_mass)
    delivery_status = property(_get_delivery_status, _set_delivery_status)

    def __repr__(self):
        return str(self.package_id)

    def __str__(self):
        message = ""
        message += "Package %s\n" % self.package_id

        location = data.Data().get_location(self.address_id)
        message += "\tAddress: %s, %s, %s %s\n\tDelivery Time: %s\n\tMass: %s kg\n\tDelivery Status: %s (%s)" % (location.address, location.city, location.state, location.zip_code, timeutil.to_time(self.delivery_time), self.mass, DeliveryStatus(self.delivery_status).name, timeutil.to_time(self.delivered_at))
        if self.has_truck_req == True:
            message += "\n\tTruck Req: %s" % self.truck_req
        if self.is_delayed == True:
            message += "\n\tDelay Time: %s" % timeutil.to_time(self.delay_time)
        if self.has_package_req == True:
            message += "\n\tPackage Req: %s" % self.package_req
        message += "\n"
        return message
