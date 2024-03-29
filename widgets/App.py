import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Game import Game
from History import History
from Instruction import Instruction


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set UI file
        filename = '../ui/App.ui'

        uic.loadUi(filename, self)

        # Connect handlers of buttons
        self.play_btn.clicked.connect(self.show_game)
        self.how_to_play_btn.clicked.connect(self.show_how_to_play)

        # Set initial settings
        self.set_design_of_main_menu()
        self.set_background_menu()
        self.initUI()

    # Set fixed size of the window
    def initUI(self):
        self.setFixedSize(1147, 655)

    # Set background of the window
    def set_background_menu(self):
        img = QPixmap('../images/background_menu.jpg')
        self.background_menu.setPixmap(img)

    # Show window of the game
    def show_game(self):
        game_widget = Game()
        self.setCentralWidget(game_widget)

    # Show window of the history
    def show_history(self):
        history_widget = History()
        self.setCentralWidget(history_widget)

    # Show window of the instruction
    def show_how_to_play(self):
        self.instruction_widget = Instruction()
        self.setCentralWidget(self.instruction_widget)
    
    # Set design of the window
    def set_design_of_main_menu(self):
        Yandex_icon_img = QPixmap('../images/yandex.png')
        self.Yandex_icon.setPixmap(Yandex_icon_img)

        img_cow = QPixmap('../images/cow.png')
        self.cow_img.setPixmap(img_cow)

        img_bull = QPixmap('../images/bull.png')
        self.bull_img.setPixmap(img_bull)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
    