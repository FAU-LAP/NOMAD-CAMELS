from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtCore import pyqtSignal

from CAMELS.utility import device_handling
from pkg_resources import resource_filename

class Manual_Control(QWidget):
    closing = pyqtSignal()

    def __init__(self, parent=None, title='Manual Control', device=None,
                 ophyd_device=None, device_list=None):
        super().__init__(parent=parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.setWindowTitle(f'CAMELS - {title}')
        self.setWindowIcon(QIcon(resource_filename('CAMELS','graphics/CAMELS.svg')))
        self.name = title
        self.device = device
        self.ophyd_device = ophyd_device
        self.device_list = device_list or []
        self.show()

    def close(self) -> bool:
        device_handling.close_devices(self.device_list)
        self.closing.emit()
        return super().close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        device_handling.close_devices(self.device_list)
        self.closing.emit()
        return super().closeEvent(a0)
