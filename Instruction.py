import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class Instruction(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('instruction.ui', self)

        self.OK_btn.clicked.connect(self.show_game)

        self.set_background_instruction()

    def set_background_instruction(self):
        self.background_instruction.setPixmap(QPixmap('background_instruction.jpg'))

    def show_game(self):
        self.parent().show_game()
