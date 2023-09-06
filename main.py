from PySide6.QtWidgets import QApplication
from main_window import MainWindow

import sys

app = QApplication(sys.argv)

window = MainWindow()

#Render window
window.show()

#Start the event loop
app.exec()