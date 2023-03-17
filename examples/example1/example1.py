from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorkerProgress, AsyncWorkerResults
from DemoAsyncWorker1 import DemoAsyncWorker1
import sys


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished
def completion_callback(results: AsyncWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult Dict: {results.results_dict}')
    sys.exit()  # Exit the App event loop


def run_main():
    app = QApplication()
    #   Create the Async Manager
    manager = AsyncManager()
    #   Create the Worker and pass in the necessary values
    demo_worker = DemoAsyncWorker1(1, cycles=3)
    #   Connect the Manager's signals to their callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    #   You can also connect to the Worker's signals directly
    # demo_worker.signals.progress.connect(progress_callback)
    # demo_worker.signals.finished.connect(completion_callback)

    #   Start the Worker and App event loop
    manager.start_worker(demo_worker)
    app.exec()


run_main()
