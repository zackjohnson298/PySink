from PySide6.QtCore import QThread, Signal, QObject
from AsyncWorker import AsyncWorker


class AsyncManager(QObject):
    worker_finished_signal = Signal(dict)
    worker_progress_signal = Signal(int, str)

    def __init__(self):
        super(AsyncManager, self).__init__()
        self.worker = AsyncWorker()
        self.thread = QThread()

    def cancel(self):
        self.worker.cancel()
        if self.thread.isRunning():
            self.thread.quit()
            # self.thread.wait()

    def start_worker(self, worker: AsyncWorker):
        self.thread = QThread()
        self.worker = worker
        self.worker.reset()
        self.worker.progress_signal.connect(self.worker_progress_signal.emit)
        self.worker.finished_signal.connect(self.worker_finished_signal.emit)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished_signal.connect(self.thread.quit)
        self.worker.finished_signal.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import time

    # Function to be called whenever progress is updated
    def progress_callback(progress_value: int, message: str):
        print(f'Progress Received, value: {progress_value}, message: {message}')

    # Function to be called when the worker is finished
    def completion_callback(results: dict):
        print(f'\nWorker Complete!')
        print(f'\tErrors: {results.get("errors")}')
        print(f'\tWarnings: {results.get("warnings")}')
        print(f'\tResult: {results.get("demo_result")}')


    class DemoAsyncWorker(AsyncWorker):
        def __init__(self, delay_seconds, cycles=4):
            super(DemoAsyncWorker, self).__init__()
            self.delay_seconds = delay_seconds
            self.cycles = cycles

        def run(self):
            progress = 0
            progress_increment = 100 / self.cycles
            # Update progress by providing a progress value from 0-10 with an optional message
            self.update_progress(0, 'Starting Task')
            for ii in range(self.cycles):
                time.sleep(self.delay_seconds)
                progress += progress_increment
                self.update_progress(progress, f'Progress message #{ii + 1}')
                # Store any errors/warnings in the provided attributes. They are emitted by default
                # self.warnings.append(f'Demo Warning {ii + 1}')
                # self.errors.append(f'Demo Error {ii + 1}')
            # Call the self.complete method to end your task, passing any results as keyword arguments
            demo_result = 12
            self.complete(demo_result=demo_result)


    app = QApplication()
    manager = AsyncManager()
    manager.worker_progress_signal.connect(progress_callback)
    manager.worker_finished_signal.connect(completion_callback)
    demo_worker = DemoAsyncWorker(1, cycles=3)
    manager.start_worker(demo_worker)
    app.exec()
