from PySink import AsyncWorker
import time


class DemoAsyncWorker(AsyncWorker):
    def __init__(self, count=5, delay_seconds=1.):
        super(DemoAsyncWorker, self).__init__()
        self.count = count
        self.delay_seconds = delay_seconds

    def run(self):
        if not self.cancelled:
            self.signals.started.emit()
            progress = 5
            self.update_progress(progress)
            for ii in range(self.count):
                time.sleep(self.delay_seconds)
                progress += int(90 / self.count)
                self.update_progress(progress)
            self.complete()
