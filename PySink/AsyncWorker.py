from PySide6.QtCore import QRunnable, Signal, QObject, Slot, QMutex
import time
import uuid


class AsyncWorkerSignals(QObject):
    started = Signal()
    progress = Signal(int, str)
    finished = Signal(dict)


class AsyncWorker(QRunnable):
    # finished_signal = Signal(dict)
    # progress_signal = Signal(int, str)

    def __init__(self, identifier=None):
        super(AsyncWorker, self).__init__()
        self.errors: list = []
        self.warnings: list = []
        self.cancelled: bool = False
        self.id = identifier if identifier is not None else str(uuid.uuid4())
        self.signals = AsyncWorkerSignals()

    def cancel(self) -> None:
        self.errors.append('Cancelled')
        self.warnings.append('Cancelled')
        self.cancelled = True
        self.signals.finished.emit(self.get_default_results())

    @Slot()
    def run(self) -> None:
        time.sleep(5)
        self.complete()

    def reset(self) -> None:
        self.errors = []
        self.warnings = []
        self.cancelled = False

    def update_progress(self, progress: int, message=None) -> None:
        if not self.cancelled:
            self.signals.progress.emit(progress, message)

    def get_default_results(self):
        return {'warnings': self.warnings, 'errors': self.errors, 'id': self.id}

    def complete(self, **kwargs) -> None:
        if not self.cancelled:
            results = {**self.get_default_results(), **kwargs}
            self.signals.finished.emit(results)
