from PySide6.QtWidgets import QApplication
from MainController import MainController
from MainView import MainView


app = QApplication()
# Create the View
view = MainView()
# Create the Controller, passing in the View
controller = MainController(view)
# Show the View
view.show()
# Start the App event loop
app.exec()
