from PySink import CancellableAsyncWorker
import time


class CustomWorker2(CancellableAsyncWorker):
    def __init__(self, delay_seconds, cycles=5):
        super(CustomWorker2, self).__init__()
        self.count = cycles
        self.delay_seconds = delay_seconds

    def run(self):
        self.emit_start()
        progress = 5
        self.update_progress(progress)
        for ii in range(self.count):
            # Since this worker is cancellable, it is good practice to check the self.cancelled flag periodically and
            #   return if it is True
            if self.cancelled:
                return
            time.sleep(self.delay_seconds)
            progress += int(90 / self.count)
            self.update_progress(progress)
        self.complete()
