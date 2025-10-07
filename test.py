from PyQt6.QtWidgets import QApplication

from deceased_parishioner.deceased_parishioner_interface import Deceased_Parishioner_Main_Interface
from parish.parish_interface_new import Parish_Main_Interface

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login_info_1 = {
        "parish_id": 1,
        "parish_name": "崇义堂区",
        "user_id": 1,
        "user_name": "admin",
        "user_type": 1,
        "user_authnum": 32767
    }
    main_window = Deceased_Parishioner_Main_Interface(login_info_1, 'testParishioner_Main_Interface')
    # main_window.resize(1000, 800)
    main_window.show()


    sys.exit(app.exec())