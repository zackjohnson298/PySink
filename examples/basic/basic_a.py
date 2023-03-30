from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorker
from PySink import AsyncWorkerProgress, AsyncWorkerResults
import sys


# Function to be called whenever a worker's task has started
def worker_started_callback(worker_id: str):
    print(f'Worker with id {worker_id} has started its task\n')


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished
def completion_callback(results: AsyncWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tErrors: {results.errors}')
    print(f'\tResults: {results.results_dict}')
    sys.exit()  # Exit the App event loop


def run_main():
    # Create an instance of QApplication. This allows us to start a Qt event loop.
    app = QApplication()
    #   Create the Async Manager
    manager = AsyncManager()
    #   Create the Worker
    worker = AsyncWorker()
    #   Connect the Worker's signals to their callbacks
    worker.signals.started.connect(worker_started_callback)
    worker.signals.progress.connect(progress_callback)
    worker.signals.finished.connect(completion_callback)
    #   You can also connect to these signals via the Manager, however this is rarely used
    # manager.worker_progress_signal.connect(progress_callback)
    # manager.worker_finished_signal.connect(completion_callback)

    #   Start the Worker
    manager.start_worker(worker)
    #   Start the App Event Loop
    app.exec()


run_main()
