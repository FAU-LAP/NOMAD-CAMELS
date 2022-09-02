from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtCore import pyqtSignal

class AddOn(QWidget):
    closing = pyqtSignal()

    def __init__(self, title='AddOn', device=None):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        self.setWindowTitle(f'CAMELS - {title}')
        self.setWindowIcon(QIcon('graphics/CAMELS.svg'))
        self.name = title
        self.device = device
        self.show()

    def close(self) -> bool:
        self.closing.emit()
        return super().close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.closing.emit()
        return super().closeEvent(a0)
