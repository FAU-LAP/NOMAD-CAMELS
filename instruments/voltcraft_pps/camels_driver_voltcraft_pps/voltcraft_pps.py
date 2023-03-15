import copy

from PyQt5.QtWidgets import QLineEdit, QLabel, QComboBox

from CAMELS.main_classes import device_class

from .voltcraft_pps_ophyd import Voltcraft_PPS_EPICS, Voltcraft_PPS


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = ['voltcraft_pps.db', 'voltcraft_pps.proto']
        req = ['drvAsynSerialPort']
        super().__init__(name='voltcraft_pps', tags=['power supply', 'voltage'],
                         directory='voltcraft_pps', ophyd_device=Voltcraft_PPS_EPICS,
                         ophyd_class_name='Voltcraft_PPS_EPICS', files=files,
                         requirements=req, non_epics_class=Voltcraft_PPS,
                         **kwargs)

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


class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'Voltcraft PPS', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        self.comboBox_connection_type.addItem('EPICS: USB-serial')
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
