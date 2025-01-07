import sys
import os
from shutil import copyfile

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QIcon, QCloseEvent

from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.utility import variables_handling, fit_variable_renaming
from nomad_camels.tools.driver_builder import Ui_VISA_Device_Builder

from importlib import resources
from nomad_camels import graphics


class Driver_Builder(Ui_VISA_Device_Builder, QDialog):
    """ """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        try:
            self.setWindowIcon(
                QIcon(str(resources.files(graphics) / "camels_icon.png"))
            )
        except:
            pass
        self.setWindowTitle("Driver-builder - NOMAD CAMELS")

        label_custom = QLabel("Custom Channels")
        label_in = QLabel("Read Channels - VISA")
        label_out = QLabel("Set Channels - VISA")
        label_config = QLabel("Config Channels - VISA")
        label_config_in = QLabel("Config Channels - Read Only - VISA")
        label_custom.setStyleSheet("font-weight: bold")
        label_in.setStyleSheet("font-weight: bold")
        label_out.setStyleSheet("font-weight: bold")
        label_config.setStyleSheet("font-weight: bold")
        label_config_in.setStyleSheet("font-weight: bold")
        label_info = QLabel(
            'The values "Write-Format-String", "Return-Parser" and "Query-String" can be left empty, if you want to use a custom function for those!'
        )
        label_info.setStyleSheet("font-weight: bold")
        label_info.setMaximumHeight(20)

        channel_info_config = [
            "Name",
            "Write-Format-String",
            "Input-Type",
            "Return-Parser",
            "Return-Type",
            "Unit",
            "Description",
        ]
        channel_info_in = [
            "Name",
            "Query-String",
            "Return-Parser",
            "Return-Type",
            "Unit",
            "Description",
        ]
        channel_info_out = [
            "Name",
            "Write-Format-String",
            "Return-Parser",
            "Return-Type",
            "Unit",
            "Description",
        ]
        comboboxes_in = {"Return-Type": ["str", "float", "int", "bool"]}
        comboboxes_out = {"Return-Type": ["None", "str", "float", "int", "bool"]}
        comboBoxes_config = dict(comboboxes_out)
        comboBoxes_config.update({"Input-Type": ["str", "float", "bool"]})

        channel_info_custom = [
            "Name",
            "Channel-Type",
            "Input-Type",
            "Unit",
            "Description",
        ]
        comboboxes_custom = {
            "Channel-Type": ["read-only", "set", "config", "config - read-only"],
            "Input-Type": ["str", "float", "bool"],
        }
        self.table_custom = AddRemoveTable(
            headerLabels=channel_info_custom, comboBoxes=comboboxes_custom
        )

        self.table_in = AddRemoveTable(
            headerLabels=channel_info_in, comboBoxes=comboboxes_in
        )
        self.table_out = AddRemoveTable(
            headerLabels=channel_info_out, comboBoxes=comboboxes_out
        )
        self.table_config = AddRemoveTable(
            headerLabels=channel_info_config, comboBoxes=comboBoxes_config
        )
        self.table_config_in = AddRemoveTable(
            headerLabels=channel_info_in, comboBoxes=comboboxes_in
        )

        self.button_build = QPushButton("Build Driver")
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.close)
        self.button_build.clicked.connect(self.build_driver)
        self.checkBox_VISA.clicked.connect(self.toggle_VISA)
        self.visa_widgets = [
            label_in,
            label_info,
            label_out,
            label_config,
            label_config_in,
            self.table_config,
            self.table_config_in,
            self.table_in,
            self.table_out,
            self.label_read_term,
            self.label_write_term,
            self.label_baud_rate,
            self.lineEdit_baud_rate,
            self.lineEdit_write_term,
            self.lineEdit_read_term,
        ]
        self.toggle_VISA()

        layout = self.layout()

        layout.addWidget(label_custom, 10, 0, 1, 3)
        layout.addWidget(self.table_custom, 11, 0, 4, 3)

        layout.addWidget(label_in, 10, 4, 1, 2)
        layout.addWidget(self.table_in, 11, 4, 1, 2)
        layout.addWidget(label_out, 10, 6, 1, 2)
        layout.addWidget(self.table_out, 11, 6, 1, 2)
        layout.addWidget(label_config_in, 13, 4, 1, 2)
        layout.addWidget(self.table_config_in, 14, 4, 1, 2)
        layout.addWidget(label_config, 13, 6, 1, 2)
        layout.addWidget(self.table_config, 14, 6, 1, 2)
        layout.addWidget(label_info, 12, 4, 1, 3)

        button_widget = QWidget()
        lay = QGridLayout()
        button_widget.setLayout(lay)
        lay.addItem(
            QSpacerItem(
                0,
                0,
                hData=QSizePolicy.Policy.Expanding,
                vData=QSizePolicy.Policy.Minimum,
            ),
            0,
            0,
        )
        lay.addWidget(self.button_build, 0, 1)
        lay.addWidget(self.button_cancel, 0, 2)
        layout.addWidget(button_widget, 50, 0, 1, 8)

        self.adjustSize()

    def toggle_VISA(self):
        visa = self.checkBox_VISA.isChecked()
        for widget in self.visa_widgets:
            widget.setHidden(not visa)
        self.adjustSize()

    def build_driver(self):
        """ """
        dev_name = fit_variable_renaming.replace_name(self.lineEdit_name.text())
        ophyd_name = dev_name.title()
        ophyd_name = fit_variable_renaming.replace_name(ophyd_name)
        search_tags = self.lineEdit_search_tags.text().split()
        visa = self.checkBox_VISA.isChecked()
        configs = inputs = outputs = configs_in = {"Name": []}
        write_term = read_term = ""
        baud_rate = 0
        if visa:
            read_term = fit_variable_renaming.replace_name(
                self.lineEdit_read_term.text()
            )
            write_term = fit_variable_renaming.replace_name(
                self.lineEdit_write_term.text()
            )
            baud_rate = int(self.lineEdit_baud_rate.text())
            inputs = self.table_in.update_table_data()
            outputs = self.table_out.update_table_data()
            configs = self.table_config.update_table_data()
            configs_in = self.table_config_in.update_table_data()

        customs = self.table_custom.update_table_data()
        names = (
            inputs["Name"]
            + outputs["Name"]
            + configs["Name"]
            + configs_in["Name"]
            + customs["Name"]
        )
        for name in names:
            if not variables_handling.check_variable_name(name, parent=self):
                return

        path = variables_handling.device_driver_path or ""
        directory = QFileDialog.getExistingDirectory(
            self, "Select driver's parent directory", f"{path}"
        )
        if not directory:
            return

        sys.path.append(directory)
        if not os.path.isfile(f"{directory}/__init__.py"):
            with open(f"{directory}/__init__.py", "w", encoding="utf-8") as f:
                pass
        module_dir = f"{directory}/{dev_name}"
        driver_dir = f"{module_dir}/nomad_camels_driver_{dev_name}"
        fname = f"{driver_dir}/{dev_name}.py"
        if os.path.isdir(driver_dir) and os.path.isfile(fname):
            answer = QMessageBox.question(
                self,
                "Driver already exists!",
                f"Driver with name {dev_name} already exists.\nDo you want to overwrite the driver?",
                buttons=QMessageBox.Yes | QMessageBox.Cancel,
                defaultButton=QMessageBox.Cancel,
            )
            if answer != QMessageBox.Yes:
                return
        if not os.path.isdir(driver_dir):
            os.makedirs(driver_dir)

        class_string = f"from .{dev_name}_ophyd import {ophyd_name}\n\n"
        class_string += "from nomad_camels.main_classes import device_class\n\n"
        class_string += "class subclass(device_class.Device):\n"
        class_string += "\tdef __init__(self, **kwargs):\n"
        class_string += f'\t\tsuper().__init__(name="{dev_name}", virtual=False, tags={search_tags}, directory="{dev_name}", ophyd_device={ophyd_name}, ophyd_class_name="{ophyd_name}", **kwargs)\n'
        for i, name in enumerate(configs["Name"]):
            if configs["Input-Type"][i] == "str":
                class_string += f'\t\tself.config["{name}"] = ""\n'
            elif configs["Input-Type"][i] == "float":
                class_string += f'\t\tself.config["{name}"] = 0\n'
            elif configs["Input-Type"][i] == "bool":
                class_string += f'\t\tself.config["{name}"] = False\n'
        for i, name in enumerate(customs["Name"]):
            if customs["Channel-Type"][i] == "config":
                if customs["Input-Type"][i] == "str":
                    class_string += f'\t\tself.config["{name}"] = ""\n'
                elif customs["Input-Type"][i] == "float":
                    class_string += f'\t\tself.config["{name}"] = 0\n'
                elif customs["Input-Type"][i] == "bool":
                    class_string += f'\t\tself.config["{name}"] = False\n'

        class_string += "\n\nclass subclass_config(device_class.Simple_Config):\n"
        class_string += '\tdef __init__(self, parent=None, data="", settings_dict=None, config_dict=None, additional_info=None):\n'
        class_string += f'\t\tsuper().__init__(parent, "{dev_name}", data, settings_dict, config_dict, additional_info)\n'
        if visa:
            class_string += '\t\tself.comboBox_connection_type.addItem("Local VISA")\n'
        class_string += "\t\tself.load_settings()\n"

        ophyd_string = "from ophyd import Component as Cpt\n\n"
        if customs:
            ophyd_string += "from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO\n"
        if visa:
            ophyd_string += "from nomad_camels.bluesky_handling.visa_signal import VISA_Signal, VISA_Signal_RO, VISA_Device\n\n"
            ophyd_string += f"class {ophyd_name}(VISA_Device):\n"
        else:
            ophyd_string += "from ophyd import Device\n\n"
            ophyd_string += f"class {ophyd_name}(Device):\n"
        open_queries = []
        open_writes = []
        comp_str, opens = make_component_str(inputs, True, False)
        ophyd_string += comp_str
        open_queries += opens
        comp_str, opens = make_component_str(outputs, False, False)
        ophyd_string += comp_str
        open_writes += opens
        comp_str, opens = make_component_str(configs, False, True)
        ophyd_string += comp_str
        open_writes += opens
        comp_str, opens = make_component_str(configs_in, True, True)
        ophyd_string += comp_str
        open_queries += opens

        comp_str, read_names, write_names = make_custom_component(customs)
        ophyd_string += comp_str

        if visa:
            ophyd_string += f'\n\tdef __init__(self, prefix="", *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, resource_name="", write_termination="{write_term}", read_termination="{read_term}", baud_rate={baud_rate}, **kwargs):\n'
            ophyd_string += f"\t\tsuper().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, resource_name=resource_name, baud_rate=baud_rate, read_termination=read_termination, write_termination=write_termination, **kwargs)\n"
        else:
            ophyd_string += f'\n\tdef __init__(self, prefix="", *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, **kwargs):\n'
            ophyd_string += f"\t\tsuper().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, **kwargs)\n"
        for name in open_queries:
            ophyd_string += f"\t\tself.{name}.query = self.{name}_query_function\n"
        for name in open_writes:
            ophyd_string += f"\t\tself.{name}.write = self.{name}_write_function\n"
        for name in read_names:
            ophyd_string += (
                f"\t\tself.{name}.read_function = self.{name}_read_function\n"
            )
        for name in write_names:
            ophyd_string += f"\t\tself.{name}.put_function = self.{name}_put_function\n"

        ophyd_string += "\n"

        for name in open_queries:
            ophyd_string += f"\tdef {name}_query_function(self):\n"
            ophyd_string += f"\t\tpass\n\n"
        for name in open_writes:
            ophyd_string += f"\tdef {name}_write_function(self, value):\n"
            ophyd_string += f"\t\tpass\n\n"

        for name in read_names:
            ophyd_string += f"\tdef {name}_read_function(self):\n"
            ophyd_string += f"\t\tpass\n\n"
        for name in write_names:
            ophyd_string += f"\tdef {name}_put_function(self, value):\n"
            ophyd_string += f"\t\tpass\n\n"

        readme_string = f"# NOMAD Camels driver for {dev_name}\n\n"
        readme_string += f"Driver for {dev_name} written for the measurement software [NOMAD Camels](https://fau-lap.github.io/NOMAD-CAMELS/).\n\n\n"
        readme_string += "## Documentation\n\n"
        readme_string += "For more information and instruments visit the [documentation](https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html)."

        toml_string = '[build-system]\nrequires = ["setuptools>=61.0"]\nbuild-backend = "setuptools.build_meta"\n\n'
        toml_string += (
            f'[project]\nname = "nomad_camels_driver_{dev_name}"\nversion = "0.1.0"\n'
        )
        toml_string += 'authors = [\n\t{name="enter your name here!", email="contact@email.com"}\n]\n'
        toml_string += (
            f'description = "Instrument driver for {dev_name} for NOMAD CAMELS"\n'
        )
        toml_string += 'readme = "README.md"\n'
        toml_string += 'requires-python = ">=3.9.6"\n'
        toml_string += 'classifiers = [\n\t"Programming Language :: Python :: 3",\n\t"License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",\n]\n\n'
        toml_string += 'dependencies = [\n\t"nomad-camels"'
        if visa:
            toml_string += ',\n\t"pyvisa",\n\t"pyvisa-py"'
        toml_string += "\n]\n\n"
        toml_string += "[project.urls]\n"
        toml_string += (
            '"NOMAD Camels GitHub" = "https://github.com/FAU-LAP/NOMAD-CAMELS"\n'
        )
        toml_string += (
            '"CAMELS Drivers GitHub" = "https://github.com/FAU-LAP/CAMELS_drivers"\n'
        )
        toml_string += '"NOMAD Camels Documentation" = "https://fau-lap.github.io/NOMAD-CAMELS/doc/instruments/instruments.html"\n'

        with open(
            os.path.join(driver_dir, f"{dev_name}.py"), "w", encoding="utf-8"
        ) as f:
            f.write(class_string)
        with open(
            os.path.join(driver_dir, f"{dev_name}_ophyd.py"), "w", encoding="utf-8"
        ) as f:
            f.write(ophyd_string)
        with open(os.path.join(driver_dir, "__init__.py"), "w", encoding="utf-8") as f:
            pass
        with open(os.path.join(module_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_string)
        with open(
            os.path.join(module_dir, "pyproject.toml"), "w", encoding="utf-8"
        ) as f:
            f.write(toml_string)
        copyfile(
            os.path.join(os.path.dirname(__file__), "../../LICENSE"),
            os.path.join(module_dir, "LICENSE"),
        )

        QMessageBox.information(
            self, "Build finished!", f'The driver "{dev_name}" has been built!'
        )

    def closeEvent(self, a0: QCloseEvent) -> None:
        """

        Parameters
        ----------
        a0: QCloseEvent :


        Returns
        -------

        """
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


def make_custom_component(dic):
    ophyd_string = ""
    read_names = []
    write_names = []
    for i, name in enumerate(dic["Name"]):
        channel_type = dic["Channel-Type"][i]
        RO = False
        if "read-only" in channel_type:
            read_names.append(name)
            RO = True
        else:
            write_names.append(name)
        conf = False
        if "config" in channel_type:
            conf = True
        ophyd_string += f'\t{name} = Cpt(Custom_Function_Signal{"RO" if RO else ""}, name="{name}", '
        if conf:
            ophyd_string += 'kind="config", '
        ophyd_string += f'metadata={{"units": "{dic["Unit"][i]}", "description": "{dic["Description"][i]}"}})\n'
    return ophyd_string, read_names, write_names


def make_component_str(dic, RO, config):
    ophyd_string = ""
    still_open = []
    for i, name in enumerate(dic["Name"]):
        ophyd_string += (
            f'\t{name} = Cpt(VISA_Signal{"_RO" if RO else ""}, name="{name}", '
        )
        if "Write-Format-String" in dic:
            write_str = dic["Write-Format-String"][i]
            if write_str:
                ophyd_string += f'write="{write_str}", '
            else:
                still_open.append(name)
        if "Query-String" in dic:
            query_str = dic["Query-String"][i]
            if query_str:
                ophyd_string += f'query="{query_str}", '
            else:
                still_open.append(name)
        parse_str = dic["Return-Parser"][i]
        if parse_str:
            ophyd_string += f'parse="{parse_str}", '
        return_str = dic["Return-Type"][i]
        if return_str == "None":
            ophyd_string += "parse_return_type=None, "
        else:
            ophyd_string += f'parse_return_type="{return_str}", '
        if config:
            ophyd_string += 'kind="config", '
        ophyd_string += f'metadata={{"units": "{dic["Unit"][i]}", "description": "{dic["Description"][i]}"}})\n'
    return ophyd_string, still_open


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QCoreApplication
    from nomad_camels.utility import exception_hook

    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = Driver_Builder()
    ui.show()
    app.exec()
