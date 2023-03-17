from PySink import AsyncWorker
import time


class DemoAsyncWorker1(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        super(DemoAsyncWorker1, self).__init__()
        # Store the values passed in during initialization
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        # Update discrete progress by providing a progress value from 0-100 with an optional message
        progress = 5
        self.update_progress(progress, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += 90 / self.cycles
            self.update_progress(progress, f'Progress message #{ii + 1}')
        # Call the self.complete method to end your task, passing any results as keyword arguments
        demo_result = 12
        self.complete(demo_result=demo_result)
