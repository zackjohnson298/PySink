from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorker, AsyncWorkerProgress, AsyncWorkerResults
import sys
import time


# Define the custom worker, inheriting from AsyncWorker
class CustomAsyncWorker(AsyncWorker):
    # Any values needed in self.run are passed in to __init__
    def __init__(self, delay_seconds: int, cycles: int):
        super(CustomAsyncWorker, self).__init__()
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    # Override AsyncWorker's .run() method
    def run(self):
        progress = 5
        self.update_progress(progress, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += 90 / self.cycles
            self.update_progress(progress, f'Progress message #{ii + 1}')

        # Result values can be passed to self.complete() as kwargs.
        self.complete(custom_result_1='result 1', custom_result_2='result2')


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished
def completion_callback(results: AsyncWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult 1: {results.results_dict.get("custom_result_1")}')
    print(f'\tResult 2: {results.results_dict.get("custom_result_2")}')
    sys.exit()  # Exit the App event loop


def run_main():
    app = QApplication()
    #   Create the Async Manager
    manager = AsyncManager()
    #   Create the Worker and pass in the necessary values
    demo_worker = CustomAsyncWorker(delay_seconds=1, cycles=3)
    #   Connect the Manager's signals to their callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    #   Start the Worker and App event loop
    manager.start_worker(demo_worker)
    app.exec()


run_main()
