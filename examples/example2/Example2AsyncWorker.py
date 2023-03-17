from PySink import AsyncWorker, AsyncWorkerResults
import time


class CustomAsyncWorkerResults(AsyncWorkerResults):
    custom_result_1 = None
    custom_result_2 = None


class Example2AsyncWorker(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        # Initialize AsyncWorker, passing in the custom result type
        super(Example2AsyncWorker, self).__init__(result_type=CustomAsyncWorkerResults)
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        progress = 0
        progress_increment = 100 / self.cycles
        self.update_progress(0, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += progress_increment
            self.update_progress(progress, f'Progress message #{ii + 1}')
        # With a custom result type, you can store your data directly
        #   into the self.results attribute
        self.result.custom_result_1 = 12
        self.result.custom_result_2 = 100
        # When returning customer result types, there is no need to pass
        #   any kwargs into self.complete
        self.complete()
