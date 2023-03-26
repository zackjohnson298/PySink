from PySide6.QtWidgets import QApplication
from PySink import AsyncManager
from PySink.Objects import AsyncWorkerProgress
from DemoAsyncWorker2 import DemoAsyncWorker2, DemoAsyncWorker2Results
import sys


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished
def completion_callback(results: DemoAsyncWorker2Results):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult Attr 1: {results.custom_result_1}')
    print(f'\tResult Attr 2: {results.custom_result_2}')
    sys.exit()  # Exit the App event loop


def run_main():
    app = QApplication()
    #   Create the Async Manager
    manager = AsyncManager()
    #   Create the Worker and pass in the necessary values
    demo_worker = DemoAsyncWorker2(1, cycles=3)
    #   Connect the Manager's signals to their callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    #   Start the Worker and App event loop
    manager.start_worker(demo_worker)
    app.exec()


run_main()
