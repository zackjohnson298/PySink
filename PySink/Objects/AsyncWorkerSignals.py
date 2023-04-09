from PySide6.QtCore import QObject, Signal
from PySink.Objects import AsyncWorkerProgress, AsyncWorkerResults


class AsyncWorkerSignals(QObject):

    started = Signal(str)                   #: Signal(str): Signals that the worker has started its task. Contains the workers unique identified.
    progress = Signal(AsyncWorkerProgress)  #: Signal(:class:`~AsyncWorkerProgress`): Signal that contains progress information for the worker.
    finished = Signal(AsyncWorkerResults)   #: Signal(:class:`~AsyncWorkerResults`): Signals that a worker has finished its task and contains the results of the worker's task.

    def __init__(self):
        """Class to store the signals of an :class:`AsyncWorker`. Custom signal type should inherit from this class."""
        super(AsyncWorkerSignals, self).__init__()
