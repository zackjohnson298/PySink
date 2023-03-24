from typing import Union

from PySide6.QtWidgets import QWidget, QProgressBar, QLabel, QGridLayout
from PySide6.QtCore import Qt
from PySink import AsyncWorkerProgress, AsyncManager, AsyncWorker
import platform


class ProgressBarWidget(QWidget):
    """An implementation of a PySide6 Progress Bar. This has a couple of helper functions that are natively compatible
    with PySink, allowing you to easily display the progress of an :class:`AsyncWorker`.

    :param parent: The parent widget
    :type parent: QWidget, optional
    """

    def __init__(self, parent=None):
        """Constructor method"""
        super(ProgressBarWidget, self).__init__(parent)

        self.progress_bar = QProgressBar()
        self.label = QLabel()

        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setContentsMargins(0, 0, 0, 0)
        self.label.setContentsMargins(0, 0, 0, 0)

        # System Dependent Layout
        # system = platform.system()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(self.progress_bar, 0, 0)
        layout.addWidget(self.label, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # self.setContentsMargins(0, 0, 0, 0)

    def set_value(self, progress_value: Union[int, float]):
        """Sets the current progress value...

        :param progress_value: The current progress value. For discrete behavior, value should be in [0, 100].
            For indeterminate behavior, value should be less than 0...
        :type progress_value: Union[int, float]
        """
        self.progress_bar.setRange(0, 0 if progress_value < 0 else 100)
        self.progress_bar.setValue(progress_value)
        self.progress_bar.setFormat('')

    def set_text(self, message: str):
        """Sets the current progress message. This will only be displayed on Windows platforms. The text is overlayed
        on top of the progress bar...

        :param message: The current progress message
        :type message: str
        """
        if platform.system() == 'Windows':
            self.label.setText(message)

    def update_progress(self, progress: AsyncWorkerProgress):
        """Updates the current progress to be displayed. This is natively emitted by an :class:`AsyncWorker` (and the
        :class:`AsyncManager`), so the emitted progress can be passed directly to this method...

        :param progress: The current progress
        :type progress: AsyncWorkerProgress
        :return:
        :rtype:
        """
        self.set_value(progress.value)
        self.set_text(progress.message)


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

