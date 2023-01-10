import json
import sys

import importlib
import os
import socket

import pandas as pd

from copy import deepcopy

from PyQt5.QtCore import QCoreApplication, Qt, QItemSelectionModel, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox,\
    QWidget, QMenu, QAction, QToolButton, QUndoStack, QShortcut, QStyle,\
    QPushButton
from PyQt5.QtGui import QIcon, QCloseEvent, QStandardItem, QStandardItemModel, QMouseEvent

from utility import exception_hook, load_save_functions, treeView_functions, qthreads, drag_drop_tree_view, number_formatting, variables_handling, \
    add_remove_table, theme_changing, console_redirect
from bluesky_handling import protocol_builder, make_catalog
from EPICS_handling import make_ioc

from frontpanels.helper_panels import pass_ask

from gui.mainWindow import Ui_MainWindow

from frontpanels.device_add_dialog import AddDeviceDialog
from frontpanels.settings_window import Settings_Window
from main_classes.protocol_class import Measurement_Protocol, General_Protocol_Settings
from commands import change_sequence

from loop_steps import make_step_of_type


from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback
import databroker


os.environ['QT_API'] = 'pyqt5'
camels_web = 'https://github.com/FAU-LAP/CAMELS'


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window for the program. Connects to all the other classes."""
    protocol_stepper_signal = pyqtSignal(int)

    def __init__(self, parent=None):
        # basic setup
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems')
        self.setWindowIcon(QIcon('graphics/CAMELS.svg'))
        presets = load_save_functions.get_preset_list()
        for pre in presets:
            self.comboBox_preset.addItem(pre)
        if not presets:
            self.comboBox_preset.addItem(f'{socket.gethostname()}')
        self.setStyleSheet("QSplitter::handle{background: gray;}")
        self.make_thread = None
        self.ioc_thread = None

        self.active_add_ons = {}
        self.add_ons = {}
        self.add_on_widget.setHidden(True)
        self.closing = False

        # devices
        self.active_devices_dict = {}
        variables_handling.devices = self.active_devices_dict
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
        # self.textEdit_console_output.setHidden(True)
        # self.textEdit_console_output_meas.setHidden(True)

        # measurements
        # self.run_thread = qthreads.Run_Protocol()
        # self.make_new_run_thread()
        self.protocols_dict = {}
        self.item_model_protocols = QStandardItemModel(0,1)
        self.listView_protocols.setModel(self.item_model_protocols)
        self.item_model_sequence = QStandardItemModel(0,1)
        self.sequence_main_widget.layout().removeWidget(self.treeView_protocol_sequence)
        self.treeView_protocol_sequence.deleteLater()
        self.treeView_protocol_sequence = drag_drop_tree_view.Drag_Drop_TreeView()
        self.treeView_protocol_sequence.del_clicked.connect(self.remove_loop_step)
        self.sequence_main_widget.layout().addWidget(self.treeView_protocol_sequence, 5, 0, 1, 3)
        self.treeView_protocol_sequence.setModel(self.item_model_sequence)
        self.treeView_protocol_sequence.customContextMenuRequested.connect(self.sequence_right_click)
        self.treeView_protocol_sequence.dragdrop.connect(self.update_loop_step_order)
        self.current_protocol = None
        self.loop_step_configuration_widget = None
        self.copied_loop_step = None
        self.sequence_main_widget.setEnabled(False)


        #connecting buttons
        self.pushButton_add_device.clicked.connect(self.add_device)
        self.pushButton_remove_device.clicked.connect(self.remove_device)
        self.actionSettings.triggered.connect(self.change_preferences)
        self.actionNew_Preset.triggered.connect(self.new_preset)
        self.actionSave_Preset.triggered.connect(self.save_state)
        self.actionSave_Preset_As.triggered.connect(self.save_preset_as)
        self.actionLoad_Backup_Preset.triggered.connect(self.load_backup_preset)
        self.actionVISA_device_builder.triggered.connect(self.launch_device_builder)
        self.pushButton_make_EPICS_environment.clicked.connect(self.make_epics_environment)
        self.pushButton_run_ioc.clicked.connect(self.run_stop_ioc)
        self.pushButton_show_console_output.clicked.connect(self.show_console_output)
        self.pushButton_clear_EPICS_output.clicked.connect(self.textEdit_console_output.clear)
        self.treeView_devices.clicked.connect(self.tree_click)
        self.pushButton_write_to_console.clicked.connect(self.write_to_console)
        self.lineEdit_send_to_IOC.returnPressed.connect(self.write_to_console)

        self.pushButton_add_protocol.clicked.connect(self.add_protocol)
        self.pushButton_remove_protocol.clicked.connect(self.remove_protocol)
        self.item_model_protocols.itemChanged.connect(self.change_protocol_name)
        self.pushButton_show_output_meas.clicked.connect(self.show_meas_output)
        self.pushButton_clear_output_meas.clicked.connect(self.textEdit_console_output_meas.clear)

        sys.stdout = self.textEdit_console_output_meas.text_writer
        sys.stderr = self.textEdit_console_output_meas.error_writer

        self.listView_protocols.clicked.connect(self.protocol_selected)
        self.pushButton_move_step_up.clicked.connect(lambda state: self.move_loop_step(-1,0))
        self.pushButton_move_step_down.clicked.connect(lambda state: self.move_loop_step(1,0))
        self.pushButton_move_step_in.clicked.connect(lambda state: self.move_loop_step(0,1))
        self.pushButton_move_step_out.clicked.connect(lambda state: self.move_loop_step(0,-1))
        self.treeView_protocol_sequence.clicked.connect(lambda x: self.tree_click_sequence(False))
        self.add_actions = []
        self.device_actions = []
        self.toolButton_add_step.setPopupMode(QToolButton.InstantPopup)
        self.pushButton_remove_step.clicked.connect(lambda x: self.remove_loop_step(True))
        self.pushButton_show_protocol_settings.clicked.connect(lambda x: self.tree_click_sequence(True))
        self.pushButton_build_protocol.clicked.connect(self.build_current_protocol)
        self.pushButton_open_protocol_external.clicked.connect(self.open_protocol)
        self.pushButton_run_protocol.clicked.connect(self.run_current_protocol)
        self.pushButton_write_to_ipython.clicked.connect(self.write_to_ipython)
        self.lineEdit_write_to_ipython.returnPressed.connect(self.write_to_ipython)
        self.lineEdit_write_to_ipython.setHidden(True)
        self.pushButton_write_to_ipython.setHidden(True)

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.pushButton_run_protocol.setIcon(icon)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        self.pushButton_pause_protocol.setIcon(icon)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        self.pushButton_stop_protocol.setIcon(icon)

        self.pushButton_pause_protocol.clicked.connect(self.pause_protocol)
        self.pushButton_stop_protocol.clicked.connect(self.stop_protocol)


        self.protocol_stepper_signal.connect(self.change_progressBar_value_meas)


        # help
        self.actionReport_Bug.triggered.connect(lambda x: os.startfile(f'{camels_web}/issues'))
        self.actionDocumentation.triggered.connect(lambda x: os.startfile(camels_web))

        # saving and loading
        self.__save_dict__ = {}
        self.saving = False
        self._current_preset = [f'{socket.gethostname()}']
        self.preset_save_dict = {'_current_preset': self._current_preset,
                                 'active_devices_dict': self.active_devices_dict,
                                 'lineEdit_device_search': self.lineEdit_device_search,
                                 'protocols_dict': self.protocols_dict}
        self.preferences = {}
        self.load_preferences()
        sys.path.append(self.preferences['device_driver_path'])
        self.load_state()
        self.device_config_widget = QWidget()
        self.comboBox_preset.currentTextChanged.connect(self.change_preset)
        self.update_add_step_actions()

        # Undo / Redo
        self.inside_function = False
        self.undo_stack = QUndoStack(self)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.actionUndo.setEnabled(self.undo_stack.canUndo())
        self.actionRedo.setEnabled(self.undo_stack.canRedo())
        QShortcut('Ctrl+z', self).activated.connect(self.undo)
        QShortcut('Ctrl+y', self).activated.connect(self.redo)
        QShortcut('Ctrl+s', self).activated.connect(self.save_state)

        QShortcut('Ctrl+x', self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut).activated.connect(self.cut_shortcut)
        QShortcut('Ctrl+v', self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut).activated.connect(self.paste_shortcut)
        QShortcut('Ctrl+c', self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut).activated.connect(self.copy_shortcut)

        # user and sample data
        self.sampledata = {}
        self.userdata = {}
        self.active_user = 'default_user'
        self.active_sample = 'default_sample'
        self.pushButton_editUserInfo.clicked.connect(self.edit_user_info)
        self.load_user_data()
        self.pushButton_editSampleInfo.clicked.connect(self.edit_sample_info)
        self.load_sample_data()
        variables_handling.CAMELS_path = os.path.dirname(__file__)

        self.show_console_output()

        if 'autostart_ioc' in self.preferences and self.preferences['autostart_ioc']:
            self.run_stop_ioc()

        # TODO remove followin line after tutorial!!!!
        # self.device_epics_widget.setHidden(True)
        self.sequence_main_widget.setHidden(True)
        self.configuration_main_widget.setHidden(True)


        self.run_engine = RunEngine()
        bec = BestEffortCallback()
        self.run_engine.subscribe(bec)
        self.databroker_catalog = databroker.catalog["CAMELS_CATALOG"]
        self.run_engine.subscribe(self.databroker_catalog.v1.insert)
        self.run_engine.subscribe(self.protocol_finished, 'stop')
        self.re_subs = []
        self.run_test = None


    def report_bug(self):
        path = f"{self.preferences['py_files_path']}/{self.current_protocol.name}.py"
        os.startfile(path)



    def mousePressEvent(self, a0: QMouseEvent) -> None:
        """Overwrite parent method to connect to undo and redo functions."""
        but = a0.button()
        if but == 8:
            self.undo()
        elif but == 16:
            self.redo()
        else:
            super().mousePressEvent(a0)

    def undo(self):
        # TODO implement actual functions
        self.undo_stack.undo()
        self.actionUndo.setEnabled(self.undo_stack.canUndo())
        self.actionRedo.setEnabled(self.undo_stack.canRedo())

    def redo(self):
        # TODO implement actual functions
        self.undo_stack.redo()
        self.actionUndo.setEnabled(self.undo_stack.canUndo())
        self.actionRedo.setEnabled(self.undo_stack.canRedo())

    # --------------------------------------------------
    # Overwriting parent-methods
    # --------------------------------------------------
    def close(self) -> bool:
        """Calling the save_state method when closing the window."""
        if self.ioc_thread:
            self.ioc_thread.terminate()
        # if self.run_thread:
        #     self.run_thread.terminate()
        if self.make_thread:
            self.make_thread.terminate()
        if self.preferences['autosave']:
            self.save_state()
        for add_on in self.active_add_ons:
            self.active_add_ons[add_on].close()
        self.closing = True
        return super().close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        """Calling the save_state method when closing the window."""
        self.closing = True
        if self.preferences['autosave']:
            self.save_state()
        if self.ioc_thread:
            self.ioc_thread.terminate()
        # if self.run_thread:
        #     self.run_thread.terminate()
        if self.make_thread:
            self.make_thread.terminate()
        # if self.preferences['autosave']:
        #     self.save_state()
        for add_on in self.active_add_ons:
            self.active_add_ons[add_on].close()
        super().closeEvent(a0)

    # --------------------------------------------------
    # user / sample methods
    # --------------------------------------------------
    def edit_user_info(self):
        """Calls dialog for user-information when
        pushButton_editUserInfo is clicked.

        The opened AddRemoveDialoge contains columns for Name, E-Mail,
        Affiliation, Address, ORCID and Phone of the user.
        If the dialog is canceled, nothing is changed, otherwise the new
        data will be written into self.userdata.
        """

        self.active_user = self.comboBox_user.currentText()
        headers = ['name', 'email', 'affiliation',
                   'address', 'orcid', 'telephone_number']
        tableData = pd.DataFrame.from_dict(self.userdata, 'index')
        dialog = add_remove_table.AddRemoveDialoge(headerLabels=headers,
                                                   parent=self,
                                                   title='User-Information',
                                                   askdelete=True,
                                                   tableData=tableData)
        if dialog.exec_():
            # changing the returned dict to dataframe and back to have a
            # dictionary that is formatted as {name: {'Name': name,...}, ...}
            dat = dialog.get_data()
            dat['Name2'] = dat['name']
            data = pd.DataFrame(dat)
            data.set_index('Name2', inplace=True)
            self.userdata = data.to_dict('index')
        self.comboBox_user.clear()
        self.comboBox_user.addItems(self.userdata.keys())
        if self.active_user in self.userdata:
            self.comboBox_user.setCurrentText(self.active_user)

    def save_user_data(self):
        """Calling the save_dictionary function with the savefile as
        %localappdata%/userdata.json and self.userdata as dictionary."""
        self.active_user = self.comboBox_user.currentText()
        userdic = {'active_user': self.active_user}
        userdic.update(self.userdata)
        load_save_functions.save_dictionary(f'{load_save_functions.appdata_path}/userdata.json', userdic)

    def load_user_data(self):
        """Loading the dictionary from %localappdata%/userdata.json,
        selecting the active user and saving the rest into self.userdata."""
        userdat = {}
        if os.path.isfile(f'{load_save_functions.appdata_path}/userdata.json'):
            with open(f'{load_save_functions.appdata_path}/userdata.json', 'r') as f:
                string_dict = json.load(f)
            load_save_functions.load_save_dict(string_dict, userdat, update_missing_key=True)
        if 'active_user' in userdat:
            self.active_user = userdat['active_user']
            userdat.pop('active_user')
        self.userdata = userdat
        self.comboBox_user.addItems(userdat.keys())
        if not self.active_user == 'default_user':
            self.comboBox_user.setCurrentText(self.active_user)

    def edit_sample_info(self):
        """Calls dialog for user-information when
        pushButton_editSampleInfo is clicked.

        The opened AddRemoveDialoge contains columns for Name,
        Identifier, and Preparation-Info.
        If the dialog is canceled, nothing is changed, otherwise the new
        data will be written into self.userdata.
        """

        self.active_sample = self.comboBox_sample.currentText()
        headers = ['name', 'sample_id', 'description']
        tableData = pd.DataFrame.from_dict(self.sampledata, 'index')
        dialog = add_remove_table.AddRemoveDialoge(headerLabels=headers, parent=self, title='Sample-Information', askdelete=True, tableData=tableData)
        if dialog.exec_():
            # changing the returned dict to dataframe and back to have a
            # dictionary that is formatted as {name: {'Name': name,...}, ...}
            dat = dialog.get_data()
            dat['Name2'] = dat['name']
            data = pd.DataFrame(dat)
            data.set_index('Name2', inplace=True)
            self.sampledata = data.to_dict('index')
        self.comboBox_sample.clear()
        self.comboBox_sample.addItems(self.sampledata.keys())
        if self.active_sample in self.sampledata.keys():
            self.comboBox_sample.setCurrentText(self.active_sample)

    def save_sample_data(self):
        """Calling the save_dictionary function with the savefile as
        %localappdata%/sampledata.json and self.sampledata as dictionary."""
        self.active_sample = self.comboBox_sample.currentText()
        sampledic = {'active_sample': self.active_sample}
        sampledic.update(self.sampledata)
        load_save_functions.save_dictionary(f'{load_save_functions.appdata_path}/sampledata.json', sampledic)

    def load_sample_data(self):
        """Loading the dictionary from %localappdata%/sampledata.json,
        selecting the active sample and saving the rest into self.sampledata."""
        sampledat = {}
        if os.path.isfile(f'{load_save_functions.appdata_path}/sampledata.json'):
            with open(f'{load_save_functions.appdata_path}/sampledata.json', 'r') as f:
                string_dict = json.load(f)
            load_save_functions.load_save_dict(string_dict, sampledat, update_missing_key=True)
        if 'active_sample' in sampledat:
            self.active_sample = sampledat['active_sample']
            sampledat.pop('active_sample')
        self.sampledata = sampledat
        self.comboBox_sample.addItems(sampledat.keys())
        if not self.active_sample == 'default_sample':
            self.comboBox_sample.setCurrentText(self.active_sample)

    # --------------------------------------------------
    # save / load methods
    # --------------------------------------------------
    def load_preferences(self):
        """Loads the preferences.

        Those may contain:
        - autosave: turn on / off autosave on closing the program.
        - dark_mode: turning dark-mode on / off.
        - number_format: the number format for display, can be either
            "mixed", "plain" or "scientific".
        - mixed_from: the exponent from where to switch to
            scientific format, if number_format is "mixed".
        - n_decimals: the number of displayed decimals of a number.
        - py_files_path: the path, where python files (e.g. protocols)
            are created.
        - meas_files_path: the path, where measurement data is stored.
        - device_driver_path: the path, where CAMELS can find the
            installed devices.
        - databroker_catalog_name: the name of the databroker catalog
        """

        self.preferences = load_save_functions.get_preferences()
        variables_handling.preferences = self.preferences
        number_formatting.preferences = self.preferences
        # if 'dark_mode' in self.preferences:
        #     self.toggle_dark_mode()
        if 'graphic_theme' in self.preferences:
            self.change_theme()
        self.change_catalog_name()
        variables_handling.device_driver_path = self.preferences['device_driver_path']
        variables_handling.meas_files_path = self.preferences['meas_files_path']

    def change_theme(self):
        theme = self.preferences['graphic_theme']
        theme_changing.change_theme(theme)
        self.toggle_dark_mode()

    def toggle_dark_mode(self):
        """Turning dark mode on / off, called whenever the settigns are
        changed. Using qdarkstyle to provide the stylesheets."""
        dark = self.preferences['dark_mode']
        variables_handling.dark_mode = dark

    def change_catalog_name(self):
        if 'meas_files_path' in self.preferences:
            catalog_name = 'CATALOG_NAME'
            if 'databroker_catalog_name' in self.preferences:
                catalog_name = self.preferences['databroker_catalog_name']
            make_catalog.make_yml(self.preferences['meas_files_path'], catalog_name)

    def launch_device_builder(self):
        from tools import VISA_device_builder
        device_builder = VISA_device_builder.VISA_Device_Builder(self)
        device_builder.show()


    def change_preferences(self):
        """Called when any preferences are changed. Makes the dictionary
         of preferences and calls save_preferences from the
         load_save_functions module."""
        settings_dialog = Settings_Window(parent=self, settings=self.preferences)
        if settings_dialog.exec_():
            self.preferences = settings_dialog.get_settings()
            number_formatting.preferences = self.preferences
            # self.toggle_dark_mode()
            self.change_catalog_name()
            load_save_functions.save_preferences(self.preferences)
            variables_handling.device_driver_path = self.preferences['device_driver_path']
            variables_handling.meas_files_path = self.preferences['meas_files_path']
        self.change_theme()
        # prefs = {'autosave': self.actionAutosave_on_closing.isChecked(),
        #          'dark_mode': self.actionDark_Mode.isChecked()}
        # load_save_functions.save_preferences(prefs)

    def save_state(self, fromload=False):
        """Saves the current states of both presets."""
        self.make_save_dict()
        load_save_functions.autosave_preset(self._current_preset[0], self.__save_dict__)
        if fromload:
            return
        # self.save_device_state()
        # self.save_measurement_state()
        self.save_user_data()
        self.save_sample_data()
        print('current state saved!')

    def new_preset(self):
        """Create a new, empty device-preset via a QFileDialog."""
        file = QFileDialog.getSaveFileName(self, 'Save Preset',
                                           load_save_functions.preset_path,
                                           '*.preset')[0]
        if not len(file):
            return
        preset_name = file.split('/')[-1][:-7]
        load_save_functions.save_preset(file, {'_current_preset': [preset_name],
                                               'active_devices_dict': {},
                                               'lineEdit_device_search': '',
                                               'protocols_dict': {}})
        self.comboBox_preset.addItem(preset_name)
        self.comboBox_preset.setCurrentText(preset_name)
        self._current_preset[0] = preset_name


    def save_preset_as(self):
        """Opens a QFileDialog to save the device preset.
        A backup / autosave of the preset is made automatically."""
        file = QFileDialog.getSaveFileName(self, 'Save Preset',
                                           load_save_functions.preset_path,
                                           '*.preset')[0]
        if not len(file):
            return
        preset_name = file.split('/')[-1][:-7]
        self.saving = True
        self.comboBox_preset.addItem(preset_name)
        self.comboBox_preset.setCurrentText(preset_name)
        self._current_preset[0] = preset_name
        self.make_save_dict()
        load_save_functions.save_preset(file, self.__save_dict__)
        self.saving = False


    def load_backup_preset(self):
        """Opens a QFileDialog in the Backup-folder of the presets.
        If a backup is selected, the current preset is put into backup."""
        file = QFileDialog.getOpenFileName(self, 'Open Preset',
                                           f'{load_save_functions.preset_path}/Backup',
                                           '*.preset')[0]
        if not len(file):
            return
        preset_name = file.split('_')[-1][:-7]
        preset = f'Backup/{file.split("/")[-2]}/{file.split("/")[-1][:-7]}'
        self.save_state()
        self._current_preset[0] = preset_name
        self.load_preset(preset)


    def load_state(self):
        """Loads the most recent presets."""
        preset = load_save_functions.get_most_recent_presets()
        if preset is not None:
            self.load_preset(preset)
        else:
            self.save_state(True)

    def change_preset(self, preset):
        """saves the old device preset,
        then changes to / loads the new preset."""
        self.save_state()
        self._current_preset[0] = preset
        self.load_preset(preset)


    def load_preset(self, preset):
        """Called when the comboBox_device_preset is changed
        (or when loading the last state). Opens the given preset."""
        if self.saving:
            return
        with open(f'{load_save_functions.preset_path}{preset}.preset', 'r') as f:
            preset_dict = json.load(f)
        load_save_functions.load_save_dict(preset_dict, self.preset_save_dict)
        self.pushButton_make_EPICS_environment.setEnabled(True)
        self.comboBox_preset.setCurrentText(self._current_preset[0])
        self.build_devices_tree()
        self.update_channels()
        variables_handling.preset = self._current_preset[0]
        self.build_protocol_list()


    def update_channels(self):
        """Called when the active devices change.
        The channels in variables_handling are updated with the ones
        provided by the active devices."""
        variables_handling.channels.clear()
        for key, dev in self.active_devices_dict.items():
            for channel in dev.get_channels():
                variables_handling.channels.update({channel: dev.channels[channel]})
        self.update_device_add_ons()

    def update_device_add_ons(self):
        layout = self.add_on_buttons.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()
        self.add_ons.clear()
        for key, dev in self.active_devices_dict.items():
            add_ons = dev.get_add_ons()
            for add_on in add_ons:
                self.add_ons[f'{key}\n{add_on}'] = add_ons[add_on]
        if self.add_ons:
            self.add_on_widget.setHidden(False)
        else:
            self.add_on_widget.setHidden(True)
        for add_on in sorted(self.add_ons):
            button = QPushButton(add_on)
            self.add_on_buttons.layout().addWidget(button)
            button.clicked.connect(lambda state, x=add_on, y=button, z=self.add_ons[add_on][1]: self.start_addon(x, y, z))

    def start_addon(self, addon, button, device=None):
        self.get_device_config(False)
        add_on = self.add_ons[addon][0](device=device)
        self.active_add_ons[addon] = add_on
        add_on.closing.connect(lambda x=addon, y=button: self.stopped_addon(x, y))
        button.setEnabled(False)

    def stopped_addon(self, addon, button):
        if self.closing:
            return
        self.active_add_ons.pop(addon)
        button.setEnabled(True)

    def make_save_dict(self):
        self.get_device_config()
        self.get_step_config()
        self.update_loop_step_order()
        for key in self.preset_save_dict:
            add_string = load_save_functions.get_save_str(self.preset_save_dict[key])
            if add_string is not None:
                self.__save_dict__.update({key: load_save_functions.get_save_str(self.preset_save_dict[key])})

    # --------------------------------------------------
    # Threads - general
    # --------------------------------------------------
    def protocol_finished(self, *args):
        # self.pushButton_run_protocol.setText('Build and run selected protocol')
        self.thread_finished()
        for sub in self.re_subs:
            self.run_engine.unsubscribe(sub)
        self.pushButton_stop_protocol.setEnabled(False)
        self.pushButton_pause_protocol.setEnabled(False)
        self.pushButton_run_protocol.setEnabled(True)
        self.pushButton_run_protocol.setText('Run')

    def make_new_run_thread(self):
        self.run_thread = qthreads.Run_Protocol()
        self.run_thread.start()
        self.run_thread.sig_step.connect(self.change_progressBar_value_meas)
        self.run_thread.info_step.connect(self.update_protocol_output)
        self.run_thread.finished.connect(self.run_thread_finished)
        self.run_thread.protocol_done.connect(self.protocol_finished)

    def run_thread_finished(self):
        # self.pushButton_run_protocol.setText('Build and run selected protocol')
        self.run_thread = None
        self.protocol_finished()
        self.make_new_run_thread()

    def make_thread_finished(self):
        self.make_thread = None
        self.pushButton_run_ioc.setEnabled(True)
        self.thread_finished()

    def thread_finished(self):
        """Called, when a run_thread or make_thread is finished. If both
         are finished, the cursor is set back to the ArrowCursor."""
        if self.make_thread is None:
            self.setCursor(Qt.ArrowCursor)

    def change_progressBar_value(self, val):
        """Sets the progressBar_devices to the given val."""
        self.progressBar_devices.setValue(val)

    def change_progressBar_value_meas(self, val):
        """Sets the progressBar_protocols to the given val."""
        self.progressBar_protocols.setValue(val)

    # --------------------------------------------------
    # devices methods
    # --------------------------------------------------
    def remove_device(self):
        """Opens a dialog to confirm removing the device, then pops it
        from the active_devices_dict."""
        index = self.treeView_devices.selectedIndexes()[0]
        dat = self.item_model_devices.itemFromIndex(index).data()
        if dat is not None and not dat.startswith('tag:'):
            remove_dialog = QMessageBox.question(self, 'Remove device?',
                                                 f'Are you sure you want to remove the device {dat}?',
                                                 QMessageBox.Yes | QMessageBox.No)
            if remove_dialog == QMessageBox.Yes:
                self.active_devices_dict.pop(dat)
                self.build_devices_tree()
                self.update_channels()
                self.ioc_config_changed()
        self.update_add_step_actions()

    def add_device(self):
        """Opens the dialog to add a device. The returned values of the
        dialog are inserted to the available devices."""
        add_dialog = AddDeviceDialog(active_devices_dict=self.active_devices_dict,
                                     parent=self)
        if add_dialog.exec_():
            self.active_devices_dict = add_dialog.active_devices_dict
        self.build_devices_tree()
        # self.pushButton_make_EPICS_environment.setEnabled(True)
        self.ioc_config_changed()
        self.update_channels()
        self.update_add_step_actions()

    def tree_click(self):
        """Called when clicking the treeView_devices. If the selected
        index is a device, it will call the config-Widget, and, if
        possible, save the settings of the last opened config-widget."""
        index = self.treeView_devices.selectedIndexes()[0]
        dat = self.item_model_devices.itemFromIndex(index).data()
        if dat is not None and not dat.startswith('tag:'):
            dev_type = self.active_devices_dict[dat].name
            py_package = importlib.import_module(f'{dev_type}.{dev_type}')
            self.get_device_config()
            self.device_config_widget = py_package.subclass_config(self, dat,
                                                                   settings_dict=self.active_devices_dict[dat].settings,
                                                                   config_dict=self.active_devices_dict[dat].config,
                                                                   ioc_dict=self.active_devices_dict[dat].ioc_settings,
                                                                   additional_info=self.active_devices_dict[dat].additional_info)
            self.devices_splitter.replaceWidget(2, self.device_config_widget)
            self.device_config_widget.ioc_change.connect(self.ioc_config_changed)
            self.device_config_widget.name_change.connect(self.name_config_changed)

    def name_config_changed(self, new_name):
        if hasattr(self.device_config_widget, 'data'):
            if self.device_config_widget.data in self.active_devices_dict:
                if new_name not in self.active_devices_dict:
                    old_name = self.device_config_widget.data
                    self.active_devices_dict[new_name] = self.active_devices_dict[old_name]
                    self.active_devices_dict.pop(old_name)
                    self.active_devices_dict[new_name].custom_name = new_name
                    self.update_channels()
                    self.build_devices_tree()
                    self.device_config_widget.data = new_name




    def ioc_config_changed(self):
        """Called when a value of device-config has changed that is part
        of the IOC (e.g. connection), sets the Make IOC button bold and
        the progressBar to zero."""
        font = self.pushButton_make_EPICS_environment.font()
        font.setBold(True)
        self.pushButton_make_EPICS_environment.setFont(font)
        self.progressBar_devices.setValue(0)

    def get_device_config(self, update=True):
        """If the currently used device_config_widget has the attribute
        data, the settings will be updated to the active_devices_dict."""
        if hasattr(self.device_config_widget, 'data'):
            if self.device_config_widget.data in self.active_devices_dict:
                self.active_devices_dict[self.device_config_widget.data].settings = self.device_config_widget.get_settings()
                self.active_devices_dict[self.device_config_widget.data].config = self.device_config_widget.get_config()
                self.active_devices_dict[self.device_config_widget.data].ioc_settings = self.device_config_widget.get_ioc_settings()
                self.active_devices_dict[self.device_config_widget.data].additional_info = self.device_config_widget.get_info()
        if update:
            self.update_channels()

    def build_devices_tree(self):
        """Builds the tree of devices.
        First it clears the tree and then iterates through all available
        devices in device_dict.
        If a search_text is given, only devices whose name includes the
        string in search_text are added to the tree."""
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
            if device.virtual:
                self.item_model_devices.item(1,0).appendRow(item)
            else:
                self.item_model_devices.item(0,0).appendRow(item)
            for tag in device.tags:
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

    # EPICS
    def make_epics_environment(self):
        """Calls the QThread Make_Ioc, creating an IOC with the
        specified devices."""
        self.setCursor(Qt.WaitCursor)
        font = self.pushButton_make_EPICS_environment.font()
        font.setBold(False)
        self.pushButton_make_EPICS_environment.setFont(font)
        self.get_device_config()
        if not make_ioc.sudo_pwd:
            pwd_dialog = pass_ask.Pass_Ask(self)
            if pwd_dialog.exec_():
                make_ioc.sudo_pwd = pwd_dialog.lineEdit_password_1.text()
        self.make_thread = qthreads.Make_Ioc(self._current_preset[0], self.active_devices_dict)
        self.make_thread.sig_step.connect(self.change_progressBar_value)
        self.make_thread.info_step.connect(self.update_console_output)
        self.make_thread.finished.connect(self.make_thread_finished)
        self.make_thread.start()
        self.pushButton_run_ioc.setEnabled(False)

    def show_console_output(self):
        """Shows / hides the textEdit_console_output."""
        if self.textEdit_console_output.isHidden():
            self.textEdit_console_output.setHidden(False)
            self.pushButton_write_to_console.setHidden(False)
            self.lineEdit_send_to_IOC.setHidden(False)
            self.pushButton_show_console_output.setText('Hide output')
        else:
            self.textEdit_console_output.setHidden(True)
            self.pushButton_write_to_console.setHidden(True)
            self.lineEdit_send_to_IOC.setHidden(True)
            self.pushButton_show_console_output.setText('Show output')

    def update_console_output(self, info):
        """Appends the given info to the current console output."""
        self.textEdit_console_output.append(info)

    def run_stop_ioc(self):
        """Calls the Run_IOC QThread. The IOC corresponding to the
        current device preset is run in that thread, until the button is
        pushed again, on which the thread is terminated."""
        if self.ioc_thread is None:
            self.ioc_thread = qthreads.Run_IOC(self._current_preset[0])
            self.ioc_thread.info_step.connect(self.update_console_output)
            self.ioc_thread.finished.connect(self.stop_ioc)
            self.pushButton_run_ioc.setText('Stop IOC')
            self.ioc_thread.start()
            self.pushButton_make_EPICS_environment.setEnabled(False)
            self.pushButton_write_to_console.setEnabled(True)
            self.lineEdit_send_to_IOC.setEnabled(True)
            self.running_checkbox_style(True)
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop)
            self.pushButton_run_ioc.setIcon(icon)
        else:
            self.ioc_thread.terminate()
            self.stop_ioc()

    def running_checkbox_style(self, is_running):
        if is_running:
            col = variables_handling.get_color('green', True)
            self.checkBox_ioc_running.setText('is running')
            self.checkBox_ioc_running.setChecked(True)
        else:
            col = variables_handling.get_color('red', True)
            self.checkBox_ioc_running.setText('not running')
            self.checkBox_ioc_running.setChecked(False)
        self.checkBox_ioc_running.setStyleSheet(f"color: rgb{col}")

    def stop_ioc(self):
        """Called, when either the IOC is terminated by hand, or when it
        is finished (e.g. because of some error). Sets the button-text
        back to "Run IOC"."""
        del self.ioc_thread
        self.ioc_thread = None
        self.pushButton_run_ioc.setText('Run IOC')
        self.pushButton_make_EPICS_environment.setEnabled(True)
        self.pushButton_write_to_console.setEnabled(False)
        self.lineEdit_send_to_IOC.setEnabled(False)
        self.running_checkbox_style(False)
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.pushButton_run_ioc.setIcon(icon)

    def write_to_console(self):
        if self.ioc_thread is not None:
            text = self.lineEdit_send_to_IOC.text()
            self.ioc_thread.write_to_ioc(text)
            self.lineEdit_send_to_IOC.clear()
        else:
            raise Exception('Can only send to running ioc!')

    # --------------------------------------------------
    # measurement methods
    # --------------------------------------------------
    def update_add_step_actions(self):
        """Called when the devices change, updating the possible
        loopsteps to include new device steps."""
        self.add_actions.clear()
        self.device_actions.clear()
        for stp in sorted(make_step_of_type.step_type_config.keys(), key=lambda x: x.lower()):
            action = QAction(stp)
            action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
            self.add_actions.append(action)
        for stp in make_step_of_type.get_device_steps():
            action = QAction(stp)
            action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
            self.device_actions.append(action)
        self.toolButton_add_step.addActions(self.add_actions)
        if self.device_actions:
            self.toolButton_add_step.addActions(self.device_actions)


    def update_protocol_output(self, info):
        """Appens the given `info` to the console_output_meas."""
        self.textEdit_console_output_meas.append(info)

    def run_current_protocol(self):
        """Calls the Run_Protocol QThread. The currently selected
        protocol is used. If the button is clicked agian, the thread is
        terminated."""
        # if self.run_thread is None:
        #     self.make_new_run_thread()
        # elif self.run_thread.paused:
        #     self.run_thread.resume()
        #     self.pushButton_run_protocol.setEnabled(False)
        #     self.pushButton_pause_protocol.setEnabled(True)
        #     self.pushButton_run_protocol.setText('Run')
        #     return
        # elif self.run_thread.already_run:
        #     self.stop_protocol()
        #     self.make_new_run_thread()
        #     print(3)
        if self.run_engine.state == 'paused':
            self.run_engine.resume()
            self.pushButton_run_protocol.setText('Run')
            self.pushButton_run_protocol.setEnabled(False)
            self.pushButton_pause_protocol.setEnabled(True)
        else:
            self.build_current_protocol(put100=False)
            self.setCursor(Qt.WaitCursor)
            path = f"{self.preferences['py_files_path']}/{self.current_protocol.name}.py"
            # self.pushButton_run_protocol.setText('Abort Run')
            # self.run_thread.run_protocol(path, self.current_protocol.get_total_steps())
            name = os.path.basename(path)[:-3]
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mod
            spec.loader.exec_module(mod)
            mod.protocol_step_information['protocol_stepper_signal'] = self.protocol_stepper_signal
            plots, self.re_subs = mod.create_plots(self.run_engine)
            self.pushButton_run_protocol.setEnabled(False)
            self.pushButton_pause_protocol.setEnabled(True)
            self.pushButton_stop_protocol.setEnabled(True)
            mod.main(self.run_engine, catalog=self.databroker_catalog)
            self.protocol_stepper_signal.emit(100)
        # self.run_test = qthreads.Run_Protocol_test(self.run_engine, mod.main)
        # self.run_test.start()
        # else:
        #     self.run_thread.terminate()
        #     self.run_thread_finished()

    def write_to_ipython(self):
        if self.run_thread is not None:
            text = self.lineEdit_write_to_ipython.text()
            self.run_thread.write_to_console(text)
            self.lineEdit_write_to_ipython.clear()
        else:
            raise Exception('No IPython shell open!')

    def pause_protocol(self):
        # if self.run_thread is not None:
        #     self.run_thread.pause()
        if self.run_engine.state == 'running':
            self.run_engine.request_pause(True)
            self.pushButton_run_protocol.setText('Resume')
            self.pushButton_run_protocol.setEnabled(True)
            self.pushButton_pause_protocol.setEnabled(False)

    def stop_protocol(self):
        # self.run_thread.terminate()
        if self.run_engine.state != 'idle':
            self.run_engine.abort('Aborted by user')
        # self.run_thread.abort()
        self.protocol_finished()

    def open_protocol(self):
        if self.current_protocol is None:
            raise Exception('You need to select a protocol!')
        path = f"{self.preferences['py_files_path']}/{self.current_protocol.name}.py"
        os.startfile(path)


    def build_current_protocol(self, *, put100=True):
        """Calls the build_protocol from bluesky_handling.protocol_builder
        for the selected protocol and provides it with a savepath and
        user- and sample-data."""
        self.progressBar_protocols.setValue(0)
        self.get_step_config()
        self.update_loop_step_order()
        self.get_device_config()
        if self.current_protocol is None:
            raise Exception('You need to select a protocol!')
        path = f"{self.preferences['py_files_path']}/{self.current_protocol.name}.py"
        user = self.comboBox_user.currentText() or 'default_user'
        sample = self.comboBox_sample.currentText() or 'default_sample'
        userdata = {'name': 'default_user'} if user == 'default_user' else self.userdata[user]
        sampledata = {'name': 'default_sample'} if sample == 'default_sample' else self.sampledata[sample]
        savepath = f'{self.preferences["meas_files_path"]}/{user}/{sample}/{self.current_protocol.filename or "data"}.h5'
        protocol_builder.build_protocol(self.current_protocol, path, savepath,
                                        userdata=userdata, sampledata=sampledata)
        self.textEdit_console_output_meas.append('\n\nBuild successfull!\n')
        self.progressBar_protocols.setValue(100 if put100 else 1)

    def tree_click_sequence(self, general=False):
        """Called when clicking the treeView_protocol_sequence."""
        self.update_loop_step_order()
        self.get_step_config()
        self.current_protocol.update_variables()
        config = None
        if general:
            config = General_Protocol_Settings(self, self.current_protocol)
            self.enable_step_move(False)
            self.label_configuration.setText('Configuration: General Protocol Settings')
        else:
            index = self.treeView_protocol_sequence.selectedIndexes()[0]
            dat = self.item_model_sequence.itemFromIndex(index).data()
            if dat is not None:
                step = self.current_protocol.loop_step_dict[dat]
                config = make_step_of_type.get_config(step)
                enable = step.step_type not in make_step_of_type.non_addables
                self.enable_step_move(enable)
                self.label_configuration.setText(f'Configuration: {step.full_name}')
        if config is not None:
            if self.loop_step_configuration_widget is not None:
                self.configuration_main_widget.layout().removeWidget(self.loop_step_configuration_widget)
                self.loop_step_configuration_widget.deleteLater()
            self.loop_step_configuration_widget = config
            self.configuration_main_widget.layout().addWidget(self.loop_step_configuration_widget, 1, 0)
            if not general:
                self.loop_step_configuration_widget.name_changed.connect(self.change_step_name)

    def enable_step_move(self, enable):
        self.pushButton_move_step_in.setEnabled(enable)
        self.pushButton_move_step_out.setEnabled(enable)
        self.pushButton_move_step_up.setEnabled(enable)
        self.pushButton_move_step_down.setEnabled(enable)

    def change_step_name(self):
        """Called when a loop_step changes its name, then updates the
        shown sequence, and also the protocol-data."""
        self.build_protocol_sequence()
        self.update_loop_step_order()

    def get_step_config(self):
        """Updates the data in the currently-to-configure loop_step."""
        if self.loop_step_configuration_widget is not None:
            self.loop_step_configuration_widget.update_step_config()


    def add_protocol(self):
        """Adds a new protocol 'Unnamed_Protocol' to the list.
        Makes sure that it has a unique filename."""
        name = self.unique_protocol_name('Unnamed_Protocol')
        protocol = {name: Measurement_Protocol(name=name)}
        self.protocols_dict.update(protocol)
        self.build_protocol_list()

    def remove_protocol(self):
        """Opens a dialog to make sure, then removes the selected
        protocol."""
        index = self.listView_protocols.selectedIndexes()[0]
        dat = self.item_model_protocols.itemFromIndex(index).data()
        if dat is not None:
            remove_dialog = QMessageBox.question(self, 'Delete protocol?', f'Are you sure you want to delete the protocol {dat}?', QMessageBox.Yes | QMessageBox.No)
            if remove_dialog == QMessageBox.Yes:
                self.protocols_dict.pop(dat)
                self.build_protocol_list()

    def change_protocol_name(self, item):
        """Changes the name of the protocol inside the protocols_dict.

        Parameters
        ----------
        item : QStandardItem
            the item of the protocol, the data is used to get the old
            name, the new text is checked to be unique.
        """

        if self.inside_function:
            return
        old_name = item.data()
        protocol_data = self.protocols_dict.pop(old_name)
        new_name = self.unique_protocol_name(item.text())
        self.inside_function = True
        item.setText(new_name)
        item.setData(new_name)
        self.inside_function = False
        self.protocols_dict.update({new_name: protocol_data})
        self.protocols_dict[new_name].name = new_name
        self.build_protocol_list()

    def unique_protocol_name(self, name):
        """Checks if 'name' is already inside the protocols_dict,
        if yes, _i is added until i is a not yet used number."""
        if name in self.protocols_dict:
            i = 2
            while True:
                if f'{name}_{i}' not in self.protocols_dict:
                    return f'{name}_{i}'
                i += 1
        else:
            return name

    def build_protocol_list(self):
        """Rebuilds the listView_protocols / the item_model_protocols."""
        self.item_model_protocols.clear()
        for protocol in sorted(self.protocols_dict, key=lambda x: x.lower()):
            item = QStandardItem(protocol)
            # item.setCheckable(True)
            item.setData(protocol)
            self.item_model_protocols.appendRow(item)

    def show_meas_output(self):
        """Shows / hides the textEdit_console_output."""
        if self.textEdit_console_output_meas.isHidden():
            self.textEdit_console_output_meas.setHidden(False)
            self.lineEdit_write_to_ipython.setHidden(False)
            self.pushButton_write_to_ipython.setHidden(False)
            self.pushButton_show_output_meas.setText('Hide output')
        else:
            self.textEdit_console_output_meas.setHidden(True)
            self.lineEdit_write_to_ipython.setHidden(True)
            self.pushButton_write_to_ipython.setHidden(True)
            self.pushButton_show_output_meas.setText('Show output')

    def protocol_selected(self):
        """Called when a protocol is clicked on. Updates the
        loop_step_order of the old protocol, the builds the sequence of
        the new one."""
        self.update_loop_step_order()
        self.build_protocol_sequence()
        ind = self.listView_protocols.selectedIndexes()[0]
        prot_name = self.item_model_protocols.itemFromIndex(ind).data()
        self.label_sequence.setText(f'{prot_name}: Sequence')
        self.sequence_main_widget.setHidden(False)
        self.configuration_main_widget.setHidden(False)
        self.tree_click_sequence(True)

    def build_protocol_sequence(self):
        """Shows / builds the protocol sequence in the treeView
        dependent on the loop_steps in the current_protocol."""
        ind = self.listView_protocols.selectedIndexes()
        if not ind:
            return
        ind = ind[0]
        ind_seq = self.treeView_protocol_sequence.selectedIndexes()
        sel_data = ''
        if ind_seq:
            sel_data = self.item_model_sequence.data(ind_seq[0])
        prot_name = self.item_model_protocols.itemFromIndex(ind).data()
        protocol = self.protocols_dict[prot_name]
        self.current_protocol = protocol
        variables_handling.current_protocol = protocol
        variables_handling.protocol_variables = self.current_protocol.variables
        variables_handling.loop_step_variables = self.current_protocol.loop_step_variables
        self.item_model_sequence.clear()
        for loop_step in protocol.loop_steps:
            loop_step.append_to_model(self.item_model_sequence)
        self.treeView_protocol_sequence.expandAll()
        self.sequence_main_widget.setEnabled(True)
        if sel_data is not None:
            new_index = treeView_functions.getItemIndex(self.item_model_sequence, sel_data)
            if new_index:
                self.treeView_protocol_sequence.selectionModel().select(new_index, QItemSelectionModel.Select)

    def sequence_right_click(self, pos):
        """Opens a specific Menu on right click in the protocol-sequence.
        If selection is not on a loop_step, it consists only of Add Step,
        otherwise it consists of Delete Step."""
        # TODO other actions
        # TODO more beautiful?
        menu = QMenu()
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if inds:
            item = self.item_model_sequence.itemFromIndex(inds[0])
            below_actions = []
            above_actions = []
            into_actions = []
            row = inds[0].row()
            parent = item.parent()
            if parent is not None:
                parent = parent.data()
            # for stp in sorted(drag_drop_tree_view.step_types, key=lambda x: x.lower()):
            device_steps = make_step_of_type.get_device_steps()
            for stp in sorted(make_step_of_type.step_type_config.keys(), key=lambda x: x.lower()):
                action = QAction(stp)
                action_a = QAction(stp)
                action_in = QAction(stp)
                action.triggered.connect(lambda state, x=stp, y=row+1, z=parent: self.add_loop_step(x, y, z))
                action_a.triggered.connect(lambda state, x=stp, y=row, z=parent: self.add_loop_step(x, y, z))
                action_in.triggered.connect(lambda state, x=stp, y=-1, z=item.data(): self.add_loop_step(x,y,z))
                below_actions.append(action)
                above_actions.append(action_a)
                into_actions.append(action_in)
            device_actions = []
            device_actions_a = []
            device_actions_in = []
            for stp in make_step_of_type.get_device_steps():
                action = QAction(stp)
                action_a = QAction(stp)
                action_in = QAction(stp)
                action.triggered.connect(lambda state, x=stp, y=row+1, z=parent: self.add_loop_step(x, y, z))
                action_a.triggered.connect(lambda state, x=stp, y=row, z=parent: self.add_loop_step(x, y, z))
                action_in.triggered.connect(lambda state, x=stp, y=-1, z=item.data(): self.add_loop_step(x,y,z))
                device_actions.append(action)
                device_actions_a.append(action_a)
                device_actions_in.append(action_in)
            insert_above_menu = QMenu('Insert Above')
            insert_above_menu.addActions(above_actions)
            insert_below_menu = QMenu('Insert Below')
            insert_below_menu.addActions(below_actions)
            if device_actions:
                insert_above_menu.addSeparator()
                insert_above_menu.addActions(device_actions_a)
                insert_below_menu.addSeparator()
                insert_below_menu.addActions(device_actions)
            if self.current_protocol.loop_step_dict[item.data()].has_children:
                add_in_menu = QMenu('Add Into')
                add_in_menu.addActions(into_actions)
                menu.addMenu(add_in_menu)
                if device_actions:
                    add_in_menu.addSeparator()
                    add_in_menu.addActions(device_actions_in)
            menu.addMenu(insert_above_menu)
            menu.addMenu(insert_below_menu)
            menu.addSeparator()
            cut_action = QAction('Cut')
            cut_action.triggered.connect(lambda state, x=item.data(): self.cut_loop_step(x))
            copy_action = QAction('Copy')
            copy_action.triggered.connect(lambda state, x=item.data(): self.copy_loop_step(x))
            paste_menu = QMenu('Paste')
            if self.copied_loop_step is not None:
                paste_above = QAction('Paste Above')
                paste_above.triggered.connect(lambda state, x=True, y=row, z=parent: self.add_loop_step(copied_step=x, position=y, parent=z))
                paste_below = QAction('Paste Below')
                paste_below.triggered.connect(lambda state, x=True, y=row+1, z=parent: self.add_loop_step(copied_step=x, position=y, parent=z))
                if self.current_protocol.loop_step_dict[item.data()].has_children:
                    paste_into = QAction('Paste Into')
                    paste_into.triggered.connect(lambda state, x=True, y=-1, z=item.data(): self.add_loop_step(copied_step=x,position=y,parent=z))
                    paste_menu.addAction(paste_into)
                paste_menu.addActions([paste_above, paste_below])
            else:
                paste_menu.setEnabled(False)
            menu.addAction(cut_action)
            menu.addAction(copy_action)
            menu.addMenu(paste_menu)
            menu.addSeparator()
            if self.current_protocol.loop_step_dict[item.data()].step_type not in make_step_of_type.non_addables:
                del_action = QAction('Delete Step')
                del_action.triggered.connect(lambda x: self.remove_loop_step(True))
                menu.addAction(del_action)
        else:
            add_actions = []
            # for stp in sorted(drag_drop_tree_view.step_types, key=lambda x: x.lower()):
            for stp in sorted(make_step_of_type.step_type_config, key=lambda x: x.lower()):
                action = QAction(stp)
                action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
                add_actions.append(action)
            device_actions = []
            for stp in make_step_of_type.get_device_steps():
                action = QAction(stp)
                action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
                device_actions.append(action)
            add_menu = QMenu('Add Step')
            add_menu.addActions(add_actions)
            if device_actions:
                add_menu.addSeparator()
                add_menu.addActions(device_actions)
            paste_action = QAction('Paste')
            if self.copied_loop_step is not None:
                paste_action.triggered.connect(lambda state, x=True, y=-1, z=None: self.add_loop_step(copied_step=x, position=y, parent=z))
            else:
                paste_action.setEnabled(False)
            menu.addMenu(add_menu)
            menu.addAction(paste_action)
        menu.exec_(self.treeView_protocol_sequence.viewport().mapToGlobal(pos))

    def paste_shortcut(self):
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if inds and (self.copied_loop_step is not None):
            ind = inds[0]
            item = self.item_model_sequence.itemFromIndex(ind)
            if self.current_protocol.loop_step_dict[item.data()].has_children:
                pos = -1
                parent = item.data()
            else:
                pos = ind.row() + 1
                parent = item.parent()
            self.add_loop_step(copied_step=True, position=pos, parent=parent)



    def cut_shortcut(self):
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if not inds:
            return
        item = self.item_model_sequence.itemFromIndex(inds[0])
        self.cut_loop_step(item.data())

    def copy_shortcut(self):
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if not inds:
            return
        item = self.item_model_sequence.itemFromIndex(inds[0])
        self.copy_loop_step(item.data())


    def cut_loop_step(self, step_name):
        """Copies the given step, then removes it."""
        self.copy_loop_step(step_name)
        self.remove_loop_step(ask=False)

    def copy_loop_step(self, step_name):
        """Makes a deepcopy of the given step and stores it in
        copied_loop_step."""
        self.copied_loop_step = deepcopy(self.current_protocol.loop_step_dict[step_name])


    def move_loop_step(self, up_down=0, in_out=0):
        """Moves a loop_step up or down in the sequence. It can also be
        moved in or out (into the loop_step above, it if accepts children).

        Parameters
        ----------
        up_down : int
            moves up if negative (lower row-number), down if positive
            (default is 0)
        in_out : int
            moves in if positive, out if negative, (default 0)
        """

        move_command = change_sequence.CommandMoveStep(self.treeView_protocol_sequence, self.item_model_sequence, up_down, in_out, self.current_protocol.loop_step_dict, self.update_loop_step_order)
        self.undo_stack.push(move_command)
        self.actionUndo.setEnabled(self.undo_stack.canUndo())
        self.actionRedo.setEnabled(self.undo_stack.canRedo())


    def add_loop_step(self, step_type='', position=-1, parent=None,
                      copied_step=False):
        """Add a loop_step of given step_type. Updates the current
        sequence into the protocol, then initializes the new step.

        Parameters
        ----------
        step_type : str
            gives the type of step to be added
        position : int, optional
            where to add the step, (default -1, append to the end)
        parent : Loop_Step, optional
            parent, where to add the new step, (default None, the step
            is added to the outermost layer of the protocol)
        copied_step : bool, optional
            if False, a new step of type step_type will be created,
            otherwise copied_loop_step will be inserted
        """

        self.update_loop_step_order()
        if copied_step:
            step = self.copied_loop_step
        else:
            # step = drag_drop_tree_view.get_loop_step_from_type(step_type)
            step = make_step_of_type.make_step(step_type)
        self.current_protocol.add_loop_step_rec(step, model=self.item_model_sequence, position=position, parent_step_name=parent)
        self.build_protocol_sequence()
        if copied_step:
            self.copy_loop_step(self.copied_loop_step.full_name)
        new_ind = treeView_functions.getItemIndex(self.item_model_sequence, step.full_name)
        self.treeView_protocol_sequence.selectionModel().select(new_ind, QItemSelectionModel.Select)

    def remove_loop_step(self, ask=True):
        """After updating the loop_step order in the protocol, the
        selected loop step is deleted (if the messagebox is accepted)."""
        self.update_loop_step_order()
        ind = self.treeView_protocol_sequence.selectedIndexes()[0]
        name = self.item_model_sequence.itemFromIndex(ind).data()
        if name is not None:
            remove_dialog = None
            if self.current_protocol.loop_step_dict[name].step_type in make_step_of_type.non_addables:
                return
            if ask:
                remove_dialog = QMessageBox.question(self, 'Delete Step?', f'Are you sure you want to delete the step {name}?', QMessageBox.Yes | QMessageBox.No)
            if not ask or remove_dialog == QMessageBox.Yes:
                self.current_protocol.remove_loop_step(name)
                self.build_protocol_sequence()

    def update_loop_step_order(self):
        """Goes through all the loop_steps in the sequence, then
        rearranges them in the protocol."""
        if self.current_protocol is not None:
            loop_steps = []
            for i in range(self.item_model_sequence.rowCount()):
                item = self.item_model_sequence.item(i, 0)
                sub_steps = treeView_functions.get_substeps(item)
                loop_steps.append((item.data(), sub_steps))
            self.current_protocol.rearrange_loop_steps(loop_steps)




if __name__ == '__main__':
    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    ui.showMaximized()
    # RE = RunEngine()
    # ui.run_engine = RE
    app.exec_()
