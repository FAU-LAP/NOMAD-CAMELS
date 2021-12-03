from main_classes import device_class


class Keithley_220(device_class.Device):
    def __init__(self):
        super().__init__()

class Keithley_220_Config(device_class.Device_Config):
    def __init__(self, parent=None):
        super().__init__(parent)