from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem
from PyQt5 import QtGui
from PyQt5.uic import loadUi
from qtconsole.qtconsoleapp import QtCore
import sqlite3
import sys

db = sqlite3.connect("data.db")
cursor = db.cursor()
date = None

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("interface.ui", self)
        self.setWindowTitle("To-do App")
        self.setWindowIcon(QtGui.QIcon(r"assets\sparkle.png"))

        self.calendarWidget.selectionChanged.connect(self.get_date)
        self.saveButton.clicked.connect(self.save)
        self.addButton.clicked.connect(self.add_task)
        self.get_date()

    def get_date(self):
        global date
        date = self.calendarWidget.selectedDate().toPyDate()
        self.update_tasks()

    def update_tasks(self):
        self.listWidget.clear()

        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date, )
        results = cursor.execute(query, row).fetchall()

        for res in results:
            item = QListWidgetItem(str(res[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)

            if res[1] == 1:
                item.setCheckState(QtCore.Qt.Checked)
            elif res[1] == 0:
                item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)

    def add_task(self):
        new_task = str(self.lineEdit.text())

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (new_task, 0, date,)

        cursor.execute(query, row)
        db.commit()
        self.update_tasks()
        self.lineEdit.clear()

    def save(self, date):
        for idx in range(self.listWidget.count()):
            item = self.listWidget.item(idx)
            task = item.text()

            if item.setCheckState == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'No' WHERE task = ? AND date = ?"

            row = (task, date,)
            cursor.execute(query, row)
        db.commit()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())