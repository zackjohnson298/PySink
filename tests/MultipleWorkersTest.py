import json

from PySide6.QtCore import Qt, Signal

from PySink import AsyncWorker, AsyncManager
from PySink.Widgets import ProgressBarWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QGridLayout, QPushButton, QWidget, \
    QVBoxLayout
import time
import sys
from random import randint


class DemoAsyncWorker(AsyncWorker):
    def __init__(self, count=5, delay_seconds=1.):
        super(DemoAsyncWorker, self).__init__()
        self.count = count
        self.delay_seconds = delay_seconds

    def run(self):
        progress = 5
        self.update_progress(progress)
        for ii in range(self.count):
            # print(f'Worker {self.id} step: {ii}')
            time.sleep(self.delay_seconds)
            progress += int(90 / self.count)
            self.update_progress(progress)
        self.complete()


class MainView(QMainWindow):
    cancel_clicked = Signal(int)

    def __init__(self, row_count=3):
        super(MainView, self).__init__()
        # Widgets/ Layouts
        self.start_button = QPushButton('Start Workers')
        self.central_layout = QVBoxLayout()

        # Store Widgets
        self.progress_widgets = []
        self.result_labels = []
        self.cancel_buttons = []
        self.progress_bars = []

        # Layout
        central_widget = QWidget()
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)
        for _ in range(row_count):
            self.add_row()
        self.central_layout.addWidget(self.start_button)
        self.setFixedSize(self.sizeHint())

    def add_row(self):
        progress_bar = ProgressBarWidget()
        cancel_button = QPushButton('Cancel')
        result_label = QLabel('None')
        progress_widget = QWidget()

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(progress_bar)
        progress_layout.addWidget(cancel_button)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_widget.setLayout(progress_layout)
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel(f'Worker {len(self.progress_widgets) + 1}:'))
        row_layout.addWidget(progress_widget)
        row_layout.addWidget(result_label)
        self.central_layout.addLayout(row_layout)

        self.progress_bars.append(progress_bar)
        self.progress_widgets.append(progress_widget)
        self.cancel_buttons.append(cancel_button)
        self.result_labels.append(result_label)

        row = len(self.cancel_buttons) - 1
        cancel_button.clicked.connect(lambda: self.cancel_clicked.emit(row))


class MainController:
    def __init__(self, view: MainView):
        self.view = view
        self.async_manager = AsyncManager()
        self.worker_row_indices = {}
        # Connect Slots
        self.view.start_button.clicked.connect(self.start_workers)
        self.view.cancel_clicked.connect(lambda row_index: self.async_manager.cancel_worker(self.worker_row_indices[row_index]))
        self.async_manager.all_workers_complete_signal.connect(lambda: self.view.start_button.setEnabled(True))
        # Initialize UI
        for widget in self.view.progress_widgets:
            widget.setVisible(False)
        # print(self.async_manager.threadpool.maxThreadCount())

    def all_workers_complete(self):
        self.view.start_button.setEnabled(True)
        self.worker_row_indices = {}

    def update_progress(self, value, message, row_index):
        if row_index in self.worker_row_indices:
            self.view.progress_bars[row_index].set_value(value)
            self.view.progress_bars[row_index].set_text(message)

    def worker_complete(self, results, row_index):
        if row_index in self.worker_row_indices:
            self.view.result_labels[row_index].setText(json.dumps(results))
            self.view.result_labels[row_index].setVisible(True)
            self.view.progress_widgets[row_index].setVisible(False)
            self.worker_row_indices.pop(row_index)

    def start_workers(self):
        print('Starting all workers')
        self.worker_row_indices = {}
        self.view.start_button.setEnabled(False)
        for row_index, (progress_widget, progress_bar, cancel_button, result_label) in enumerate(zip(self.view.progress_widgets, self.view.progress_bars, self.view.cancel_buttons, self.view.result_labels)):
            # Set UI State
            progress_widget.setVisible(True)
            result_label.setVisible(False)
            # Initialize Worker
            worker = DemoAsyncWorker(count=randint(3, 6), delay_seconds=0.1*randint(5, 10))
            self.worker_row_indices[row_index] = worker.id
            worker.signals.progress.connect(lambda value, message, r_index=row_index: self.update_progress(value, message, r_index))
            worker.signals.finished.connect(lambda results, r_index=row_index: self.worker_complete(results, r_index))
            # cancel_button.clicked.connect(worker.cancel)
            self.async_manager.start_worker(worker)


def run_test():
    app = QApplication()
    window = MainView(row_count=7)
    controller = MainController(window)
    window.show()
    app.exec()


if __name__ == '__main__':
    run_test()

