from PySide6.QtCore import QThread, Signal, QObject
from PySink.AsyncWorker import AsyncWorker


class AsyncManager(QObject):
    worker_finished_signal = Signal(dict)
    worker_progress_signal = Signal(int, str)

    def __init__(self):
        super(AsyncManager, self).__init__()
        self.worker = AsyncWorker()
        self.thread = QThread()

    def cancel(self):
        self.worker.cancel()
        if self.thread.isRunning():
            self.thread.quit()
            # self.thread.wait()

    def start_worker(self, worker: AsyncWorker):
        self.thread = QThread()
        self.worker = worker
        self.worker.reset()
        self.worker.progress_signal.connect(self.worker_progress_signal.emit)
        self.worker.finished_signal.connect(self.worker_finished_signal.emit)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished_signal.connect(self.thread.quit)
        self.worker.finished_signal.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
