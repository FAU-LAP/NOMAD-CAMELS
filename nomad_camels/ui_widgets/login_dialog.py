import sys
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QGridLayout, QDialogButtonBox

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username_label = QLabel("Username/email:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.username = None
        self.password = None

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(self.username_label, 0, 0)
        layout.addWidget(self.username_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.button_box, 2, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle('Enter Login')

    def accept(self):
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        super().accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.exec()
