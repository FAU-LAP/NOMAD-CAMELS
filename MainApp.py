import json
import sys
import importlib

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QCloseEvent, QStandardItem, QStandardItemModel

from utility import exception_hook, load_save_functions, treeView_functions, qthreads

from gui.mainWindow import Ui_MainWindow

from frontpanels.device_add_dialog import AddDeviceDialog
from EPICS_handling import make_ioc

device_path = r'C:\Users\od93yces\FAIRmat\devices_drivers/'

class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window for the program. Connects to all the other classes."""
    def __init__(self, parent=None):
        # basic setup
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CECS - Configurable Experimental Control System')
        self.setWindowIcon(QIcon('graphics/FAIRmat_L.png'))
        predev, premeas = load_save_functions.get_preset_list()
        for pre in predev:
            self.comboBox_device_preset.addItem(pre)
        if not predev:
            self.comboBox_device_preset.addItem('Default')
        for pre in premeas:
            self.comboBox_measurement_preset.addItem(pre)
        if not premeas:
            self.comboBox_measurement_preset.addItem('Default')
        self.setStyleSheet("QSplitter::handle{background: gray;}")

        # devices
        self.active_devices_dict = {}
        self.lineEdit_device_search.returnPressed.connect(self.build_devices_tree)
        self.item_model_devices = QStandardItemModel(0,1)
        self.treeView_devices.setModel(self.item_model_devices)
        self.treeView_devices.setHeaderHidden(True)
        all_devices = QStandardItem('All devices')
        all_devices.setEditable(False)
        virtual_devices = QStandardItem('Virtual devices')
        virtual_devices.setEditable(False)
        by_tags = QStandardItem('Devices by tags')
        by_tags.setEditable(False)
        self.item_model_devices.appendRow(all_devices)
        self.item_model_devices.appendRow(virtual_devices)
        self.item_model_devices.appendRow(by_tags)

        self.textEdit_console_output.setHidden(True)


        #connecting buttons
        self.pushButton_add_device.clicked.connect(self.add_device)
        self.pushButton_remove_device.clicked.connect(self.remove_device)
        self.actionAutosave_on_closing.changed.connect(self.change_preferences)
        self.actionSave_Device_Preset.triggered.connect(self.save_device_preset)
        self.pushButton_make_EPICS_environment.clicked.connect(self.make_epics_environment)
        self.pushButton_show_console_output.clicked.connect(self.show_console_output)
        self.treeView_devices.clicked.connect(self.tree_click)

        # saving and loading
        self.__save_dict_devices__ = {}
        self.__save_dict_meas__ = {}
        self.saving = False
        self._current_device_preset = 'Default'
        self._current_measurement_preset = 'Default'
        self.device_save_dict = {'_current_device_preset': self._current_device_preset,
                                 'active_devices_dict': self.active_devices_dict,
                                 'lineEdit_device_search': self.lineEdit_device_search}
        self.meas_save_dict = {'_current_measurement_preset': self._current_measurement_preset}
        self.load_preferences()
        self.load_state()
        self.device_config_widget = QWidget()
        self.comboBox_device_preset.currentTextChanged.connect(self.change_device_preset)
        # self.comboBox_measurement_preset.currentTextChanged.connect(self.change_measurement_preset)

    def remove_device(self):
        index = self.treeView_devices.selectedIndexes()[0]
        dat = self.item_model_devices.itemFromIndex(index).data()
        if dat is not None and not dat.startswith('tag:'):
            remove_dialog = QMessageBox.question(self, 'Remove device?', f'Are you sure you want to remove the device {dat}?', QMessageBox.Yes | QMessageBox.No)
            if remove_dialog == QMessageBox.Yes:
                self.active_devices_dict.pop(dat)
                self.build_devices_tree()

    def tree_click(self):
        index = self.treeView_devices.selectedIndexes()[0]
        dat = self.item_model_devices.itemFromIndex(index).data()
        if dat is not None and not dat.startswith('tag:'):
            if 'py_package' in self.active_devices_dict[dat]:
                if hasattr(self.device_config_widget, 'data'):
                    if self.device_config_widget.data in self.active_devices_dict:
                        self.active_devices_dict[self.device_config_widget.data].update({'settings': self.device_config_widget.get_settings()})
                self.device_config_widget = self.active_devices_dict[dat]['py_package'].subclass_config(self, dat, self.active_devices_dict[dat]['settings'])
                self.splitter.replaceWidget(2, self.device_config_widget)
                # while layout.count():
                #     child = layout.takeAt(0)
                #     if child.widget():
                #         child.widget().deleteLater()
                # widget = self.active_devices_dict[dat]['py_package'].subclass_config()
                # layout.addWidget(widget)


    def show_console_output(self):
        if self.textEdit_console_output.isHidden():
            self.textEdit_console_output.setHidden(False)
            self.pushButton_show_console_output.setText('Hide console output')
        else:
            self.textEdit_console_output.setHidden(True)
            self.pushButton_show_console_output.setText('Show console output')

    def save_device_preset(self):
        """Opens a QFileDialog to save the device preset. A backup / autosave of the preset is made automatically."""
        file = QFileDialog.getSaveFileName(self, 'Save Device Preset', load_save_functions.preset_path, '*.predev')[0]
        preset_name = file.split('/')[-1][:-7]
        self.saving = True
        self.comboBox_device_preset.addItem(preset_name)
        self.comboBox_device_preset.setCurrentText(preset_name)
        self.make_device_save_dict()
        load_save_functions.save_preset(file, self.__save_dict_devices__)
        self.saving = False

    def save_measurement_preset(self):
        """Opens a QFileDialog to save the device preset. A backup / autosave of the preset is made automatically."""
        file = QFileDialog.getSaveFileName(self, 'Save Measurement Preset', load_save_functions.preset_path, '*.premeas')[0]
        preset_name = file.split('/')[-1][:-8]
        self.saving = True
        self.comboBox_measurement_preset.addItem(preset_name)
        self.comboBox_measurement_preset.setCurrentText(preset_name)
        self.make_measurement_save_dict()
        load_save_functions.save_preset(file, self.__save_dict_meas__)
        self.saving = False

    def add_device(self):
        """Opens the dialog to add a device. The returned values of the dialog are inserted to the available devices."""
        add_dialog = AddDeviceDialog(active_devices_dict=self.active_devices_dict, parent=self)
        if add_dialog.exec_():
            self.active_devices_dict = add_dialog.active_devices_dict
        self.build_devices_tree()
        self.pushButton_make_EPICS_environment.setEnabled(True)

    def make_epics_environment(self):
        self.setCursor(Qt.WaitCursor)
        self.make_thread = qthreads.Make_Ioc(self._current_device_preset, self.active_devices_dict)
        self.make_thread.sig_step.connect(self.change_progressBar_value)
        self.make_thread.info_step.connect(self.update_console_output)
        self.make_thread.finished.connect(self.thread_finished)
        self.make_thread.start()

    def thread_finished(self):
        self.setCursor(Qt.ArrowCursor)

    def change_progressBar_value(self, val):
        self.progressBar_devices.setValue(val)

    def update_console_output(self, info):
        self.textEdit_console_output.append(info)

    def build_devices_tree(self):
        for i in range(3):
            item = self.item_model_devices.item(i,0)
            while item.rowCount() > 0:
                item.removeRow(0)
        tags = []
        search_text = self.lineEdit_device_search.text()
        for key, device in sorted(self.active_devices_dict.items()):
            if search_text.lower() not in key.lower():
                continue
            item = QStandardItem(key)
            item.setEditable(False)
            item.setData(key)
            if device['virtual']:
                self.item_model_devices.item(1,0).appendRow(item)
            else:
                self.item_model_devices.item(0,0).appendRow(item)
            for tag in device['tags']:
                item = QStandardItem(key)
                item.setEditable(False)
                item.setData(key)
                if tag not in tags:
                    tag_item = QStandardItem(tag)
                    tag_item.setEditable(False)
                    tag_item.setData(f'tag:{tag}')
                    self.item_model_devices.item(2,0).appendRow([tag_item])
                    tags.append(tag)
                else:
                    ind = treeView_functions.getItemIndex(self.item_model_devices, f'tag:{tag}')
                    tag_item = self.item_model_devices.itemFromIndex(ind)
                tag_item.appendRow([item])

    def load_preferences(self):
        """Loads the preferences.
        - autosave: turn on / off autosave on closing the program."""
        prefs = load_save_functions.get_preferences()
        if 'autosave' in prefs:
            self.actionAutosave_on_closing.setChecked(prefs['autosave'])

    def change_preferences(self):
        """Called when any preferences are changed. Makes the dictionary of preferences and calls save_preferences from the load_save_functions module."""
        prefs = {'autosave': self.actionAutosave_on_closing.isChecked()}
        load_save_functions.save_preferences(prefs)

    def make_device_save_dict(self):
        """Creates / Updates the __save_dict_devices__"""
        for key in self.device_save_dict:
            add_string = load_save_functions.get_save_str(self.device_save_dict[key])
            if add_string is not None:
                self.__save_dict_devices__.update({key: load_save_functions.get_save_str(self.device_save_dict[key])})

    def make_measurement_save_dict(self):
        """Creates / Updates the __save_dict_meas__"""
        for key in self.meas_save_dict:
            add_string = load_save_functions.get_save_str(self.meas_save_dict[key])
            if add_string is not None:
                self.__save_dict_meas__.update({key: load_save_functions.get_save_str(self.meas_save_dict[key])})



    def save_state(self):
        """Saves the current states of both presets."""
        self.save_device_state()
        self.save_measurement_state()

    def save_device_state(self):
        """makes the __save_dict_devices__, then calls the autosave."""
        self.make_device_save_dict()
        load_save_functions.autosave_preset(self._current_device_preset, self.__save_dict_devices__)

    def save_measurement_state(self):
        """makes the __save_dict_meas__, then calls the autosave."""
        self.make_measurement_save_dict()
        load_save_functions.autosave_preset(self._current_measurement_preset, self.__save_dict_meas__, False)


    def load_state(self):
        """Loads a specific state of the provided task."""
        predev, premeas = load_save_functions.get_most_recent_presets()
        if predev is not None:
            self.load_device_preset(predev)
        else:
            self.save_device_state()
        if premeas is not None:
            self.load_measurement_preset(premeas)
        else:
            self.save_measurement_state()

    def change_device_preset(self, preset):
        """saves the old device preset, then changes to / loads the new preset."""
        self.save_device_state()
        self._current_device_preset = preset
        self.load_device_preset(preset)

    def change_measurement_preset(self, preset):
        """saves the old measurement preset, then changes to / loads the new preset."""
        self.save_measurement_state()
        self._current_measurement_preset = preset
        self.load_measurement_preset(preset)

    def load_device_preset(self, preset):
        """Called when the comboBox_device_preset is changed (or when loading the last state). Opens the given preset."""
        if self.saving:
            return
        # self.save_device_state()
        with open(f'{load_save_functions.preset_path}{preset}.predev', 'r') as f:
            preset_dict = json.load(f)
        load_save_functions.load_save_dict(preset_dict, self.device_save_dict)
        self.pushButton_make_EPICS_environment.setEnabled(True)
        self.comboBox_device_preset.setCurrentText(self._current_device_preset)
        self.build_devices_tree()
        for d in self.active_devices_dict:
            info = self.active_devices_dict[d]
            try:
                package_name = info['name'].replace(' ', '_')
                info.update({'py_package': importlib.import_module(f'{package_name}.{package_name}')})
            except Exception as e:
                print(e)

    def load_measurement_preset(self, premeas):
        """Called when the comboBox_measurement_preset is changed (or when loading the last state). Opens the given preset."""
        if self.saving:
            return
        # self.save_measurement_state()
        with open(f'{load_save_functions.preset_path}{premeas}.predev', 'r') as f:
            preset_dict = json.load(f)
        load_save_functions.load_save_dict(preset_dict, self.meas_save_dict)
        self.comboBox_measurement_preset.setCurrentText(self._current_measurement_preset)

    def close(self) -> bool:
        """Calling the save_state method when closing the window."""
        if self.actionAutosave_on_closing.isChecked():
            self.save_state()
        return super().close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        """Calling the save_state method when closing the window."""
        if self.actionAutosave_on_closing.isChecked():
            self.save_state()
        super().closeEvent(a0)


if __name__ == '__main__':
    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ui.showMaximized()
    app.exec_()
