from PySide6.QtCore import Signal, QObject, QThreadPool
from PySink.AsyncWorker import AsyncWorker, AsyncWorkerResults, AsyncWorkerProgress
from PySink.CancellableAsyncWorker import CancellableAsyncWorker


class AsyncManager(QObject):
    worker_finished_signal = Signal(AsyncWorkerResults)
    worker_progress_signal = Signal(AsyncWorkerProgress)
    all_workers_complete_signal = Signal()

    def __init__(self):
        super(AsyncManager, self).__init__()
        self.threadpool = QThreadPool()
        self.workers: {str: AsyncWorker} = {}

    def cancel_all_workers(self) -> {str: str}:
        current_worker_ids = list(self.workers.keys())
        errors = {}
        for worker_id in current_worker_ids:
            error = self.cancel_worker(worker_id)
            if error:
                errors[worker_id] = error
        if len(errors) == 0:
            self.threadpool.clear()
        return errors

    def cancel_worker(self, worker_id: str):
        worker = self.workers.get(worker_id)
        if worker is None:
            return f'There is no worker with id: {worker_id} currently running'
        if not isinstance(worker, CancellableAsyncWorker):
            return f'Worker if type {type(worker)} is not Cancellable'
        worker.cancel()
        return None

    def start_worker(self, worker: AsyncWorker):
        if worker.id in self.workers:
            raise KeyError(f'Worker with id: {worker.id} already running')
        worker.reset()
        worker.setAutoDelete(True)
        worker.signals.progress.connect(self.worker_progress_signal.emit)
        worker.signals.finished.connect(self._worker_complete_callback)
        self.workers[worker.id] = worker
        self.threadpool.start(worker)

    def _worker_complete_callback(self, results: AsyncWorkerResults):
        worker_id = results.id
        if worker_id and worker_id in self.workers:
            self.worker_finished_signal.emit(results)
            self.workers.pop(worker_id)
            if len(self.workers) == 0:
                self.all_workers_complete_signal.emit()

