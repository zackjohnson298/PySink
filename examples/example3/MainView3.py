from PySink.Objects import AsyncWorkerProgress
from PySink.Widgets import ProgressBarWidget
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QGridLayout


class RowItem(QWidget):
    cancel_signal = Signal()

    def __init__(self, title: str, parent=None):
        super(RowItem, self).__init__(parent)
        self.progress_bar = ProgressBarWidget()
        self.cancel_button = QPushButton('Cancel')
        self.title_label = QLabel(title)
        self.result_label = QLabel()
        self.warnings_label = QLabel()
        self.errors_label = QLabel()
        self.progress_widget = QWidget()
        self.output_widget = QWidget()

        # Connect slots
        self.cancel_button.clicked.connect(self.cancel_signal.emit)

        # Layout
        progress_layout = QHBoxLayout(self.progress_widget)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.cancel_button)
        # progress_layout.setContentsMargins(0, 0, 0, 0)

        output_layout = QGridLayout(self.output_widget)
        output_layout.addWidget(self.result_label, 0, 0)
        output_layout.addWidget(self.warnings_label, 0, 1)
        output_layout.addWidget(self.errors_label, 0, 2)
        # output_layout.setContentsMargins(0, 0, 0, 0)

        central_layout = QGridLayout(self)
        central_layout.addWidget(self.title_label, 0, 0)
        central_layout.addWidget(self.output_widget, 0, 1, 1, 3)
        central_layout.addWidget(self.progress_widget, 0, 1, 1, 3)
        central_layout.setContentsMargins(0, 0, 0, 0)
        self.reset()

    def reset(self):
        self.hide_progress()
        self.result_label.setText('Waiting to Run')
        self.warnings_label.clear()
        self.errors_label.clear()
        self.progress_bar.reset()

    def set_result(self, result):
        self.result_label.setText(str(result))

    def set_warnings(self, warnings):
        self.warnings_label.setText(str(warnings))

    def set_errors(self, errors):
        self.errors_label.setText(str(errors))

    def set_progress(self, progress: AsyncWorkerProgress):
        self.progress_bar.update_progress(progress)

    def show_progress(self):
        self.progress_widget.setVisible(True)
        self.output_widget.setVisible(False)

    def hide_progress(self):
        self.progress_widget.setVisible(False)
        self.output_widget.setVisible(True)


class MainView3(QMainWindow):
    start_signal = Signal()
    cancel_signal = Signal()
    closed = Signal()

    def __init__(self, row_count=3):
        super(MainView3, self).__init__()
        # Widgets
        self.start_button = QPushButton('Start All Workers')
        self.cancel_all_button = QPushButton('Cancel All Workers')
        self.row_items = [RowItem(f'Worker {ii+1}:', parent=self) for ii in range(row_count)]

        # Connect Slots
        self.start_button.clicked.connect(self.start_signal.emit)
        self.cancel_all_button.clicked.connect(self.cancel_signal.emit)

        # Layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel('Worker:'), 0, 0)
        grid_layout.addWidget(QLabel('Result:'), 0, 1)
        grid_layout.addWidget(QLabel('Warnings:'), 0, 2)
        grid_layout.addWidget(QLabel('Errors:'), 0, 3)
        for ii, row_item in enumerate(self.row_items):
            grid_layout.addWidget(row_item, ii+1, 0, 1, 4)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_all_button)
        button_layout.setContentsMargins(0, 0, 0, 0)

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.addLayout(grid_layout)
        central_layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)
        self.setFixedHeight(self.sizeHint().height())
        self.setWindowTitle('PySink Example 3')

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def hide_all_progress(self):
        for widget in self.row_items:
            widget.hide_progress()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    window = MainView3()
    window.show()
    app.exec()
