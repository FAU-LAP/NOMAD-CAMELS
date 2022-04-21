from keysight_e5270b.keysight_e5270b_ophyd import Keysight_E5270B
from keysight_e5270b.keysight_e5270b_config import Ui_keysight_e5270b_config

from main_classes import device_class
from utility.number_formatting import format_number

from PyQt5.QtWidgets import QWidget





class subclass(device_class.Device):
    def __init__(self):
        # package = importlib.import_module('keysight_e5270b.keysight_e5270b_ophyd')
        # ophyd_device = package.Keysight_E5270B
        files = ['keysight_e5270b.db', 'keysight_e5270b.proto']
        req = ['prologixSup']
        super().__init__(name='keysight_e5270b', virtual=False, tags=['SMU', 'voltage', 'current'], directory='keysight_e5270b', ophyd_device=Keysight_E5270B, requirements=req, files=files)
        self.ophyd_class_name = 'Keysight_E5270B'

class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None):
        super().__init__(parent, 'Keysight E5270B', data, settings_dict)
        self.comboBox_connection_type.addItem('prologix-GPIB')
        self.sub_widget = subclass_config_sub(settings_dict=settings_dict, parent=self)
        self.layout().addWidget(self.sub_widget, 3, 0, 1, 2)
        self.load_settings()

    def get_settings(self):
        super().get_settings()
        return self.sub_widget.get_settings()

class subclass_config_sub(QWidget, Ui_keysight_e5270b_config):
    def __init__(self, settings_dict=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.settings_dict = settings_dict

        if 'setADC1' in settings_dict:
            self.radioButton_highResADC.setChecked(True)
            if settings_dict['setADC1'] == 0:
                self.radioButton_highSpeedADC.setChecked(True)

        if 'currComp1' in settings_dict:
            self.lineEdit_currComp.setText(format_number(settings_dict['currComp1']))
        else:
            self.lineEdit_currComp.setText('0')

        if 'voltComp1' in settings_dict:
            self.lineEdit_voltComp.setText(format_number(settings_dict['voltComp1']))
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
        if 'VoutRange1' in settings_dict and settings_dict['VoutRange1'] in voltage_ranges_values:
            i = voltage_ranges_values.index(settings_dict['VoutRange1'])
            self.comboBox_voltRange.setCurrentText(voltage_ranges_names[i])
        else:
            self.comboBox_voltRange.setCurrentIndex(0)
        if 'IoutRange1' in settings_dict and settings_dict['IoutRange1'] in current_ranges_values:
            i = current_ranges_values.index(settings_dict['IoutRange1'])
            self.comboBox_currRange.setCurrentText(current_ranges_names[i])
        else:
            self.comboBox_currRange.setCurrentIndex(0)
        if 'VmeasRange1' in settings_dict and settings_dict['VmeasRange1'] in voltage_ranges_values:
            i = voltage_ranges_values.index(settings_dict['VmeasRange1'])
            self.comboBox_voltMeasRange.setCurrentText(voltage_ranges_names[i])
        else:
            self.comboBox_voltMeasRange.setCurrentIndex(0)
        if 'ImeasRange1' in settings_dict and settings_dict['ImeasRange1'] in current_ranges_values:
            i = current_ranges_values.index(settings_dict['ImeasRange1'])
            self.comboBox_currMeasRange.setCurrentText(current_ranges_names[i])
        else:
            self.comboBox_currMeasRange.setCurrentIndex(0)

        self.checkBox_outputFilter.setChecked(settings_dict['outputFilter1'] if 'outputFilter1' in settings_dict else False)

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

        self.radioButton_highResADC.clicked.connect(self.adc_switch)
        self.radioButton_highSpeedADC.clicked.connect(self.adc_switch)
        self.adc_switch()


    def adc_switch(self):
        check_val = self.radioButton_highResADC.isChecked()
        res = [self.label_resPLC, self.label_resMode, self.comboBox_highResMode, self.lineEdit_highResPLC]
        speed = [self.label_speedPLC, self.label_speedMode, self.comboBox_highSpeedMode, self.lineEdit_highSpeedPLC]
        for r in res:
            r.setEnabled(check_val)
        for s in speed:
            s.setEnabled(not check_val)

    def get_settings(self):
        self.settings_dict['currComp1'] = float(self.lineEdit_currComp.text())
        self.settings_dict['voltComp1'] = float(self.lineEdit_voltComp.text())
        self.settings_dict['VoutRange1'] = self.voltage_ranges[self.comboBox_voltRange.currentText()]
        self.settings_dict['IoutRange1'] = self.current_ranges[self.comboBox_currRange.currentText()]
        self.settings_dict['VmeasRange1'] = self.voltage_ranges[self.comboBox_voltMeasRange.currentText()]
        self.settings_dict['ImeasRange1'] = self.current_ranges[self.comboBox_currMeasRange.currentText()]
        self.settings_dict['setADC1'] = int(self.radioButton_highResADC.isChecked())
        self.settings_dict['outputFilter1'] = int(self.checkBox_outputFilter.isChecked())
        self.settings_dict['speedADCPLC'] = int(float(self.lineEdit_highSpeedPLC.text()))
        self.settings_dict['resADCPLC'] = int(float(self.lineEdit_highResPLC.text()))
        self.settings_dict['speedADCmode'] = self.adc_modes[self.comboBox_highSpeedMode.currentText()]
        self.settings_dict['resADCmode'] = self.adc_modes[self.comboBox_highResMode.currentText()]
        return self.settings_dict
