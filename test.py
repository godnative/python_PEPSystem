import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 QLineEdit Example')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Press Enter to print text:', self)
        layout.addWidget(self.label)

        self.line_edit = QLineEdit(self)
        self.line_edit.returnPressed.connect(self.on_return_pressed)
        layout.addWidget(self.line_edit)

        self.setLayout(layout)

    def on_return_pressed(self):
        text = self.line_edit.text()
        print(text)
        self.label.setText(f'You entered: {text}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())
