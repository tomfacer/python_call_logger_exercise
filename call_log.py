import threading

MAX_QUEUE_SIZE = 10
DEFAULT_SLEEP = 1000

class CallLog:

    def __init__(self):
        self.success_call_count = 0
        self.rejected_call_count = 0
        self.queue = []
        self.avg_call_duration = 0
        self.total_duration_all_calls = 0
        self.lock = threading.Lock() # updating queue

        self.sleep = DEFAULT_SLEEP

    def __str__(self):
        return 'success_call_count={} ' \
               'rejected_call_count={} ' \
               'queue_size={} ' \
               'avg_call_duration={} ' \
               'total_duration_all_calls={}'.format(
            self.success_call_count,
            self.rejected_call_count,
            len(self.queue),
            self.avg_call_duration,
            self.total_duration_all_calls
        )

    def print_queue(self):
        print(self.queue)

    def increment_success_call_count(self):
        self.success_call_count += 1
        self.sleep += 10

    def increment_rejected_call_count(self):
        self.rejected_call_count += 1
        self.sleep -= 50

    def add_to_queue(self, val: int):
        with self.lock:
            if len(self.queue) >= MAX_QUEUE_SIZE:
                removed_val = self.queue.pop()
                self._remove_val_from_avg(removed_val)

            self.queue.insert(0, val)
            self.total_duration_all_calls += val
            self._recalculate_avg()


    def _remove_val_from_avg(self, val: int):
        self.total_duration_all_calls -= val
        self._recalculate_avg()

    def _recalculate_avg(self):
        self.avg_call_duration = int(self.total_duration_all_calls / len(self.queue))

    # def _reset(self):
    #     with self.lock:
    #         self.queue = []
    #         self.avg_call_duration = 0
    #         self.total_duration_all_calls = 0
    #         self.sleep = DEFAULT_SLEEP