from CAMELS.main_classes import device_class
from .andor_newton_config import Ui_andor_newton_config
from .andor_newton_ophyd import Andor_Newton
from PyQt5.QtWidgets import QTabWidget


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='andor_newton', virtual=False, tags=['Camera', 'spectrometer', 'CCD', 'spectrum', 'Andor',], directory='andor_newton', ophyd_device=Andor_Newton, ophyd_class_name='Andor_Newton', **kwargs)
        # for key, val in default_settings.items():
        #     self.config[f'{key}1'] = val
        #     self.config[f'{key}2'] = val

class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, config_dict=None, additional_info=None, **kwargs):
        super().__init__(parent, 'Andor Newton', data, settings_dict=settings_dict, config_dict=config_dict, additional_info=additional_info, no_ioc_connection=True, **kwargs)
        self.comboBox_connection_type.addItem('Windows dll')
        # self.comboBox_connection_type.addItem('Local VISA')
        self.tab_widget = QTabWidget()
        conf1 = {}
        for key, val in config_dict.items():
            if key.endswith('1'):
                conf1[key[:-1]] = val
        self.channel_widge_1 = subclass_config_sub(config_dict=conf1, parent=parent, settings_dict=settings_dict)
        self.tab_widget.addTab(self.channel_widge_1, 'Channel 1')
        self.layout().addWidget(self.tab_widget, 20, 0, 1, 5)
        self.load_settings()

    def get_config(self):
        conf1 = self.channel_widge_1.get_config()
        for key, val in conf1.items():
            self.config_dict[f'{key}1'] = val
        return super().get_config()


class subclass_config_sub(device_class.Device_Config_Sub, Ui_andor_newton_config):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(parent=parent, config_dict=config_dict,
                         settings_dict=settings_dict)
        self.setupUi(self)
        if 'serial_number' in self.config_dict:
            self.serial_number.setValue(self.config_dict['serial_number'])
        if 'set_temperature' in self.config_dict:
            self.set_temperature.setValue(self.config_dict['set_temperature'])
        if 'comboBox_shutter_mode' in self.config_dict:
            self.comboBox_shutter_mode.setCurrentText(self.config_dict['comboBox_shutter_mode'])
        if 'exposure_time' in self.config_dict:
            self.exposure_time.setValue(self.config_dict['exposure_time'])
        if 'comboBox_readout_mode' in self.config_dict:
            self.comboBox_readout_mode.setCurrentText(self.config_dict['comboBox_readout_mode'])
        if 'preamp_gain' in self.config_dict:
            self.preamp_gain.setValue(self.config_dict['preamp_gain'])
        if 'horizontal_binning' in self.config_dict:
            self.horizontal_binning.setValue(self.config_dict['horizontal_binning'])
        if 'hs_speed' in self.config_dict:
            self.hs_speed.setValue(self.config_dict['hs_speed'])
        if 'vs_speed' in self.config_dict:
            self.vs_speed.setValue(self.config_dict['vs_speed'])
        if 'number_of_tracks' in self.config_dict:
            self.number_of_tracks.setValue(self.config_dict['number_of_tracks'])
        if 'track_height' in self.config_dict:
            self.track_height.setValue(self.config_dict['track_height'])
        if 'start_row' in self.config_dict:
            self.start_row.setValue(self.config_dict['start_row'])
        if 'end_row' in self.config_dict:
            self.end_row.setValue(self.config_dict['end_row'])


    def get_config(self):
        self.config_dict['serial_number'] = self.serial_number.value()
        self.config_dict['set_temperature'] = self.set_temperature.value()
        self.config_dict['comboBox_shutter_mode'] = self.comboBox_shutter_mode.currentText()
        self.config_dict['exposure_time'] = self.exposure_time.value()
        self.config_dict['comboBox_readout_mode'] = self.comboBox_readout_mode.currentText()
        self.config_dict['preamp_gain'] = self.preamp_gain.value()
        self.config_dict['horizontal_binning'] = self.horizontal_binning.value()
        self.config_dict['hs_speed'] = self.hs_speed.value()
        self.config_dict['vs_speed'] = self.vs_speed.value()
        self.config_dict['number_of_tracks'] = self.number_of_tracks.value()
        self.config_dict['track_height'] = self.track_height.value()
        self.config_dict['start_row'] = self.start_row.value()
        self.config_dict['end_row'] = self.end_row.value()
        return super().get_config()

