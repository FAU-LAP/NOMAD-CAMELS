import os.path

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon, QCloseEvent

from utility.add_remove_table import AddRemoveTable
from utility import variables_handling, fit_variable_renaming
from tools.VISA_builder import Ui_VISA_Device_Builder

class VISA_Device_Builder(QWidget, Ui_VISA_Device_Builder):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        if os.path.isdir('graphics'):
            self.setWindowIcon(QIcon('graphics/CAMELS.svg'))
        else:
            self.setWindowIcon(QIcon('../graphics/CAMELS.svg'))

        label_in = QLabel('Input Channels')
        label_out = QLabel('Output Channels')
        label_config = QLabel('Config Channels')
        label_config_in = QLabel('Config Channels - Input Only')
        label_in.setStyleSheet("font-weight: bold")
        label_out.setStyleSheet("font-weight: bold")
        label_config.setStyleSheet("font-weight: bold")
        label_config_in.setStyleSheet("font-weight: bold")

        channel_info_config = ['Name', 'Format-String', 'Input-Type']
        channel_info_in = ['Name', 'Query-Text', 'fetch number from return-string']
        channel_info_out = ['Name', 'Format-String']
        comboBoxes = {'Input-Type': ['str', 'float', 'bool']}
        self.table_in = AddRemoveTable(headerLabels=channel_info_in,
                                       checkables=2, editables=[0,1])
        self.table_out = AddRemoveTable(headerLabels=channel_info_out)
        self.table_config = AddRemoveTable(headerLabels=channel_info_config,
                                           comboBoxes=comboBoxes)
        self.table_config_in = AddRemoveTable(headerLabels=channel_info_in,
                                              checkables=2, editables=[0,1])

        self.button_build = QPushButton('Build Device')
        self.button_cancel = QPushButton('Cancel')
        self.button_cancel.clicked.connect(self.close)
        self.button_build.clicked.connect(self.build_device)

        layout = self.layout()
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
        self.resize(600, 700)

    def build_device(self):
        name = fit_variable_renaming.replace_name(self.lineEdit_name.text())
        ophyd_name = fit_variable_renaming.replace_name(self.lineEdit_ophyd_name.text())
        read_term = fit_variable_renaming.replace_name(self.lineEdit_read_term.text())
        write_term = fit_variable_renaming.replace_name(self.lineEdit_write_term.text())
        baud_rate = int(self.lineEdit_baud_rate.text())
        search_tags = self.lineEdit_search_tags.text().split()
        inputs = self.table_in.update_table_data()
        outputs = self.table_out.update_table_data()
        configs = self.table_config.update_table_data()
        configs_in = self.table_config_in.update_table_data()

        path = variables_handling.device_driver_path or ''
        directory = QFileDialog.getExistingDirectory(self, "Select device-driver directory", f'{path}')
        if not directory:
            return

        fdir = f'{directory}/{name}'
        os.mkdir(fdir)

        class_string = f'from {name}.{name}_ophyd import {ophyd_name}\n\n'
        class_string += 'from main_classes import device_class\n\n'
        class_string += 'class subclass(device_class.Device):\n'
        class_string += '\tdef __init__(self, **kwargs):\n'
        class_string += f'\t\tsuper().__init__(name="{name}", virtual=False, tags={search_tags}, directory="{name}", ophyd_device={ophyd_name}, ophyd_class_name="{ophyd_name}", **kwargs)\n\n'
        class_string += 'class subclass_config(device_class.Simple_Config):\n'
        class_string += '\tdef __init__(self, parent=None, data="", settings_dict=None, config_dict=None, ioc_dict=None, additional_info=None):\n'
        class_string += f'\t\tsuper().__init__(parent, "{name}", data, settings_dict, config_dict, ioc_dict, additional_info)\n'
        class_string += '\t\tself.comboBox_connection_type.addItem("Local VISA")\n'
        class_string += '\t\tself.load_settings()\n'

        ophyd_string = 'from ophyd import Component as Cpt\n\n'
        ophyd_string += 'from bluesky_handling.visa_signal import VISA_Signal_Write, VISA_Signal_Read, VISA_Device\n\n'
        ophyd_string += f'class {ophyd_name}(VISA_Device):\n'
        for i, name in enumerate(inputs['Name']):
            ophyd_string += f'\t{name} = Cpt(VISA_Signal_Read, name="{name}", query_text="{inputs["Query-Text"][i]}", match_return={inputs["fetch number from return-string"][i]})\n'
        for i, name in enumerate(outputs['Name']):
            ophyd_string += f'\t{name} = Cpt(VISA_Signal_Write, name="{name}", put_format_string="{inputs["Format-String"][i]}")\n'
        for i, name in enumerate(configs['Name']):
            ophyd_string += f'\t{name} = Cpt(VISA_Signal_Write, name="{name}", put_format_string="{inputs["Format-String"][i]}")\n'
        for i, name in enumerate(configs_in['Name']):
            ophyd_string += f'\t{name} = Cpt(VISA_Signal_Read, name="{name}", query_text="{inputs["Query-Text"][i]}", match_return={inputs["fetch number from return-string"][i]})\n'

        ophyd_string += f'\n\tdef __init__(self, prefix="", *, name, kind=None, read_attrs=None, configuration_attrs=None, parent=None, resource_name="", **kwargs):\n'
        ophyd_string += f'\t\tsuper().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs, configuration_attrs=configuration_attrs, parent=parent, resource_name=resource_name, baud_rate={baud_rate}, read_termination="{read_term}", write_termination="{write_term}", **kwargs)'

    def closeEvent(self, a0: QCloseEvent) -> None:
        discard_dialog = QMessageBox.question(self, 'Discard Changes?',
                                              f'All changes will be lost!',
                                              QMessageBox.Yes | QMessageBox.No)
        if discard_dialog != QMessageBox.Yes:
            a0.ignore()
            return
        super().closeEvent(a0)






if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QCoreApplication
    import sys
    from utility import exception_hook
    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = VISA_Device_Builder()
    ui.show()
    app.exec_()
