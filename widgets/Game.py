from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QPixmap
import sqlite3
import time
import random

from DataBase import HistoryDataBase
from constants import DIFFICULTY_LEVELS, DIFFICULTY_LITERALS


class Game(QWidget):
    def __init__(self):
        super().__init__()

        # Set UI file 
        uic.loadUi('../ui/Game.ui', self)

        # Connect handlers of buttons
        self.start_game_btn.clicked.connect(self.start_game)
        self.guess_btn.clicked.connect(self.guess_number)
        self.finish_game_btn.clicked.connect(self.finish_game)
        self.history_btn.clicked.connect(self.show_history)
        self.how_to_play_btn.clicked.connect(self.show_how_to_play)
        self.draft_btn.clicked.connect(self.show_draft)

        # Connect handlers of inputs
        self.input_choice.textChanged.connect(self.change_input)
        self.difficulty_select.currentTextChanged.connect(self.set_difficulty_level)

        # Set initial settings
        self.set_difficulty_level()
        self.screen_of_game.setVisible(False)
        self.draft.setVisible(False)
        self.info_draft.setVisible(False)
        for i in range(10):
            exec('self.n{}.setVisible(False)'.format(i))
        self.set_background_game()

        self.count_finish = 1

    # Set background of the window
    def set_background_game(self):
        img = QPixmap('../images/background_game.jpg')
        self.background_game.setPixmap(img)

    # Show window of the history
    def show_history(self):
        self.parent().show_history()
    
    # Show window of the instruction
    def show_how_to_play(self):
        self.parent().show_how_to_play()
    
    # Get random digit
    def get_random_digit(self, variable_numbers, digit_capacity):
        variable_numbers = variable_numbers.copy()
        random_digit = ''

        for i in range(digit_capacity):
            random_number = random.choice(variable_numbers)
            random_number_index = variable_numbers.index(random_number)
            
            random_digit += str(random_number)
            del variable_numbers[random_number_index]

        return random_digit

    # Change diffculty of game
    def set_difficulty_level(self):
        index = self.difficulty_select.currentIndex()
        self.variable_numbers, self.digit_capacity = DIFFICULTY_LEVELS[index]
        self.complexity = DIFFICULTY_LITERALS[index]

        str_of_varable_numbers = ', '.join(self.variable_numbers)
        self.variable_numbers_label.setText(str_of_varable_numbers)
        self.digit_capacity_label.setText(str(self.digit_capacity))

    def start_game(self):
        # Set initial UI settings
        self.screen_of_game.setVisible(True)
        self.difficulty_select.setEnabled(False)
        self.finish_game_btn.setEnabled(True)
        self.input_choice.setText('')
        self.action_label.setText('Попробуйте угадать число')

        self.win_img.setVisible(False)
        self.draft.setVisible(True)
        self.tableWidget.setEnabled(True)
        self.history_btn.setVisible(False)
        self.how_to_play_btn.setVisible(False)
        self.start_game_btn.setVisible(False)

        self.set_design_of_result_area()

        self.random_digit = self.get_random_digit(self.variable_numbers, self.digit_capacity)

        self.n_rows = 1
        self.attempts = 0
        self.draft_visible = False

        self.count_finish = 0
        self.finish_game_btn.setText('Завершить игру')

        self.time_start = time.time()

        self.bull_label.setText('0')
        self.cow_label.setText('0')
        self.action_setHorizontalHeaderLabels()
        
    def finish_game(self):
        self.count_finish += 1
        # Exit button
        if self.count_finish == 1:
            self.finish_game_btn.setText('Выйти из игры')
        elif self.count_finish == 2:
            exit()

        # Set initial UI settings
        self.screen_of_game.setVisible(False)
        self.difficulty_select.setEnabled(True)
        self.tableWidget.setEnabled(False)
        self.draft.setVisible(False)
        self.win_img.setText('')
        Text = 'Твое число: {}.\n Давай поиграем еще?'
        self.action_label.setText(Text.format(self.random_digit))

        self.tableWidget.clear()
        self.action_setHorizontalHeaderLabels()
        self.tableWidget.setRowCount(0)
        self.n_rows == 0
        self.draft_visible = True
        self.show_draft()

        self.history_btn.setVisible(True)
        self.how_to_play_btn.setVisible(True)
        self.start_game_btn.setVisible(True)

    # Set design of the game
    def set_design_of_result_area(self):
        image_X = QPixmap('../images/X_img.png')
        self.X_img.setPixmap(image_X)
        self.X_img2.setPixmap(image_X)
        
        img_cow = QPixmap('../images/cow.png')
        self.cow_img.setPixmap(img_cow)

        img_bull = QPixmap('../images/bull.png')
        self.bull_img.setPixmap(img_bull)

    # Set characteristics of the input 
    def change_input(self, text):
        first_cond = self.input_choice.text() != ''
        sec_cond = len(str(self.input_choice.text())) == self.digit_capacity
        if first_cond and sec_cond:
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

    # Try to guess nubmer
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
    
    # Enter HotKey to try guess number
    def keyPressEvent(self, event):
        if event.key() - Qt.Key_Enter == -1 and self.guess_btn.isEnabled():
            self.guess_number()
        event.accept()
    
    # Set horizontal header labels of the table
    def action_setHorizontalHeaderLabels(self):
        self.tableWidget.setHorizontalHeaderLabels(["Число", "Быки", "Коровы"])
    
    # Output message if you win and add information about it in the table
    def win(self):
        self.finish_game_btn.setText('Выйти из игры')
        self.count_finish = 1
        history_table = HistoryDataBase()
        history_table.connect()

        self.finish_time = time.time()
        self.time = self.finish_time - self.time_start
        self.time = float('{:.2f}'.format(self.time))

        history_table.add_item(self.attempts, self.complexity, self.time)
        history_table.close()

        self.action_label.setText('Ты выиграл! Поиграем еще?')
        self.screen_of_game.setVisible(False)
        self.start_game_btn.setVisible(True)
        self.difficulty_select.setEnabled(True)
        self.history_btn.setVisible(True)
        self.how_to_play_btn.setVisible(True)

        self.win_img.setVisible(True)

        img_of_win = QPixmap('../images/img_when_win.png')
        self.win_img.setPixmap(img_of_win)

        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)

        self.n_rows == 0

        self.tableWidget.setEnabled(False)

        self.action_setHorizontalHeaderLabels()

        self.draft.setVisible(False)
        self.draft_visible = True
        self.show_draft()

    # Set value of the table
    def set_value_table(self):
        self.tableWidget.setRowCount(self.n_rows)

        n_rows_table = self.n_rows - 1
        self.tableWidget.setItem(n_rows_table, 0, QTableWidgetItem(str(self.choice)))
        self.tableWidget.setItem(n_rows_table, 1, QTableWidgetItem(str(self.bull_count)))
        self.tableWidget.setItem(n_rows_table, 2, QTableWidgetItem(str(self.cow_count)))

        self.n_rows += 1
    
    def visible_of_checkbox(self, flag):
        for i in self.variable_numbers:
            if not flag:
                exec('self.n{}.setChecked(False)'.format(i))
            exec('self.n{}.setVisible({})'.format(i, flag))
            self.draft_visible = flag

    def show_draft(self):
        if not self.draft_visible:
            line_of_numbers = '          '.join(self.variable_numbers)
            self.numbers_of_draft.setText(line_of_numbers)
            self.visible_of_checkbox(True)
            self.info_draft.setVisible(True)
            self.draft_btn.setText('Отключи, если мешает')
        
        else:
            line = ' ' * 95
            self.numbers_of_draft.setText(line)
            self.visible_of_checkbox(False)    
            self.info_draft.setVisible(False)
            self.draft_btn.setText('Включи помощника')
            