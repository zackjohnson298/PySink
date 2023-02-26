from PySide6.QtWidgets import QApplication
from MainController import MainController
from MainView import MainView


app = QApplication()
view = MainView()
controller = MainController(view)
view.show()
app.exec()