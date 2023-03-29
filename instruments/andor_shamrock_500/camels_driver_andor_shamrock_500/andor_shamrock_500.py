from CAMELS.main_classes import device_class
from .andor_shamrock_500_config import Ui_andor_shamrock500_config
from .andor_shamrock_500_ophyd import Andor_Shamrock_500
from PyQt5.QtWidgets import QTabWidget


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='andor_shamrock_500', virtual=False,
                         tags=[ 'spectrometer', 'spectrum', 'Andor',],
                         directory='andor_shamrock_500', ophyd_device=Andor_Shamrock_500,
                         ophyd_class_name='Andor_Shamrock_500', **kwargs)

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


class subclass_config_sub(device_class.Device_Config_Sub, Ui_andor_shamrock500_config):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(parent=parent, config_dict=config_dict,
                         settings_dict=settings_dict)
        self.setupUi(self)
        if 'set_grating_number' in self.config_dict:
            self.set_grating_number.setValue(self.config_dict['set_grating_number'])
        if 'initial_wavelength' in self.config_dict:
            self.initial_wavelength.setValue(self.config_dict['initial_wavelength'])
        if 'input_port' in self.config_dict:
            self.input_port.setCurrentText(self.config_dict['input_port'])
        if 'output_port' in self.config_dict:
            self.output_port.setCurrentText(self.config_dict['output_port'])
        if 'select_camera' in self.config_dict:
            self.select_camera.setCurrentText(self.config_dict['select_camera'])
        if 'input_slit_size' in self.config_dict:
            self.input_slit_size.setValue(self.config_dict['input_slit_size'])
        if 'output_slit_size' in self.config_dict:
            self.output_slit_size.setValue(self.config_dict['output_slit_size'])



    def get_config(self):
        self.config_dict['set_grating_number'] = self.set_grating_number.value()
        self.config_dict['initial_wavelength'] = self.initial_wavelength.value()
        self.config_dict['input_port'] = self.input_port.currentText()
        self.config_dict['output_port'] = self.output_port.currentText()
        self.config_dict['select_camera'] = self.select_camera.currentText()
        self.config_dict['input_slit_size'] = self.input_slit_size.value()
        self.config_dict['output_slit_size'] = self.output_slit_size.value()
        return super().get_config()