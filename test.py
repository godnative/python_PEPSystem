import sys

from PyQt6.QtWidgets import QApplication

from Event.EventBaptismInterFace import EventBaptism_Main_Interface
from Parishioner.Parishioner_Interface import Parishioner_Main_Interface
from family.family_interface import Family_Main_Interface

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EventBaptism_Main_Interface(1)
    ex.show()
    sys.exit(app.exec())
