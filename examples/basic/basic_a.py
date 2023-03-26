from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorker
from PySink import AsyncWorkerProgress, AsyncWorkerResults
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
    #   Create the Worker
    worker = AsyncWorker()
    #   Connect the Manager's signals to their callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    #   You can also connect to the Worker's signals directly
    # worker.signals.progress.connect(progress_callback)
    # worker.signals.finished.connect(completion_callback)

    #   Start the Worker
    manager.start_worker(worker)
    #   Start the App Event Loop
    app.exec()


run_main()
