from CAMELS.main_classes import device_class
from andor_newton.andor_newton_config import Ui_andor_newton_config
from andor_newton.andor_newton_ophyd import Andor_Newton

from PyQt5.QtWidgets import QTabWidget

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='andor_newton', virtual=False, tags=['SMU', 'voltage', 'current', 'resistance'], directory='keysight_b2912', ophyd_device=Keysight_B2912, ophyd_class_name='Keysight_B2912', **kwargs)
        for key, val in default_settings.items():
            self.config[f'{key}1'] = val
            self.config[f'{key}2'] = val

class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, config_dict=None, additional_info=None, **kwargs):
        super().__init__(parent, 'Keysight B2912', data, settings_dict=settings_dict, config_dict=config_dict, additional_info=additional_info, no_ioc_connection=True, **kwargs)
        self.comboBox_connection_type.addItem('EPICS: LAN')
        self.comboBox_connection_type.addItem('Local VISA')
        self.tab_widget = QTabWidget()
        conf1 = {}
        conf2 = {}
        for key, val in config_dict.items():
            if key.endswith('1'):
                conf1[key[:-1]] = val
            elif key.endswith('2'):
                conf2[key[:-1]] = val
        self.channel_widge_1 = subclass_config_sub(config_dict=conf1, parent=parent, settings_dict=settings_dict)
        self.channel_widge_2 = subclass_config_sub(config_dict=conf2, parent=parent, settings_dict=settings_dict)
        self.tab_widget.addTab(self.channel_widge_1, 'Channel 1')
        self.tab_widget.addTab(self.channel_widge_2, 'Channel 2')
        self.layout().addWidget(self.tab_widget, 20, 0, 1, 5)
        self.load_settings()

    def get_config(self):
        conf1 = self.channel_widge_1.get_config()
        conf2 = self.channel_widge_2.get_config()
        for key, val in conf1.items():
            self.config_dict[f'{key}1'] = val
        for key, val in conf2.items():
            self.config_dict[f'{key}2'] = val
        return super().get_config()


class subclass_config_sub(device_class.Device_Config_Sub, Ui_B2912_channel):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(parent=parent, config_dict=config_dict,
                         settings_dict=settings_dict)
        self.setupUi(self)

        self.sources = ['Voltage', 'Current']
        self.comboBox_source.addItems(self.sources)
        if 'source' in config_dict and config_dict['source'] in self.sources:
            self.comboBox_source.setCurrentText(config_dict['source'])

        self.low_terminals = ['Ground', 'Float']
        self.comboBox_low_terminal.addItems(self.low_terminals)
        if 'low_terminal' in config_dict and config_dict['low_terminal'] in self.low_terminals:
            self.comboBox_low_terminal.setCurrentText(config_dict['source'])

        self.ranges_voltage = ['2E-1 V', '2 V', '20 V', '200 V']
        self.ranges_current = ['1E-8 A', '1E-7 A', '1E-6 A', '1E-5 A', '1E-4 A', '1E-3 A', '1E-2 A', '1E-1 A', '1 A', '1.5 A', '3 A', '10 A']
        self.ranges_resistance = ['2 Ohm', '20 Ohm', '200 Ohm', '2E3 Ohm', '20E3 Ohm', '200E3 Ohm', '2E6 Ohm', '20E6 Ohm', '200E6 Ohm']

        if 'source_auto' in self.config_dict:
            self.checkBox_source_auto.setChecked(self.config_dict['source_auto'])
        else:
            self.checkBox_source_auto.setChecked(True)

        self.load_source_options()
        self.checkBox_source_auto.clicked.connect(self.load_source_options)
        self.comboBox_source.currentTextChanged.connect(self.load_source_options)

        if 'output_protection' in config_dict:
            self.checkBox_output_protection.setChecked(config_dict['output_protection'])
        if 'current_compliance' in config_dict:
            self.lineEdit_current_compliance.setText(str(config_dict['current_compliance']))
        else:
            self.lineEdit_current_compliance.setText('0.1')
        if 'voltage_compliance' in config_dict:
            self.lineEdit_voltage_compliance.setText(str(config_dict['voltage_compliance']))
        else:
            self.lineEdit_voltage_compliance.setText('2')

        if 'NPLC' in config_dict:
            self.lineEdit_NPLC.setText(str(config_dict['NPLC']))
        else:
            self.lineEdit_NPLC.setText('1')

        if 'four_wire_meas' in config_dict:
            self.checkBox_four_wire_meas.setChecked(config_dict['four_wire_meas'])
        if 'current_auto_range' in config_dict:
            self.checkBox_current_auto_range.setChecked(config_dict['current_auto_range'])
        if 'voltage_auto_range' in config_dict:
            self.checkBox_voltage_auto_range.setChecked(config_dict['voltage_auto_range'])
        if 'resistance_auto_range' in config_dict:
            self.checkBox_resistance_auto_range.setChecked(config_dict['resistance_auto_range'])
        if 'resistance_compensation' in config_dict:
            self.checkBox_resistance_compensation.setChecked(config_dict['resistance_compensation'])

        auto_range_modes = ['Normal', 'Resolution', 'Speed']
        self.comboBox_voltage_auto_mode.addItems(auto_range_modes)
        self.comboBox_current_auto_mode.addItems(auto_range_modes)
        if 'voltage_auto_mode' in config_dict and config_dict['voltage_auto_mode'] in auto_range_modes:
            self.comboBox_voltage_auto_mode.setCurrentText(config_dict['voltage_auto_mode'])
        if 'current_auto_mode' in config_dict and config_dict['current_auto_mode'] in auto_range_modes:
            self.comboBox_current_auto_mode.setCurrentText(config_dict['current_auto_mode'])

        self.comboBox_current_lower_lim.addItems(self.ranges_current)
        if 'current_lower_lim' in self.config_dict and self.config_dict['current_lower_lim'] in self.ranges_current:
            self.comboBox_current_lower_lim.setCurrentText(self.config_dict['current_lower_lim'])
        self.comboBox_current_range.addItems(self.ranges_current)
        if 'current_range' in self.config_dict and self.config_dict['current_range'] in self.ranges_current:
            self.comboBox_current_range.setCurrentText(self.config_dict['current_range'])
        self.comboBox_voltage_lower_lim.addItems(self.ranges_voltage)
        if 'voltage_lower_lim' in self.config_dict and self.config_dict['voltage_lower_lim'] in self.ranges_voltage:
            self.comboBox_voltage_lower_lim.setCurrentText(self.config_dict['voltage_lower_lim'])
        self.comboBox_voltage_range.addItems(self.ranges_voltage)
        if 'voltage_range' in self.config_dict and self.config_dict['voltage_range'] in self.ranges_voltage:
            self.comboBox_voltage_range.setCurrentText(self.config_dict['voltage_range'])
        self.comboBox_resistance_range.addItems(self.ranges_resistance)
        if 'resistance_range' in self.config_dict and self.config_dict['resistance_range'] in self.ranges_resistance:
            self.comboBox_resistance_range.setCurrentText(self.config_dict['resistance_range'])
        self.comboBox_resistance_upper_lim.addItems(self.ranges_resistance)
        if 'resistance_upper_lim' in self.config_dict and self.config_dict['resistance_upper_lim'] in self.ranges_resistance:
            self.comboBox_resistance_upper_lim.setCurrentText(self.config_dict['resistance_upper_lim'])


    def load_source_options(self):
        src_v = True
        if self.comboBox_source.currentText() == 'Current':
            src_v = False
        auto_source = self.checkBox_source_auto.isChecked()
        self.comboBox_source_range.clear()
        self.comboBox_range_lower_lim.clear()
        if src_v:
            self.comboBox_source_range.addItems(self.ranges_voltage)
            self.comboBox_range_lower_lim.addItems(self.ranges_voltage)
            if 'source_range' in self.config_dict and self.config_dict['source_range'] in self.ranges_voltage:
                self.comboBox_source_range.setCurrentText(self.config_dict['source_range'])
            if 'range_lower_lim' in self.config_dict and self.config_dict['range_lower_lim'] in self.ranges_voltage:
                self.comboBox_range_lower_lim.setCurrentText(self.config_dict['range_lower_lim'])
        else:
            self.comboBox_source_range.addItems(self.ranges_current)
            self.comboBox_range_lower_lim.addItems(self.ranges_current)
            if 'source_range' in self.config_dict and self.config_dict['source_range'] in self.ranges_current:
                self.comboBox_source_range.setCurrentText(self.config_dict['source_range'])
            if 'range_lower_lim' in self.config_dict and self.config_dict['range_lower_lim'] in self.ranges_current:
                self.comboBox_range_lower_lim.setCurrentText(self.config_dict['range_lower_lim'])
        self.comboBox_source_range.setEnabled(not auto_source)
        self.comboBox_range_lower_lim.setEnabled(auto_source)


    def get_config(self):
        self.config_dict['source'] = self.comboBox_source.currentText()
        self.config_dict['low_terminal'] = self.comboBox_low_terminal.currentText()
        self.config_dict['source_range'] = self.comboBox_source_range.currentText()
        self.config_dict['range_lower_lim'] = self.comboBox_range_lower_lim.currentText()
        self.config_dict['current_auto_mode'] = self.comboBox_current_auto_mode.currentText()
        self.config_dict['current_lower_lim'] = self.comboBox_current_lower_lim.currentText()
        self.config_dict['current_range'] = self.comboBox_current_range.currentText()
        self.config_dict['voltage_range'] = self.comboBox_voltage_range.currentText()
        self.config_dict['voltage_auto_mode'] = self.comboBox_voltage_auto_mode.currentText()
        self.config_dict['voltage_lower_lim'] = self.comboBox_voltage_lower_lim.currentText()
        self.config_dict['resistance_range'] = self.comboBox_resistance_range.currentText()
        self.config_dict['resistance_upper_lim'] = self.comboBox_resistance_upper_lim.currentText()
        self.config_dict['source_auto'] = self.checkBox_source_auto.isChecked()
        self.config_dict['output_protection'] = self.checkBox_output_protection.isChecked()
        self.config_dict['four_wire_meas'] = self.checkBox_four_wire_meas.isChecked()
        self.config_dict['current_auto_range'] = self.checkBox_current_auto_range.isChecked()
        self.config_dict['voltage_auto_range'] = self.checkBox_voltage_auto_range.isChecked()
        self.config_dict['resistance_auto_range'] = self.checkBox_resistance_auto_range.isChecked()
        self.config_dict['resistance_compensation'] = self.checkBox_resistance_compensation.isChecked()
        self.config_dict['current_compliance'] = float(self.lineEdit_current_compliance.text())
        self.config_dict['voltage_compliance'] = float(self.lineEdit_voltage_compliance.text())
        self.config_dict['NPLC'] = float(self.lineEdit_NPLC.text())
        return super().get_config()

