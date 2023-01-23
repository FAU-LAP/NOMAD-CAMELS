from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtCore import pyqtSignal

from utility import device_handling

class AddOn(QWidget):
    closing = pyqtSignal()

    def __init__(self, parent=None, title='AddOn', device=None,
                 ophyd_device=None, device_list=None):
        super().__init__(parent=parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.setWindowTitle(f'CAMELS - {title}')
        self.setWindowIcon(QIcon('graphics/CAMELS.svg'))
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
