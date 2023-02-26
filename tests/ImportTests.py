from PySink import AsyncManager
from PySink import AsyncWorker
from PySink.Widgets import ProgressBarWidget
from PySide6.QtWidgets import QApplication, QMainWindow


worker = AsyncWorker()
manager = AsyncManager()

app = QApplication()
window = QMainWindow()
widget = ProgressBarWidget()
# widget = ProgressBarWidget()
widget.set_value(-1)
widget.set_text('hello')
window.setCentralWidget(widget)
window.show()
app.exec()


