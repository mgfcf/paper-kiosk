from datetime import datetime, timedelta
import logging

min_sleep_minutes = 0
max_history_entries = 25


class Looper(object):
    """Manages loop times and sleeps until next loop."""

    def __init__(self, loop_interval, run_on_hour=False, max_loop_count=0):
        self.interval = int(str(loop_interval))
        self.on_hour = run_on_hour
        self.loop_history = []
        self.loop_count = 0
        self.max_loop_count = int(str(max_loop_count))

    def begin_loop(self):
        begin_time = datetime.now()
        logging.info("\n__________Starting new loop [" + str(self.loop_count) + "]__________")
        logging.info("Datetime: " + str(begin_time) + "\n")
        self.__add_beginning__(begin_time)

    def __add_beginning__(self, time):
        self.loop_history.append((time,))

        if len(self.loop_history) > max_history_entries:
            dif = len(self.loop_history) - max_history_entries
            self.loop_history = self.loop_history[dif:]

    def __add_ending__(self, time):
        current = self.get_current()
        self.loop_history[-1] = (current[0], time)

    def end_loop(self):
        end_time = datetime.now()
        self.__add_ending__(end_time)

        self.loop_count += 1
        while self.loop_count > 86400:
            self.loop_count -= 86400

    def was_last_loop(self):
        if self.max_loop_count == 0:
            return False
        return self.max_loop_count <= self.loop_count

    def get_current(self):
        return self.loop_history[-1]

    def time_until_next(self):
        interval_duration = timedelta(minutes=self.interval)
        loop_duration = self.get_last_duration()
        sleep_time = interval_duration - loop_duration
        if self.on_hour:
            time_until_hour = self.get_time_to_next_hour()
            if time_until_hour < sleep_time:
                return time_until_hour

        if sleep_time < timedelta(0):
            sleep_time = timedelta(0, 0, 0, 0, min_sleep_minutes)
        return sleep_time

    def get_last_duration(self):
        if len(self.loop_history) == 0:
            return
        begin, end = self.loop_history[-1]
        return end - begin

    def get_time_to_next_hour(self):
        cur = datetime.now()
        rounded = datetime(cur.year, cur.month, cur.day, cur.hour)
        next_hour_time = rounded + timedelta(hours=1)
        return next_hour_time - datetime.now()

    def is_new_hour_loop(self):
        if len(self.loop_history) < 2:
            return False
        previous_loop = self.loop_history[-2]
        current_loop = self.get_current()

        if previous_loop[0].hour != current_loop[0].hour:
            return True
        else:
            return False
