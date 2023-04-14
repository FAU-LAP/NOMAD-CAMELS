from nomad-camels.main_classes import device_class
from .demo_device_ophyd import Demo_Device

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='demo_device', virtual=True,
                         tags=['virtual', 'demo', 'ophyd', 'detector'],
                         ophyd_device=Demo_Device, ophyd_class_name='Demo_Device',
                         directory='demo_device', **kwargs)


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None, **kwargs):
        super().__init__(parent, 'Demo Device', data, settings_dict,
                         config_dict, ioc_dict, additional_info, **kwargs)
        self.table = QTableWidget()
        self.table.setRowCount(7)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['X', 'Y', 'Z'])
        self.table.setVerticalHeaderLabels(['mu', 'amplitude', 'sigma', 'motor noise level', 'detector noise level', 'motor delay', 'system delay'])
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.layout().addWidget(self.table, 10, 0, 1, 5)
        mus = settings_dict['mus'] if 'mus' in settings_dict else [0, 3, -4]
        amps = settings_dict['amps'] if 'amps' in settings_dict else [1, 2, 27]
        sigmas = settings_dict['sigmas'] if 'sigmas' in settings_dict else [5, 7, 0.1]
        detector_noises = settings_dict['detector_noises'] if 'detector_noises' in settings_dict else [0, 0, 0]
        motor_noises = settings_dict['motor_noises'] if 'motor_noises' in settings_dict else [0, 0, 0]
        set_delays = settings_dict['set_delays'] if 'set_delays' in settings_dict else [0, 0, 0]
        system_delays = settings_dict['system_delays'] if 'system_delays' in settings_dict else [0, 0, 0]
        for i, mu in enumerate(mus):
            item = QTableWidgetItem(str(mu))
            self.table.setItem(0, i, item)
        for i, amp in enumerate(amps):
            item = QTableWidgetItem(str(amp))
            self.table.setItem(1, i, item)
        for i, sigma in enumerate(sigmas):
            item = QTableWidgetItem(str(sigma))
            self.table.setItem(2, i, item)
        for i, motor_noise in enumerate(motor_noises):
            item = QTableWidgetItem(str(motor_noise))
            self.table.setItem(3, i, item)
        for i, detector_noise in enumerate(detector_noises):
            item = QTableWidgetItem(str(detector_noise))
            self.table.setItem(4, i, item)
        for i, set_delays in enumerate(set_delays):
            item = QTableWidgetItem(str(set_delays))
            self.table.setItem(5, i, item)
        for i, system_delays in enumerate(system_delays):
            item = QTableWidgetItem(str(system_delays))
            self.table.setItem(6, i, item)

    def get_settings(self):
        mus = []
        for i in range(3):
            mus.append(float(self.table.item(0, i).text()))
        self.settings_dict['mus'] = mus
        amps = []
        for i in range(3):
            amps.append(float(self.table.item(1, i).text()))
        self.settings_dict['amps'] = amps
        sigmas = []
        for i in range(3):
            sigmas.append(float(self.table.item(2, i).text()))
        self.settings_dict['sigmas'] = sigmas
        motor_noises = []
        for i in range(3):
            motor_noises.append(float(self.table.item(3, i).text()))
        self.settings_dict['motor_noises'] = motor_noises
        detector_noises = []
        for i in range(3):
            detector_noises.append(float(self.table.item(4, i).text()))
        self.settings_dict['detector_noises'] = detector_noises
        set_delays = []
        for i in range(3):
            set_delays.append(float(self.table.item(5, i).text()))
        self.settings_dict['set_delays'] = set_delays
        system_delays = []
        for i in range(3):
            system_delays.append(float(self.table.item(6, i).text()))
        self.settings_dict['system_delays'] = system_delays
        return super().get_settings()
