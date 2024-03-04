import os

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QGridLayout,
    QDialogButtonBox,
    QComboBox,
    QPushButton,
)
from PySide6.QtGui import QPixmap, Qt

from importlib import resources
from nomad_camels import graphics

from nomad_camels.utility import variables_handling

nomad_url = "https://nomad-lab.eu/prod/v1/staging/gui/analyze/apis"


class LoginDialog(QDialog):
    """UI widget to handle the login to NOMAD."""

    def __init__(self, parent=None):
        super().__init__(parent)

        info_label = QLabel(
            "We strongly recommend you to use NOMAD's app token for connecting.\nCopy the token from NOMAD (link below)."
        )

        oasis_url = ""
        if "NOMAD_URL" in variables_handling.preferences:
            oasis_url = variables_handling.preferences["NOMAD_URL"]

        self.comboBox_nomad_choice = QComboBox()
        self.comboBox_nomad_choice.addItems(["central NOMAD", "NOMAD Oasis"])

        self.pushButton_token = QPushButton("get the\ntoken!")
        self.pushButton_token.clicked.connect(self.open_token_link)

        if oasis_url:
            self.comboBox_nomad_choice.setCurrentText("NOMAD Oasis")

        self.label_oasis_url = QLabel("Oasis URL:")
        self.lineEdit_oasis_url = QLineEdit(oasis_url)

        self.label_logo = QLabel()
        self.label_logo.setAlignment(Qt.AlignCenter)

        self.label_info_oasis = QLabel(
            "Hint: You can set the URL for the Oasis also in the settings of CAMELS.\nCurrently we only support direct login for NOMAD Oasis via username/password.\nIf you use Single-Sing-On for your Oasis, you need to use NOMAD's app token."
        )
        self.label_auth_type = QLabel("Authentification-Type:")
        self.comboBox_auth_type = QComboBox()
        self.comboBox_auth_type.addItems(["user/password", "token"])
        self.comboBox_auth_type.setCurrentText("token")
        self.comboBox_auth_type.currentTextChanged.connect(self.change_login)

        self.username_label = QLabel("Username/email:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.label_token = QLabel("Authentication Token:")
        self.lineEdit_token = QLineEdit()
        self.lineEdit_token.setEchoMode(QLineEdit.Password)

        self.username = None
        self.password = None

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(self.comboBox_nomad_choice, 10, 0, 1, 2)
        layout.addWidget(self.label_oasis_url, 11, 0)
        layout.addWidget(self.lineEdit_oasis_url, 11, 1)
        layout.addWidget(self.label_logo, 12, 0)
        layout.addWidget(self.pushButton_token, 12, 1)

        layout.addWidget(self.label_info_oasis, 15, 0, 1, 2)

        layout.addWidget(info_label, 0, 0, 1, 2)
        layout.addWidget(self.label_auth_type, 1, 0)
        layout.addWidget(self.comboBox_auth_type, 1, 1)

        layout.addWidget(self.username_label, 5, 0)
        layout.addWidget(self.username_input, 5, 1)
        layout.addWidget(self.password_label, 6, 0)
        layout.addWidget(self.password_input, 6, 1)

        layout.addWidget(self.label_token, 7, 0)
        layout.addWidget(self.lineEdit_token, 7, 1)

        layout.addWidget(self.button_box, 20, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("Log in to NOMAD")
        self.change_login()
        self.url = None
        self.token = None

        self.comboBox_nomad_choice.currentTextChanged.connect(self.change_login)

    def open_token_link(self):
        if self.comboBox_nomad_choice.currentText() == "NOMAD Oasis":
            path = self.lineEdit_oasis_url.text()
            if "/api/" in path:
                path = path.split("/api/")[0]
            if "/gui/" in path:
                path = path.split("/gui/")[0]
            if path.endswith("/"):
                path = path[:-1]
            path = f"{path}/gui/analyze/apis"
        else:
            path = nomad_url
        os.startfile(path)

    def accept(self):
        oasis = self.comboBox_nomad_choice.currentText() == "NOMAD Oasis"
        use_token = self.comboBox_auth_type.currentText() == "token"
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        if oasis:
            self.url = self.lineEdit_oasis_url.text()
        if use_token:
            self.token = self.lineEdit_token.text()
            if "Bearer%20" in self.token:
                self.token = self.token.split("Bearer%20")[-1]
            self.token = self.token.replace('"', "")
        super().accept()

    def change_login(self):
        oasis = self.comboBox_nomad_choice.currentText() == "NOMAD Oasis"
        image = QPixmap()
        if oasis:
            image.load(str(resources.files(graphics) / "oasis-horizontal.png"))
        else:
            image.load(str(resources.files(graphics) / "nomad-horizontal.png"))
        self.label_logo.setPixmap(image)

        self.label_oasis_url.setHidden(not oasis)
        self.lineEdit_oasis_url.setHidden(not oasis)
        # self.comboBox_auth_type.setHidden(not oasis)
        # self.label_auth_type.setHidden(not oasis)
        self.label_info_oasis.setHidden(not oasis)

        use_token = self.comboBox_auth_type.currentText() == "token"
        self.username_input.setHidden(use_token)
        self.username_label.setHidden(use_token)
        self.password_input.setHidden(use_token)
        self.password_label.setHidden(use_token)
        self.label_token.setHidden(not use_token)
        self.lineEdit_token.setHidden(not use_token)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.exec()
