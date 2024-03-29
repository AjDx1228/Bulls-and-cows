import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Instruction(QWidget):
    def __init__(self):
        super().__init__()

        # Set UI file
        uic.loadUi('../ui/instruction.ui', self)

        # Connect handlers of buttons
        self.OK_btn.clicked.connect(self.show_game)

        self.set_background_instruction()

    # Set background of the windows
    def set_background_instruction(self):
        img = QPixmap('../images/background_instruction.jpg')
        self.background_instruction.setPixmap(img)

    # Show window of the game
    def show_game(self):
        self.parent().show_game()
        