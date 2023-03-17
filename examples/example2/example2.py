from PySide6.QtWidgets import QApplication
from PySink import AsyncManager, AsyncWorkerProgress, AsyncWorkerResults
from Example2AsyncWorker import Example2AsyncWorker, CustomAsyncWorkerResults


# Function to be called whenever progress is updated
def progress_callback(progress: AsyncWorkerProgress):
    print(f'Progress Received, value: {progress.value}, message: {progress.message}')


# Function to be called when the worker is finished
def completion_callback(results: CustomAsyncWorkerResults):
    print(f'\nWorker Complete!')
    print(f'\tErrors: {results.errors}')
    print(f'\tWarnings: {results.warnings}')
    print(f'\tResult Attr: {results.custom_result_1}')
    print(f'\tResult Attr: {results.custom_result_2}')


def run_main():
    app = QApplication()
    manager = AsyncManager()
    # Connect the Manager's signals to your callbacks
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    # Create your Worker, and pass in the necessary values
    demo_worker = Example2AsyncWorker(1, cycles=3)
    # Start the Worker
    manager.start_worker(demo_worker)
    app.exec()


run_main()
