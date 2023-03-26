from PySide6.QtWidgets import QApplication
from MainController2 import MainController2
from MainView2 import MainView2


app = QApplication()
view = MainView2()
controller = MainController2(view)
view.show()
app.exec()
