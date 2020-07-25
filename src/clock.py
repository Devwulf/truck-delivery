from src.event import Event
import threading
import src.timeutil as timeutil
from src.borg import Borg

class Clock(Borg):
    """
    Used to simulate the passing of time. Important to simulate
    trucks driving around and delivering packages.
    """
    def __init__(self, initialize=False):
        """
        Space: O(1) Time: O(1)

        :param initialize: If True, this singleton should be initialized.
        """
        Borg.__init__(self)
        if initialize:
            self.on_tick = Event()
            self.on_stop = Event()
            self.start_time = 0
            self.current_time = 0
            self.end_time = 0
            self.interval_secs = 0
            self.time_delta = 0
            self.timer = None

    def start(self, start_time, end_time, interval_secs, time_delta):
        """
        Starts the clock at the given start time, and automatically ends
        at the given end time.

        Space: O(1) Time: O(1)

        :param start_time: The time to start the clock at.
        :param end_time: The time to end the clock at.
        :param interval_secs: The interval (in seconds) that the Thread waits before ticking.
        :param time_delta: The interval of time (in seconds) that should pass for this virtual clock every tick.
        :return: N/A
        """
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
        """
        Stops the timer by canceling the current Thread.

        Space: O(1) Time: O(1)

        :return: N/A
        """
        if self.timer is None:
            return
        self.timer.cancel()
        self.timer = None

    def _tick(self):
        """
        Runs every tick of the clock. This also handles the functions
        subscribed to the on_tick event.

        Space: O(1) Time: O(1)

        :return: N/A
        """
        self.current_time += self.time_delta
        self.on_tick(self, self.current_time)
        if len(self.on_tick) <= 0 or self.current_time >= self.end_time:
            self.on_stop(self, self.current_time)
            self.stop()
            return

        self.timer = threading.Timer(self.interval_secs, self._tick)
        self.timer.start()