from PyQt6.QtWidgets import QApplication

from user.User_Interface import User_Modify_Interface

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    school = {
        "school_id": 1,
        "school_name": "崇义小学"
    }
    user = {
        "user_id": 1,
        "user_name": "admin",
        "user_password": "admin",
        "user_type": 0,
        "user_authnum": 0,
        "user_note": ""
    }

    main_window = User_Modify_Interface(school, user, "User_Main_Interface")
    main_window.show()

    sys.exit(app.exec())
