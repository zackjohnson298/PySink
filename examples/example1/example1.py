from PySide6.QtWidgets import QApplication
from MainController1 import MainController1
from MainView1 import MainView1


app = QApplication()
# Create the View
view = MainView1()
# Create the Controller, passing in the View
controller = MainController1(view)
# Show the View
view.show()
# Start the App event loop
app.exec()
