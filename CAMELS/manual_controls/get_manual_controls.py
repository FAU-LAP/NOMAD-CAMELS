from PySide6.QtWidgets import QDialog, QGridLayout, QDialogButtonBox, QComboBox, QLabel
from PySide6.QtCore import Qt

from CAMELS.utility import variables_handling
from CAMELS.manual_controls.stage_control import stage_control

manual_controls = {'Stage_Control': [stage_control.Stage_Control,
                                     stage_control.Stage_Control_Config]}


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
        self.std_controls = manual_controls
        self.selection_box.addItems(sorted(self.std_controls.keys(),
                                           key=lambda x: x.lower()))
        self.instr_controls = get_instrument_controls()
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



def get_instrument_controls():
    controls = {}
    for name, instr in sorted(variables_handling.devices.items(),
                              key=lambda x: x[0].lower()):
        adds = instr.get_controls()
        controls.update(adds)
    return controls

def get_control_by_type_name(name):
    if name in manual_controls:
        return manual_controls[name]
    instr_controls = get_instrument_controls()
    if name in instr_controls:
        return instr_controls[name]
    raise Exception(f'Manual Control of type {name} is not defined!')
