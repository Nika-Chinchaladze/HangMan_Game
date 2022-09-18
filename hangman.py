from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QRegExpValidator, QPixmap
from PyQt5.QtCore import QRegExp
from PyQt5 import uic
from random import choice
import Actor_Names as an

class Chincharito(QMainWindow):
    def __init__(self):
        super(Chincharito, self).__init__()

        uic.loadUi("hang.ui", self)

        # define content:
        self.head_label = self.findChild(QLabel, "head_label")
        self.word_label = self.findChild(QLabel, "word_label")
        self.image_label = self.findChild(QLabel, "image_label")
        self.answer_label = self.findChild(QLabel, "answer_label")
        self.check_button = self.findChild(QPushButton, "check_button")
        self.close_button = self.findChild(QPushButton, "close_button")
        self.start_button = self.findChild(QPushButton, "start_button")
        self.restart_button = self.findChild(QPushButton, "restart_button")
        self.letter_line = self.findChild(QLineEdit, "letter_line")
        self.check_button.setEnabled(False)
        self.restart_button.setEnabled(False)

        # define some validators:
        allowed = QRegExp("[a-z-A-Z_]+")
        boom = QRegExpValidator(allowed)
        self.letter_line.setValidator(boom)

        # meaningful variables:
        self.stages = ["seventh.jpg", "sixth.jpg", "fifth.jpg", "fourth.jpg", "third.jpg", "second.jpg"]

        # call defined methods from here:
        self.start_button.clicked.connect(self.Start_Game)
        self.restart_button.clicked.connect(self.Restart_Game)
        self.close_button.clicked.connect(lambda: self.close())
        self.check_button.clicked.connect(self.Check_Word)

        self.show()

# ------------------------------------- logic ------------------------------------ #
    # define colors:
    def Green(self):
        self.answer_label.setStyleSheet("background-color: rgb(155, 255, 184)")
    def Red(self):
        self.answer_label.setStyleSheet("background-color: rgb(255, 178, 216)")
    def White(self):
        self.answer_label.setStyleSheet("background-color: rgb(240, 240, 240)")

    # define method for start button:
    def Start_Game(self):
        self.display = []
        self.life = 6
        self.place = 5
        self.chosen_actor = choice(an.Word_List)
        self.length = len(self.chosen_actor)
        for i in self.chosen_actor:
            self.display.append("_")
        self.word_label.setText(f"{self.display}")
        self.check_button.setEnabled(True)
        self.start_button.setEnabled(False)
    
    def Restart_Game(self):
        self.display = []
        self.life = 6
        self.place = 5
        self.chosen_actor = choice(an.Word_List)
        self.length = len(self.chosen_actor)
        for i in self.chosen_actor:
            self.display.append("_")
        self.word_label.setText(f"{self.display}")
        self.image_label.setPixmap(QPixmap("first.jpg"))
        self.answer_label.setText("")
        self.White()
        self.check_button.setEnabled(True)

    
    # define method for check button:
    def Check_Word(self):
        letter = self.letter_line.text()
        letter = letter.upper()
        if len(letter) == 1:
            for position in range(self.length):
                if letter == self.chosen_actor[position]:
                    self.display[position] = letter
                    self.answer_label.setText("Good Job, You Hit the Target!")
                    self.Green()

            if letter not in self.chosen_actor:
                self.life -= 1
                self.answer_label.setText(f"{letter} - wrong letter, you left {self.life} lives!")
                self.image_label.setPixmap(QPixmap(self.stages[self.place]))
                self.place -= 1
                self.Red()
                if self.life == 0:
                    self.answer_label.setText("You Have Just Killed an Innocent Man!")
                    self.check_button.setEnabled(False)
                    self.restart_button.setEnabled(True)
                    self.Red()

            self.word_label.setText(f"{self.display}")
            self.letter_line.setText("")

            if "_" not in self.display:
                self.answer_label.setText("Congratulations, You Have Just Saved Human's Life!")
                self.word_label.setText(f"<font color='blue'><b>GUESSED NAME:</b></font color> {self.chosen_actor}")
                self.image_label.setPixmap(QPixmap("freedom.jpg"))
                self.check_button.setEnabled(False)
                self.restart_button.setEnabled(True)
                self.Green()
            
            if self.answer_label.text() == "You Have Just Killed an Innocent Man!":
                self.word_label.setText(f"CORRECT NAME WAS: <font color='red'><b>{self.chosen_actor}</b></font color>")
        elif len(letter) > 1:
            self.answer_label.setText("Please Enter Only One Letter!")
            self.Red()
        elif len(letter) == 0:
            self.answer_label.setText("Please Fill Letter Field!")
            self.Red()


# -------------------------------------- end ------------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    rito = Chincharito()
    sys.exit(app.exec_())