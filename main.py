import sqlite3
import sys
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QLabel, QRadioButton, QPushButton, QApplication, QWidget,
                             QGridLayout, QButtonGroup, QMainWindow, QTableWidget, QTableWidgetItem, QComboBox)
from PyQt5 import uic


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.pushButton_add.clicked.connect(self.add)
        self.pushButton_delete.clicked.connect(self.delete)
        self.connection = sqlite3.connect("films.sqlite")
        self.update_table()

    def update_table(self):
        self.tableWidget.clear()
        base_query = "SELECT * FROM films"
        addition_query = self.lineEdit.text()
        query = base_query + " " + addition_query
        cursor = self.connection.cursor()
        data = cursor.execute(query).fetchall()

        query_genre = "SELECT * FROM genres"
        self.genres = cursor.execute(query_genre).fetchall()
        for i, line in enumerate(data):
            self.tableWidget: QTableWidget
            count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(count)
            for j, elem in enumerate(line):
                if j == 3:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(next(filter(lambda x: x[0] == elem, self.genres))[1])))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
    def add(self):
        self.add_windows = AddWindow(self.genres)
        self.add_windows.show()

    def delete(self):
        self.tableWidget: QTableWidget
        selected_items = self.tableWidget.selectedIndexes()
        rows = sorted(set(map(lambda t: t.row(), selected_items)), reverse=True)
        ids = list(map(lambda row: self.tableWidget.item(row, 0).text(), rows))
        cursor = self.connection.cursor()
        for id, row in zip(ids, rows):
            self.tableWidget.removeRow(row)
            cursor.execute(f"DELETE FROM films WHERE id={id}")
        self.connection.commit()


class AddWindow(QWidget):
    def __init__(self, genres):
        super().__init__()
        self.genres = genres
        uic.loadUi("add.ui", self)
        self.connection = sqlite3.connect("films.sqlite")
        self.pushButton_ok.clicked.connect(self.ok)
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.comboBox_genre : QComboBox
        self.comboBox_genre.addItems(map(lambda t: t[1], genres))

    def ok(self):
        pass

    def cancel(self):
        pass



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