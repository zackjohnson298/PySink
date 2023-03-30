from PySide6.QtWidgets import QApplication
from MainController3 import MainController3
from MainView3 import MainView3


app = QApplication()
view = MainView3(row_count=10)
controller = MainController3(view)
view.show()
app.exec()
