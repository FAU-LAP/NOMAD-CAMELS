from PyQt5.QtWidgets import QWidget

class Device:
    """general class for all devices"""
    def __init__(self):
        self.__save_dict__ = {}

class Device_Config(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
