from PySide6.QtCore import QThread, Signal, QObject, QThreadPool
from PySink.AsyncWorker import AsyncWorker


class AsyncManager(QObject):
    # worker_finished_signal = Signal(dict)
    # worker_progress_signal = Signal(int, str)
    all_workers_complete_signal = Signal()

    def __init__(self):
        super(AsyncManager, self).__init__()
        # self.worker = AsyncWorker()
        self.threadpool = QThreadPool()
        self.workers: {str: AsyncWorker} = {}
        # self.threads: {str: QThread} = {}

    def cancel_worker(self, worker_id: str):
        worker = self.workers.get(worker_id)
        if worker is None:
            return f'There is no worker with id: {worker_id} currently running'
        worker.cancel()
        return None

    def start_worker(self, worker: AsyncWorker):
        # self.thread = QThread()
        if worker.id in self.workers:
            raise KeyError(f'Worker with id: {worker.id} already running')
        if len(self.workers) == self.threadpool.maxThreadCount():
            raise RuntimeError(f'Cannot start new thread, max thread count {self.threadpool.maxThreadCount()} already met')
        worker.reset()
        worker.setAutoDelete(True)
        worker.signals.finished.connect(self._worker_complete_callback)
        self.workers[worker.id] = worker
        self.threadpool.start(worker)
        # print(f'{worker.id} started, current workers: {list(self.workers.keys())}')
        # self.worker.progress_signal.connect(self.worker_progress_signal.emit)
        # self.worker.finished_signal.connect(self.worker_finished_signal.emit)
        # self.worker.moveToThread(self.thread)
        # self.thread.started.connect(self.worker.run)
        # self.worker.signals.finished.connect(self.thread.quit)
        # self.worker.signals.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.thread.start()

    def _worker_complete_callback(self, results: dict):
        worker_id = results.get('id')
        if worker_id and worker_id in self.workers:
            self.workers.pop(worker_id)
            if len(self.workers) == 0:
                self.all_workers_complete_signal.emit()

