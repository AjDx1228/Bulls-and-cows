import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from Game import Game
from History import History
from Instruction import Instruction

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('App.ui', self)

        self.play_btn.clicked.connect(self.show_game)
        self.history_btn.clicked.connect(self.show_history)
        self.how_to_play_btn.clicked.connect(self.show_how_to_play)

        self.set_design_of_main_menu()
    
    def show_game(self):
        game_widget = Game()
        self.setCentralWidget(game_widget)

    def show_history(self):
        history_widget = History()
        self.setCentralWidget(history_widget)
    
    def show_how_to_play(self):
        self.instruction_widget = Instruction()
        self.setCentralWidget(self.instruction_widget)
    
    def set_design_of_main_menu(self):
        Yandex_icon_img = QPixmap('yandex.png')
        self.Yandex_icon.setPixmap(Yandex_icon_img)

        img_cow = QPixmap('cow.png')
        self.cow_img.setPixmap(img_cow)

        img_bull = QPixmap('bull.png')
        self.bull_img.setPixmap(img_bull)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())