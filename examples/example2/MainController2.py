from PySink import AsyncManager, AsyncWorkerResults
from MainView2 import MainView2
from CustomWorker2 import CustomWorker2
from random import randint


class MainController2:
    def __init__(self, view: MainView2):
        self.view = view
        self.async_manager = AsyncManager()
        # Connect Slots
        self.view.start_signal.connect(self.start_worker)
        self.async_manager.worker_progress_signal.connect(self.view.set_progress)
        self.async_manager.worker_finished_signal.connect(self.worker_complete)
        # Initialize UI
        self.view.clear()
        self.view.hide_progress()
        self.view.start_button.setEnabled(True)
        self.view.cancel_button.setEnabled(False)

    def start_worker(self):
        # Set UI State
        self.view.clear()
        self.view.start_button.setEnabled(False)
        self.view.cancel_button.setEnabled(True)
        self.view.show_progress()
        # Initialize Worker
        worker = CustomWorker2(cycles=randint(3, 6), delay_seconds=0.1 * randint(5, 10))
        # Connect View's Cancel signal to the new Worker's cancel method
        self.view.cancel_signal.connect(worker.cancel)
        # Start Worker
        self.async_manager.start_worker(worker)

    def worker_complete(self, results: AsyncWorkerResults):
        self.view.hide_progress()
        self.view.set_result(results.results_dict)
        self.view.set_warnings(results.warnings)
        self.view.set_errors(results.errors)
        self.view.start_button.setEnabled(True)
        self.view.cancel_button.setEnabled(False)




