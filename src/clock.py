from src.event import Event
import threading
import src.timeutil as timeutil
from src.borg import Borg

class Clock(Borg):
    def __init__(self, initialize=False):
        Borg.__init__(self)
        if initialize:
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

        try:
            start = timeutil.to_seconds(start_time)
            end = timeutil.to_seconds(end_time)

            self.start_time = start
            self.current_time = start
            self.end_time = end
            self.interval_secs = interval_secs
            self.time_delta = time_delta
            self.timer = threading.Timer(interval_secs, self._tick)
            self.timer.start()
        except ValueError as e:
            print(e)

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