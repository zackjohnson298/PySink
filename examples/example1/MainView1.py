from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QGridLayout, QLabel
from PySide6.QtCore import Signal

from PySink import AsyncWorkerProgress
from PySink.Widgets import ProgressBarWidget


class MainView1(QMainWindow):
    start_signal = Signal()

    def __init__(self):
        super(MainView1, self).__init__()
        # Widgets
        self.start_button = QPushButton('Start')
        self.progress_bar = ProgressBarWidget()
        self.warnings_label = QLabel()
        self.errors_label = QLabel()
        self.result_label = QLabel()

        # Connect Signals
        self.start_button.clicked.connect(self.start_signal.emit)

        # Layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel('Result:'), 0, 0)
        grid_layout.addWidget(QLabel('Warnings:'), 0, 1)
        grid_layout.addWidget(QLabel('Errors:'), 0, 2)
        grid_layout.addWidget(self.result_label, 1, 0)
        grid_layout.addWidget(self.warnings_label, 1, 1)
        grid_layout.addWidget(self.errors_label, 1, 2)

        central_layout = QVBoxLayout()
        central_layout.addLayout(grid_layout)
        central_layout.addWidget(self.start_button)
        central_layout.addWidget(self.progress_bar)
        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('PySink Example 1')
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
        self.start_button.setVisible(False)
        self.progress_bar.setVisible(True)

    def hide_progress(self):
        self.progress_bar.setVisible(False)
        self.start_button.setVisible(True)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    window = MainView1()
    window.show()
    p = window.grab()
    p.save('example2_main_view.png', 'png')

    app.exec()
