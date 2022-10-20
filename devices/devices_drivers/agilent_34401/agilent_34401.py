from agilent_34401.agilent_34401_ophyd import Agilent_34401

from main_classes import device_class

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = ['agilent_34401.db', 'agilent_34401.proto']
        req = ['prologixSup']
        super().__init__(name='agilent_34401', virtual=False, tags=['DMM', 'voltage', 'current'], directory='agilent_34401', ophyd_device=Agilent_34401, requirements=req, files=files, ophyd_class_name='Agilent_34401', **kwargs)

class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'Agilent 34401', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        self.comboBox_connection_type.addItem('EPICS: prologix-GPIB')
        self.sub_widget = subclass_config_sub(config_dict=self.config_dict, parent=self)
        self.layout().addWidget(self.sub_widget, 20, 0, 1, 5)
        self.load_settings()

    def get_config(self):
        super().get_config()
        return self.sub_widget.get_config()


class subclass_config_sub(device_class.Device_Config_Sub):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(parent=parent, settings_dict=settings_dict,
                         config_dict=config_dict)
        self.config_dict = config_dict
        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        label = QLabel('# PLC')
        self.lineEdit_nPLC = QLineEdit('1')
        if 'nPLC' in config_dict:
            self.lineEdit_nPLC.setText(str(config_dict['nPLC']))

        layout.addWidget(label, 0, 0)
        layout.addWidget(self.lineEdit_nPLC, 0, 1)

    def get_config(self):
        self.config_dict['nPLC'] = int(float(self.lineEdit_nPLC.text()))
        return {}
        return self.config_dict
