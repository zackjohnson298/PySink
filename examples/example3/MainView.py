from PySink import AsyncWorkerProgress
from PySink.Widgets import ProgressBarWidget
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout


class RowItem(QWidget):
    cancel_signal = Signal()

    def __init__(self, title: str, parent=None):
        super(RowItem, self).__init__(parent)
        self.progress_bar = ProgressBarWidget()
        self.cancel_button = QPushButton('Cancel')
        self.title_label = QLabel(title)
        self.progress_widget = QWidget()
        self.result_label = QLabel()
        # Connect slots
        self.cancel_button.clicked.connect(self.cancel_signal.emit)
        # Layout
        progress_layout = QHBoxLayout(self.progress_widget)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.cancel_button)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.progress_widget)
        layout.addWidget(self.result_label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.reset()

    def reset(self):
        self.result_label.setText('Waiting to Run')
        self.progress_bar.set_value(0)

    def update_progress(self, progress: AsyncWorkerProgress):
        self.progress_bar.update_progress(progress)

    def show_progress(self):
        self.progress_widget.setVisible(True)
        self.result_label.setVisible(False)

    def hide_progress(self):
        self.progress_widget.setVisible(False)
        self.result_label.setVisible(True)

    def set_result(self, result_message):
        self.result_label.setText(result_message)


class MainView(QMainWindow):
    start_signal = Signal()
    cancel_signal = Signal()
    closed = Signal()

    def __init__(self, row_count=3):
        super(MainView, self).__init__()
        # Widgets/ Layouts
        self.start_button = QPushButton('Start All Workers')
        self.cancel_all_button = QPushButton('Cancel All Workers')
        self.row_items = [RowItem(f'Worker {ii+1}:', parent=self) for ii in range(row_count)]
        # Connect Slots
        self.start_button.clicked.connect(self.start_signal.emit)
        self.cancel_all_button.clicked.connect(self.cancel_signal.emit)
        # Layout
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        for row_item in self.row_items:
            central_layout.addWidget(row_item)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_all_button)
        button_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)
        self.setFixedSize(self.sizeHint())

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def hide_all_progress(self):
        for widget in self.row_items:
            widget.hide_progress()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    window = MainView()
    window.show()
    app.exec()