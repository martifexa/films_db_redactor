import sys
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QLabel, QRadioButton, QPushButton, QApplication, QWidget,
                             QGridLayout, QButtonGroup)


class Window(QWidget):
    def __init__(self):
        super().__init__()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    QtWidgets.QApplication.quit()
    # or QtWidgets.QApplication.exit(0)


sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())