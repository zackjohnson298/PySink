from PySink import AsyncWorker, AsyncWorkerResults
import time


class CustomAsyncWorkerResults(AsyncWorkerResults):
    demo_result = None


class Example3AsyncWorker(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        super(Example3AsyncWorker, self).__init__(result_type=CustomAsyncWorkerResults)
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        progress = 5
        progress_increment = 90 / self.cycles
        # Update progress by providing a progress value from 0-100 with an
        #   optional message
        self.update_progress(0, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += progress_increment
            self.update_progress(progress, f'Progress message #{ii + 1}')
        # Even with custom result types, you can still pass values in to
        #   self.complete. Be warned, if the kwarg is not an attribute
        #   of the custom result type, an AttributeError will be raised
        demo_result = 12
        self.complete(demo_result=demo_result)
