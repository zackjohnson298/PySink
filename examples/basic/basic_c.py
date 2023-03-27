from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorker, AsyncWorkerProgress, AsyncWorkerResults
import sys
import time


# Define a class representing your result type, storing result values as attributes
class CustomWorkerResults(AsyncWorkerResults):
    custom_result_1 = None
    custom_result_2 = None


class CustomAsyncWorker(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        # Initialize AsyncWorker, passing in the custom result type
        super(CustomAsyncWorker, self).__init__(result_type=CustomWorkerResults)
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def run(self):
        progress = 5
        self.update_progress(progress, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += 90 / self.cycles
            self.update_progress(progress, f'Progress message #{ii + 1}')

        # With a custom result type, you can store your data directly into the self.results attribute. In this case,
        #   there is no need to pass any kwargs into self.complete
        self.results.custom_result_1 = 'result 1'
        self.results.custom_result_2 = 'result 2'
        self.complete()

        # You can still pass results to self.complete() as kwargs. However, each key MUST be defined as an attribute
        #   of the custom return type, else an AttributeError will be raised
        # self.complete(custom_result_1=12, custom_result_2=100)


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished. The results are now of type CustomWorkerResults.
def completion_callback(results: CustomWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult Attribute 1: {results.custom_result_1}')
    print(f'\tResult Attribute 2: {results.custom_result_2}')
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