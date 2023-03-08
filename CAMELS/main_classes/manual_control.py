from PyQt5.QtWidgets import QWidget, QGridLayout, QDialog, QDialogButtonBox, QLabel, QLineEdit, QMessageBox, QComboBox
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtCore import pyqtSignal, Qt

from CAMELS.utility import device_handling
from CAMELS.manual_controls import get_manual_controls

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



# class Manual_Control_Config(QDialog):
#     def __init__(self, control=Manual_Control(), parent=None, title='Manual Control Config'):
#         super().__init__(parent=parent)
#         layout = QGridLayout()
#         self.setLayout(layout)
#
#         self.setWindowTitle(title)
#
#         self.buttonBox = QDialogButtonBox()
#         self.buttonBox.setOrientation(Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
#         self.buttonBox.setObjectName("buttonBox")
#         self.buttonBox.rejected.connect(self.reject)
#         self.buttonBox.accepted.connect(self.accept)
#
#         name_label = QLabel('Name:')
#         self.lineEdit_name = QLineEdit(control.name)
#         self.control = control
#
#         layout.addWidget(name_label, 0, 0)
#         layout.addWidget(self.lineEdit_name, 0, 1)
#         layout.addWidget(self.buttonBox, 11, 0, 1, 2)
#
#     def accept(self):
#         self.control.name = self.lineEdit_name.text()
#         super().accept()
#
#     def closeEvent(self, a0: QCloseEvent) -> None:
#         discard_dialog = QMessageBox.question(self, 'Discard Changes?',
#                                               f'All changes will be lost!',
#                                               QMessageBox.Yes | QMessageBox.No)
#         if discard_dialog != QMessageBox.Yes:
#             a0.ignore()
#             return
#         super().closeEvent(a0)


class New_Manual_Control_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.setWindowTitle('New Manual Control - CAMELS')

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.selection_box = QComboBox()
        self.std_controls = get_manual_controls.manual_controls
        self.selection_box.addItems(sorted(self.std_controls.keys(),
                                           key=lambda x: x.lower()))
        self.instr_controls = get_manual_controls.get_instrument_controls()
        self.selection_box.addItems(sorted(self.instr_controls.keys(),
                                           key=lambda x: x.lower()))

        self.selected_control = None

        label = QLabel('What kind of manual control do you want to add?')
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.selection_box, 1, 0)
        layout.addWidget(self.buttonBox, 2, 0)


    def accept(self):
        name = self.selection_box.currentText()
        if name in self.std_controls:
            self.selected_control = self.std_controls[name]
        else:
            self.selected_control = self.instr_controls[name]
        super().accept()

