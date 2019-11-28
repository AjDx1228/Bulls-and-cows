from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt
import sqlite3

from DataBase import HistoryDataBase


class History(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('History.ui',self)

        self.init_table()

        self.clear_history.clicked.connect(self.clear_history_in_db)

    def init_table(self):
        self.table = HistoryDataBase()
        self.table.connect()
        cur = self.table.get_all()

        rows_count = self.table.get_rows_count()
        self.history_tableWidget.setRowCount(rows_count)

        for row, form in enumerate(cur):
            for column, item in enumerate(form):
                self.history_tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

        self.table.close()

    def clear_history_in_db(self):
        self.table = HistoryDataBase()
        self.table.connect()

        self.table.action_of_clear_history()
        self.history_tableWidget.clear()
        self.history_tableWidget.setHorizontalHeaderLabels(["Кол-во попыток", "Сложность", "Время"])
        self.history_tableWidget.setRowCount(0)

        self.table.close()

        