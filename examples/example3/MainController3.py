from PySink import AsyncManager, AsyncWorkerResults
from MainView3 import MainView3
from CustomWorker3 import CustomWorker3
from random import randint


class MainController3:
    def __init__(self, view: MainView3):
        self.view = view
        self.async_manager = AsyncManager()
        # Connect Slots
        self.view.start_signal.connect(self.start_workers)
        self.view.cancel_signal.connect(self.cancel_all_workers)
        self.view.closed.connect(self.cancel_all_workers)
        self.async_manager.all_workers_finished_signal.connect(self.all_workers_complete_callback)
        # Initialize UI
        self.view.hide_all_progress()
        self.view.start_button.setEnabled(True)
        self.view.cancel_all_button.setEnabled(False)

    def start_workers(self):
        # Set UI State
        self.view.start_button.setEnabled(False)
        self.view.cancel_all_button.setEnabled(True)
        for row_index, row_item in enumerate(self.view.row_items):
            # Set UI State
            row_item.reset()
            # Initialize Worker
            worker = CustomWorker3(cycles=randint(3, 6), delay_seconds=0.1 * randint(5, 10))
            # Connect UI Signals
            row_item.cancel_signal.connect(worker.cancel)
            # Connect Worker's Signals
            worker.signals.progress.connect(row_item.set_progress)
            worker.signals.finished.connect(lambda results, r_index=row_index: self.worker_complete(results, r_index))
            # Since some workers may be queued, it's good practice to not show progress until the worker starts
            worker.signals.started.connect(row_item.show_progress)
            # Start Worker
            self.async_manager.start_worker(worker)

    def worker_complete(self, results: AsyncWorkerResults, row_index):
        self.view.row_items[row_index].hide_progress()
        self.view.row_items[row_index].set_result(results.results_dict)
        self.view.row_items[row_index].set_warnings(results.warnings)
        self.view.row_items[row_index].set_errors(results.errors)

    def all_workers_complete_callback(self):
        self.view.start_button.setEnabled(True)
        self.view.cancel_all_button.setEnabled(False)

    def cancel_all_workers(self):
        self.async_manager.cancel_all_workers()



