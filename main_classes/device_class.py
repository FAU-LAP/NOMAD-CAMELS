from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QFont

class Device:
    """general class for all devices"""
    def __init__(self):
        self.__save_dict__ = {}

class Device_Config(QWidget):
    def __init__(self, parent=None, device_name='', data='', settings_dict=None):
        super().__init__(parent)
        if settings_dict is None:
            settings_dict = {}
        self.data = data

        layout = QGridLayout()
        self.setLayout(layout)

        label_title = QLabel(f'{device_name} - Configuration')
        title_font = QFont('MS Shell Dlg 2', 10)
        title_font.setWeight(QFont.Bold)
        label_title.setFont(title_font)
        label_connection = QLabel('Connection-type:')
        self.comboBox_connection_type = QComboBox()
        self.connector = QWidget()
        layout.addWidget(label_title, 0, 0, 1, 2)
        layout.addWidget(label_connection, 1, 0)
        layout.addWidget(self.comboBox_connection_type, 1, 1)
        self.settings_dict = settings_dict
        self.comboBox_connection_type.currentTextChanged.connect(self.connection_type_changed)

    def connection_type_changed(self):
        if self.comboBox_connection_type.currentText() == 'prologix-GPIB':
            self.connector = Prologix_Config()
            self.layout().addWidget(self.connector, 2, 0, 1, 2)

    def get_settings(self):
        self.settings_dict.update({'connection': {'type': self.comboBox_connection_type.currentText()}})
        self.settings_dict['connection'].update(self.connector.get_settings())
        return self.settings_dict

    def load_settings(self):
        if 'connection' in self.settings_dict:
            self.comboBox_connection_type.setCurrentText(self.settings_dict['connection']['type'])
            self.connector.load_settings(self.settings_dict['connection'])


class Prologix_Config(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setLayout(layout)

        label_ip = QLabel('IP-Address:')
        label_GPIB = QLabel('GPIB-Address:')
        self.lineEdit_ip = QLineEdit()
        self.lineEdit_GPIB = QLineEdit()

        layout.addWidget(label_ip, 0, 0)
        layout.addWidget(label_GPIB, 1, 0)
        layout.addWidget(self.lineEdit_ip, 0, 1)
        layout.addWidget(self.lineEdit_GPIB, 1, 1)

    def get_settings(self):
        return {'IP-Address': self.lineEdit_ip.text(),
                'GPIB-Address': self.lineEdit_GPIB.text()}

    def load_settings(self, settings_dict):
        if 'IP-Address' in settings_dict:
            self.lineEdit_ip.setText(settings_dict['IP-Address'])
        if 'GPIB-Address' in settings_dict:
            self.lineEdit_GPIB.setText(settings_dict['GPIB-Address'])