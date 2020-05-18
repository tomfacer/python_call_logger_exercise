import time


class Timer:
    def __init__(self):
        self.timer = time.time_ns()

    def get_elapsed_in_nanos(self):
        return time.time_ns() - self.timer

    def get_elapsed_in_millis(self):
        return int(self.get_elapsed_in_nanos() / 1000000)