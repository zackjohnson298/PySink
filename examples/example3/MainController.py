from PySink import AsyncManager
from DemoAsyncWorker3 import DemoAsyncWorker3, DemoAsyncWorker3Results
from MainView import MainView


class MainController:
    def __init__(self, view: MainView):
        self.view = view
        # Create an AsyncManager and save it as an attribute
        self.async_manager = AsyncManager()
        # Connect UI Signals
        self.view.button_pushed_signal.connect(self.start_worker)
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
        worker = DemoAsyncWorker3(2, cycles=5)
        self.async_manager.start_worker(worker)

    def worker_complete_callback(self, results: DemoAsyncWorker3Results):
        # Set UI State
        self.view.clear()
        self.view.hide_progress()
        # Handle results
        self.view.set_result(results.demo_result)
        self.view.set_warnings(results.warnings)
        self.view.set_errors(results.errors)


