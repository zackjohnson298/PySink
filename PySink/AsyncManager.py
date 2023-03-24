from PySide6.QtCore import Signal, QObject, QThreadPool
from PySink.AsyncWorker import AsyncWorker, AsyncWorkerResults, AsyncWorkerProgress
from PySink.CancellableAsyncWorker import CancellableAsyncWorker


class AsyncManager(QObject):
    #: Signal: Signals that a worker has started its task. Contains the id of the worker.
    worker_started_signal = Signal(str)
    #: Signal: Signal that contains progress data for a worker.
    worker_progress_signal = Signal(AsyncWorkerProgress)
    #: Signal: Signals that a worker has finished its task. Contains the results of the worker.
    worker_finished_signal = Signal(AsyncWorkerResults)
    #: Signal: Signals that all workers have finished their tasks.
    all_workers_complete_signal = Signal()

    def __init__(self):
        """Class that manages all AsyncWorkers and their corresponding threads. The manager can cancel workers by id,
        cancel all active (and cancellable) workers, and the worker's signals can also be accessed via the manager.
        All threads/workers will be garbage collected upon the worker's completion..
        """
        super(AsyncManager, self).__init__()
        self.threadpool = QThreadPool()
        self.workers: {str: AsyncWorker} = {}

    def cancel_all_workers(self) -> {str: str}:
        """Attempts to cancel all workers that are active and cancellable..

        :return: A dictionary of errors if they are encountered, keyed by worker id.
        :rtype: dict
        """
        current_worker_ids = list(self.workers.keys())
        errors = {}
        for worker_id in current_worker_ids:
            error = self.cancel_worker(worker_id)
            if error:
                errors[worker_id] = error
        if len(errors) == 0:
            self.threadpool.clear()
        return errors

    def cancel_worker(self, worker_id: str) -> str:
        """Attempts to cancel the worker with the given id...

        :param worker_id: The unique identifier of the worker to be cancelled
        :type worker_id: str
        :return: An message describing the issue if the worker could not be cancelled or does not exist
        :rtype: str
        """
        worker = self.workers.get(worker_id)
        if worker is None:
            return f'There is no worker with id: {worker_id} currently running'
        if not isinstance(worker, CancellableAsyncWorker):
            return f'Worker if type {type(worker)} is not Cancellable'
        worker.cancel()
        return ''

    def start_worker(self, worker: AsyncWorker) -> None:
        """Starts the worker on a new thread (or queues the worker if there are no threads available).
        Once the worker is on the thread, the worker's .run() method is called..

        :param worker: The worker to be run
        :type worker: AsyncWorker
        """
        if worker.id in self.workers:
            raise KeyError(f'Worker with id: {worker.id} already running')
        worker.reset()
        worker.setAutoDelete(True)
        worker.signals.started.connect(lambda worker_id=worker.id: self.worker_started_signal.emit(worker_id))
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

