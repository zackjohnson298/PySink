from PySink import AsyncManager, AsyncWorkerProgress, AsyncWorkerResults
from Example3AsyncWorker import Example3AsyncWorker, CustomAsyncWorkerResults
from MainView import MainView


class MainController:
    def __init__(self, view: MainView):
        self.view = view
        self.async_manager = AsyncManager()
        # Connect UI Signals
        self.view.button_pushed_signal.connect(self.start_task)
        # Connect Async Signals
        self.async_manager.worker_progress_signal.connect(self.view.set_progress)
        self.async_manager.worker_finished_signal.connect(self.task_complete_callback)
        # Initialize UI State
        self.view.button.setVisible(True)
        self.view.progress_bar.setVisible(False)

    def start_task(self):
        # Update UI
        self.view.clear()
        self.view.show_progress()
        # Initialize/Start Worker
        worker = Example3AsyncWorker(2, cycles=5)
        self.async_manager.start_worker(worker)

    def task_complete_callback(self, results: CustomAsyncWorkerResults):
        # Update UI
        self.view.clear()
        self.view.show_button()
        # Handle results
        self.view.set_result(results.demo_result)
        self.view.set_warnings(results.warnings)
        self.view.set_errors(results.errors)


