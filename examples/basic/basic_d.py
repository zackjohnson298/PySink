from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal
from PySink import AsyncManager, AsyncWorker, AsyncWorkerProgress, AsyncWorkerResults, AsyncWorkerSignals
import sys
import time


# Define a class representing your result type, storing result values as attributes
class CustomWorkerResults(AsyncWorkerResults):
    custom_result_1 = None
    custom_result_2 = None


# Define a class representing your signal type, storing result values as attributes
class CustomWorkerSignals(AsyncWorkerSignals):
    custom_signal = Signal(str)


class CustomAsyncWorker(AsyncWorker):
    def __init__(self, delay_seconds: int, cycles=4):
        # Initialize AsyncWorker, passing in the custom result type
        super(CustomAsyncWorker, self).__init__(result_type=CustomWorkerResults, signal_type=CustomWorkerSignals)
        self.delay_seconds = delay_seconds
        self.cycles = cycles

    def do_part_1(self):
        progress = 5
        self.update_progress(progress, 'Starting Task')
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += 90 / (2 * self.cycles)
            self.update_progress(progress, f'Progress message from part 1 #{ii + 1}')
        self.results.custom_result_1 = 'result 1'

    def do_part_2(self):
        progress = 50
        for ii in range(self.cycles):
            time.sleep(self.delay_seconds)
            progress += 90 / (2 * self.cycles)
            self.update_progress(progress, f'Progress message from part 2 #{ii + 1}')
        self.results.custom_result_2 = 'result 2'

    def run(self):
        self.emit_start()
        self.do_part_1()
        self.signals.custom_signal.emit('custom signal value')
        self.do_part_2()
        self.complete()


# Function to be called when the custom signal is emitted
def custom_signal_callback(signal_value):
    print(f'\nCustom Signal received! Value: {signal_value}\n')


# Function to be called whenever a worker's task has started
def worker_started_callback(worker_id: str):
    print(f'Worker with id {worker_id} has started its task\n')


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
    worker = CustomAsyncWorker(delay_seconds=1, cycles=3)
    #   Connect the Worker's signals to their callbacks
    worker.signals.custom_signal.connect(custom_signal_callback)
    worker.signals.started.connect(worker_started_callback)
    worker.signals.progress.connect(progress_callback)
    worker.signals.finished.connect(completion_callback)
    #   Start the Worker and App event loop
    manager.start_worker(worker)
    app.exec()


run_main()
