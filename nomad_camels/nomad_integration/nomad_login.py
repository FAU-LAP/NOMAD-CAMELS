from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QGridLayout, QDialogButtonBox, QComboBox
from PySide6.QtGui import QPixmap, Qt

from pkg_resources import resource_filename

from nomad_camels.utility import variables_handling


class LoginDialog(QDialog):
    """UI widget to handle the login to NOMAD."""
    def __init__(self, parent=None):
        super().__init__(parent)

        oasis_url = ''
        if 'NOMAD_URL' in variables_handling.preferences:
            oasis_url = variables_handling.preferences['NOMAD_URL']

        self.comboBox_nomad_choice = QComboBox()
        self.comboBox_nomad_choice.addItems(['central NOMAD', 'NOMAD Oasis'])

        if oasis_url:
            self.comboBox_nomad_choice.setCurrentText('NOMAD Oasis')

        self.label_oasis_url = QLabel('Oasis URL:')
        self.lineEdit_oasis_url = QLineEdit(oasis_url)

        self.label_logo = QLabel()
        self.label_logo.setAlignment(Qt.AlignCenter)

        self.label_info_oasis = QLabel('Hint: You can set the URL for the Oasis also in the settings of CAMELS.\nCurrently we only support direct login for NOMAD Oasis via username/password.\nIf you use Single-Sing-On for your Oasis, copy the authorization token from your browser.')
        self.label_auth_type = QLabel('Authentification-Type:')
        self.comboBox_auth_type = QComboBox()
        self.comboBox_auth_type.addItems(['user/password', 'token'])
        self.comboBox_auth_type.currentTextChanged.connect(self.change_login)

        self.username_label = QLabel("Username/email:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.label_token = QLabel('Authentification Token:')
        self.lineEdit_token = QLineEdit()

        self.username = None
        self.password = None

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(self.comboBox_nomad_choice, 0, 0, 1, 2)
        layout.addWidget(self.label_oasis_url, 1, 0)
        layout.addWidget(self.lineEdit_oasis_url, 1, 1)
        layout.addWidget(self.label_logo, 2, 0, 1, 2)

        layout.addWidget(self.label_info_oasis, 5, 0, 1, 2)
        layout.addWidget(self.label_auth_type, 6, 0)
        layout.addWidget(self.comboBox_auth_type, 6, 1)

        layout.addWidget(self.username_label, 10, 0)
        layout.addWidget(self.username_input, 10, 1)
        layout.addWidget(self.password_label, 11, 0)
        layout.addWidget(self.password_input, 11, 1)

        layout.addWidget(self.label_token, 13, 0)
        layout.addWidget(self.lineEdit_token, 13, 1)

        layout.addWidget(self.button_box, 20, 0, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle('Log in to NOMAD')
        self.change_login()
        self.url = None
        self.token = None

        self.comboBox_nomad_choice.currentTextChanged.connect(self.change_login)


    def accept(self):
        oasis = self.comboBox_nomad_choice.currentText() == 'NOMAD Oasis'
        use_token = self.comboBox_auth_type.currentText() == 'token'
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        if oasis:
            self.url = self.lineEdit_oasis_url.text()
        if oasis and use_token:
            self.token = self.lineEdit_token.text()
            if 'Bearer%20' in self.token:
                self.token = self.token.split('Bearer%20')[-1]
            self.token = self.token.replace('"', '')
        super().accept()

    def change_login(self):
        oasis = self.comboBox_nomad_choice.currentText() == 'NOMAD Oasis'
        image = QPixmap()
        if oasis:
            image.load(resource_filename('nomad_camels', 'graphics/oasis-horizontal.png'))
        else:
            image.load(resource_filename('nomad_camels', 'graphics/nomad-horizontal.png'))
        self.label_logo.setPixmap(image)

        self.label_oasis_url.setHidden(not oasis)
        self.lineEdit_oasis_url.setHidden(not oasis)
        self.comboBox_auth_type.setHidden(not oasis)
        self.label_auth_type.setHidden(not oasis)
        self.label_info_oasis.setHidden(not oasis)

        use_token = self.comboBox_auth_type.currentText() == 'token'
        self.username_input.setHidden(oasis and use_token)
        self.username_label.setHidden(oasis and use_token)
        self.password_input.setHidden(oasis and use_token)
        self.password_label.setHidden(oasis and use_token)
        self.label_token.setHidden(not oasis or not use_token)
        self.lineEdit_token.setHidden(not oasis or not use_token)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.exec()
