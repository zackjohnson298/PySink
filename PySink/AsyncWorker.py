from PySide6.QtCore import QRunnable, Signal, QObject, Slot, QMutex
from typing import Optional, Any
import time
import uuid


class AsyncWorkerResults(object):
    errors = []
    warnings = []
    id = None
    results_dict = {}


class AsyncWorkerProgress:
    value: 0
    message: None
    id: None


class AsyncWorkerSignals(QObject):
    started = Signal()
    progress = Signal(AsyncWorkerProgress)
    finished = Signal(AsyncWorkerResults)


class AsyncWorker(QRunnable):
    def __init__(self, identifier=None, result_type=AsyncWorkerResults):
        super(AsyncWorker, self).__init__()
        self.errors: list = []
        self.warnings: list = []
        self.cancelled: bool = False
        self.id = identifier if identifier is not None else str(uuid.uuid4())
        self.signals = AsyncWorkerSignals()
        self.result = result_type()
        self.result_type = result_type

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
        self.result = self.result_type()

    def update_progress(self, progress_value: int, message=None) -> None:
        if not self.cancelled:
            progress = AsyncWorkerProgress()
            progress.value = progress_value
            progress.message = message
            progress.id = self.id
            self.signals.progress.emit(progress)

    def get_default_results(self, clear=True) -> AsyncWorkerResults:
        if clear:
            self.result = self.result_type()
        self.result.errors = self.errors
        self.result.warnings = self.warnings
        self.result.id = self.id
        return self.result

    def complete(self, **kwargs) -> None:
        if self.cancelled:
            return
        self.get_default_results(clear=False)
        if self.result_type == AsyncWorkerResults:
            self.result.results_dict = kwargs
        else:
            for key in kwargs:
                getattr(self.result, key)
                setattr(self.result, key, kwargs[key])
        self.signals.finished.emit(self.result)
