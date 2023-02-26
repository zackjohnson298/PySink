from PySink import AsyncWorker, AsyncManager
from PySide6.QtWidgets import QApplication
from PySink import AsyncManager
from DemoAsyncWorker import DemoAsyncWorker


# Function to be called whenever progress is updated
def progress_callback(progress_value: int, message: str):
    print(f'Progress Received, value: {progress_value}, message: {message}')


# Function to be called when the worker is finished
def completion_callback(results: dict):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.get("errors")}')
    print(f'\tWarnings: {results.get("warnings")}')
    print(f'\tResult: {results.get("demo_result")}')


def run_main():
    app = QApplication()
    manager = AsyncManager()
    # Connect the Manager's signals to your callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    # Create your Worker, and pass in the necessary values
    demo_worker = DemoAsyncWorker(1, cycles=3)
    # Start the Worker
    manager.start_worker(demo_worker)

    app.exec()


run_main()
