import copy

from keysight_e5270b.keysight_e5270b_ophyd import Keysight_E5270B
from keysight_e5270b.keysight_e5270b_config import Ui_keysight_e5270b_config
from keysight_e5270b.keysight_e5270b_config_channel import Ui_keysight_e5270b_config_channel

from main_classes import device_class
from utility.number_formatting import format_number
from utility.variables_handling import get_color

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal





class subclass(device_class.Device):
    def __init__(self):
        # package = importlib.import_module('keysight_e5270b.keysight_e5270b_ophyd')
        # ophyd_device = package.Keysight_E5270B
        files = ['keysight_e5270b.db', 'keysight_e5270b.proto']
        req = []
        super().__init__(name='keysight_e5270b', virtual=False, tags=['SMU', 'voltage', 'current'], directory='keysight_e5270b', ophyd_device=Keysight_E5270B, requirements=req, files=files, ophyd_class_name='Keysight_E5270B')
        for i in range(1, 9):
            key = f'active{i}'
            if key not in self.config:
                self.config[key] = False

    def get_config(self):
        config_dict = copy.deepcopy(self.config)
        removes = []
        for i in range(1, 9):
            if not self.config[f'active{i}']:
                for key in self.config:
                    if str(i) in key:
                        removes.append(key)
            else:
                removes.append(f'active{i}')
        for r in removes:
            config_dict.pop(r)
        return config_dict

    def get_channels(self):
        channels = copy.deepcopy(super().get_channels())
        removes = []
        for i in range(1, 9):
            if not self.config[f'active{i}']:
                for key in self.channels:
                    if key.endswith(str(i)):
                        removes.append(key)
        for r in removes:
            channels.pop(r)
        return channels


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, config_dict=None):
        super().__init__(parent, 'Keysight E5270B', data, settings_dict, config_dict)
        self.comboBox_connection_type.addItem('prologix-GPIB')
        self.sub_widget = subclass_config_sub(settings_dict=self.config_dict, parent=self)
        self.layout().addWidget(self.sub_widget, 20, 0, 1, 2)
        self.load_settings()

    def get_config(self):
        super().get_config()
        return self.sub_widget.get_settings()

class subclass_config_sub(QWidget, Ui_keysight_e5270b_config):
    def __init__(self, settings_dict=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.settings_dict = settings_dict

        self.adc_modes = {'Auto Mode': 0,
                          'Manual Mode': 1,
                          'PLC Mode': 2}
        adc_mode_values = list(self.adc_modes.values())
        adc_mode_keys = list(self.adc_modes.keys())
        self.comboBox_highResMode.addItems(self.adc_modes.keys())
        self.comboBox_highSpeedMode.addItems(self.adc_modes.keys())
        if 'speedADCmode' in settings_dict and settings_dict['speedADCmode'] in adc_mode_values:
            i = adc_mode_values.index(settings_dict['speedADCmode'])
            self.comboBox_highSpeedMode.setCurrentText(adc_mode_keys[i])
        else:
            self.comboBox_highSpeedMode.setCurrentText(adc_mode_keys[2])
        if 'resADCmode' in settings_dict and settings_dict['resADCmode'] in adc_mode_values:
            i = adc_mode_values.index(settings_dict['resADCmode'])
            self.comboBox_highResMode.setCurrentText(adc_mode_keys[i])
        else:
            self.comboBox_highResMode.setCurrentText(adc_mode_keys[2])

        if 'speedADCPLC' in settings_dict:
            self.lineEdit_highSpeedPLC.setText(str(settings_dict['speedADCPLC']))
        else:
            self.lineEdit_highSpeedPLC.setText('5')
        if 'resADCPLC' in settings_dict:
            self.lineEdit_highResPLC.setText(str(settings_dict['resADCPLC']))
        else:
            self.lineEdit_highResPLC.setText('5')

        self.channel_widgets = []
        for i, tab in enumerate([self.channel1, self.channel2, self.channel3, self.channel4, self.channel5, self.channel6, self.channel7, self.channel8]):
            sub_widget = subclass_config_channel(settings_dict, self, i+1)
            self.channel_widgets.append(sub_widget)
            tab.layout().addWidget(sub_widget)
            sub_widget.activate_sig.connect(lambda state, x=i: self.change_tab_color(state, x))
            sub_widget.activate()


    def change_tab_color(self, state, i):
        if state:
            col = get_color('black')
        else:
            col = get_color('grey')
        self.tabWidget.tabBar().setTabTextColor(i, col)

    def get_settings(self):
        for channel_widget in self.channel_widgets:
            channel_widget.get_settings()
        self.settings_dict['speedADCPLC'] = int(float(self.lineEdit_highSpeedPLC.text()))
        self.settings_dict['resADCPLC'] = int(float(self.lineEdit_highResPLC.text()))
        self.settings_dict['speedADCmode'] = self.adc_modes[self.comboBox_highSpeedMode.currentText()]
        self.settings_dict['resADCmode'] = self.adc_modes[self.comboBox_highResMode.currentText()]
        return self.settings_dict


class subclass_config_channel(QWidget, Ui_keysight_e5270b_config_channel):
    activate_sig = pyqtSignal(bool)

    def __init__(self, settings_dict=None, parent=None, number=1):
        super().__init__(parent)
        self.setupUi(self)
        self.settings_dict = settings_dict
        self.number = number

        if f'setADC{self.number}' in settings_dict:
            self.radioButton_highResADC.setChecked(True)
            if settings_dict[f'setADC{self.number}'] == 0:
                self.radioButton_highSpeedADC.setChecked(True)

        if f'currComp{self.number}' in settings_dict:
            self.lineEdit_currComp.setText(format_number(settings_dict[f'currComp{self.number}']))
        else:
            self.lineEdit_currComp.setText('0')

        if f'voltComp{self.number}' in settings_dict:
            self.lineEdit_voltComp.setText(format_number(settings_dict[f'voltComp{self.number}']))
        else:
            self.lineEdit_voltComp.setText('0')

        voltage_ranges = {'Auto Range': 0,
                          '0.5 V auto lim': 5,
                          '2 V auto lim': 20,
                          '5 V auto lim': 50,
                          '20 V auto lim': 200,
                          '40 V auto lim': 400,
                          '100 V auto lim': 1000,
                          '0.5 V fixed': -5,
                          '2 V fixed': -20,
                          '5 V fixed': -50,
                          '20 V fixed': -200,
                          '40 V fixed': -400,
                          '100 V fixed': -1000}
        self.voltage_ranges = voltage_ranges
        voltage_out_ranges = {}
        for v_range in voltage_ranges:
            if 'fixed' not in v_range:
                voltage_out_ranges.update({v_range: voltage_ranges[v_range]})

        current_ranges = {'Auto Range': 0,
                          '1 pA auto lim': 8,
                          '10 pA auto lim': 9,
                          '100 pA auto lim': 10,
                          '1 nA auto lim': 11,
                          '10 nA auto lim': 12,
                          '100 nA auto lim': 13,
                          '1 µA auto lim': 14,
                          '10 µA auto lim': 15,
                          '100 µA auto lim': 16,
                          '1 mA auto lim': 17,
                          '10 mA auto lim': 18,
                          '100 mA auto lim': 19,
                          '1 pA fixed': -8,
                          '10 pA fixed': -9,
                          '100 pA fixed': -10,
                          '1 nA fixed': -11,
                          '10 nA fixed': -12,
                          '100 nA fixed': -13,
                          '1 µA fixed': -14,
                          '10 µA fixed': -15,
                          '100 µA fixed': -16,
                          '1 mA fixed': -17,
                          '10 mA fixed': -18,
                          '100 mA fixed': -19}
        self.current_ranges = current_ranges
        current_out_ranges = {}
        for c_range in current_ranges:
            if 'fixed' not in c_range:
                current_out_ranges.update({c_range: current_ranges[c_range]})

        self.comboBox_voltRange.addItems(voltage_out_ranges.keys())
        self.comboBox_currRange.addItems(current_out_ranges.keys())
        self.comboBox_voltMeasRange.addItems(voltage_ranges.keys())
        self.comboBox_currMeasRange.addItems(current_ranges.keys())

        current_ranges_names = list(current_ranges.keys())
        current_ranges_values = list(current_ranges.values())
        voltage_ranges_names = list(voltage_ranges.keys())
        voltage_ranges_values = list(voltage_ranges.values())
        if f'VoutRange{self.number}' in settings_dict and settings_dict[f'VoutRange{self.number}'] in voltage_ranges_values:
            i = voltage_ranges_values.index(settings_dict[f'VoutRange{self.number}'])
            self.comboBox_voltRange.setCurrentText(voltage_ranges_names[i])
        else:
            self.comboBox_voltRange.setCurrentIndex(0)
        if f'IoutRange{self.number}' in settings_dict and settings_dict[f'IoutRange{self.number}'] in current_ranges_values:
            i = current_ranges_values.index(settings_dict[f'IoutRange{self.number}'])
            self.comboBox_currRange.setCurrentText(current_ranges_names[i])
        else:
            self.comboBox_currRange.setCurrentIndex(0)
        if f'VmeasRange{self.number}' in settings_dict and settings_dict[f'VmeasRange{self.number}'] in voltage_ranges_values:
            i = voltage_ranges_values.index(settings_dict[f'VmeasRange{self.number}'])
            self.comboBox_voltMeasRange.setCurrentText(voltage_ranges_names[i])
        else:
            self.comboBox_voltMeasRange.setCurrentIndex(0)
        if f'ImeasRange{self.number}' in settings_dict and settings_dict[f'ImeasRange{self.number}'] in current_ranges_values:
            i = current_ranges_values.index(settings_dict[f'ImeasRange{self.number}'])
            self.comboBox_currMeasRange.setCurrentText(current_ranges_names[i])
        else:
            self.comboBox_currMeasRange.setCurrentIndex(0)

        self.checkBox_outputFilter.setChecked(settings_dict[f'outputFilter{self.number}'] if f'outputFilter{self.number}' in settings_dict else False)

        if f'active{self.number}' in settings_dict:
            self.checkBox_channel_active.setChecked(settings_dict[f'active{self.number}'])
        self.checkBox_channel_active.clicked.connect(self.activate)

    def activate(self):
        active = self.checkBox_channel_active.isChecked()
        for child in self.children():
            if child is not self.checkBox_channel_active and child is not self.layout():
                child.setEnabled(active)
        self.activate_sig.emit(active)

    def get_settings(self):
        self.settings_dict[f'active{self.number}'] = float(self.checkBox_channel_active.isChecked())
        self.settings_dict[f'currComp{self.number}'] = float(self.lineEdit_currComp.text())
        self.settings_dict[f'voltComp{self.number}'] = float(self.lineEdit_voltComp.text())
        self.settings_dict[f'VoutRange{self.number}'] = self.voltage_ranges[self.comboBox_voltRange.currentText()]
        self.settings_dict[f'IoutRange{self.number}'] = self.current_ranges[self.comboBox_currRange.currentText()]
        self.settings_dict[f'VmeasRange{self.number}'] = self.voltage_ranges[self.comboBox_voltMeasRange.currentText()]
        self.settings_dict[f'ImeasRange{self.number}'] = self.current_ranges[self.comboBox_currMeasRange.currentText()]
        self.settings_dict[f'setADC{self.number}'] = int(self.radioButton_highResADC.isChecked())
        self.settings_dict[f'outputFilter{self.number}'] = int(self.checkBox_outputFilter.isChecked())
        return self.settings_dict
