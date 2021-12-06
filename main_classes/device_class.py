from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QFont

class Device:
    """general class for all devices"""
    def __init__(self):
        self.__save_dict__ = {}

class Device_Config(QWidget):
    """Parent class for the configuration-widgets (shown on the frontpanel) of the devices.
    Arguments:
        - parent: handed to QWidget, usually the MainApp.
        - device_name: name of the device for the title of the widget.
        - data: data from the treeView_devices. It is needed to connect the settings to the correct device.
        - settings_dict: all the current settings of the device."""
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
        """Called when the comboBox_connection_type is changed. Switches to another connector-widget to specify things like the Address of the device."""
        if self.comboBox_connection_type.currentText() == 'prologix-GPIB':
            self.connector = Prologix_Config()
            self.layout().addWidget(self.connector, 2, 0, 1, 2)

    def get_settings(self):
        """Updates the settings_dict with the current settings.
        Overwrite this function for each device to specify the settings. It is recommended to still call the parent for the connection-settings."""
        self.settings_dict.update({'connection': {'type': self.comboBox_connection_type.currentText()}})
        self.settings_dict['connection'].update(self.connector.get_settings())
        return self.settings_dict

    def load_settings(self):
        """Loads the settings from the settings_dict. Depending on the connection-type, the correct widget is set and the settings entered.
        Overwrite this function (and call it) for the specific settings."""
        if 'connection' in self.settings_dict:
            self.comboBox_connection_type.setCurrentText(self.settings_dict['connection']['type'])
            self.connector.load_settings(self.settings_dict['connection'])


class Prologix_Config(QWidget):
    """Widget for the settings when the connection is via a Prologix GPIB-Ethernet adapter."""
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
        """Returns the set IP-Address and GPIB-Address."""
        return {'IP-Address': self.lineEdit_ip.text(),
                'GPIB-Address': self.lineEdit_GPIB.text()}

    def load_settings(self, settings_dict):
        """Loads the settings_dict, specifically the IP-Address and the GPIB-Address."""
        if 'IP-Address' in settings_dict:
            self.lineEdit_ip.setText(settings_dict['IP-Address'])
        if 'GPIB-Address' in settings_dict:
            self.lineEdit_GPIB.setText(settings_dict['GPIB-Address'])