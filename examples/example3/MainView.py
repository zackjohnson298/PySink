from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QGridLayout, QLabel
from PySide6.QtCore import Signal

from PySink.Objects import AsyncWorkerProgress
from PySink.Widgets import ProgressBarWidget


class MainView(QMainWindow):
    button_pushed_signal = Signal()

    def __init__(self):
        super(MainView, self).__init__()

        # Widgets
        self.button = QPushButton('Start')
        self.progress_bar = ProgressBarWidget()
        self.warnings_label = QLabel()
        self.errors_label = QLabel()
        self.result_label = QLabel()

        # Connect Signals
        self.button.clicked.connect(self.button_pushed_signal.emit)

        # Layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel('Result:'), 0, 0)
        grid_layout.addWidget(QLabel('Warnings:'), 1, 0)
        grid_layout.addWidget(QLabel('Error:'), 2, 0)
        grid_layout.addWidget(self.result_label, 0, 1)
        grid_layout.addWidget(self.warnings_label, 1, 1)
        grid_layout.addWidget(self.errors_label, 2, 1)

        central_layout = QVBoxLayout()
        central_layout.addLayout(grid_layout)
        central_layout.addWidget(self.button)
        central_layout.addWidget(self.progress_bar)
        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('PySink Example 3')
        self.setFixedWidth(280)
        self.setFixedHeight(120)

    def set_result(self, result):
        self.result_label.setText(str(result))

    def set_warnings(self, warnings):
        self.warnings_label.setText(str(warnings))

    def set_errors(self, errors):
        self.errors_label.setText(str(errors))

    def set_progress(self, progress: AsyncWorkerProgress):
        self.progress_bar.update_progress(progress)

    def clear(self):
        self.warnings_label.setText('')
        self.errors_label.setText('')
        self.result_label.setText('')

    def show_progress(self):
        self.button.setVisible(False)
        self.progress_bar.setVisible(True)

    def hide_progress(self):
        self.progress_bar.setVisible(False)
        self.button.setVisible(True)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    window = MainView()
    window.show()
    p = window.grab()
    p.save('example2_main_view.png', 'png')

    app.exec()

