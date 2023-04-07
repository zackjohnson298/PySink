from PySink import AsyncManager
from CustomWorker1 import CustomWorker1, CustomWorker1Results
from MainView1 import MainView1


class MainController1:
    def __init__(self, view: MainView1):
        self.view = view
        # Create an AsyncManager and save it as an attribute
        self.async_manager = AsyncManager()
        # Connect UI Signals
        self.view.start_signal.connect(self.start_worker)
        # Connect Async Signals
        self.async_manager.worker_progress_signal.connect(self.view.set_progress)
        self.async_manager.worker_finished_signal.connect(self.worker_complete_callback)
        # Initialize UI State
        self.view.hide_progress()

    def start_worker(self):
        # Set UI State
        self.view.clear()
        self.view.show_progress()
        # Initialize/Start Worker
        worker = CustomWorker1(2, cycles=5)
        self.async_manager.start_worker(worker)

    def worker_complete_callback(self, results: CustomWorker1Results):
        # Set UI State
        self.view.clear()
        self.view.hide_progress()
        # Handle results
        self.view.set_result(results.demo_result)
        self.view.set_warnings(results.warnings)
        self.view.set_errors(results.errors)
