from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt
import sqlite3
from PyQt5.QtGui import QPixmap

from DataBase import HistoryDataBase
from constants import DIFFICULTY_LEVELS, DIFFICULTY_LITERALS


class History(QWidget):
    def __init__(self):
        super().__init__()

        # Set UI file
        uic.loadUi('../ui/History.ui', self)

        # Acton with table
        self.refresh_table()
        self.set_background_history()

        # Connect handlers of buttons
        self.clear_history.clicked.connect(self.clear_history_in_table)
        self.back_to_farm.clicked.connect(self.show_game)
        self.difficulty_select.currentTextChanged.connect(self.refresh_table)
        
    # Set background of the window
    def set_background_history(self):
        img = QPixmap('../images/background_history.jpg')
        self.background_history.setPixmap(img)
    
    # Show window of the game
    def show_game(self):
        self.parent().show_game()
    
    # Clear the table
    def clear_table(self):
        self.history_tableWidget.clear()
        self.ar_of_tble = ["Кол-во попыток", "Сложность", "Время"]
        self.history_tableWidget.setHorizontalHeaderLabels(self.ar_of_tble)
        self.history_tableWidget.setRowCount(0)

    # Reset table
    def refresh_table(self):
        self.table = HistoryDataBase()
        self.table.connect()

        index = self.difficulty_select.currentIndex()

        if index == 0:
            self.clear_table()
            cur = self.table.get_all()
            rows_count = self.table.get_rows_count()
        else:
            self.clear_table()
            complexity = DIFFICULTY_LITERALS[index - 1]
            cur = self.table.get_history_games(complexity)
            rows_count = self.table.get_rows_count_for_complexity(complexity)

        self.history_tableWidget.setRowCount(rows_count)

        for row, form in enumerate(cur):
            for column, item in enumerate(form):
                self.history_tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

        self.table.close()

    # Clear history in the table
    def clear_history_in_table(self):
        self.table = HistoryDataBase()
        self.table.connect()
        self.table.action_of_clear_history()

        self.clear_table()

        self.table.close()   
        