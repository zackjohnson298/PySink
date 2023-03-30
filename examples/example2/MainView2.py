from PySink.Objects import AsyncWorkerProgress
from PySink.Widgets import ProgressBarWidget
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QGridLayout


class MainView2(QMainWindow):
    start_signal = Signal()
    cancel_signal = Signal()

    def __init__(self):
        super(MainView2, self).__init__()
        # Widgets
        self.start_button = QPushButton('Start')
        self.cancel_button = QPushButton('Cancel')
        self.progress_bar = ProgressBarWidget()
        self.warnings_label = QLabel()
        self.errors_label = QLabel()
        self.result_label = QLabel()
        self.progress_widget = QWidget()

        # Connect Slots
        self.start_button.clicked.connect(self.start_signal.emit)
        self.cancel_button.clicked.connect(self.cancel_signal.emit)

        # Layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel('Result:'), 0, 0)
        grid_layout.addWidget(QLabel('Warnings:'), 0, 1)
        grid_layout.addWidget(QLabel('Errors:'), 0, 2)
        grid_layout.addWidget(self.result_label, 1, 0)
        grid_layout.addWidget(self.warnings_label, 1, 1)
        grid_layout.addWidget(self.errors_label, 1, 2)

        progress_layout = QHBoxLayout(self.progress_widget)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.cancel_button)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        central_layout = QVBoxLayout()
        central_layout.addLayout(grid_layout)
        central_layout.addWidget(self.progress_widget)
        central_layout.addWidget(self.start_button)
        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('PySink Example 2')
        self.setFixedWidth(280)
        self.setFixedHeight(120)

    def clear(self):
        self.progress_bar.reset()
        self.warnings_label.setText('')
        self.errors_label.setText('')
        self.result_label.setText('')

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
        self.start_button.setVisible(False)

    def hide_progress(self):
        self.progress_widget.setVisible(False)
        self.start_button.setVisible(True)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    window = MainView2()
    window.show()
    app.exec()