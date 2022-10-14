from main_classes import device_class

from bruker_magnet_ni_daq.bruker_magnet_ni_daq_ophyd import Bruker_Magnet_NI_DAQ
from bruker_magnet_ni_daq.bruker_magnet_ni_daq_config import Ui_bruker_magnet_config


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='bruker_magnet_ni_daq',
                         tags=['magnet'], directory='bruker_magnet_ni_daq',
                         ophyd_device=Bruker_Magnet_NI_DAQ,
                         ophyd_class_name='Bruker_Magnet_NI_DAQ', **kwargs)

    def get_config(self):
        return {}

    def get_finalize_steps(self):
        s = '\t\tfrom bluesky_handling import daq_signal\n'
        s += '\t\tdaq_signal.close_tasks()\n'
        return s


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'Bruker Magnet (DAQ)', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        self.layout().removeWidget(self.comboBox_connection_type)
        self.comboBox_connection_type.deleteLater()
        self.layout().removeWidget(self.label_connection)
        self.label_connection.deleteLater()
        self.layout().removeWidget(self.checkBox_use_local_ioc)
        self.checkBox_use_local_ioc.deleteLater()
        self.layout().removeWidget(self.lineEdit_ioc_name)
        self.lineEdit_ioc_name.deleteLater()
        self.layout().removeWidget(self.label_ioc_name)
        self.label_ioc_name.deleteLater()
        self.sub_widget = subclass_config_sub(config_dict, self, settings_dict)
        self.layout().addWidget(self.sub_widget, 20, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        return self.sub_widget.get_settings()

    def get_config(self):
        return self.sub_widget.get_config()

    def get_ioc_settings(self):
        return {}


class subclass_config_sub(device_class.Device_Config_Sub, Ui_bruker_magnet_config):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(parent=parent, config_dict=config_dict,
                         settings_dict=settings_dict)
        self.setupUi(self)
        self.settings_dict = settings_dict

        if 'power_on_line' in settings_dict:
            self.lineEdit_power_on.setText(settings_dict['power_on_line'])
        else:
            self.lineEdit_power_on.setText('Bruker/port1/line0')

        if 'power_off_line' in settings_dict:
            self.lineEdit_power_off.setText(settings_dict['power_off_line'])
        else:
            self.lineEdit_power_off.setText('Bruker/port1/line1')

        if 'power_read_line' in settings_dict:
            self.lineEdit_power_read.setText(settings_dict['power_read_line'])
        else:
            self.lineEdit_power_read.setText('Bruker/port0/line0')

        if 'reverse_line' in settings_dict:
            self.lineEdit_reverse.setText(settings_dict['reverse_line'])
        else:
            self.lineEdit_reverse.setText('Bruker/port1/line2')

        if 'polarity_read_line' in settings_dict:
            self.lineEdit_polarity.setText(settings_dict['polarity_read_line'])
        else:
            self.lineEdit_polarity.setText('Bruker/port0/line1')

        if 'wait_time' in settings_dict:
            self.lineEdit_wait_time.setText(str(settings_dict['wait_time']))
        else:
            self.lineEdit_wait_time.setText('5')

        if 'reverse_time' in settings_dict:
            self.lineEdit_reverse_time.setText(str(settings_dict['reverse_time']))
        else:
            self.lineEdit_reverse_time.setText('25')


    def get_settings(self):
        self.settings_dict['power_on_line'] = self.lineEdit_power_on.text()
        self.settings_dict['power_off_line'] = self.lineEdit_power_off.text()
        self.settings_dict['power_read_line'] = self.lineEdit_power_read.text()
        self.settings_dict['reverse_line'] = self.lineEdit_reverse.text()
        self.settings_dict['polarity_read_line'] = self.lineEdit_polarity.text()
        self.settings_dict['wait_time'] = float(self.lineEdit_wait_time.text())
        self.settings_dict['reverse_time'] = float(self.lineEdit_reverse_time.text())
        return self.settings_dict

