from PySide6.QtWidgets import QLabel, QDialog, QGridLayout, QLineEdit, QDialogButtonBox

import hashlib

from nomad_camels.ui_widgets.warn_popup import WarnPopup


class Password_Dialog(QDialog):
    """
    Dialog to enter a password or create a new one.
    If double_pass is True or compare_hash is None, after accepting the dialog, the entered password can be accessed via the password attribute.

    Parameters
    ----------
    parent : QWidget
        Parent widget.
    double_pass : bool, optional
        Whether to ask for a password twice, by default False.
        Use this, if the user should create a new password.
    compare_hash : str, optional
        Hashed password to compare with, by default None.
        Use this, if the entered password should be compared directly.
    """

    def __init__(self, parent=None, double_pass=False, compare_hash=None):
        super().__init__(parent)
        self.compare_hash = compare_hash
        self.setWindowTitle("Enter Password - NOMAD CAMELS")
        self.double_pass = double_pass
        # if double_pass:
        self.label_text = QLabel("Enter password:")
        # else:
        #     self.label_text = QLabel('Enter password to save changes:')
        self.label_2 = QLabel("Confirm password:")
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password_2 = QLineEdit()
        self.lineEdit_password_2.setEchoMode(QLineEdit.Password)

        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label_text, 0, 0)
        self.layout.addWidget(self.lineEdit_password, 0, 1)
        if double_pass:
            self.layout.addWidget(self.label_2, 1, 0)
            self.layout.addWidget(self.lineEdit_password_2, 1, 1)
        self.layout.addWidget(self.buttonbox, 2, 0, 1, 2)
        self.setLayout(self.layout)

        self.password = None

    def accept(self):
        if self.double_pass:
            if self.lineEdit_password.text() == self.lineEdit_password_2.text():
                self.password = self.lineEdit_password.text()
                return super().accept()
            else:
                self.lineEdit_password.setText("")
                self.lineEdit_password_2.setText("")
                WarnPopup(
                    text="Passwords did not match", title="Passwords did not match"
                )
                return
        password = self.lineEdit_password.text()
        if self.compare_hash:
            hashed_password = hash_password(password)
            if hashed_password != self.compare_hash:
                self.lineEdit_password.setText("")
                WarnPopup(
                    text="Incorrect password, please try again",
                    title="Incorrect password",
                )
                return
        else:
            self.password = self.lineEdit_password.text()
        return super().accept()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
