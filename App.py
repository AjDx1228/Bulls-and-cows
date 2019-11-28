import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, QVBoxLayout
from PyQt5.QtCore import Qt

from Game import Game
from History import History

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('App.ui', self)

        self.show_game()

        action_show_game = QAction(self)
        action_show_game.triggered.connect(self.show_game)
        action_show_history = QAction(self)
        action_show_history.triggered.connect(self.show_history)

        self.game_menu.addAction(action_show_game)
        self.history_menu.addAction(action_show_history)
    
    def show_game(self):
        self.game_widget = Game()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.game_widget)
        self.setCentralWidget(widget)

    def show_history(self):
        self.history_widget = History()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.history_widget)
        self.setCentralWidget(widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())