import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt

from Game import Game

class Instruction(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('instruction.ui', self)

        self.game_btn.clicked.connect(self.game_show)

    def game_show(self):
        self.game_widget = Game()
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(self.game_widget)
        self.setCentralWidget(widget)
