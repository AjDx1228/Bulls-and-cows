from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QPixmap
import sqlite3
import time

import util
from DataBase import HistoryDataBase
from constants import DIFFICULTY_LEVELS, DIFFICULTY_LITERALS

class Game(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('Game.ui',self)

        # Connect handlers of buttons
        self.start_game_btn.clicked.connect(self.start_game)
        self.guess_btn.clicked.connect(self.guess_number)
        self.finish_game_btn.clicked.connect(self.finish_game)

        # Connect handlers of inputs
        self.input_choice.textChanged.connect(self.change_input)
        self.difficulty_select.currentTextChanged.connect(self.set_difficulty_level)

        # Set initial settings
        self.set_difficulty_level()
        self.screen_of_game.setVisible(False)
        self.finish_game_btn.setEnabled(False)

    def set_difficulty_level(self):
        index = self.difficulty_select.currentIndex()
        self.variable_numbers, self.digit_capacity = DIFFICULTY_LEVELS[index]
        self.complexity = DIFFICULTY_LITERALS[index]

        str_of_varable_numbers = ', '.join(self.variable_numbers)
        self.variable_numbers_label.setText(str_of_varable_numbers)
        self.digit_capacity_label.setText(str(self.digit_capacity))

    def start_game(self):
        # Set initial UI settings
        self.start_game_btn.setEnabled(False)
        self.screen_of_game.setVisible(True)
        self.difficulty_select.setEnabled(False)
        self.finish_game_btn.setEnabled(True)
        self.input_choice.setText('')
        self.action_label.setText('Попробуйте угадать число')

        self.win_img.setVisible(False)
        self.tableWidget.setEnabled(True)

        self.set_design_of_result_area()
        self.random_digit = util.get_random_digit(self.variable_numbers, self.digit_capacity)

        self.n_rows = 1
        self.attempts = 0

        self.time_start = time.time()

        self.bull_label.setText('0')
        self.cow_label.setText('0')
        self.action_setHorizontalHeaderLabels()
        
    def finish_game(self):
        # Set initial UI settings
        self.screen_of_game.setVisible(False)
        self.difficulty_select.setEnabled(True)
        self.start_game_btn.setEnabled(True)
        self.finish_game_btn.setEnabled(False)  
        self.tableWidget.setEnabled(False)
        self.win_img.setText('')
        self.action_label.setText('Давай поиграем еще?')

        self.tableWidget.clear()
        self.action_setHorizontalHeaderLabels()
        self.tableWidget.setRowCount(0)
        self.n_rows == 0

    def set_design_of_result_area(self):
        image_X = QPixmap('X_img.png')
        self.X_img.setPixmap(image_X)
        self.X_img2.setPixmap(image_X)
        
        img_cow = QPixmap('cow.png')
        self.cow_img.setPixmap(img_cow)

        img_bull = QPixmap('bull.png')
        self.bull_img.setPixmap(img_bull)

    def change_input(self, text):
        if self.input_choice.text() != '' and len(str(self.input_choice.text())) == self.digit_capacity:
            self.guess_btn.setEnabled(True)
        else:
            self.guess_btn.setEnabled(False)

        if len(text) > self.digit_capacity:
            self.input_choice.setText(text[:-1])
            return
        
        res = ''

        for i in range(0, len(text)):
            if text[i] not in text[:i] and text[i] in self.variable_numbers:
                res += text[i]

        self.input_choice.setText(res)
  
    def guess_number(self):
        self.choice = self.input_choice.text()
        self.bull_count = 0
        self.cow_count = 0

        self.attempts += 1

        for i in range(self.digit_capacity):
            if self.choice[i] == self.random_digit[i]:
                self.bull_count += 1
                continue

            if self.choice[i] in self.random_digit:
                self.cow_count += 1

        self.set_value_table()
    
        if self.bull_count == self.digit_capacity:
            self.win()
  
        self.bull_label.setText(str(self.bull_count))
        self.cow_label.setText(str(self.cow_count))
        self.input_choice.setText('')
    
    def keyPressEvent(self, event):
        if event.key() - Qt.Key_Enter == -1 and self.guess_btn.isEnabled():
            self.guess_number()
        event.accept()
    
    def action_setHorizontalHeaderLabels(self):
        self.tableWidget.setHorizontalHeaderLabels(["Число", "Быки", "Коровы"])
    
    def win(self):
        history_table = HistoryDataBase()
        history_table.connect()

        self.finish_time = time.time()
        self.time = self.finish_time - self.time_start
        self.time = float('{:.2f}'.format(self.time))

        history_table.add_item(self.attempts, self.complexity, self.time)
        history_table.close()

        self.action_label.setText('Ты выиграл! Поиграем еще?')
        self.screen_of_game.setVisible(False)
        self.finish_game_btn.setEnabled(False)
        self.start_game_btn.setEnabled(True)
        self.difficulty_select.setEnabled(True)

        self.win_img.setVisible(True)

        img_of_win = QPixmap('img_when_win.png')
        self.win_img.setPixmap(img_of_win)

        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

        self.n_rows == 0

        self.tableWidget.setEnabled(False)

        self.action_setHorizontalHeaderLabels()

    
    def set_value_table(self):
        self.tableWidget.setRowCount(self.n_rows)

        self.tableWidget.setItem(self.n_rows - 1, 0, QTableWidgetItem(str(self.choice)))
        self.tableWidget.setItem(self.n_rows - 1, 1, QTableWidgetItem(str(self.bull_count)))
        self.tableWidget.setItem(self.n_rows - 1, 2, QTableWidgetItem(str(self.cow_count)))

        self.n_rows += 1