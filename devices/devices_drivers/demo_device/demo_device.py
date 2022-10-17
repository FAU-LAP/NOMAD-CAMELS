from main_classes import device_class, measurement_channel
import ophyd.sim

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='demo_device',
                         virtual=True,
                         tags=['virtual', 'demo', 'ophyd', 'detector'],
                         directory='demo_device', **kwargs)
        self.channels = {'demo_device_read_val': measurement_channel.Measurement_Channel(name='demo_device_read_val', device=self.name)}


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, additional_info=None):
        super().__init__(parent, self.name, data, settings_dict, additional_info)
        self.load_settings()

    def read_channels(self, channels, use_set, n_tabs=1):
        tabs = '\t' * n_tabs
        prot_string = ''
        for channel in channels:
            pass
