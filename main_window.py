from PyQt5.QtWidgets import *
from tab_widget import TabWidget
import sys

# CSV format to save in the same file:
# Time wake up | Nb h sleep | Wake up w alarm (1: True, 0: False) |
# n h working (-1: no data, ) | How awake I am throughout the day (see habit_test)
# | Gym (1:True; 0:False, -1:not recorded)


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('- GUI improve your habits -')

    def initUI(self):
        self.tab_w = TabWidget(self)
        self.setCentralWidget(self.tab_w)
        self.show()


def main():
    app = QApplication(sys.argv)
    m = MainWin()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
