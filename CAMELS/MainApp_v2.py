import sys
import os
import socket
import json
import pandas as pd

from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QFileDialog
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon

from CAMELS.gui.mainWindow_v2 import Ui_MainWindow
from CAMELS.utility import exception_hook

from pkg_resources import resource_filename

from CAMELS.bluesky_handling import make_catalog
from CAMELS.frontpanels.manage_instruments import ManageInstruments
from CAMELS.frontpanels.settings_window import Settings_Window
from CAMELS.frontpanels.protocol_config import Protocol_Config
from CAMELS.frontpanels.helper_panels.button_move_scroll_area import Drop_Scroll_Area
from CAMELS.utility import load_save_functions, add_remove_table, variables_handling, number_formatting, theme_changing, options_run_button

from collections import OrderedDict


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window for the program. Connects to all the other classes."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.button_area_meas = Drop_Scroll_Area(self, 100, 100)
        self.button_area_manual = Drop_Scroll_Area(self, 100, 100)
        self.meas_widget.layout().addWidget(self.button_area_meas, 2, 0, 1, 3)
        self.manual_widget.layout().addWidget(self.button_area_manual, 2, 0, 1, 3)
        self.button_area_manual.setHidden(True)

        self.setWindowTitle('CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems')
        self.setWindowIcon(QIcon(resource_filename('CAMELS','graphics/CAMELS_Icon_v2.ico')))

        arrow = self.style().standardIcon(QStyle.SP_ArrowUp)
        self.label_arrow.setPixmap(arrow.pixmap(130,130))

        self.setStyleSheet("QSplitter::handle{background: gray;}")

        # saving / loading
        self.__save_dict__ = {}
        self._current_preset = [f'{socket.gethostname()}']
        self.active_instruments = {}
        self.protocols_dict = OrderedDict()
        variables_handling.protocols = self.protocols_dict
        self.preset_save_dict = {'_current_preset': self._current_preset,
                                 'active_instruments': self.active_instruments,
                                 'protocols_dict': self.protocols_dict}
        self.preferences = {}
        self.load_preferences()
        self.load_state()

        self.with_or_without_instruments()
        self.populate_meas_buttons()
        self.adjustSize()

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


        # actions
        self.actionSettings.triggered.connect(self.change_preferences)
        self.actionSave_Preset_As.triggered.connect(self.save_preset_as)
        self.actionSave_Preset.triggered.connect(self.save_state)
        self.actionNew_Preset.triggered.connect(self.new_preset)
        self.actionLoad_Backup_Preset.triggered.connect(self.load_backup_preset)
        self.actionVISA_device_builder.triggered.connect(self.launch_device_builder)

        # buttons
        self.pushButton_manage_instr.clicked.connect(self.manage_instruments)
        self.pushButton_add_meas.clicked.connect(self.add_measurement_protocol)

    def with_or_without_instruments(self):
        available = False
        if self.active_instruments:
            available = True
        self.main_splitter.setHidden(not available)
        self.label_arrow.setHidden(available)
        self.label_no_instruments.setHidden(available)

    def manage_instruments(self):
        self.setCursor(Qt.WaitCursor)
        dialog = ManageInstruments(active_instruments=self.active_instruments,
                                   parent=self)
        self.setCursor(Qt.ArrowCursor)
        if dialog.exec():
            self.active_instruments.clear()
            self.active_instruments.update(dialog.active_instruments)
        self.with_or_without_instruments()

    # --------------------------------------------------
    # Overwriting parent-methods
    # --------------------------------------------------
    def close(self) -> bool:
        """Calling the save_state method when closing the window."""
        if self.preferences['autosave']:
            self.save_state()
        return super().close()

    def closeEvent(self, a0):
        """Calling the save_state method when closing the window."""
        if self.preferences['autosave']:
            self.save_state()
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

    def save_state(self, fromload=False):
        """Saves the current states of both presets."""
        self.make_save_dict()
        load_save_functions.autosave_preset(self._current_preset[0], self.__save_dict__)
        if fromload:
            return
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
                                               'active_instruments': {},
                                               'protocols_dict': OrderedDict()})
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
        self._current_preset[0] = preset_name
        self.make_save_dict()
        load_save_functions.save_preset(file, self.__save_dict__)


    def load_backup_preset(self):
        """Opens a QFileDialog in the Backup-folder of the presets.
        If a backup is selected, the current preset is put into backup."""
        file = QFileDialog.getOpenFileName(self, 'Open Preset',
                                           f'{load_save_functions.preset_path}',
                                           '*.preset')[0]
        if not len(file):
            return
        preset_name = file.split('_')[-1][:-7]
        # preset = f'Backup/{file.split("/")[-2]}/{file.split("/")[-1][:-7]}'
        self.save_state()
        self._current_preset[0] = preset_name
        self.load_preset(file)


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
        try:
            with open(f'{load_save_functions.preset_path}{preset}.preset', 'r') as f:
                preset_dict = json.load(f)
        except:
            with open(preset, 'r') as f:
                preset_dict = json.load(f)
        load_save_functions.load_save_dict(preset_dict, self.preset_save_dict)
        self.update_channels()
        variables_handling.preset = self._current_preset[0]

    def make_save_dict(self):
        for key in self.preset_save_dict:
            add_string = load_save_functions.get_save_str(self.preset_save_dict[key])
            if add_string is not None:
                self.__save_dict__.update({key: load_save_functions.get_save_str(self.preset_save_dict[key])})

    def update_channels(self):
        """Called when the active devices change.
        The channels in variables_handling are updated with the ones
        provided by the active devices."""
        variables_handling.channels.clear()
        for key, dev in self.active_instruments.items():
            for channel in dev.get_channels():
                variables_handling.channels.update({channel: dev.channels[channel]})

    # --------------------------------------------------
    # protocols
    # --------------------------------------------------
    def add_measurement_protocol(self):
        dialog = Protocol_Config()
        dialog.show()
        dialog.accepted.connect(self.add_prot_to_data)

    def add_prot_to_data(self, protocol):
        self.protocols_dict[protocol.name] = protocol
        self.populate_meas_buttons()


    def populate_meas_buttons(self):
        if not self.protocols_dict:
            self.button_area_meas.setHidden(True)
        else:
            self.button_area_meas.setHidden(False)
        for prot in self.protocols_dict:
            button = options_run_button.Options_Run_Button(prot)
            self.button_area_meas.add_button(button, prot)

    # --------------------------------------------------
    # tools
    # --------------------------------------------------
    def launch_device_builder(self):
        from CAMELS.tools import VISA_device_builder
        device_builder = VISA_device_builder.VISA_Device_Builder(self)
        device_builder.show()



if __name__ == '__main__':
    sys.excepthook = exception_hook.exception_hook
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    # RE = RunEngine()
    # ui.run_engine = RE
    app.exec_()