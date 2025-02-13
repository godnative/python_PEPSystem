import sys

from PyQt6.QtWidgets import QApplication

from Parishioner.Parishioner_Interface import Parishioner_Main_Interface

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Parishioner_Main_Interface()
    ex.show()
    sys.exit(app.exec())
