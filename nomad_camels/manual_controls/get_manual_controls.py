"""This package provides access to all classes of Manual_Control that
can be used by CAMELS, including device specific ones."""

from PySide6.QtWidgets import QDialog, QGridLayout, QDialogButtonBox, QComboBox, QLabel
from PySide6.QtCore import Qt

from nomad_camels.utility import variables_handling
from nomad_camels.manual_controls.stage_control import stage_control
from nomad_camels.manual_controls.set_panel import set_panel

manual_controls = {
    "Stage_Control": [stage_control.Stage_Control, stage_control.Stage_Control_Config],
    "Set_Panel": [set_panel.Set_Panel, set_panel.Set_Panel_Config],
}


class New_Manual_Control_Dialog(QDialog):
    """A dialog that provides the user with a selection of available manual
    controls."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QGridLayout()
        self.setLayout(layout)

        self.setWindowTitle("New Manual Control - NOMAD CAMELS")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.selection_box = QComboBox()
        self.std_controls = manual_controls
        self.selection_box.addItems(
            sorted(self.std_controls.keys(), key=lambda x: x.lower())
        )
        self.instr_controls = get_instrument_controls()
        self.selection_box.addItems(
            sorted(self.instr_controls.keys(), key=lambda x: x.lower())
        )

        self.selected_control = None

        label = QLabel("What kind of manual control do you want to add?")
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.selection_box, 1, 0)
        layout.addWidget(self.buttonBox, 2, 0)

    def accept(self):
        """Writes the control that was selected into `self.selected_control`."""
        name = self.selection_box.currentText()
        if name in self.std_controls:
            self.selected_control = self.std_controls[name]
        else:
            self.selected_control = self.instr_controls[name]
        super().accept()


def get_instrument_controls():
    """Goes through all configured instruments and checks them for manual
    controls. If there are any, they will be added to a dictionary.

    Returns
    -------
    controls : dict{'<name>': (Manual_Control, Manual_Control_Config)}
        Dictionary with the manual controls and there config widgets.
    """
    controls = {}
    for name, instr in sorted(
        variables_handling.devices.items(), key=lambda x: x[0].lower()
    ):
        adds = instr.get_controls()
        controls.update(adds)
    return controls


def get_control_by_type_name(name):
    """
    Returns a tuple/list of the specified control's class / config-class.

    Parameters
    ----------
    name : str
        Name of the manual control (could be CAMELS-main or instrument specific)

    Returns
    -------
    tuple(Manual_Control, Manual_Control_Config)
    """
    if name in manual_controls:
        return manual_controls[name]
    instr_controls = get_instrument_controls()
    if name in instr_controls:
        return instr_controls[name]
    raise Exception(f"Manual Control of type {name} is not defined!")
