import sys

from PyQt6.QtWidgets import QApplication

from Event.EvenMarriageInterface import EventMarriage_Main_Interface

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EventMarriage_Main_Interface(1)
    ex.show()
    sys.exit(app.exec())