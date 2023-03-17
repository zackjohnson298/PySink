from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorkerProgress, AsyncWorkerResults
from DemoAsyncWorker import DemoAsyncWorker, DemoAsyncWorkerResults


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished
def default_completion_callback(results: AsyncWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult Dict: {results.results_dict}')


def custom_return_type_completion_callback(results: DemoAsyncWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult Attr: {results.demo_result}')


def run_main():
    app = QApplication()
    manager = AsyncManager()
    # Connect the Manager's signals to your callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(default_completion_callback)
    manager.worker_finished_signal.connect(custom_return_type_completion_callback)
    # Create your Worker, and pass in the necessary values
    demo_worker = DemoAsyncWorker(1, cycles=3)
    # Start the Worker
    manager.start_worker(demo_worker)
    app.exec()


run_main()
