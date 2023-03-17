from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorkerProgress, AsyncWorkerResults
from Example1AsyncWorker import Example1AsyncWorker


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished
def completion_callback(results: AsyncWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult Dict: {results.results_dict}')


def run_main():
    app = QApplication()
    manager = AsyncManager()
    # Connect the Manager's signals to your callbacks (you can also connect to the Worker's signal directly)
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    # Create your Worker, and pass in the necessary values
    demo_worker = Example1AsyncWorker(1, cycles=3)
    # Start the Worker
    manager.start_worker(demo_worker)
    app.exec()


run_main()
