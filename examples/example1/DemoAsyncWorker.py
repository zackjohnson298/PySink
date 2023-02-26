from PySink import AsyncWorker
import time


class DemoAsyncWorker(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        super(DemoAsyncWorker, self).__init__()
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        progress = 0
        progress_increment = 100 / self.cycles
        # Update progress by providing a progress value from 0-10 with an
        #   optional message
        self.update_progress(0, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += progress_increment
            self.update_progress(progress, f'Progress message #{ii + 1}')
        # Call the self.complete method to end your task, passing any
        #   results as keyword arguments
        demo_result = 12
        self.complete(demo_result=demo_result)
