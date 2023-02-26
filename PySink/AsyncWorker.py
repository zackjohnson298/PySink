from PySide6.QtCore import QObject, Signal
import time


class AsyncWorker(QObject):
    finished_signal = Signal(dict)
    progress_signal = Signal(int, str)

    def __init__(self):
        super(AsyncWorker, self).__init__()
        self.errors: list = []
        self.warnings: list = []
        self.cancelled: bool = False

    def cancel(self) -> None:
        self.errors.append('Cancelled')
        self.warnings.append('Cancelled')
        self.cancelled = True
        self.complete()

    def run(self) -> None:
        time.sleep(5)
        self.complete()

    def reset(self) -> None:
        self.errors = []
        self.warnings = []
        self.cancelled = False

    def update_progress(self, progress: int, message=None) -> None:
        self.progress_signal.emit(progress, message)

    def complete(self, **kwargs) -> None:
        results = {'warnings': self.warnings, 'errors': self.errors}
        if not self.cancelled:
            results = {**results, **kwargs}
        self.finished_signal.emit(results)
