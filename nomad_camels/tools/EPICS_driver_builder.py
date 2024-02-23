import sys
import os
import ast

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QGridLayout,
)
from PySide6.QtGui import QIcon, QCloseEvent

from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.utility import variables_handling, fit_variable_renaming

from importlib import resources
from nomad_camels import graphics


class EPICS_Driver_Builder(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        try:
            self.setWindowIcon(
                QIcon(str(resources.files(graphics) / "camels_icon.png"))
            )
        except:
            pass
        self.setWindowTitle("EPICS-driver-builder - NOMAD CAMELS")

        label_name = QLabel("Instrument Name:")
        self.lineEdit_name = QLineEdit()

        label_in = QLabel("Input Channels")
        label_out = QLabel("Output Channels")
        label_config = QLabel("Config Channels")
        label_config_in = QLabel("Config Channels - Read Only")
        label_in.setStyleSheet("font-weight: bold")
        label_out.setStyleSheet("font-weight: bold")
        label_config.setStyleSheet("font-weight: bold")
        label_config_in.setStyleSheet("font-weight: bold")

        channel_info_config = ["PV-Name", "Datatype"]
        channel_info = ["PV-Name"]
        comboBoxes = {"Datatype": ["str", "float", "bool"]}
        self.table_in = AddRemoveTable(headerLabels=channel_info)
        self.table_out = AddRemoveTable(headerLabels=channel_info)
        self.table_config = AddRemoveTable(
            headerLabels=channel_info_config, comboBoxes=comboBoxes
        )
        self.table_config_in = AddRemoveTable(headerLabels=channel_info)

        self.button_build = QPushButton("Build Driver")
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.close)
        self.button_build.clicked.connect(self.build_device)

        layout = QGridLayout()
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_name, 0, 1, 1, 3)
        layout.addWidget(label_in, 10, 0, 1, 2)
        layout.addWidget(self.table_in, 11, 0, 1, 2)
        layout.addWidget(label_out, 10, 2, 1, 2)
        layout.addWidget(self.table_out, 11, 2, 1, 2)
        layout.addWidget(label_config_in, 30, 0, 1, 2)
        layout.addWidget(self.table_config_in, 31, 0, 1, 2)
        layout.addWidget(label_config, 30, 2, 1, 2)
        layout.addWidget(self.table_config, 31, 2, 1, 2)
        layout.addWidget(self.button_build, 50, 2)
        layout.addWidget(self.button_cancel, 50, 3)
        self.setLayout(layout)
        # self.resize(600, 700)

    def build_device(self):
        dev_name = fit_variable_renaming.replace_name(self.lineEdit_name.text())
        inputs = self.table_in.update_table_data()
        outputs = self.table_out.update_table_data()
        configs = self.table_config.update_table_data()
        configs_in = self.table_config_in.update_table_data()

        path = (
            variables_handling.device_driver_path
            or QFileDialog.getExistingDirectory(self, "Select directory for drivers")
        )
        if not path:
            return

        def check_builtin(pv):
            if pv in vars(__builtins__):
                raise Exception(
                    f'PV-name "{pv}" resembles python builtin function or variable!\nDefine another name!\nYou may change the PV-name later in the code, see the documentation for more information.'
                )
            try:
                ast.parse(f"{pv} = None")
            except (ValueError, SyntaxError, TypeError):
                raise Exception(
                    f'PV-name "{pv}" resembles python builtin function or variable!\nDefine another name!\nYou may change the PV-name later in the code, see the documentation for more information.'
                )

        all_good = True
        for name in inputs["PV-Name"]:
            all_good = all_good and variables_handling.check_variable_name(
                name, parent=self
            )
        for name in outputs["PV-Name"]:
            all_good = all_good and variables_handling.check_variable_name(
                name, parent=self
            )
        for name in configs["PV-Name"]:
            all_good = all_good and variables_handling.check_variable_name(
                name, parent=self
            )
        for name in configs_in["PV-Name"]:
            all_good = all_good and variables_handling.check_variable_name(
                name, parent=self
            )
        if not all_good:
            raise Exception(
                f"Some PV-name resemble python builtin function or variable!\nDefine another name!\nYou may change the PV-name later in the code, see the documentation for more information."
            )
        directory = f"{path}/nomad_camels_driver_{dev_name}"
        sys.path.append(directory)
        fname = f"{directory}/{dev_name}.py"
        if os.path.isdir(directory) and os.path.isfile(fname):
            answer = QMessageBox.question(
                self,
                "Instrument already exists!",
                f"Instrument type with name {dev_name} already exists.\nDo you want to overwrite the existing instrument driver?",
                buttons=QMessageBox.Yes | QMessageBox.Cancel,
                defaultButton=QMessageBox.Cancel,
            )
            if answer != QMessageBox.Yes:
                return
        if not os.path.isdir(directory):
            os.mkdir(directory)

        class_string = f"from nomad_camels_driver_{dev_name}.{dev_name}_ophyd import {dev_name}_Ophyd\n\n"
        class_string += "from nomad_camels.main_classes import device_class\n\n"
        class_string += "class subclass(device_class.Device):\n"
        class_string += "\tdef __init__(self, **kwargs):\n"
        class_string += f'\t\tsuper().__init__(name="{dev_name}", virtual=False, directory="{dev_name}", ophyd_device={dev_name}_Ophyd, ophyd_class_name="{dev_name}_Ophyd", **kwargs)\n'
        for i, name in enumerate(configs["PV-Name"]):
            if configs["Datatype"][i] == "str":
                class_string += f'\t\tself.config["{name}"] = ""\n'
            elif configs["Datatype"][i] == "float":
                class_string += f'\t\tself.config["{name}"] = 0\n'
            elif configs["Datatype"][i] == "bool":
                class_string += f'\t\tself.config["{name}"] = False\n'
        class_string += "\n\nclass subclass_config(device_class.Simple_Config):\n"
        class_string += '\tdef __init__(self, parent=None, data="", settings_dict=None, config_dict=None, additional_info=None):\n'
        class_string += f'\t\tsuper().__init__(parent, "{dev_name}", data, settings_dict, config_dict, additional_info)\n'
        class_string += '\t\tself.comboBox_connection_type.addItem("EPICS")\n'
        class_string += "\t\tself.load_settings()\n"

        ophyd_string = "from ophyd import Component as Cpt\n\n"
        ophyd_string += "from ophyd import Device, EpicsSignal, EpicsSignalRO\n\n"
        ophyd_string += f"class {dev_name}_Ophyd(Device):\n"
        for i, name in enumerate(inputs["PV-Name"]):
            ophyd_string += f'\t{name} = Cpt(EpicsSignalRO, "{name}")\n'
        for i, name in enumerate(outputs["PV-Name"]):
            ophyd_string += f'\t{name} = Cpt(EpicsSignal, "{name}")\n'
        for i, name in enumerate(configs["PV-Name"]):
            ophyd_string += f'\t{name} = Cpt(EpicsSignal, "{name}",kind="config")\n'
        for i, name in enumerate(configs_in["PV-Name"]):
            ophyd_string += f'\t{name} = Cpt(EpicsSignalRO, "{name}", kind="config")\n'

        ophyd_string += f'\n\tdef __init__(self, prefix="", *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, **kwargs):\n'
        ophyd_string += f"\t\tsuper().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)"

        with open(f"{directory}/{dev_name}.py", "w", encoding="utf-8") as f:
            f.write(class_string)
        with open(f"{directory}/{dev_name}_ophyd.py", "w", encoding="utf-8") as f:
            f.write(ophyd_string)
        # with open(f'{directory}/__init__.py', 'w') as f:
        #     f.write(ophyd_string)

        QMessageBox.information(
            self, "Build finished!", f"The instrument-driver {dev_name} has been built!"
        )
        self.accept()

    def closeEvent(self, a0: QCloseEvent) -> None:
        discard_dialog = QMessageBox.question(
            self,
            "Discard Changes?",
            f"All changes will be lost!",
            QMessageBox.Yes | QMessageBox.No,
        )
        if discard_dialog != QMessageBox.Yes:
            a0.ignore()
            return
        super().closeEvent(a0)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QCoreApplication
    from nomad_camels.utility import exception_hook

    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = EPICS_Driver_Builder()
    ui.show()
    app.exec()
