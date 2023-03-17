from PySink import AsyncWorker


class CancellableAsyncWorker(AsyncWorker):
    def __init__(self, *args, **kwargs):
        super(CancellableAsyncWorker, self).__init__(*args, **kwargs)
        self.cancelled: bool = False

    def cancel(self) -> None:
        self.errors.append('Cancelled')
        self.warnings.append('Cancelled')
        self.cancelled = True
        self.signals.finished.emit(self.get_default_results())

    def reset(self):
        self.cancelled = False
        super().reset()

    def update_progress(self, progress_value: int, message=None) -> None:
        if not self.cancelled:
            super().update_progress(progress_value, message)

    def emit_start(self):
        if not self.cancelled:
            super().emit_start()

    def complete(self, **kwargs) -> None:
        if not self.cancelled:
            super().complete(**kwargs)
