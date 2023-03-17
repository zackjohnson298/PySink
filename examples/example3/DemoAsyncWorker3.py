from PySink import AsyncWorker, AsyncWorkerResults
import time


class DemoAsyncWorker3Results(AsyncWorkerResults):
    demo_result = None


class DemoAsyncWorker3(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        super(DemoAsyncWorker3, self).__init__(result_type=DemoAsyncWorker3Results)
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        progress = 5
        self.update_progress(progress, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += 90 / self.cycles
            self.update_progress(progress, f'Progress message #{ii + 1}')

        # Setting results directly
        self.result.demo_result = 12
        self.complete()

        # Passing results as kwargs
        # self.complete(demo_result=12)

