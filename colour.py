from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPalette, QColor

# Custom widget class called 'Colour' inheriting from base QWidget class
class Colour(QWidget):

    def __init__(self, colour):
        super(Colour, self).__init__()
        # Tells the widget to automatically fill widget background with window colour
        self.setAutoFillBackground(True)

        # Creating new temp palette called self.palette = global desktop palette (by default)
        palette = self.palette()
        # Color role = enum of different symbolic colors used in current GUI (for example ColorRole.Window may be a type of grey)
        # Setting Window color to given parameter 'colour'
        palette.setColor(QPalette.ColorRole.Window, QColor(colour))
        # Set widget palette to a new widget with new colour role
        self.setPalette(palette)