"""The main window of the program. It contains all the other classes and is the main interface for the user."""

import sys
import os
import platform, subprocess
import re
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(__file__))
import json
import pathlib

from PySide6.QtWidgets import QMainWindow, QStyle, QFileDialog, QLabel
from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QIcon, QPixmap, QShortcut

from nomad_camels.gui.mainWindow_v2 import Ui_MainWindow
from nomad_camels.gui.tags_ui import TagWidget, FlowLayout
from importlib import resources
from nomad_camels import graphics
from nomad_camels.utility.databroker_export import clean_filename

from nomad_camels.frontpanels.helper_panels.button_move_scroll_area import (
    RenameTabWidget,
)
from nomad_camels.utility import (
    load_save_functions,
    variables_handling,
    number_formatting,
    theme_changing,
    update_camels,
    logging_settings,
    qthreads,
    plot_placement,
)
from nomad_camels.ui_widgets import (
    options_run_button,
    warn_popup,
    variable_tool_tip_box,
)
from nomad_camels.extensions import extension_contexts
from nomad_camels.bluesky_handling.evaluation_helper import Evaluator
from nomad_camels.bluesky_handling import helper_functions

from collections import OrderedDict
import importlib
import logging


camels_github = "https://github.com/FAU-LAP/NOMAD-CAMELS"
camels_github_pages = "https://fau-lap.github.io/NOMAD-CAMELS/"


class MainWindow(Ui_MainWindow, QMainWindow):
    """
    Main window for the NOMAD CAMELS application.

    This class connects to all the other components and handles user interactions,
    protocol execution, device management, and various settings/preferences.
    """

    protocol_stepper_signal = Signal(float)
    run_done_file_signal = Signal(str)
    fake_signal = Signal(int)
    protocol_finished_signal = Signal()
    start_timer_signal = Signal()

    def __init__(self, parent=None, start_proxy_bool=True):
        """
        Initialize the MainWindow.

        Sets up the UI, redirects stdout and stderr to the console widget,
        initializes device and protocol management, connects signals to slots,
        and loads user preferences and state.

        Args:
            parent (Optional[QWidget]): Parent widget, defaults to None.
            start_proxy_bool (bool): Flag to start proxy, defaults to True.
        """
        super().__init__(parent=parent)
        self.setupUi(self)
        sys.stdout = self.textEdit_console_output.text_writer
        sys.stderr = self.textEdit_console_output.error_writer

        # Initialize extension contexts
        self.extension_user = {}
        self.extension_sample = {}
        self.eln_context = extension_contexts.ELN_Context(self)
        extension_contexts.active_eln_context = self.eln_context
        self.extension_contexts = {"ELN_Context": self.eln_context}
        self.extensions = []

        # Set alignment for various widgets
        self.sample_widget.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.user_widget.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.session_upload_widget.layout().setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Initialize protocol and manual tabs dictionaries with default tabs
        self.protocol_tabs_dict = OrderedDict({"Protocols": []})
        self.manual_tabs_dict = OrderedDict({"Manuals": []})
        self.button_area_meas = RenameTabWidget(self, self.protocol_tabs_dict)
        self.button_area_manual = RenameTabWidget(self, self.manual_tabs_dict)
        self.meas_widget.layout().addWidget(self.button_area_meas, 2, 0, 1, 4)
        self.manual_widget.layout().addWidget(self.button_area_manual, 2, 0, 1, 3)
        self.lineEdit_session.set_check_function(
            check_function=variable_tool_tip_box.check_no_special_characters,
            tooltip="Session name must not contain special characters.\n"
            "Please use only letters, numbers and underscores.",
        )

        # Set window title and icon
        self.setWindowTitle(
            "NOMAD CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems"
        )
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "CAMELS_Icon.png")))

        # Set the logo image
        image = QPixmap()
        image.load(str(resources.files(graphics) / "CAMELS_horizontal.png"))
        self.label_logo.setPixmap(image)

        # Set the arrow image using the style standard icon
        arrow = self.style().standardIcon(QStyle.SP_ArrowUp)
        self.label_arrow.setPixmap(arrow.pixmap(130, 130))

        # Set icons for pause, resume, and stop buttons
        icon = self.style().standardIcon(QStyle.SP_MediaPause)
        self.pushButton_pause.setIcon(icon)
        icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        self.pushButton_resume.setIcon(icon)
        icon = self.style().standardIcon(QStyle.SP_MediaStop)
        self.pushButton_stop.setIcon(icon)

        # Apply stylesheet to splitter handles
        # self.setStyleSheet("QSplitter::handle{background: gray;}")
        # self.setStyleSheet("QSplitter::handle{background: gray;}")
        self.protocol_stepper_signal.connect(self._update_remaining_time_progress_bar)
        self._protocol_start_time = time.time()

        # Initialize fastAPI server variables
        self.fastapi_thread = None
        self.current_api_port = None

        # Initialize saving and state variables
        self.__save_dict__ = {}
        if os.name == "nt":
            name = os.environ["COMPUTERNAME"]
        else:
            name = os.uname()[1]

        self._current_preset = [name]
        self.active_instruments = {}
        variables_handling.devices = self.active_instruments
        self.protocols_dict = OrderedDict()
        variables_handling.protocols = self.protocols_dict
        self.manual_controls = OrderedDict()
        variables_handling.manual_controls = self.manual_controls
        self.preset_save_dict = {
            "_current_preset": self._current_preset,
            "active_instruments": self.active_instruments,
            "protocols_dict": self.protocols_dict,
            "manual_controls": self.manual_controls,
            "protocol_tabs_dict": self.protocol_tabs_dict,
            "manual_tabs_dict": self.manual_tabs_dict,
            "watchdogs": variables_handling.watchdogs,
        }
        self.preferences = {}
        self.load_preferences()
        if self.preferences["auto_check_updates"]:
            update_camels.auto_update(self)
        self.load_state()

        self.open_windows = []
        self.current_protocol_device_list = []

        self.active_controls = {}
        self.open_plots = []

        # User and sample data
        self.sampledata = {}
        self.userdata = {}
        self.active_user = "default_user"
        self.active_sample = "default_sample"

        self.nomad_user = None
        self.nomad_sample = None
        self.last_save_file = None

        # Setup upload type combobox
        self.comboBox_upload_type.addItems(
            ["auto upload", "ask after run", "don't upload"]
        )
        self.comboBox_upload_type.setCurrentText("don't upload")
        self.comboBox_upload_type.currentTextChanged.connect(self.show_nomad_upload)

        self.checkBox_use_nomad_sample.clicked.connect(self.show_nomad_sample)

        # Connect buttons for editing user and sample info and load their data
        self.pushButton_editUserInfo.clicked.connect(self.edit_user_info)
        self.load_user_data()
        self.pushButton_editSampleInfo.clicked.connect(self.edit_sample_info)
        self.load_sample_data()
        variables_handling.CAMELS_path = os.path.dirname(__file__)

        # Connect user combobox signals and set user type
        self.comboBox_user.currentTextChanged.connect(self.change_user)
        self.comboBox_user_type.addItems(["local user", "NOMAD user"])
        self.comboBox_user_type.currentTextChanged.connect(self.change_user_type)
        self.change_user_type()

        self.pushButton_login_nomad.clicked.connect(self.login_logout_nomad)
        self.pushButton_nomad_sample.clicked.connect(self.select_nomad_sample)

        # Connect various action menu items to functions
        self.actionSettings.triggered.connect(self.change_preferences)
        self.actionSave_Preset_As.triggered.connect(self.save_preset_as)
        self.actionSave_Preset.triggered.connect(self.save_state)
        self.actionNew_Preset.triggered.connect(self.new_preset)
        self.actionLoad_Backup_Preset.triggered.connect(self.load_backup_preset)
        self.action_driver_builder.triggered.connect(self.launch_device_builder)
        self.actionEPICS_driver_builder.triggered.connect(self.launch_epics_builder)
        self.actionExport_from_databroker.triggered.connect(self.launch_data_exporter)
        self.actionReport_Bug.triggered.connect(
            lambda x: variables_handling.open_link(f"{camels_github}/issues")
        )
        self.actionDocumentation.triggered.connect(
            lambda x: variables_handling.open_link(camels_github_pages)
        )
        self.actionUpdate_CAMELS.triggered.connect(
            lambda x: update_camels.question_message_box(self)
        )
        self.actionExport_CAMELS_hdf5_to_csv_json.triggered.connect(
            self.launch_hdf5_exporter
        )
        self.actionQuit.triggered.connect(self.close)

        # Connect push buttons for manual and measurement controls
        self.pushButton_add_manual.clicked.connect(self.add_manual_control)

        self.pushButton_manage_instr.clicked.connect(self.manage_instruments)
        self.pushButton_add_meas.clicked.connect(self.add_measurement_protocol)
        self.pushButton_import_protocol.clicked.connect(
            self.import_measurement_protocol
        )

        self.pushButton_stop.clicked.connect(self.stop_protocol)
        self.pushButton_pause.clicked.connect(self.pause_protocol)
        self.pushButton_resume.clicked.connect(self.resume_protocol)

        self.pushButton_clear_log.clicked.connect(self.textEdit_console_output.clear)
        self.pushButton_close_plots.clicked.connect(self.close_plots)
        self.pushButton_show_log.clicked.connect(self.show_hide_log)
        self.show_hide_log()

        QShortcut("Ctrl+s", self).activated.connect(self.save_state)

        # self.show()
        self.adjustSize()

        self.live_variable_box = None

        self.saving_plot_list = []
        self.run_engine = None
        self.databroker_catalog = None
        self.still_running = False
        self.re_subs = []
        self.protocol_module = None
        self.protocol_savepath = ""
        self.running_protocol = None
        self.run_queue_widget.protocols_dict = self.protocols_dict
        self.run_queue_widget.protocol_signal.connect(self.next_queued_protocol)
        self.run_queue_widget.variable_table = self.queue_variable_table
        self.queue_variable_table.setHidden(True)
        self.run_queue_widget.setHidden(True)
        self.label_queue.setHidden(True)
        self.devices_from_queue = []

        # load extensions
        self.load_extensions()
        self.actionManage_Extensions.triggered.connect(self.manage_extensions)

        self.actionWatchdogs.triggered.connect(self.open_watchdog_definition)
        self.eva = Evaluator()
        self.update_watchdogs()

        # Start additional import thread
        self.importer_thread = qthreads.Additional_Imports_Thread(self)
        self.importer_thread.start(priority=QThread.LowPriority)

        # Setup measurement tags UI and flow layout for tags
        self.container = self.scrollAreaWidgetContents
        self.flow_layout = FlowLayout(self.container)
        self.container.setLayout(self.flow_layout)
        self.lineEdit_tags.returnPressed.connect(self.add_tag)

        self._was_aborted = False
        self._timer = QTimer()
        self._timer.timeout.connect(self._check_RE_done)
        self.start_timer_signal.connect(self._start_timer)
        self.protocol_finished_signal.connect(self.play_finished_sound)

        version = update_camels.get_version()
        if self.preferences["last_shown_notes"] != version:
            update_camels.show_release_notes()
            self.preferences["last_shown_notes"] = version
            load_save_functions.save_preferences(self.preferences)
        if start_proxy_bool:
            # Setup a single ZMQ proxy, dispatcher and publisher for all plots
            from bluesky.callbacks.zmq import RemoteDispatcher, Publisher
            from nomad_camels.main_classes.plot_proxy import StoppableProxy as Proxy
            from threading import Thread
            from zmq.error import ZMQError
            import asyncio

            if sys.platform == "win32":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

            def setup_threads():
                try:
                    proxy = Proxy(5577, 5578)
                    proxy_created = True
                except ZMQError as e:
                    # If the proxy is already running, a ZMQError will be raised.
                    proxy = None  # We will use the already running proxy.
                    proxy_created = False

                def start_proxy():
                    if proxy_created and proxy is not None:
                        proxy.start()

                dispatcher = RemoteDispatcher("localhost:5578")

                def start_dispatcher():
                    try:
                        dispatcher.start()
                    except asyncio.exceptions.CancelledError:
                        # This error is raised when the dispatcher is stopped. It can therefore be ignored
                        pass

                return proxy, dispatcher, start_proxy, start_dispatcher

            self.publisher = Publisher("localhost:5577")
            self.proxy, self.dispatcher, start_proxy, start_dispatcher = setup_threads()
            proxy_thread = Thread(target=start_proxy, daemon=True)
            dispatcher_thread = Thread(target=start_dispatcher, daemon=True)
            proxy_thread.start()
            dispatcher_thread.start()

    def add_tag(self):
        """
        Add a tag from the line edit to the flow layout.

        Reads the text from the tag line edit, creates a TagWidget if the text is not empty,
        adds it to the layout, and clears the line edit.
        """
        text = self.lineEdit_tags.text().strip()
        if text:
            tag = TagWidget(text)
            self.flow_layout.addWidget(tag)
            self.lineEdit_tags.clear()

    def start_API_server(self, api_port):
        """
        Start the FastAPI server on the specified port.

        This method initializes and starts a FastAPI thread for remote API control,
        and connects its signals to various slot functions in the main window. The API emits signals to the main app to perform most of the tasks like queuing and starting protocols. You can enable the API and set the port in the Settings Window of CAMELS.

        Args:
            api_port (int): The port number on which to start the API server.
        """
        if hasattr(self, "fastapi_thread") and self.fastapi_thread is not None:
            pass
        else:
            try:
                from nomad_camels.api.api import FastapiThread
            except ImportError:
                warn_popup.WarnPopup(
                    self,
                    "The FastAPI server could not be started. The required packages are not installed.",
                    "FastAPI server error",
                    info_icon=True,
                )
                return

            self.current_api_port = api_port
            # Initialize the FastAPI server thread
            self.fastapi_thread = FastapiThread(self, api_port)
            # Connect signals for error, protocol start, user/sample/session setting, and protocol queueing
            self.fastapi_thread.port_error_signal.connect(self.clear_fastapi_thread)
            self.fastapi_thread.start_protocol_signal.connect(self.run_protocol)
            self.fastapi_thread.set_user_signal.connect(self.set_user)
            self.fastapi_thread.set_sample_signal.connect(self.set_sample)
            self.fastapi_thread.set_session_signal.connect(self.set_session)
            self.fastapi_thread.queue_protocol_signal.connect(self.queue_protocol)
            self.fastapi_thread.remove_queue_protocol_signal.connect(
                self.remove_queue_protocol
            )
            self.fastapi_thread.set_checkbox_signal.connect(self.set_checkbox)
            self.fastapi_thread.queue_protocol_with_variables_signal.connect(
                self.queue_protocol_with_variables_signal
            )
            self.fastapi_thread.change_variables_queued_protocol_signal.connect(
                self.change_variables_queued_protocol
            )
            # Start the API server thread
            self.fastapi_thread.start()

    def set_user(self, user_name):
        """
        Set the active user to the specified user name (called by the API).

        Args:
            user_name (str): The name of the user to set.

        Raises:
            ValueError: If the given user does not exist in the user data.
        """
        if user_name not in self.userdata:
            raise ValueError(
                f"User {user_name} can not be set as it does not exist. Please create this user first."
            )
        self.active_user = user_name
        self.comboBox_user.setCurrentText(user_name)

    def set_sample(self, sample_name):
        """
        Set the active sample to the specified sample name (called by the API).

        Args:
            sample_name (str): The name of the sample to set.

        Raises:
            ValueError: If the given sample does not exist in the sample data.
        """
        # Check if the sample exists
        if sample_name not in self.sampledata:
            import pandas as pd

            # make dataframe with keys of sampledata as index and the values as columns
            df = pd.DataFrame.from_dict(self.sampledata, orient="index")
            if sample_name in df["name"]:
                sample_name = df[df["name"] == sample_name].index[0]
            elif sample_name in df["sample_id"]:
                sample_name = df[df["sample_id"] == sample_name].index[0]
            else:
                raise ValueError(
                    f"Sample {sample_name} can not be set as it does not exist or is not accessible to user {self.get_user_name_data()[0]}. Please create this sample first."
                )

        # Set the active sample to the sample name
        self.active_sample = sample_name
        self.comboBox_sample.setCurrentText(sample_name)

    def set_session(self, session_name):
        """
        Set the active session name (called by the API).

        Args:
            session_name (str): The session name to set.
        """
        self.lineEdit_session.setText(session_name)

    def stop_API_server(self):
        """
        Stop the FastAPI server if it is running.
        """
        if hasattr(self, "fastapi_thread") and self.fastapi_thread is not None:
            self.fastapi_thread.stop_server()
            self.fastapi_thread.deleteLater()
            self.fastapi_thread = None
            self.current_api_port = None

    def remove_queue_protocol(self, protocol_name):
        """
        Remove a protocol from the run queue (called by the API).

        Args:
            protocol_name (str): The name of the protocol to remove.
        """
        self.run_queue_widget.remove_item_by_name(protocol_name)

    def set_checkbox(self, protocol_name):
        """
        Check the checkbox of a protocol in the run queue (called by the API).

        Args:
            protocol_name (str): The name of the protocol whose checkbox is to be set.
        """
        self.run_queue_widget.check_checkbox(protocol_name)

    def queue_protocol_with_variables_signal(
        self, protocol_name, variables, index, api_uuid
    ):
        """
        Update variables for a queued protocol (called by the API).

        Args:
            protocol_name (str): The name of the protocol.
            variables (dict): The variables to update.
            index (int): The index in the queue.
            api_uuid (str): The API unique identifier.
        """
        self.run_queue_widget.setHidden(False)
        self.label_queue.setHidden(False)
        if protocol_name in self.protocols_dict:
            self.run_queue_widget.add_item(protocol_name, api_uuid)
        protocol_name = list(self.run_queue_widget.protocol_name_variables.keys())[
            index
        ]
        self.run_queue_widget.update_variables_queue(
            protocol_name, variables, index=index
        )

    def change_variables_queued_protocol(self, protocol_name, variables, index):
        """
        Update variables of an already queued protocol (called by the API).

        Args:
            protocol_name (str): The protocol name.
            variables (dict): The updated variables.
            index (int): The index of the protocol in the queue.
        """
        self.run_queue_widget.setHidden(False)
        self.label_queue.setHidden(False)
        self.run_queue_widget.update_variables_queue(
            protocol_name, variables, index=index
        )

    def open_watchdog_definition(self):
        """
        Open the watchdog definition dialog.

        Disconnects active watchdog signals, shows the dialog, and then updates watchdogs.
        """
        # IMPORT Watchdog_Definer only if it is needed
        from nomad_camels.bluesky_handling.watchdogs import Watchdog_Definer

        dialog = Watchdog_Definer(self)
        for watchdog in variables_handling.watchdogs.values():
            if not watchdog.active:
                continue
            watchdog.condition_met.disconnect(self.watchdog_triggered)
        dialog.exec()
        self.update_watchdogs()

    def update_watchdogs(self):
        """
        Update watchdogs by connecting their condition_met signals to the watchdog_triggered slot.
        """
        for watchdog in variables_handling.watchdogs.values():
            if not watchdog.active:
                continue
            watchdog.eva = self.eva
            watchdog.condition_met.connect(self.watchdog_triggered)

    def show_hide_log(self):
        """
        Toggle the visibility of the console log and clear log button.

        If the log is hidden, it becomes visible, and vice versa. Also updates the text of the show/hide button.
        """
        is_hidden = self.textEdit_console_output.isHidden()
        self.textEdit_console_output.setHidden(not is_hidden)
        self.pushButton_clear_log.setHidden(not is_hidden)
        self.pushButton_show_log.setText("Hide Log" if is_hidden else "Show Log")

    def check_password_protection(self):
        """
        Check for password protection and prompt for a password if enabled.

        Returns:
            bool: True if there is no password protection or if the entered password is correct, False otherwise.
        """
        if (
            "password_protection" in self.preferences
            and self.preferences["password_protection"]
        ):
            from nomad_camels.utility.password_widgets import Password_Dialog

            dialog = Password_Dialog(
                self, compare_hash=self.preferences["password_hash"]
            )
            if not dialog.exec():
                return False
        return True

    def manage_extensions(self):
        """
        Open the extension manager dialog.

        Requires password protection if enabled. On successful changes, prompts for a restart.
        """
        if not self.check_password_protection():
            return
        self.setCursor(Qt.WaitCursor)
        from nomad_camels.extensions.extension_management import Extension_Manager
        from nomad_camels.utility.update_camels import restart_camels

        dialog = Extension_Manager(self.preferences, self)
        if dialog.exec():
            # self.load_extensions()
            load_save_functions.save_preferences(self.preferences)
            warn_popup.WarnPopup(
                self,
                "Extensions will be loaded after restart.",
                "Restart required",
                info_icon=True,
            )
            restart_camels(self, True)
        self.setCursor(Qt.ArrowCursor)

    def load_extensions(self):
        """
        Load extensions as specified in the preferences.

        If no extensions are specified, defaults are added. Paths are added to sys.path
        and each extension is imported and instantiated with the required contexts.
        """
        if not "extensions" in self.preferences:
            from nomad_camels.utility.load_save_functions import standard_pref

            self.preferences["extensions"] = standard_pref["extensions"]
        if not "extension_path" in self.preferences:
            from nomad_camels.utility.load_save_functions import standard_pref

            self.preferences["extension_path"] = standard_pref["extension_path"]
        sys.path.append(self.preferences["extension_path"])
        for f in pathlib.Path(self.preferences["extension_path"]).rglob("*"):
            # check if f is a directory that starts with 'nomad_camels_extension_'
            if f.is_dir() and f.name.startswith("nomad_camels_extension_"):
                sys.path.append(str(f.parent))
        for extension in self.preferences["extensions"]:
            try:
                extension_module = importlib.import_module(extension)
            except (ModuleNotFoundError, AttributeError) as e:
                logging.warning(f"Could not load extension {extension}.\n{e}")
                continue
            config = getattr(extension_module, "EXTENSION_CONFIG")
            name = config["name"]
            # check the required extensions contexts and hand them to the extension
            contexts = {}
            for context in config["required_contexts"]:
                contexts[context] = self.extension_contexts[context]
            self.extensions.append(getattr(extension_module, name)(**contexts))

    def bluesky_setup(self):
        """
        Set up the Bluesky RunEngine and databroker catalog.

        This method is called when the first protocol is run and configures
        the run engine with callbacks, loads the databroker catalog, and subscribes to events.
        """
        # IMPORT bluesky only if it is needed
        from bluesky_handling.run_engine_overwrite import RunEngineOverwrite
        from bluesky.callbacks.best_effort import BestEffortCallback
        import databroker

        self.run_engine = RunEngineOverwrite()
        self.run_engine.subscribe(self.eva)
        bec = BestEffortCallback()
        self.run_engine.subscribe(bec)
        self.importer_thread.wait()
        self.databroker_catalog = self.importer_thread.catalog
        self.importer_thread.deleteLater()
        self.change_catalog_name()
        self.run_engine.subscribe(self.databroker_catalog.v1.insert)
        self.run_engine.subscribe(self.protocol_finished, "stop")
        self.still_running = False
        self.re_subs = []
        self.protocol_module = None
        self.protocol_savepath = ""
        self.running_protocol = None

    def with_or_without_instruments(self):
        """
        Check if active instruments are available and update the UI accordingly.

        Hides protocol and manual controls if no instruments are active.
        """
        available = False
        if self.active_instruments:
            available = True
        self.main_splitter.setHidden(not available)
        self.pushButton_resume.setHidden(not available)
        self.pushButton_pause.setHidden(not available)
        self.pushButton_stop.setHidden(not available)
        self.progressBar_protocols.setHidden(not available)
        # self.textEdit_console_output.setHidden(not available)
        # self.pushButton_clear_log.setHidden(not available)
        self.pushButton_close_plots.setHidden(not available)
        self.label_arrow.setHidden(available)
        self.label_no_instruments.setHidden(available)

    def manage_instruments(self):
        """
        Open the instrument manager dialog.

        Allows users to add or remove instruments. After the dialog, the active instruments are updated.
        """
        self.setCursor(Qt.WaitCursor)
        # IMPORT ManageInstruments only if it is needed
        from nomad_camels.frontpanels.manage_instruments import ManageInstruments

        dialog = ManageInstruments(
            active_instruments=self.active_instruments, parent=self
        )
        self.setCursor(Qt.ArrowCursor)
        if dialog.exec():
            self.active_instruments.clear()
            self.active_instruments.update(dialog.active_instruments)
            self.update_channels()
        self.with_or_without_instruments()

    def add_to_open_windows(self, window):
        """
        Add a window to the list of open windows.

        Connects the window's closing signal to remove it from the list when closed.

        Args:
            window (QWidget): The window to add.
        """
        self.open_windows.append(window)
        window.closing.connect(lambda x=window: self.open_windows.remove(x))

    def add_to_plots(self, plot):
        """
        Add a plot to the list of open plots and to the list of open windows.

        Connects signals so that when the plot is closed or reopened, the lists are updated.

        Args:
            plot (QWidget): The plot to add.
        """
        self.open_plots.append(plot)
        plot.closing.connect(lambda x=plot: self.open_plots.remove(x))
        plot.reopened.connect(lambda x=plot: self.open_plots.append(x))
        plot.reopened.connect(lambda x=plot: self.open_windows.append(x))
        self.add_to_open_windows(plot)

    def close_plots(self):
        """
        Close all currently open plots and reset plot placement variables.
        """
        for plot in list(self.open_plots):
            plot.close()
        plot_placement.reset_variables()

    # --------------------------------------------------
    # Overwriting parent-methods
    # --------------------------------------------------
    def close(self) -> bool:
        """
        Overwrite the close method to save state when closing the window.

        Returns:
            bool: The result of the parent's close() method.
        """
        ret = super().close()
        return ret

    def closeEvent(self, a0):
        """
        Handle the close event by closing all open windows, stopping the API server,
        and saving the state if autosave is enabled.

        Args:
            a0 (QCloseEvent): The close event.
        """
        if hasattr(self, "proxy") and self.proxy is not None:
            self.proxy.stop()
        for window in list(self.open_windows):
            window.close()
        if self.open_windows:
            a0.ignore()
            return
        self.stop_API_server()
        super().closeEvent(a0)
        if self.preferences["autosave"]:
            self.save_state()

    # --------------------------------------------------
    # User / Sample methods
    # --------------------------------------------------
    def login_logout_nomad(self):
        """
        Handle logging in/out of NOMAD when the corresponding button is clicked.

        Depending on the current state, either logs out or initiates the login process.
        """
        # IMPORT nomad_communication only if it is needed
        from nomad_camels.nomad_integration import nomad_communication

        if nomad_communication.token:
            nomad_communication.logout_of_nomad()
            self.pushButton_login_nomad.setText("NOMAD login")
            self.label_nomad_user.setText("not logged in")
            self.pushButton_nomad_sample.setText("select NOMAD sample")
            self.nomad_user = None
            self.nomad_sample = None
        else:
            self.login_nomad()
        self.show_nomad_sample()
        self.show_nomad_upload()

    def login_nomad(self):
        """
        Handle the login process to NOMAD.

        If login is successful, updates the UI to reflect NOMAD-related controls.
        """
        # IMPORT nomad_communication only if it is needed
        from nomad_camels.nomad_integration import nomad_communication

        nomad_communication.ensure_login(self)
        if not nomad_communication.token:
            return
        load_save_functions.save_preferences(self.preferences)
        self.pushButton_login_nomad.setText("NOMAD logout")
        user_data = nomad_communication.get_user_information(self)
        for key in ["created", "is_admin", "is_oasis_admin"]:
            if key in user_data:
                user_data.pop(key)
        user_data["ELN-service"] = "nomad"
        self.label_nomad_user.setText(user_data["name"])
        self.nomad_user = user_data

    def show_nomad_upload(self):
        """
        Show or hide NOMAD upload settings based on whether a NOMAD user is logged in.

        Updates UI elements related to uploading data to NOMAD.
        """
        nomad = self.nomad_user is not None
        self.nomad_upload_widget.setHidden(not nomad)
        auto_upload = self.comboBox_upload_type.currentText() == "auto upload"
        self.comboBox_upload_choice.setHidden(not nomad or not auto_upload)
        if nomad:
            # IMPORT nomad_communication only if it is needed
            from nomad_camels.nomad_integration import nomad_communication

            # The get_user_upload_names function is a lambda function that is called when the combobox is clicked. It fetches the available uploads from NOMAD.
            self.comboBox_upload_choice.getDynamicItems = (
                lambda: nomad_communication.get_user_upload_names(self)
            )

    def change_user_type(self):
        """
        Adjust UI elements based on the selected user type.

        For example, shows NOMAD login button if NOMAD user is selected.
        """
        user_type = self.comboBox_user_type.currentText()
        if user_type not in ["local user", "NOMAD user"]:
            return
        nomad = user_type == "NOMAD user"
        self.user_widget_nomad.setHidden(not nomad)
        self.user_widget_default.setHidden(nomad)
        if not nomad:
            self.nomad_user = None
        else:
            self.login_nomad()
        self.show_nomad_sample()
        self.show_nomad_upload()
        self.change_user()

    def edit_user_info(self):
        """
        Open a dialog to edit user information.

        The dialog displays user data such as name, email, affiliation, ORCID, phone number etc.
        On acceptance, updates the user data.
        """
        # IMPORT pandas and add_remove_table only if it is needed
        import pandas as pd
        from nomad_camels.ui_widgets import add_remove_table

        self.active_user = self.comboBox_user.currentText()
        headers = [
            "name",
            "email",
            "affiliation",
            "address",
            "orcid",
            "telephone_number",
        ]
        tableData = pd.DataFrame.from_dict(self.userdata, "index")

        dialog = add_remove_table.AddRemoveDialoge(
            headerLabels=headers,
            parent=self,
            title="User-Information",
            askdelete=True,
            tableData=tableData,
            check_string_function=variable_tool_tip_box.check_no_special_characters,
            checkstrings=[0],
        )
        if dialog.exec():
            # Changing the returned dict to dataframe and back to ensure proper formatting. Dictionary is formatted as {name: {'Name': name,...}, ...}
            dat = dialog.get_data()
            if re.search(r"[^\w\s]", str(dat["name"][0])):
                raise ValueError(
                    "Name contains special characters.\nPlease use only letters, numbers and whitespace."
                )
            # Remove trailing whitespace from name
            dat["name"][0] = dat["name"][0].strip()
            dat["Name2"] = dat["name"]
            data = pd.DataFrame(dat)
            data.set_index("Name2", inplace=True)
            self.userdata = data.to_dict("index")
            self.comboBox_user.currentTextChanged.disconnect(self.change_user)
            self.comboBox_user.clear()
            self.comboBox_user.addItems(
                sorted(self.userdata.keys(), key=lambda x: x.lower())
            )
            if self.active_user in self.userdata:
                self.comboBox_user.setCurrentText(self.active_user)
            self.comboBox_user.currentTextChanged.connect(self.change_user)
            self.save_user_data()

    def save_user_data(self):
        """
        Save the current user data to a JSON file.

        The active user is saved along with the complete user data dictionary.
        """
        self.active_user = self.comboBox_user.currentText()
        userdic = {"active_user": self.active_user}
        userdic.update(self.userdata)
        load_save_functions.save_dictionary(
            os.path.join(load_save_functions.appdata_path, "userdata.json"), userdic
        )

    def load_user_data(self):
        """
        Load user data from a JSON file.

        Sets the active user and updates the user data dictionary.
        """
        userdat = {}
        userfile = os.path.join(load_save_functions.appdata_path, "userdata.json")
        if os.path.isfile(userfile):
            with open(userfile, "r", encoding="utf-8") as f:
                string_dict = json.load(f)
            load_save_functions.load_save_dict(
                string_dict, userdat, update_missing_key=True
            )
        if "active_user" in userdat:
            self.active_user = userdat["active_user"]
            userdat.pop("active_user")
        self.userdata = userdat
        self.comboBox_user.addItems(userdat.keys())
        if not self.active_user == "default_user":
            self.comboBox_user.setCurrentText(self.active_user)

    def change_user(self):
        """
        Update the active user when the user selection changes.

        Also refreshes the samples shown.
        """
        self.active_user = self.comboBox_user.currentText()
        self.update_shown_samples()

    def edit_sample_info(self):
        """
        Open a dialog to edit sample information.

        The dialog displays sample data such as name, identifier, and description.
        On acceptance, updates the sample data using the new hierarchical structure.
        """
        # IMPORT pandas and add_remove_table only if it is needed
        import pandas as pd
        from nomad_camels.ui_widgets import add_remove_table

        self.active_sample = self.comboBox_sample.currentText()
        headers = ["name", "sample_id", "description", "owner"]
        tableData = pd.DataFrame.from_dict(self.sampledata, "index")

        if not "owner" in tableData.columns:
            tableData["owner"] = ""

        # Filter tableData to only include samples owned by the active user or with no owner
        tableData = tableData[
            (tableData["owner"] == self.get_user_name_data()[0])
            | (tableData["owner"] == "")
        ]

        dialog = add_remove_table.AddRemoveDialoge(
            headerLabels=headers,
            parent=self,
            title="Sample-Information",
            askdelete=True,
            tableData=tableData,
            default_values={"owner": self.get_user_name_data()[0]},
            check_duplicates=[0, 1],
            editables=[0, 1, 2],
        )

        dialog.resize(800, 600)
        dialog.table.table.setColumnWidth(0, 150)
        dialog.table.table.setColumnWidth(1, 150)
        dialog.table.table.setColumnWidth(2, 350)
        dialog.table.table.setColumnWidth(3, 150)

        # Store the desired column widths (initially set to default values)
        desired_widths = [150, 150, 350, 150]

        # Function to update desired widths when user manually resizes columns
        def update_desired_widths():
            for i in range(dialog.table.table.model().columnCount()):
                desired_widths[i] = dialog.table.table.columnWidth(i)

        # Connect to header section resized signal to capture manual resizing
        dialog.table.table.horizontalHeader().sectionResized.connect(
            lambda logical_index, old_size, new_size: update_desired_widths()
        )

        # Override the resizeColumnsToContents method to maintain current widths
        original_resize = dialog.table.table.resizeColumnsToContents

        def custom_resize():
            # Update desired widths to current widths before any auto-resize
            update_desired_widths()
            # Then restore our current column widths (don't call original resize)
            for i, width in enumerate(desired_widths):
                if i < dialog.table.table.model().columnCount():
                    dialog.table.table.setColumnWidth(i, width)

        # Replace the method
        dialog.table.table.resizeColumnsToContents = custom_resize

        # Also override the clicked signal connection that triggers resize
        dialog.table.table.clicked.disconnect()
        dialog.table.table.clicked.connect(lambda: None)  # Do nothing on click

        # Enable text wrapping and auto row height adjustment
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QStyledItemDelegate, QHeaderView

        class WordWrapDelegate(QStyledItemDelegate):
            def paint(self, painter, option, index):
                # Enable word wrapping for text display
                option.displayAlignment = Qt.AlignTop | Qt.AlignLeft
                super().paint(painter, option, index)

            def sizeHint(self, option, index):
                # Calculate size hint based on wrapped text
                size = super().sizeHint(option, index)
                if index.column() == 2:  # Description column
                    # Get the text and calculate wrapped height
                    text = index.data()
                    if text:
                        # Use the column width to calculate wrapped text height
                        column_width = dialog.table.table.columnWidth(index.column())
                        font_metrics = option.fontMetrics
                        text_rect = font_metrics.boundingRect(
                            0,
                            0,
                            column_width - 10,
                            0,  # -10 for padding
                            Qt.TextWordWrap,
                            str(text),
                        )
                        size.setHeight(max(size.height(), text_rect.height() + 10))
                return size

        # Set the delegate for text wrapping
        word_wrap_delegate = WordWrapDelegate()
        dialog.table.table.setItemDelegate(word_wrap_delegate)

        # Enable word wrap in the table
        dialog.table.table.setWordWrap(True)

        # Set text elide mode to none so full text is shown when wrapped
        dialog.table.table.setTextElideMode(Qt.ElideNone)

        # Enable automatic row height adjustment
        dialog.table.table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        if dialog.exec():
            # Changing the returned dict to dataframe and back to ensure proper formatting.
            dat = dialog.get_data()
            for i, d in enumerate(dat["name"]):
                dat["name"][i] = d.strip()
                if not dat["name"][i] and dat["sample_id"][i]:
                    dat["name"][i] = dat["sample_id"][i]
                elif not dat["name"][i] and not dat["sample_id"][i]:
                    n = 1
                    while f"sample_{n}" in dat["name"]:
                        n += 1
                    dat["name"][i] = f"sample_{n}"
                    from nomad_camels.ui_widgets.toast_notification import (
                        show_warning_toast,
                    )

                    show_warning_toast(
                        f"Sample name was empty. Set to \"{dat['name'][i]}\".",
                        title="Set empty sample name",
                        parent=self,
                    )
            dat = pd.DataFrame(dat)
            dat["unique_name"] = dat.apply(
                lambda row: (
                    f'{row["name"]} / {row["sample_id"]}, {row["owner"]}'
                    if row["name"] != row["sample_id"] and row["sample_id"]
                    else f'{row["name"]}, {row["owner"]}'
                ),
                axis=1,
            )
            dat["display_name"] = dat.apply(
                lambda row: (
                    f'{row["name"]} / {row["sample_id"]}'
                    if row["name"] != row["sample_id"] and row["sample_id"]
                    else row["name"]
                ),
                axis=1,
            )
            dat.set_index("unique_name", inplace=True)
            data_dict = dat.to_dict("index")
            removers = []
            for key, value in self.sampledata.items():
                if not "owner" in value or (
                    value["owner"] == self.get_user_name_data()[0]
                    and key not in data_dict
                ):
                    removers.append(key)
            for key in removers:
                self.sampledata.pop(key)
            self.sampledata.update(dat.to_dict("index"))

            self.update_shown_samples()
            self.save_sample_data()

    def update_shown_samples(self):
        """
        Refresh the sample combobox with samples that are owned by the active user or have no owner.
        """
        self.comboBox_sample.clear()
        self.comboBox_sample.addItems(
            sorted(
                [
                    (
                        self.sampledata[key]["display_name"]
                        if "display_name" in self.sampledata[key]
                        else key
                    )
                    for key in self.sampledata.keys()
                    if self.sampledata[key].get("owner", "")
                    == self.get_user_name_data()[0]
                    or not self.sampledata[key].get("owner", "")
                ],
                key=lambda x: x.lower(),
            )
        )
        self.comboBox_sample.setCurrentText(self.active_sample)

    def save_sample_data(self):
        """
        Save the current sample data to a JSON file.
        """
        self.active_sample = self.comboBox_sample.currentText()
        sampledic = {"active_sample": self.active_sample}
        sampledic.update(self.sampledata)
        load_save_functions.save_dictionary(
            os.path.join(load_save_functions.appdata_path, "sampledata.json"), sampledic
        )

    def load_sample_data(self):
        """
        Load sample data from a JSON file.

        Sets the active sample and updates the sample data dictionary.
        """
        sampledat = {}
        samplefile = os.path.join(load_save_functions.appdata_path, "sampledata.json")
        if os.path.isfile(samplefile):
            with open(samplefile, "r", encoding="utf-8") as f:
                string_dict = json.load(f)
            load_save_functions.load_save_dict(
                string_dict, sampledat, update_missing_key=True
            )

        # Extract active sample
        if "active_sample" in sampledat:
            self.active_sample = sampledat["active_sample"]
            sampledat.pop("active_sample")
        self.sampledata = sampledat
        self.update_shown_samples()
        # self.comboBox_sample.addItems(sampledat.keys())
        # if not self.active_sample == "default_sample":
        #     self.comboBox_sample.setCurrentText(self.active_sample)

    def get_user_samples(self):
        """
        Get samples that belong to the current active user or are shared.

        Returns:
            dict: Dictionary of sample_id -> sample_data for the current user
        """
        user_samples = {}

        for global_key, sample_data in self.sampledata.items():
            # Parse the global key to extract user and sample_id
            if "::" in global_key:
                user, sample_id = global_key.split("::", 1)
                if user == self.get_user_name_data()[0]:
                    user_samples[sample_id] = sample_data  # Use clean sample_id as key
            else:
                # Shared sample (no user prefix)
                sample_id = global_key
                owner = sample_data.get("owner", "")
                if not owner or owner == "shared":
                    user_samples[sample_id] = sample_data  # Use clean sample_id as key

        return user_samples

    def select_nomad_sample(self):
        """
        Open a dialog to select a sample from NOMAD.

        Updates the NOMAD sample and updates the corresponding UI elements.
        """
        # IMPORT sample_selection only if it is needed
        from nomad_camels.nomad_integration import entry_selection

        upload_id = None
        entry_id = None
        if self.nomad_sample is not None:
            metadata = self.nomad_sample.get("NOMAD_entry_metadata", {})
            upload_id = metadata.get("upload_id", None)
            entry_id = metadata.get("entry_id", None)

        dialog = entry_selection.EntrySelector(
            self, upload_id=upload_id, entry_id=entry_id
        )
        if dialog.exec():
            self.nomad_sample = dialog.return_data
            if "name" in self.nomad_sample:
                name = self.nomad_sample["name"]
            else:
                name = self.nomad_sample["Name"]
            self.pushButton_nomad_sample.setText(f'change sample "{name}"')
        self.show_nomad_sample()

    def show_nomad_sample(self):
        """
        Show or hide NOMAD sample settings based on user selection and NOMAD login status.

        Updates the sample widget display and enables/disables the NOMAD sample selection button.
        """
        nomad = self.nomad_user is not None
        self.sample_widget_nomad.setHidden(not nomad)
        active_sample = self.nomad_sample is not None
        use_nomad = self.checkBox_use_nomad_sample.isChecked()
        use_nomad_sample = active_sample and use_nomad and nomad
        self.sample_widget_default.setHidden(use_nomad_sample)
        self.sample_widget_default.setEnabled(not use_nomad)
        self.pushButton_nomad_sample.setEnabled(use_nomad)

    # --------------------------------------------------
    # Save / Load methods
    # --------------------------------------------------
    def load_preferences(self):
        """
        Load application preferences.

        Those may contain:
        - autosave: turn on / off autosave on closing the program.
        - dark_mode: turning dark-mode on / off.
        - number_format: the number format for display, can be either "mixed", "plain" or "scientific".
        - mixed_from: the exponent from where to switch to scientific format, if number_format is "mixed".
        - n_decimals: the number of displayed decimals of a number.
        - py_files_path: the path, where python files (e.g. protocols) are created.
        - meas_files_path: the path, where measurement data is stored.
        - device_driver_path: the path, where NOMAD CAMELS can find the installed devices.
        - databroker_catalog_name: the name of the databroker catalog
        After loading, the dependent settings are updated.
        """
        self.preferences = load_save_functions.get_preferences()
        self.update_preference_settings()

    def update_preference_settings(self):
        """
        Update settings that depend on the preferences.

        This includes number formatting, device driver path, databroker catalog name, and graphic theme.
        """
        number_formatting.preferences = self.preferences
        variables_handling.preferences = self.preferences
        variables_handling.device_driver_path = self.preferences["device_driver_path"]
        variables_handling.meas_files_path = self.preferences["meas_files_path"]
        if "graphic_theme" in self.preferences:
            self.change_theme()
        self.change_catalog_name()
        logging_settings.update_log_settings()
        if self.preferences["enable_API"]:
            if not self.current_api_port:
                self.start_API_server(self.preferences["API_port"])
            else:
                if self.current_api_port != self.preferences["API_port"]:
                    self.stop_API_server()
                    self.start_API_server(self.preferences["API_port"])
        else:
            self.stop_API_server()

    def change_theme(self):
        """
        Change the graphic theme of the application based on the current preferences.
        """
        theme = self.preferences["graphic_theme"]
        if "material_theme" in self.preferences:
            material_theme = self.preferences["material_theme"]
        else:
            material_theme = None
        dark = self.preferences["dark_mode"]
        theme_changing.change_theme(
            theme, material_theme=material_theme, dark_mode=dark
        )
        self.toggle_dark_mode()

    def toggle_dark_mode(self):
        """
        Toggle dark mode on or off based on the preferences.
        """
        dark = self.preferences["dark_mode"]
        variables_handling.dark_mode = dark
        self.lineEdit_session.check_string()

    def change_catalog_name(self):
        """
        Change the name of the databroker catalog.

        If the catalog does not exist, a temporary catalog is used.
        """
        if not hasattr(self, "databroker_catalog") or self.databroker_catalog is None:
            return
        # IMPORT databroker only if it is needed
        import databroker

        if "meas_files_path" in self.preferences:
            catalog_name = "CATALOG_NAME"
            if "databroker_catalog_name" in self.preferences:
                catalog_name = self.preferences["databroker_catalog_name"]
            # IMPORT make_catalog only if it is needed
            from nomad_camels.bluesky_handling import make_catalog

            make_catalog.make_yml(
                self.preferences["meas_files_path"], catalog_name, ask_restart=True
            )
            databroker.catalog.force_reload()
            try:
                self.databroker_catalog = databroker.catalog[catalog_name]
            except KeyError:
                # IMPORT warnings only if it is needed
                import warnings

                warnings.warn(
                    "Could not find databroker catalog, using temporary catalog. If data is not transferred, it might get lost."
                )
                self.databroker_catalog = databroker.temp()

    def change_preferences(self):
        """
        Open the settings dialog to change preferences.

        On acceptance, updates the preferences dictionary, saves it, and updates the dependent settings.
        """
        # IMPORT Settings_Window only if it is needed
        from nomad_camels.frontpanels.settings_window import Settings_Window

        settings_dialog = Settings_Window(parent=self, settings=self.preferences)
        if settings_dialog.exec():
            self.preferences.update(settings_dialog.get_settings())
            load_save_functions.save_preferences(self.preferences)
        self.update_preference_settings()

    def save_state(self, fromload=False, do_backup=True):
        """
        Save the current application state.

        Saves the device preset along with user and sample data. Optionally creates a backup.

        Args:
            fromload (bool, optional): Indicates if the save is triggered from a load operation. Defaults to False.
            do_backup (bool, optional): Indicates whether to perform a backup. Defaults to True.
        """
        if (
            "password_protection" in self.preferences
            and self.preferences["password_protection"]
        ):
            from PySide6.QtWidgets import QMessageBox

            msg_box = QMessageBox()
            msg_box.setText(
                "This version of NOMAD CAMELS is password protected.\nDo you want to save changes?"
            )
            msg_box.setWindowTitle("Save changes?")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if msg_box.exec() == QMessageBox.Cancel:
                return
            from nomad_camels.utility.password_widgets import Password_Dialog

            dialog = Password_Dialog(
                self, compare_hash=self.preferences["password_hash"]
            )
            if not dialog.exec():
                return
        self.make_save_dict()
        load_save_functions.autosave_preset(
            self._current_preset[0], self.__save_dict__, do_backup
        )
        if fromload:
            return
        self.save_user_data()
        self.save_sample_data()
        print("current state saved!")

    def new_preset(self):
        """
        Create a new, empty device preset via a file dialog.

        Saves the new preset and reloads the state.
        """
        file = QFileDialog.getSaveFileName(
            self, "Save Preset", load_save_functions.preset_path, "*.preset"
        )[0]
        if not len(file):
            return
        preset_name = file.split("/")[-1][:-7]
        load_save_functions.save_preset(
            file,
            {
                "_current_preset": [preset_name],
                "active_instruments": {},
                "protocols_dict": OrderedDict(),
            },
        )
        self._current_preset[0] = preset_name
        self.load_state()

    def save_preset_as(self):
        """
        Save the current preset under a new name via a file dialog.

        A backup/autosave is performed automatically.
        """
        file = QFileDialog.getSaveFileName(
            self, "Save Preset", load_save_functions.preset_path, "*.preset"
        )[0]
        if not len(file):
            return
        preset_name = file.split("/")[-1][:-7]
        self._current_preset[0] = preset_name
        self.make_save_dict()
        load_save_functions.save_preset(file, self.__save_dict__)

    def load_backup_preset(self):
        """
        Load a preset from the backup folder via a file dialog.

        If a backup is selected, the current preset is first saved, then the backup is loaded.
        """
        file = QFileDialog.getOpenFileName(
            self, "Open Preset", load_save_functions.preset_path, "*.preset"
        )[0]
        if not file:
            return
        # preset_name = file.split('_')[-1][:-7]
        # preset = f'Backup/{file.split("/")[-2]}/{file.split("/")[-1][:-7]}'
        self.save_state()
        # self._current_preset[0] = preset_name
        self.load_preset(file)

    def load_state(self):
        """
        Load the most recent preset.

        If the most recent preset fails to load, attempts to load the second most recent preset.
        """
        n_preset = 1
        while True:
            try:
                presets = load_save_functions.get_most_recent_presets(True)
                preset = presets[-n_preset]
                if preset is not None:
                    self.load_preset(preset)
                else:
                    self.save_state(True)
                    self.load_state()
                break
            except Exception as e:
                warn_popup.WarnPopup(
                    self,
                    f'Could not load the most recent preset "{preset}".\nThe second newest will be loaded instead.\n\nError Message:\n{e}',
                    "Load Error",
                )
                n_preset += 1

    def change_preset(self, preset):
        """
        Save the current preset and load a new one.

        Args:
            preset (str): The name of the new preset to load.
        """
        self.save_state()
        self._current_preset[0] = preset
        self.load_preset(preset)

    def load_preset(self, preset):
        """
        Load the specified preset from file.

        Resets active instruments, protocols, manual controls, and updates the UI accordingly.

        Args:
            preset (str): The name or path of the preset to load.
        """
        try:
            with open(
                os.path.join(load_save_functions.preset_path, f"{preset}.preset"),
                "r",
                encoding="utf-8",
            ) as f:
                preset_dict = json.load(f)
        except FileNotFoundError:
            with open(preset, "r", encoding="utf-8") as f:
                preset_dict = json.load(f)
        self.active_instruments.clear()
        self.protocols_dict.clear()
        self.manual_controls.clear()
        self.protocol_tabs_dict.clear()
        self.manual_tabs_dict.clear()
        variables_handling.watchdogs.clear()
        try:
            load_save_functions.load_save_dict(preset_dict, self.preset_save_dict)
        except Exception as e:
            text = f"Could not load preset {preset}.\nAn empty preset will be loaded instead.\nTo handle this error, you may want to install a missing driver or remove some settings from the preset.\n\nError Message:\n{e}"
            warn_popup.WarnPopup(self, text, "Load Error")
            load_save_functions.load_save_dict(
                {}, self.preset_save_dict, remove_extra_key=True
            )
            self._current_preset[0] = "empty_preset"
        self.update_channels()
        variables_handling.preset = self._current_preset[0]
        self.populate_meas_buttons()
        self.populate_manuals_buttons()
        self.with_or_without_instruments()
        self.adjustSize()

    def make_save_dict(self):
        """
        Create the dictionary to be saved for the current preset.

        This includes active instruments, protocols, manual controls, and tabs.
        """
        self.manual_tabs_dict = self.button_area_manual.update_order()
        self.protocol_tabs_dict = self.button_area_meas.update_order()
        self.preset_save_dict = {
            "_current_preset": self._current_preset,
            "active_instruments": self.active_instruments,
            "protocols_dict": self.protocols_dict,
            "manual_controls": self.manual_controls,
            "protocol_tabs_dict": self.protocol_tabs_dict,
            "manual_tabs_dict": self.manual_tabs_dict,
            "watchdogs": {
                name: wd.get_definition()
                for name, wd in variables_handling.watchdogs.items()
            },
        }
        for key in self.preset_save_dict:
            add_string = load_save_functions.get_save_str(self.preset_save_dict[key])
            if add_string is not None:
                self.__save_dict__.update(
                    {key: load_save_functions.get_save_str(self.preset_save_dict[key])}
                )

    def update_channels(self):
        """
        Update the channels information from the active instruments.

        Clears existing channels in variables_handling and updates with channels from each active device.
        """
        variables_handling.channels.clear()
        for key, dev in self.active_instruments.items():
            # for channel in dev.get_channels():
            variables_handling.channels.update(dev.get_channels())
            variables_handling.config_channels.update(dev.config_channels)

    # --------------------------------------------------
    # Manual controls
    # --------------------------------------------------
    def add_manual_control(self):
        """
        Open a dialog to add a new manual control.

        On acceptance, adds the control data to the manual controls.
        """
        # IMPORT New_Manual_Control_Dialog only if needed
        from nomad_camels.manual_controls.get_manual_controls import (
            New_Manual_Control_Dialog,
        )

        dialog = New_Manual_Control_Dialog(self)
        if dialog.exec():
            control_cls, options_cls = dialog.selected_control
            options = options_cls()
            if options.exec():
                self.add_manual_control_to_data(options.control_data)

    def add_manual_control_to_data(self, control_data):
        """
        Add a manual control using the provided control data.

        Args:
            control_data (dict): Data for the manual control to add.
        """
        self.manual_controls[control_data["name"]] = control_data
        self.add_button_to_manuals(control_data["name"])
        self.button_area_manual.setHidden(False)

    def remove_manual_control(self, control_name):
        """
        Remove a manual control from the manual controls list and update the UI.

        Args:
            control_name (str): The name of the manual control to remove.
        """
        self.manual_controls.pop(control_name)
        # for controls in self.manual_tabs_dict.values():
        #     if control_name in controls:
        #         controls.remove(control_name)
        #         break
        self.button_area_manual.remove_button(control_name)
        if not self.manual_controls:
            self.button_area_manual.setHidden(True)

    def move_manual_control(self, control_name):
        """
        Move a manual control to another tab.

        Opens a dialog to select a new tab, and if different from the current tab,
        moves the control.

        Args:
            control_name (str): The name of the manual control to move.
        """
        from nomad_camels.frontpanels.helper_panels.button_move_scroll_area import (
            MoveDialog,
        )

        control_data = self.manual_controls[control_name]
        dialog = MoveDialog(parent=self, button_name=control_name)
        dialog.add_tabs_from_widget(self.button_area_manual)

        if dialog.exec():
            new_tab = dialog.get_tab()
            old_tab = self.button_area_manual.get_active_tab()
            if new_tab == old_tab:
                return
            self.remove_manual_control(control_name)
            self.add_button_to_manuals(control_name, new_tab)
            self.manual_controls[control_name] = control_data
            self.manual_tabs_dict = self.button_area_manual.update_order()
            self.button_area_manual.setHidden(False)

    def update_man_cont_data(self, control_data, old_name):
        """
        Update data for a manual control.

        Removes the old entry and updates it with the new control data, renaming buttons accordingly.

        Args:
            control_data (dict): The updated manual control data.
            old_name (str): The previous name of the manual control.
        """
        self.manual_controls.pop(old_name)
        self.manual_controls[control_data["name"]] = control_data
        button = self.button_area_manual.rename_button(old_name, control_data["name"])
        self.add_functions_to_manual_button(button, control_data["name"])

    def open_manual_control_config(self, control_name):
        """
        Open the configuration dialog for a manual control.

        If the dialog is accepted, updates the manual control data accordingly.

        Args:
            control_name (str): The name of the manual control to configure.
        """
        # IMPORT get_control_by_type_name only if needed
        from nomad_camels.manual_controls.get_manual_controls import (
            get_control_by_type_name,
        )

        control_data = self.manual_controls[control_name]
        config_cls = get_control_by_type_name(control_data["control_type"])[1]
        dialog = config_cls(parent=self, control_data=control_data)
        if dialog.exec():
            self.update_man_cont_data(dialog.control_data, control_name)

    def add_button_to_manuals(self, name, tab=""):
        """
        Add a button for a manual control in the manual controls area.

        Args:
            name (str): The name of the manual control.
            tab (str, optional): The tab where the button should be added. Defaults to the active tab.
        """
        button = options_run_button.Options_Run_Button(
            name, small_text="Start", protocol_options=False
        )
        # get active tab
        tab = tab or self.button_area_manual.get_active_tab()
        self.button_area_manual.add_button(button, name, tab)
        self.add_functions_to_manual_button(button, name)

    def add_functions_to_manual_button(self, button, name):
        """
        Connect functions to a manual control button.

        Functions include opening configuration, starting, deleting, and moving the manual control.

        Args:
            button (Options_Run_Button): The button to update.
            name (str): The name of the manual control.
        """
        button.config_function = (
            lambda state=None, x=name: self.open_manual_control_config(x)
        )
        button.run_function = lambda state=None, x=name: self.start_manual_control(x)
        button.del_function = lambda x=name: self.remove_manual_control(x)
        button.move_function = lambda x=name: self.move_manual_control(x)
        button.update_functions()

    def populate_manuals_buttons(self):
        """
        Populate the manual controls area with buttons for each manual control.

        Clears the area and then adds buttons according to the current manual controls data.
        """
        self.button_area_manual.clear_area()
        addeds = []
        for tab, controls in list(self.manual_tabs_dict.items()):
            if not controls:
                del self.manual_tabs_dict[tab]
            for control in controls:
                if control in self.manual_controls and control not in addeds:
                    self.add_button_to_manuals(control, tab)
                    addeds.append(control)
        for control in self.manual_controls:
            if control not in addeds:
                self.add_button_to_manuals(control, "manual controls")
        if not self.manual_controls:
            self.manual_tabs_dict.clear()
            self.button_area_manual.create_new_tab("manual controls")
        self.button_area_manual.setCurrentIndex(0)

    def start_manual_control(self, name):
        """
        Start a manual control.

        Instantiates the control class and opens it in a new window. Also disables the single-run button.

        Args:
            name (str): The name of the manual control to start.
        """
        # IMPORT get_control_by_type_name only if needed
        from nomad_camels.manual_controls.get_manual_controls import (
            get_control_by_type_name,
        )

        control_data = self.manual_controls[name]
        control_type = control_data["control_type"]
        control_cls = get_control_by_type_name(control_type)[0]
        control = control_cls(control_data=control_data)
        self.open_windows.append(control)
        control.closing.connect(
            lambda x=control, y=name: self.close_manual_control(x, y)
        )
        self.button_area_manual.disable_single_run(name)

    def close_manual_control(self, control, name):
        """
        Handle the closing of a manual control.

        Removes the control from the list of open windows and re-enables its button.

        Args:
            control (Manual_Control): The control that is closing.
            name (str): The name of the manual control.
        """
        self.open_windows.remove(control)
        self.button_area_manual.enable_single_run(name)

    # --------------------------------------------------
    # Protocols
    # --------------------------------------------------
    def add_measurement_protocol(self, *, copied_protocol=None):
        """
        Open an empty protocol configuration dialog.

        On acceptance, the protocol is added to the protocols data.
        """
        # IMPORT Protocol_Config only if needed
        from nomad_camels.frontpanels.protocol_config import Protocol_Config

        if copied_protocol is not None:
            from copy import deepcopy

            protocol = deepcopy(copied_protocol)
            protocol.name = f"{protocol.name}_copy_"
            # If an old protocol is provided, open it in the dialog
            dialog = Protocol_Config(protocol)
        else:
            dialog = Protocol_Config()
        dialog.show()
        dialog.accepted.connect(self.add_prot_to_data)
        self.add_to_open_windows(dialog)

    def import_measurement_protocol(self):
        """
        Import a protocol from a file.

        Opens a file dialog to select a protocol file (.cprot), then loads and opens its configuration dialog.
        """
        # IMPORT Protocol_Config and Path_Button_Dialog only if needed
        from nomad_camels.frontpanels.protocol_config import Protocol_Config
        from nomad_camels.ui_widgets.path_button_edit import Path_Button_Dialog

        dialog = Path_Button_Dialog(
            self,
            default_dir=self.preferences["py_files_path"],
            file_extension="*.cprot",
            title="Choose Protocol - NOMAD CAMELS",
            text="select the protocol you want to import",
        )
        if not dialog.exec():
            return
        prot_path = dialog.path
        prot = load_save_functions.load_protocol(prot_path)
        dialog = Protocol_Config(prot)
        dialog.show()
        dialog.accepted.connect(self.add_prot_to_data)
        self.add_to_open_windows(dialog)

    def add_prot_to_data(self, protocol):
        """
        Add a measurement protocol to the protocols dictionary.

        Also adds a corresponding button to the measurement controls area.

        Args:
            protocol (Measurement_Protocol): The protocol to add.
        """
        self.protocols_dict[protocol.name] = protocol
        self.add_button_to_meas(protocol.name)
        if self.button_area_meas.isHidden():
            self.button_area_meas.setHidden(False)

    def remove_protocol(self, prot_name):
        """
        Remove a protocol from the protocols dictionary and update the UI.

        Args:
            prot_name (str): The name of the protocol to remove.
        """
        self.protocols_dict.pop(prot_name)
        self.button_area_meas.remove_button(prot_name)
        if not self.protocols_dict:
            self.button_area_meas.setHidden(True)

    def move_protocol(self, protocol_name):
        """
        Move a protocol to a different tab.

        Opens a move dialog to choose a new tab and moves the protocol button accordingly.

        Args:
            protocol_name (str): The name of the protocol to move.
        """
        from nomad_camels.frontpanels.helper_panels.button_move_scroll_area import (
            MoveDialog,
        )

        protocol = self.protocols_dict[protocol_name]
        dialog = MoveDialog(parent=self, button_name=protocol_name)
        dialog.add_tabs_from_widget(self.button_area_meas)

        if dialog.exec():
            new_tab = dialog.get_tab()
            old_tab = self.button_area_meas.get_active_tab()
            if new_tab == old_tab:
                return
            self.remove_protocol(protocol_name)
            self.add_button_to_meas(protocol_name, new_tab)
            self.protocols_dict[protocol_name] = protocol
            self.protocol_tabs_dict = self.button_area_meas.update_order()
            self.button_area_meas.setHidden(False)

    def update_prot_data(self, protocol, old_name):
        """
        Update the data of a protocol.

        Removes the old protocol entry and replaces it with the updated one, renaming buttons accordingly.

        Args:
            protocol (Measurement_Protocol): The updated protocol.
            old_name (str): The old name of the protocol.
        """
        self.protocols_dict.pop(old_name)
        self.protocols_dict[protocol.name] = protocol
        button = self.button_area_meas.rename_button(old_name, protocol.name)
        self.add_functions_to_meas_button(button, protocol.name)
        file_path = f"{self.preferences['py_files_path']}/{protocol.name}.cprot"
        protocol_dict = load_save_functions.get_save_str(protocol)
        load_save_functions.save_dictionary(file_path, protocol_dict)

    def open_protocol_config(self, prot_name):
        """
        Open the configuration dialog for a protocol.

        If the dialog is accepted, updates the protocol data.

        Args:
            prot_name (str): The name of the protocol to configure.
        """
        # IMPORT Protocol_Config only if needed
        if not self.check_password_protection():
            return
        from nomad_camels.frontpanels.protocol_config import Protocol_Config

        for dialog in self.open_windows:
            if isinstance(dialog, Protocol_Config):
                if dialog.old_name == prot_name:
                    dialog.raise_()
                    return

        dialog = Protocol_Config(self.protocols_dict[prot_name])
        dialog.show()
        dialog.accepted.connect(lambda x, y=prot_name: self.update_prot_data(x, y))
        self.add_to_open_windows(dialog)

    def add_button_to_meas(self, name, tab=""):
        """
        Add a button for a measurement protocol to the measurement controls area.

        Args:
            name (str): The name of the protocol.
            tab (str, optional): The tab to add the button to; defaults to the active tab.
        """
        button = options_run_button.Options_Run_Button(name)
        # get active tab
        tab = tab or self.button_area_meas.get_active_tab()
        self.button_area_meas.add_button(button, name, tab)
        self.add_functions_to_meas_button(button, name)
        if not self.protocol_tabs_dict.get(tab):
            self.protocol_tabs_dict[tab] = []
        if not name in self.protocol_tabs_dict[tab]:
            self.protocol_tabs_dict[tab].append(name)

    def add_functions_to_meas_button(self, button, name):
        """
        Connect functions to a measurement protocol button.

        Functions include configuration, running, building, opening, data path access,
        deletion, moving, and queuing the protocol.

        Args:
            button (Options_Run_Button): The protocol button to update.
            name (str): The name of the protocol.
        """
        button.config_function = lambda state=None, x=name: self.open_protocol_config(x)
        button.run_function = lambda state=None, x=name: self.run_protocol(x)
        button.build_function = lambda x=name: self.build_protocol(x)
        button.external_function = lambda x=name: self.open_protocol(x)
        button.data_path_function = lambda x=name: self.open_data_path(x)
        button.del_function = lambda x=name: self.remove_protocol(x)
        button.move_function = lambda x=name: self.move_protocol(x)
        button.duplicate_function = lambda x=name: self.add_measurement_protocol(
            copied_protocol=self.protocols_dict[x]
        )
        button.queue_function = lambda state=None, x=name: self.queue_protocol(x)
        button.update_functions()

    def open_data_path(self, protocol_name):
        """
        Open the data path for a protocol in the file explorer.

        Args:
            protocol_name (str): The name of the protocol.
        """
        user = self.get_user_name_data()[0]
        sample = self.get_sample_name_data()[0]
        protocol = self.protocols_dict[protocol_name]
        if protocol.use_nexus:
            file_ending = ".nxs"
        else:
            file_ending = ".h5"
        savepath = f"{self.preferences['meas_files_path']}/{user}/{sample}/{protocol.filename or 'data'}{file_ending}"
        savepath = os.path.normpath(savepath)
        while not os.path.exists(savepath):
            savepath = os.path.dirname(savepath)

        if platform.system() == "Windows":
            # /select, specifies that the file should be highlighted
            subprocess.Popen(f'explorer /select,"{savepath}"')
        elif platform.system() == "Darwin":
            # -R, specifies that the file should be revealed in finder
            subprocess.Popen(["open", "-R", savepath])
        else:
            # Linux doesn't support highlighting a specific file in the file explorer
            subprocess.Popen(["xdg-open", os.path.dirname(savepath)])

    def populate_meas_buttons(self):
        """
        Populate the measurement protocols area with buttons.

        Clears the area and then adds buttons for each protocol.
        """
        self.button_area_meas.clear_area()
        addeds = []
        for tab, protocols in list(self.protocol_tabs_dict.items()):
            if not protocols:
                del self.protocol_tabs_dict[tab]
            for prot in protocols:
                if prot in self.protocols_dict and prot not in addeds:
                    self.add_button_to_meas(prot, tab)
                    addeds.append(prot)
        for prot in self.protocols_dict:
            if prot not in addeds:
                self.add_button_to_meas(prot, "protocols")
        if not self.protocols_dict:
            self.protocol_tabs_dict.clear()
            self.button_area_meas.create_new_tab("protocols")
        self.button_area_meas.setCurrentIndex(0)

    def next_queued_protocol(self, protocol_name, variables, api_uuid=None):
        """
        Run the next queued protocol if the run engine is idle.

        Args:
            protocol_name (str): The name of the protocol.
            variables (dict): The variables for the protocol.
            api_uuid (Optional[str]): The API unique identifier, defaults to None.
        """
        if self.run_engine and self.run_engine.state != "idle":
            return
        if api_uuid == "":
            api_uuid = None
        self.run_queue_widget.remove_first()
        self.run_protocol(protocol_name, api_uuid=api_uuid, variables=variables)

    def run_protocol(self, protocol_name, api_uuid=None, variables=None):
        """
        Run a measurement protocol.

        Builds and imports the protocol file, instantiates required devices,
        and executes the protocol. Manages UI updates and handles NOMAD uploads if applicable.

        Args:
            protocol_name (str): The name of the protocol to run.
            api_uuid (Optional[str]): The API unique identifier, defaults to None.
            variables (Optional[dict]): Variables for the protocol, defaults to None.
        """
        self.setCursor(Qt.WaitCursor)
        plot_placement.reset_variables()
        # IMPORT importlib, bluesky, ophyd and time only if needed
        import importlib

        if not self.run_engine:
            self.bluesky_setup()
        self.still_running = True
        # IMPORT device_handling only if needed
        from nomad_camels.utility import device_handling

        if "autosave_run" in self.preferences and self.preferences["autosave_run"]:
            self.save_state(do_backup=self.preferences["backup_before_run"])
        self.button_area_meas.disable_run_buttons()
        try:
            self.pushButton_resume.setEnabled(False)
            self.pushButton_pause.setEnabled(False)
            self.pushButton_stop.setEnabled(True)
            self.build_protocol(protocol_name, ask_file=False, variables=variables)
            protocol = self.protocols_dict[protocol_name]
            self.running_protocol = protocol
            path = f"{self.preferences['py_files_path']}/{protocol.name}.py"
            name = os.path.basename(path)[:-3]
            spec = importlib.util.spec_from_file_location(name, path)
            self.protocol_module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = self.protocol_module
            spec.loader.exec_module(self.protocol_module)
            self.protocol_module.protocol_step_information[
                "protocol_stepper_signal"
            ] = self.protocol_stepper_signal
            plots, subs, app, plots_plotly = self.protocol_module.create_plots(
                self.run_engine
            )
            for plot in plots:
                self.add_to_plots(plot)
            device_list = protocol.get_used_devices()
            self.current_protocol_device_list = list(device_list)
            self.re_subs += subs
            self.instantiate_devices_thread = device_handling.InstantiateDevicesThread(
                device_list, skip_config=protocol.skip_config
            )
            if api_uuid is not None:
                self.instantiate_devices_thread.successful.connect(
                    lambda: self.run_protocol_part2(
                        api_uuid,
                    )
                )
            else:
                self.instantiate_devices_thread.successful.connect(
                    lambda: self.run_protocol_part2()
                )
            self.instantiate_devices_thread.exception_raised.connect(
                self.propagate_exception
            )
            self.instantiate_devices_thread.start()
        except Exception as e:
            self.protocol_finished()
            if isinstance(e, IndentationError):
                text = "The protocol did not compile correctly, please check whether there are for example any if-statements or loops that do not have children-steps."
                raise Exception(text) from e
            else:
                raise e
        self.close_old_queue_devices()

    def propagate_exception(self, exception):
        """
        Handle exceptions raised during device instantiation.

        Calls protocol_finished and then raises the exception.

        Args:
            exception (Exception): The exception that was raised.
        """
        self.protocol_finished()
        raise exception

    def run_protocol_part2(self, api_uuid=None):
        """
        Continue running the protocol after devices are instantiated.

        Executes the main protocol steps, sets up live windows and subscriptions,
        and handles NOMAD uploads if applicable.

        Args:
            api_uuid (Optional[str]): The API unique identifier, defaults to None.
        """
        additionals = {}
        try:
            devs = self.instantiate_devices_thread.devices
            dev_data = self.instantiate_devices_thread.device_config
            self.instantiate_devices_thread.quit()
            self.instantiate_devices_thread.wait()
            self.instantiate_devices_thread.deleteLater()
            self.instantiate_devices_thread = None
            additionals = self.protocol_module.steps_add_main(self.run_engine, devs)
            self.add_subs_and_plots_from_dict(additionals)
            self.current_protocol_devices = devs
        except Exception as e:
            self.protocol_finished()
            raise e
        import time

        self.saving_plot_list = list(
            set(
                self.protocol_module.plots
                + helper_functions.make_recoursive_plot_list_of_sub_steps(additionals)
            )
        )

        if self.running_protocol.h5_during_run:
            from nomad_camels.bluesky_handling.helper_functions import (
                saving_function,
            )
            from event_model import RunRouter

            self.run_router = RunRouter(
                [
                    lambda x, y: saving_function(
                        name=x,
                        start_doc=y,
                        path=self.protocol_module.save_path,
                        new_file_each=self.protocol_module.new_file_each_run,
                        plot_data=self.saving_plot_list,
                        do_nexus_output=self.running_protocol.use_nexus,
                        new_file_hours=self.protocol_module.new_file_hours,
                    )
                ]
            )
            self.re_subs.append(self.run_engine.subscribe(self.run_router))
        live_windows = self.protocol_module.create_live_windows()
        for window in live_windows:
            self.add_to_open_windows(window)

        if self.running_protocol.use_nexus:
            protocol_savepath = f"{self.protocol_savepath}.nxs"
        else:
            protocol_savepath = f"{self.protocol_savepath}.h5"

        self.pushButton_resume.setEnabled(False)
        self.pushButton_pause.setEnabled(True)
        self.pushButton_stop.setEnabled(True)
        self.protocol_module.run_protocol_main(
            self.run_engine,
            catalog=self.databroker_catalog,
            devices=devs,
            md={
                "devices": dev_data,
                "api_uuid": api_uuid,  # Include the uuid in the metadata
            },
            dispatcher=self.dispatcher,
            publisher=self.publisher,
            additionals=additionals,
        )
        self.pushButton_resume.setEnabled(False)
        self.pushButton_pause.setEnabled(False)
        self.pushButton_stop.setEnabled(False)
        self.protocol_stepper_signal.emit(100)
        nomad = self.nomad_user is not None
        if self.last_save_file:
            file = helper_functions.get_newest_file(self.last_save_file)
        else:
            file = helper_functions.get_newest_file(protocol_savepath)
        file = os.path.normpath(file)
        self.run_done_file_signal.emit(file)
        # Check if the protocol was executed using the api and save results to db if true
        if api_uuid is not None:
            from nomad_camels.api.api import write_protocol_result_path_to_db

            write_protocol_result_path_to_db(api_uuid, message=file)
        if not nomad:
            return
        while self.still_running:
            time.sleep(0.1)
        if self.nomad_sample and self.checkBox_use_nomad_sample.isChecked():
            if "name" in self.nomad_sample:
                name = f"/{self.nomad_sample['name']}"
            elif "Name" in self.nomad_sample:
                name = f"/{self.nomad_sample['Name']}"
            else:
                name = ""
        else:
            name = f"/{self.active_sample}"
        if self.comboBox_upload_type.currentText() == "auto upload":
            # IMPORT nomad_communication only if needed
            from nomad_camels.nomad_integration import nomad_communication

            upload = self.comboBox_upload_choice.currentText()
            nomad_communication.upload_file(
                file, upload, f"CAMELS_data{name}", parent=self
            )
        elif self.comboBox_upload_type.currentText() == "ask after run":
            # IMPORT file_uploading only if needed
            from nomad_camels.nomad_integration import file_uploading

            dialog = file_uploading.UploadDialog(self, file, f"CAMELS_data{name}")

    def add_subs_and_plots_from_dict(self, dictionary):
        """
        Recursively add subscriptions and plots from a dictionary.

        The dictionary may contain keys 'subs' and 'plots' or nested dictionaries.

        Args:
            dictionary (dict): Dictionary containing subscriptions and plots.
        """
        for k, v in dictionary.items():
            if k == "subs":
                self.re_subs += v
            elif k == "plots":
                for plot in v:
                    self.add_to_plots(plot)
            elif isinstance(v, dict):
                self.add_subs_and_plots_from_dict(v)

    def pause_protocol(self):
        """
        Pause the currently running protocol.

        Requests the run engine to pause and updates the UI buttons accordingly.
        """
        if self.run_engine and self.run_engine.state == "running":
            self.run_engine.request_pause()
            self.pushButton_resume.setEnabled(True)
            self.pushButton_pause.setEnabled(False)

    def update_live_variables(self, variables):
        """
        Update live variables during protocol execution.

        Args:
            variables (dict): The new values for the live variables.
        """
        self.protocol_module.namespace.update(variables)

    def watchdog_triggered(self, watchdog):
        """
        Handle a triggered watchdog condition.

        Pauses the protocol, executes the watchdog protocol if defined, and shows a warning popup.

        Args:
            watchdog (Watchdog): The triggered watchdog object.
        """
        from nomad_camels.utility import device_handling
        import bluesky, ophyd
        import bluesky.plan_stubs as bps

        warn_text = (
            f"Watchdog {watchdog.name} triggered with condition {watchdog.condition}"
        )
        logging.warning(warn_text)
        watchdog.was_triggered = True
        warning = warn_popup.WarnPopup(
            self,
            warn_text,
            "Watchdog Triggered",
            do_not_pause=True,
        )
        self.pause_protocol()
        self.setEnabled(False)
        subs = []
        try:
            if not self.run_engine:
                self.bluesky_setup()
            from nomad_camels.bluesky_handling.protocol_builder import build_from_path

            if not watchdog.execute_at_condition:
                raise Exception(
                    f'Watchdog "{watchdog.name}" has nothing to execute when condition is met'
                )
            protocol = load_save_functions.load_protocol(watchdog.execute_at_condition)
            protocol_name = protocol.name

            user, userdata = self.get_user_name_data()
            sample, sampledata = self.get_sample_name_data()
            savepath = f"{self.preferences['meas_files_path']}/{user}/{sample}/watchdog_execution.nxs"
            build_from_path(
                watchdog.execute_at_condition,
                save_path=savepath,
                userdata=userdata,
                sampledata=sampledata,
                catalog=self.databroker_catalog,
            )
            path = pathlib.Path(watchdog.execute_at_condition)
            spec = importlib.util.spec_from_file_location(
                path.stem, path.with_suffix(".py")
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            if not watchdog.plots:
                plots, subs, app, plots_plotly = module.create_plots(
                    self.run_engine, stream="watchdog_triggered"
                )
                watchdog.plots = plots
            else:
                for plot in watchdog.plots:
                    self.run_engine.subscribe(plot.livePlot)
            for plot in watchdog.plots:
                self.add_to_plots(plot)
            device_list = protocol.get_used_devices()
            devs, dev_data = device_handling.instantiate_devices(
                device_list, skip_config=protocol.skip_config
            )
            additionals = module.steps_add_main(self.run_engine, devs)
            self.add_subs_and_plots_from_dict(additionals)
            module.protocol_stepper_signal = self.fake_signal
            module.protocol_step_information["protocol_stepper_signal"] = (
                self.fake_signal
            )
            if self.run_engine.state == "paused":

                def pause_plan():
                    namespace = self.eva.namespace.copy()
                    module.namespace.update(namespace)
                    self.eva.namespace = module.namespace
                    yield from getattr(module, f"{protocol_name}_plan_inner")(
                        devs, self.eva, stream_name="watchdog_triggered"
                    )
                    yield from bps.checkpoint()
                    yield from bps.pause()
                    yield from bps.checkpoint()
                    self.eva.namespace = namespace

                self.run_engine._plan_stack.append(pause_plan())
                self.run_engine._response_stack.append(None)
                self.run_engine.resume()
                # wait for run engine to pause again
                while self.run_engine.state == "running":
                    import time

                    time.sleep(0.1)
            else:
                module.run_protocol_main(
                    self.run_engine,
                    catalog=self.databroker_catalog,
                    devices=devs,
                    md={"devices": dev_data},
                )
        except Exception as e:
            if not isinstance(e, bluesky.utils.RunEngineInterrupted):
                self.stop_protocol()
                self.setEnabled(True)
                raise e
        finally:
            for sub in subs:
                self.run_engine.unsubscribe(sub)
            self.setEnabled(True)
            if not warning.clicked_by_user:
                warning.exec()
            watchdog.was_triggered = False

    def stop_protocol(self):
        """
        Stop the currently running protocol.

        Aborts the run engine, and if necessary, runs the end protocol.
        Also handles cleanup of device threads.
        """
        if self.run_engine.state != "idle":
            self._was_aborted = True
            self.pushButton_resume.setEnabled(False)
            self.pushButton_pause.setEnabled(False)
            self.pushButton_stop.setEnabled(False)
            self.setWindowTitle(
                "Protocol aborted, waiting for cleanup... - NOMAD CAMELS"
            )
            self.run_engine.abort("Aborted by user")
        if (
            self.instantiate_devices_thread
            and self.instantiate_devices_thread.isRunning()
        ):
            self.instantiate_devices_thread.successful.disconnect()
            self.instantiate_devices_thread.exception_raised.disconnect()
            self.old_devices_thread = self.instantiate_devices_thread
            self.old_devices_thread.finished.connect(
                self.close_unused_instantiated_devices
            )
            self.protocol_finished()
        # self.protocol_finished()

    def close_unused_instantiated_devices(self):
        """
        Close devices that were instantiated but are no longer in use.

        Called after stopping protocols that were queued.
        """
        devs = self.old_devices_thread.devices
        from nomad_camels.utility import device_handling

        device_handling.close_devices(devs)

    def resume_protocol(self):
        """
        Resume a paused protocol.

        Updates the UI buttons and instructs the run engine to resume.
        """
        if self.run_engine.state == "paused":
            self.pushButton_resume.setEnabled(False)
            self.pushButton_pause.setEnabled(True)
            self.run_engine.resume()

    def protocol_finished(self, *args):
        """
        Handle the end of protocol execution.

        Removes subscriptions, cleans up devices, checks if a queued protocol should be run next,
        and performs final UI updates.
        """
        # IMPORT databroker_export and device_handling only if needed
        if self._was_aborted:
            if not self.run_engine.state == "idle":
                self.start_timer_signal.emit()
                return
        self.protocol_finished_part_2()

    def _start_timer(self):
        self._timer.start(1000)

    def _check_RE_done(self):
        if self.run_engine.state == "idle":
            self._timer.stop()
            self.protocol_finished_part_2()

    def protocol_finished_part_2(self):
        if self._was_aborted and self.running_protocol.use_end_protocol:
            try:
                self.run_engine(
                    self.protocol_module.ending_steps(
                        self.run_engine, self.current_protocol_devices
                    )
                )
            except Exception as e:
                logging.error(f"Error during end protocol steps: {e}")
        self._was_aborted = False
        self.setWindowTitle(
            "NOMAD CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems"
        )
        if (
            self.protocol_module
            and hasattr(self.protocol_module, "uids")
            and self.protocol_module.uids
            and (
                not self.running_protocol.h5_during_run
                or self.running_protocol.export_csv
                or self.running_protocol.export_json
            )
        ):
            runs = self.databroker_catalog[tuple(self.protocol_module.uids)]
            from nomad_camels.bluesky_handling.helper_functions import export_function

            export_function(
                runs,
                self.protocol_savepath,
                not self.running_protocol.h5_during_run,
                self.preferences["new_file_each_run"],
                self.running_protocol.export_csv,
                self.running_protocol.export_json,
                self.protocol_module.plots,
                self.running_protocol.use_nexus,
            )
        for sub in self.re_subs:
            self.run_engine.unsubscribe(sub)
        self.re_subs.clear()
        self.devices_from_queue.append(self.current_protocol_device_list)
        if self.run_queue_widget.check_next_protocol():
            return
        self.run_queue_widget.setHidden(True)
        self.label_queue.setHidden(True)
        self.current_protocol_device_list = []
        self.close_old_queue_devices()
        self.pushButton_stop.setEnabled(False)
        self.pushButton_pause.setEnabled(False)
        self.pushButton_resume.setEnabled(False)
        self.button_area_meas.enable_run_buttons()
        self.protocol_stepper_signal.emit(100)
        self.setCursor(Qt.ArrowCursor)
        if "number_databroker_files" in variables_handling.preferences:
            n_files = variables_handling.preferences["number_databroker_files"]
            if n_files > 0:
                name = self.preferences["databroker_catalog_name"]
                meas_dir = self.preferences["meas_files_path"]
                catalog_dir = f"{meas_dir}/databroker/{name}"
                if os.path.isdir(catalog_dir):
                    files = os.listdir(catalog_dir)
                    if len(files) > n_files:
                        files.sort(key=lambda x: os.path.getmtime(f"{catalog_dir}/{x}"))
                        for file in files[:-n_files]:
                            os.remove(f"{catalog_dir}/{file}")
        self.still_running = False
        self.protocol_finished_signal.emit()

    def play_finished_sound(self):
        if variables_handling.preferences["finished_sound"]:
            try:
                from PySide6.QtMultimedia import QSoundEffect
                from PySide6.QtCore import QUrl

                self.sound_effect = QSoundEffect()
                self.sound_effect.setSource(
                    QUrl.fromLocalFile(str(resources.files(graphics) / "done.wav"))
                )
                self.sound_effect.play()
            except Exception as e:
                logging.warning(f"Error playing sound: {e}")

    def _update_remaining_time_progress_bar(self, step):
        self.progressBar_protocols.setValue(step)
        now = time.time()
        elapsed_time = now - self._protocol_start_time
        remaining_time = (elapsed_time / step) * (100 - step)
        if step > 100:
            self.progressBar_protocols.setValue(99)
            if elapsed_time > 3600:
                elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                remaining_time_str = "??:??:??"
            else:
                elapsed_time_str = time.strftime("%M:%S", time.gmtime(elapsed_time))
                remaining_time_str = "??:??"
        elif remaining_time > 3600 or elapsed_time > 3600:
            remaining_time_str = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
            elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        else:
            remaining_time_str = time.strftime("%M:%S", time.gmtime(remaining_time))
            elapsed_time_str = time.strftime("%M:%S", time.gmtime(elapsed_time))
        self.label_remaining_time.setText(f"{elapsed_time_str} / {remaining_time_str}")

    def close_old_queue_devices(self):
        """
        Close devices from previously queued protocols that are not used in the current protocol.
        """
        # IMPORT device_handling only if needed
        from nomad_camels.utility import device_handling

        currently_in_use = self.current_protocol_device_list

        for_close = []
        for device_list in self.devices_from_queue:
            for device in device_list:
                if device not in currently_in_use:
                    for_close.append(device)
        for_close = list(set(for_close))
        if for_close:
            device_handling.close_devices(for_close)

    def build_protocol(self, protocol_name, ask_file=True, variables=None):
        """
        Build the protocol file for the specified protocol.

        Calls the protocol builder to export the protocol as a Python file.

        Args:
            protocol_name (str): The name of the protocol.
            ask_file (bool, optional): Whether to prompt for a file location. Defaults to True.
            variables (Optional[dict], optional): Optional variables to override protocol defaults. Defaults to None.
        """
        from copy import deepcopy

        self.progressBar_protocols.setValue(0)
        self._protocol_start_time = time.time()
        protocol = deepcopy(self.protocols_dict[protocol_name])
        protocol.variables = variables or protocol.variables
        protocol.session_name = self.lineEdit_session.text()
        if re.search(r"[^\w\s]", protocol.session_name):
            raise ValueError(
                "Session name contains special characters.\nPlease use only letters, numbers and whitespace."
            )

        if ask_file:
            path = QFileDialog.getSaveFileName(
                self, "Export Protocol", protocol_name, "*.py"
            )[0]
            if not path:
                return
        else:
            path = f"{self.preferences['py_files_path']}/{protocol_name}.py"
        protocol.measurement_description = self.textEdit_meas_description.toPlainText()
        protocol.tags = self.flow_layout.get_all_tags()
        user, userdata = self.get_user_name_data()
        sample, sampledata = self.get_sample_name_data()
        savepath = f"{self.preferences['meas_files_path']}/{user}/{sample}/{protocol.session_name}/{protocol.filename or protocol.session_name or 'data'}"
        self.protocol_savepath = savepath
        # IMPORT protocol_builder only if needed
        from nomad_camels.bluesky_handling import protocol_builder

        protocol_builder.build_protocol(
            protocol, path, savepath, userdata=userdata, sampledata=sampledata
        )
        self.update_prot_data(protocol, protocol_name)
        print("\n\nBuild successful!\n")
        self.progressBar_protocols.setValue(100 if ask_file else 1)

    def queue_protocol(self, protocol_name, api_uuid=None):
        """
        Add a protocol to the execution queue.

        Updates the run queue widget and makes it visible.

        Args:
            protocol_name (str): The name of the protocol to queue.
            api_uuid (Optional[str], optional): The API unique identifier, defaults to None.
        """
        if protocol_name in self.protocols_dict:
            self.run_queue_widget.add_item(protocol_name, api_uuid=api_uuid)
            self.run_queue_widget.setHidden(False)
            self.label_queue.setHidden(False)

    def get_user_name_data(self):
        """
        Retrieve the current user name and associated data.

        Returns:
            tuple: A tuple containing the user name and user data dictionary.
        """
        if self.nomad_user:
            userdata = self.nomad_user
            user = userdata["name"]
        elif self.extension_user:
            userdata = self.extension_user
            user = userdata["name"]
        else:
            user = self.active_user or "default_user"
            userdata = (
                {"name": "default_user"}
                if user == "default_user"
                else self.userdata[user]
            )
        user = clean_filename(user)
        return user, userdata

    def get_sample_name_data(self):
        """
        Retrieve the current sample name and associated data.

        Returns:
            tuple: A tuple containing the sample name and sample data dictionary.
        """
        if self.nomad_sample and self.checkBox_use_nomad_sample.isChecked():
            sampledata = self.nomad_sample
            if "name" in sampledata:
                sample = sampledata["name"]
            elif "Name" in sampledata:
                sample = sampledata["Name"]
            else:
                sample = "NOMAD-Sample"
        elif self.extension_sample:
            sampledata = self.extension_sample
            sample = sampledata["name"]
        else:
            sample = self.comboBox_sample.currentText() or "default_sample"
            if not sample in self.sampledata:
                for s in self.sampledata:
                    if (
                        "display_name" in self.sampledata[s]
                        and self.sampledata[s]["display_name"] == sample
                    ):
                        sampledata = self.sampledata[s]
                        break
            else:
                sampledata = (
                    {"name": "default_sample"}
                    if sample == "default_sample"
                    else self.sampledata[sample]
                )
            sample = sampledata["name"]
        sample = clean_filename(sample)
        return sample, sampledata

    def open_protocol(self, protocol_name):
        """
        Open the protocol file in the default editor.

        If the protocol file does not exist, it is built first.

        Args:
            protocol_name (str): The name of the protocol to open.
        """
        path = f"{self.preferences['py_files_path']}/{protocol_name}.py"
        if not os.path.isfile(path):
            self.build_protocol(protocol_name, False)
        variables_handling.open_link(path)

    # --------------------------------------------------
    # Tools
    # --------------------------------------------------
    def launch_device_builder(self):
        """
        Launch the device driver builder dialog.

        Opens a dialog to assist in building device drivers.
        """
        # IMPORT device_driver_builder only if needed
        from nomad_camels.tools import device_driver_builder

        device_builder = device_driver_builder.Driver_Builder(self)
        device_builder.show()

    def launch_epics_builder(self):
        """
        Launch the EPICS driver builder dialog.

        Opens a dialog to assist in building EPICS drivers.
        """
        # IMPORT EPICS_driver_builder only if needed
        from nomad_camels.tools import EPICS_driver_builder

        device_builder = EPICS_driver_builder.EPICS_Driver_Builder(self)
        device_builder.show()

    def launch_data_exporter(self):
        """
        Launch the data exporter dialog.

        Opens a dialog to assist in exporting data from the databroker.
        """
        # IMPORT databroker_exporter only if needed
        from nomad_camels.tools import databroker_exporter

        exporter = databroker_exporter.Datbroker_Exporter(self)
        exporter.show()

    def launch_hdf5_exporter(self):
        """
        Launch the HDF5 exporter dialog.

        Opens a dialog to assist in exporting HDF5 files.
        """
        from nomad_camels.utility import databroker_export

        exporter = databroker_export.ExportH5_dialog(self)
        exporter.exec()

    def clear_fastapi_thread(self, *args):
        """
        Clear the FastAPI server thread if an error occurs.

        Also displays a warning popup indicating the server failed to start.
        """
        if self.fastapi_thread:
            self.fastapi_thread = None
            # Show pop up box with warning that the server failed to start
            warn_popup.WarnPopup(
                self,
                "The FastAPI server failed to start.\nMake sure the Port you entered is correct.",
                "FastAPI Server Error",
            )
