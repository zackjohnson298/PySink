from PySink import AsyncWorker, AsyncWorkerResults
import time


class DemoAsyncWorker2Results(AsyncWorkerResults):
    custom_result_1 = None
    custom_result_2 = None


class DemoAsyncWorker2(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        # Initialize AsyncWorker, passing in the custom result type
        super(DemoAsyncWorker2, self).__init__(result_type=DemoAsyncWorker2Results)
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        progress = 5
        self.update_progress(progress, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += 90 / self.cycles
            self.update_progress(progress, f'Progress message #{ii + 1}')

        # With a custom result type, you can store your data directly into the self.results attribute. In this case,
        #   there is no need to pass any kwargs into self.complete
        self.result.custom_result_1 = 12
        self.result.custom_result_2 = 100
        self.complete()

        # Result values can be passed to self.complete() as kwargs. However, each key MUST be defined as an attribute
        #   of the custom return type, else an AttributeError will be raised
        # self.complete(custom_result_1=12, custom_result_2=100)
