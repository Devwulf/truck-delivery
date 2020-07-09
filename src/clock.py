import re
from datetime import datetime
from event import Event
import threading

time_regex = "^([1-9]|0[1-9]|1[0-2])[:]([0-5][0-9])[ ]([AP]M)$"

class Clock:
    def __init__(self):
        self.onTick = Event()
        self.start_time = 0
        self.current_time = 0
        self.end_time = 0
        self.interval_secs = 0
        self.time_delta = 0
        self.timer = None

    def start(self, start_time, end_time, interval_secs, time_delta):
        if self.timer is not None:
            return
        start_match = re.match(time_regex, start_time)
        end_match = re.match(time_regex, end_time)
        if start_match is None or end_match is None:
            raise ValueError("Either the start_time or end_time does not match the time format! Time should be formatted as: hh:mm (AM/PM)")

        start = self._since_midnight_in_minutes(start_time)
        end = self._since_midnight_in_minutes(end_time)

        self.start_time = start
        self.current_time = start
        self.end_time = end
        self.interval_secs = interval_secs
        self.time_delta = time_delta
        self.timer = threading.Timer(interval_secs, self._tick)
        self.timer.start()

    def stop(self):
        if self.timer is None:
            return
        self.timer.cancel()
        self.timer = None

    def _tick(self):
        self.current_time += self.time_delta
        self.onTick(self, self.current_time)
        if self.current_time >= self.end_time:
            self.stop()
            return

        self.timer = threading.Timer(self.interval_secs, self._tick)
        self.timer.start()

    @staticmethod
    def _since_midnight_in_minutes(time):
        return (datetime.strptime(time, "%I:%M %p") - datetime.strptime("12:00 AM", "%I:%M %p")).total_seconds() / 60