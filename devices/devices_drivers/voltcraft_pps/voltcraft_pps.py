import copy

from PyQt5.QtWidgets import QLineEdit, QLabel, QComboBox

from main_classes import device_class

from voltcraft_pps.voltcraft_pps_ophyd import Voltcraft_PPS


class subclass(device_class.Device):
    def __init__(self):
        files = ['voltcraft_pps.db', 'voltcraft_pps.proto']
        req = ['drvAsynSerialPort']
        super().__init__(name='voltcraft_pps', tags=['power supply', 'voltage'],
                         directory='voltcraft_pps', ophyd_device=Voltcraft_PPS,
                         ophyd_class_name='Voltcraft_PPS', files=files,
                         requirements=req)

    def get_channels(self):
        channels = copy.deepcopy(super().get_channels())
        conf = self.get_config()
        if 'outputMode' in conf:
            if conf['outputMode'] == 'voltage' or conf['outputMode'] == 0:
                for chan in channels:
                    if chan.endswith('setP'):
                        channels.pop(chan)
                        break
            else:
                for chan in channels:
                    if chan.endswith('setV'):
                        channels.pop(chan)
                        break
        return channels


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None):
        super().__init__(parent, 'Voltcraft PPS', data, settings_dict,
                         config_dict, ioc_dict)
        self.comboBox_connection_type.addItem('USB-serial')
        self.lineEdit_R = QLineEdit()
        self.lineEdit_R.setText(str(config_dict['setR']))
        self.labelR = QLabel('Resistance:')
        labelOutput = QLabel('Output mode:')

        modes = ['voltage', 'power']
        self.comboBox_output_mode = QComboBox()
        self.comboBox_output_mode.addItems(modes)
        if config_dict['outputMode'] in modes:
            self.comboBox_output_mode.setCurrentText(config_dict['outputMode'])
        self.comboBox_output_mode.currentTextChanged.connect(self.mode_change)

        self.layout().addWidget(labelOutput, 20, 0)
        self.layout().addWidget(self.comboBox_output_mode, 20, 1)
        self.layout().addWidget(self.labelR, 20, 2)
        self.layout().addWidget(self.lineEdit_R, 20, 3, 1, 2)

        self.mode_change()


    def mode_change(self):
        power = self.comboBox_output_mode.currentText() == 'power'
        self.labelR.setEnabled(power)
        self.lineEdit_R.setEnabled(power)

    def get_config(self):
        super().get_config()
        self.config_dict['outputMode'] = self.comboBox_output_mode.currentText()
        r = self.lineEdit_R.text()
        self.config_dict['setR'] = float(r) if r else 0
        return self.config_dict
