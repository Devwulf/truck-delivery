# Mark Christian Malabanan, Student ID #001233960

from datetime import datetime
from time import gmtime
from time import strftime
import re

time_regex = "^([1-9]|0[1-9]|1[0-2])[:]([0-5][0-9])[:]([0-5][0-9])[ ]([AP]M)$"
time_no_secs_regex = "^([1-9]|0[1-9]|1[0-2])[:]([0-5][0-9])[ ]([AP]M)$"

def to_time(seconds:int) -> str:
    """
    Converts the given time in seconds to a human-readable time string
    of the format `HH:MM:SS [AM/PM]`

    Space: O(1) Time: O(1)

    :param seconds: The seconds of the day that will be converted to a time string.
    :return: The human-readable time string based on the given seconds.
    """
    secs = int(seconds)
    return strftime("%I:%M:%S %p", gmtime(seconds))

def to_seconds(time:str) -> int:
    """
    Converts the given human-readable time of the format `HH:MM(:SS) [AM/PM]`
    to the amount of seconds since 12:00 AM of the same day.

    Space: O(1) Time: O(1)

    :param time: The time string that will be converted to seconds.
    :return: The total amount of seconds based on the given time string.
    """
    value = time
    match = re.match(time_no_secs_regex, value)
    if match is not None:
        value = value.replace(" ", ":00 ")
    match = re.match(time_regex, value)
    if match is None:
        raise ValueError("The given time of '%s' does not match the time format! Time should be formatted as: hh:mm:ss (AM/PM)" % value)
    return int((datetime.strptime(value, "%I:%M:%S %p") - datetime.strptime("12:00:00 AM", "%I:%M:%S %p")).total_seconds())