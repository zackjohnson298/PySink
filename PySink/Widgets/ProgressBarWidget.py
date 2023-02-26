from PySide6.QtWidgets import QWidget, QProgressBar, QLabel, QGridLayout
from PySide6.QtCore import Qt
import platform


class ProgressBarWidget(QWidget):
    def __init__(self):
        super(ProgressBarWidget, self).__init__()

        self.progress_bar = QProgressBar()
        self.label = QLabel()

        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setContentsMargins(0, 0, 0, 0)
        self.label.setContentsMargins(0, 0, 0, 0)

        # System Dependent Layout
        system = platform.system()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(self.progress_bar, 0, 0)
        layout.addWidget(self.label, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # self.setContentsMargins(0, 0, 0, 0)

    def set_value(self, progress_value):
        self.progress_bar.setRange(0, 0 if progress_value < 0 else 100)
        self.progress_bar.setValue(progress_value)
        self.progress_bar.setFormat('')

    def set_text(self, message):
        if platform.system() == 'Windows':
            self.label.setText(message)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication()
    window = QMainWindow()
    widget = ProgressBarWidget()
    widget.set_value(-1)
    widget.set_text('hello')
    window.setCentralWidget(widget)
    window.show()
    app.exec()

