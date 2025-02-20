from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QFrame,
    QCheckBox,
    QTextEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from ophyd import EpicsSignalRO
from ophyd import Device as OphydDevice
from ophyd.signal import SignalRO

from nomad_camels.main_classes.measurement_channel import Measurement_Channel
from nomad_camels.ui_widgets.warn_popup import WarnPopup

from nomad_camels.extensions import extension_contexts
from nomad_camels.nomad_integration import entry_selection, nomad_communication


class Device:
    """General class for all devices/instruments.

    If subclassing this in a driver, subclass should be called "subclass", it
    will be imported via importlib in that way.
    Any derived device should also provide the name of its ophyd-class
    as a string self.ophyd_class_name.

    Attributes
    ----------
    name : str
        represents the device, should be unique
    virtual : bool
        whether the device does not need any hardware
    tags : list
        list of strings for the device search
    ophyd_class_name : str
        name of the class of ophyd_device
    settings : dict
        settings handed to the ophyd class at runtime of the protocol
    config : dict
        values, the config-attributes / components of the ophyd device should be
        set to
    channels : dict
        channels of the device (i.e.: Signals that are not config)
    controls : dict
        Dictionary of additional manual controls this device provides
    """

    def __init__(
        self,
        name="",
        virtual=False,
        tags=None,
        ophyd_device=None,
        ophyd_class_name="",
        additional_info=None,
        non_channel_functions=None,
        main_thread_only=False,
        **kwargs,
    ):
        """
        Parameters
        ----------
        name : str
            represents the device, should be unique
        virtual : bool
            whether the device does not need any hardware
        tags : list
            list of strings for the device search
        ophyd_device : ophyd.Device
            used for initialisation of the channels, the class used for
            the bluesky-integration
        ophyd_class_name : str
            name of the class of ophyd_device
        """

        self.__save_dict__ = {}  # TODO use or remove
        self.name = name
        self.custom_name = name
        self.virtual = virtual
        self.tags = [] if tags is None else tags
        self.additional_info = additional_info or {}
        self.settings = {}
        self.config = {}
        self.passive_config = {}
        self.channels = {}
        self.config_channels = {}
        self.non_channel_functions = non_channel_functions or []
        self.main_thread_only = main_thread_only
        self.ophyd_class_name = ophyd_class_name
        if ophyd_device is None:
            ophyd_device = OphydDevice
        self.ophyd_class = ophyd_device
        self.ophyd_instance = ophyd_device(name="test")
        self.get_channels()
        for comp in self.ophyd_instance.walk_components():
            name = comp.item.attr
            dev_class = comp.item.cls
            if name in self.ophyd_instance.configuration_attrs:
                # use default value of the component
                value = getattr(self.ophyd_instance, name)._readback
                if check_output(dev_class):
                    self.config.update({f"{name}": value})
                else:
                    self.passive_config.update({f"{name}": value})
        self.controls = {}
        config_channel_metadata = {}
        for chan in self.config_channels:
            config_channel_metadata[chan] = self.config_channels[chan].get_meta_str()
        self.additional_info["config_channel_metadata"] = config_channel_metadata

    def get_necessary_devices(self):
        """Returns a list of the devices that this device needs to function
        (e.g. for a PID controller)."""
        return []

    def get_controls(self):
        """Returns the device's specific manual controls.

        Returns
        -------
        self.controls : dict
            Dictionary of the device's manual controls
        """
        return self.controls

    def get_non_channel_functions(self):
        funcs = []
        for func in self.non_channel_functions:
            funcs.append(f"{self.custom_name}.{func}")
        return funcs

    def get_finalize_steps(self):
        """Returns the string used in the 'finally' part of the protocol's main
        function to e.g. close the instrument communication.

        Returns
        -------
        step_str : str
        """
        s = f"\t\tif '{self.custom_name}' in devs and hasattr(devs['{self.custom_name}'], 'finalize_steps') and callable(devs['{self.custom_name}'].finalize_steps):\n"
        s += f"\t\t\tdevs['{self.custom_name}'].finalize_steps()\n"
        return s

    def get_passive_config(self):
        """Not used."""
        return self.passive_config

    def get_config(self):
        """returns self.config, should be overwritten for special
        purposes (e.g. leaving out some keys of the dictionary)

        Returns
        -------
        self.config : dict
        """
        return self.config

    def get_settings(self):
        """returns self.settings, should be overwritten for special
        purposes (e.g. leaving out some keys of the dictionary)

        Returns
        -------
        self.settings : dict
        """
        return self.settings

    def get_additional_info(self):
        """Returns the additional information about the instrument.

        Returns
        -------
        self.additional_info : dict
        """
        return self.additional_info

    def get_channels(self):
        """returns self.channels, should be overwritten for special
        purposes (e.g. leaving out some keys of the dictionary)

        Returns
        -------
        self.channels : dict
            dictionary containing the device's channels
        """
        self.channels = {}
        outputs = get_outputs(self.ophyd_instance)
        channels, config_channels = get_channels(
            self.ophyd_instance, include_metadata=True, include_config=True
        )
        for chan_info in channels:
            chan, metadata = chan_info
            is_out = chan in outputs
            channel = Measurement_Channel(
                name=f"{self.custom_name}.{chan}",
                output=is_out,
                device=self.custom_name,
                metadata=metadata,
            )
            self.channels.update({f"{self.custom_name}_{chan}": channel})
        for config_chan_info in config_channels:
            chan, metadata = config_chan_info
            is_out = chan in outputs
            channel = Measurement_Channel(
                name=f"{self.custom_name}.{chan}",
                output=is_out,
                device=self.custom_name,
                metadata=metadata,
            )
            self.config_channels.update({f"{self.custom_name}_{chan}": channel})
        return self.channels

    def get_additional_string(self):
        """returns a string that will be added into the protocol after
        connecting to the device.

        Returns
        -------
        additional_str : str
        """
        return ""

    def get_special_steps(self):
        """returns a dictionary containing containing device-specific
        loopsteps. The key is the loopstep's name, the value a list
        containing the Class of the step, and its config-widget.

        Returns
        -------
        steps : dict{'<step_name>': [Step_Class, Step_Config]}
        """
        return {}


def get_configs(ophyd_instance):
    """Returns the configuration and passive configuration of the given
    ophyd-instance.

    Parameters
    ----------
    ophyd_instance : ophyd.Device
        The ophyd-device that should be checked

    Returns
    -------
    config : dict
        The configuration of the device
    passive_config : dict
        The passive configuration of the device
    """
    config = {}
    passive_config = {}
    for comp in ophyd_instance.walk_components():
        name = comp.item.attr
        dev_class = comp.item.cls
        if name in ophyd_instance.configuration_attrs:
            value = getattr(ophyd_instance, name)._readback
            if check_output(dev_class):
                config.update({f"{name}": value})
            else:
                passive_config.update({f"{name}": value})
    return config, passive_config


def check_output(cls) -> bool:
    """Returns False if the give `cls` is an instance of a read-only Signal."""
    output = not issubclass(cls, EpicsSignalRO)
    output = output and not issubclass(cls, SignalRO)
    return output


def get_outputs(dev: OphydDevice):
    """walks through the components of an ophyd-device and checks
    whether they can be written

    Parameters
    ----------
    dev : ophyd.Device
        The device that should be checked


    Returns
    -------
    outputs : list
        List of the outputs' names
    """
    outputs = []
    for comp in dev.walk_components():
        cls = comp.item.cls
        name = comp.item.attr
        if check_output(cls):
            outputs.append(name)
    return outputs


def get_channels(dev: OphydDevice, include_metadata=False, include_config=False):
    """returns the components of an ophyd-device that are not listed in
    the configuration

    Parameters
    ----------
    dev : ophyd.Device
        The device that should be checked

    include_metadata : bool, default False
        If True, also returns the compnents' metadata

    Returns
    -------
    channels : list
        list of the device's channels
        if metadata is True, it will be a list of tuples containing the channels'
        names and their metadata
    """
    channels = []
    config_channels = []
    for comp in dev.walk_components():
        name = comp.item.attr
        if name not in dev.configuration_attrs:
            real_channel = True
        else:
            real_channel = False
            if not include_config:
                continue
        if include_metadata:
            if hasattr(comp.item, "kwargs") and "metadata" in comp.item.kwargs:
                metadata = comp.item.kwargs["metadata"]
            else:
                metadata = {}
            if real_channel:
                channels.append((name, metadata))
            else:
                config_channels.append((name, metadata))
        else:
            if real_channel:
                channels.append(name)
            else:
                config_channels.append(name)
    if include_config:
        return channels, config_channels
    return channels


class Device_Config(QWidget):
    """Parent class for the configuration-widgets
    (shown on the frontpanel) of the devices.

    Parameters
    ----------

    Returns
    -------

    """

    name_change = Signal(str)

    def __init__(
        self,
        parent=None,
        device_name="",
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
    ):
        """
        Parameters
        ----------
        parent : QWidget
            handed to QWidget, usually the MainApp
        device_name : str
            name of the device for the title of the widget
        data : str
            data from the treeView_devices, it is needed to connect the
            settings to the correct device
        settings_dict : dict
            all the current settings of the device
        config_dict : dict
            the current configuration of the device
        """

        super().__init__(parent)
        if settings_dict is None:
            settings_dict = {}
        if config_dict is None:
            config_dict = {}
        self.data = data

        layout = QGridLayout()
        self.setLayout(layout)

        label_title = QLabel(f"{device_name} - Configuration")
        title_font = QFont("MS Shell Dlg 2", 10)
        title_font.setWeight(QFont.Bold)
        label_title.setFont(title_font)

        self.label_custom_name = QLabel("Custom name:")
        self.lineEdit_custom_name = QLineEdit(data)

        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.textEdit_desc = QTextEdit(parent=self)
        self.textEdit_desc.textChanged.connect(self.adjust_text_edit_size)
        self.textEdit_desc.setPlaceholderText("Enter your description here.")
        if additional_info and "description" in additional_info:
            self.textEdit_desc.setText(additional_info["description"])
        self.adjust_text_edit_size()

        self.label_connection = QLabel("Connection-type:")
        self.comboBox_connection_type = QComboBox()
        self.connector = Connection_Config()
        self.comboBox_connection_type.currentTextChanged.connect(
            self.connection_type_changed
        )

        self.label_id = QLabel("ID:")
        self.lineEdit_id = QLineEdit()
        if additional_info and "ELN-instrument-id" in additional_info:
            self.lineEdit_id.setText(additional_info["ELN-instrument-id"])
        self.pushbutton_id = QPushButton("...")
        self.pushbutton_id.setFixedWidth(30)
        id_info_text = "If you use an ELN, you can get the instrument's ID there. The ID can help to connect to other entries in the ELN.\nIn NOMAD Oasis, it is the Lab-ID of the instrument's entry.\nYou can leave this empty if you do not have an ID."
        self.pushbutton_id.setToolTip(id_info_text)
        self.label_id.setToolTip(id_info_text)
        self.lineEdit_id.setToolTip(id_info_text)

        layout.addWidget(label_title, 0, 0, 1, 5)
        layout.addWidget(self.label_custom_name, 1, 0)
        layout.addWidget(self.lineEdit_custom_name, 1, 1, 1, 4)
        layout.addWidget(self.textEdit_desc, 2, 0, 1, 5)
        layout.addWidget(self.label_id, 3, 0)
        layout.addWidget(self.lineEdit_id, 3, 1, 1, 3)
        layout.addWidget(self.pushbutton_id, 3, 4)
        layout.addWidget(self.line_2, 4, 0, 1, 5)
        layout.addWidget(self.label_connection, 5, 0)
        layout.addWidget(self.comboBox_connection_type, 5, 1, 1, 4)
        layout.addWidget(self.connector, 6, 0, 1, 5)

        self.settings_dict = settings_dict
        self.config_dict = config_dict
        self.additional_info = additional_info or {}
        self.lineEdit_custom_name.textChanged.connect(
            lambda x: self.name_change.emit(x)
        )
        self.ELN_metadata = {}
        if additional_info and "ELN-metadata" in additional_info:
            self.ELN_metadata = additional_info["ELN-metadata"]
        self.pushbutton_id.clicked.connect(self.eln_connection_button_clicked)
        self.load_settings()

    def eln_connection_button_clicked(self):
        logged_in = check_logged_in()
        if not logged_in:
            WarnPopup(
                self,
                "You need to be logged in to NOMAD or another ELN to use this feature!\nCannot get instrument ID from ELN.",
                "Not logged in!",
                info_icon=True,
            )
        elif logged_in == "NOMAD":
            selector = entry_selection.EntrySelector(self, "Instrument")
            if selector.exec():
                self.ELN_metadata = selector.return_data
                self.lineEdit_id.setText(
                    self.ELN_metadata.pop("identifier")
                    if "identifier" in self.ELN_metadata
                    else (
                        self.ELN_metadata["name"]
                        if "name" in self.ELN_metadata
                        else self.ELN_metadata["Name"]
                    )
                )
        elif logged_in == "ELN":
            try:
                eln_data = extension_contexts.active_eln_context.selection_function(
                    self
                )
                if eln_data:
                    self.ELN_metadata = eln_data
                    self.lineEdit_id.setText(
                        str(self.ELN_metadata["identifier"])
                        if "identifier" in self.ELN_metadata
                        else (
                            self.ELN_metadata["name"]
                            if "name" in self.ELN_metadata
                            else self.ELN_metadata["Name"]
                        )
                    )
            except Exception as e:
                raise Exception("Selection of ELN entry failed!") from e

    def showEvent(self, event):
        """Called when the widget is shown."""
        super().showEvent(event)
        self.adjust_text_edit_size()

    def adjust_text_edit_size(self):
        """Adjusts the size of the textEdit_desc based on its content."""
        document = self.textEdit_desc.document()
        document_height = document.size().height()
        self.textEdit_desc.setFixedHeight(document_height + 5)  # Add some padding

    def connection_type_changed(self):
        """Called when the comboBox_connection_type is changed. Switches
        to another connector-widget to specify things like the Address
        of the device.

        Parameters
        ----------

        Returns
        -------

        """
        conn_old = self.connector
        if self.comboBox_connection_type.currentText() == "Local VISA":
            self.connector = Local_VISA()
        self.connector.load_settings(self.settings_dict)
        self.layout().replaceWidget(conn_old, self.connector)
        conn_old.deleteLater()

    def get_settings(self):
        """Updates the settings_dict with the current settings.
        Overwrite this function for each device to specify the settings.
        It is recommended to still call the super() method for the
        connection-settings.

        Parameters
        ----------

        Returns
        -------

        """
        self.settings_dict.update(
            {"connection": {"type": self.comboBox_connection_type.currentText()}}
        )
        self.settings_dict["connection"].update(self.connector.get_settings())
        return self.settings_dict

    def load_settings(self):
        """Loads the settings from the settings_dict. Depending on the
        connection-type, the correct widget is set and the settings
        entered. Overwrite this function (and call it) for the specific
        settings.

        Parameters
        ----------

        Returns
        -------

        """
        self.connection_type_changed()
        no_choice = self.comboBox_connection_type.count() < 2
        self.label_connection.setHidden(no_choice)
        self.comboBox_connection_type.setHidden(no_choice)

    def get_config(self):
        """Returns the config_dict of the device. Overwrite this
        function for each device to specify the config.

        Parameters
        ----------

        Returns
        -------

        """
        return self.config_dict

    def get_info(self):
        """ """
        self.additional_info["description"] = self.textEdit_desc.toPlainText()
        self.additional_info["ELN-instrument-id"] = self.lineEdit_id.text()
        if "ELN-service" in self.ELN_metadata:
            self.additional_info["ELN-service"] = self.ELN_metadata.pop("ELN-service")
        else:
            self.additional_info["ELN-service"] = ""
        self.additional_info["ELN-metadata"] = self.ELN_metadata
        return self.additional_info


class Device_Config_Sub(QWidget):
    """ """

    def __init__(self, settings_dict=None, parent=None, config_dict=None):
        super().__init__()
        self.settings_dict = settings_dict or {}
        self.config_dict = config_dict or {}
        if settings_dict is None and config_dict is None:
            self.setLayout(QGridLayout())
            self.layout().addWidget(QLabel("Nothing to configure!"))

    def get_config(self):
        """ """
        return self.config_dict

    def get_settings(self):
        """ """
        return self.settings_dict


class Connection_Config(QWidget):
    """Base Class for the widgets used to specify the connection of a
    given device.

    Parameters
    ----------

    Returns
    -------

    """

    connection_change = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def get_settings(self):
        """Overwrite to return the connection-specific settings"""
        return {}

    def load_settings(self, settings_dict):
        """Overwrite to load the connection-specific settings from
        `settings_dict`.

        Parameters
        ----------
        settings_dict :


        Returns
        -------

        """
        pass


class Local_VISA(Connection_Config):
    """ """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.only_resource_name = False

        label_port = QLabel("Resource-Name:")
        self.comboBox_port = QComboBox()
        try:
            import pyvisa
        except ImportError:
            from PySide6.QtWidgets import QMessageBox

            msg = (
                f"You need PyVISA for VISA communication.\n\n"
                "Do you want to install it now?"
            )

            # Show a question message box.
            reply_update_modules = QMessageBox.question(
                None,
                "Install PyVISA?",
                msg,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply_update_modules == QMessageBox.Yes:
                import sys
                import subprocess

                # Build the pip install command.
                command = [sys.executable, "-m", "pip", "install", "nomad-camels[visa]"]
                # Optionally, you might show another popup or a console message indicating progress.
                subprocess.check_call(command)
                QMessageBox.information(
                    None,
                    "Installation Complete",
                    "The required modules have been installed.\nYou might need to restart CAMELS for the changes to take effect.",
                )

        try:
            rm = pyvisa.ResourceManager()
        except OSError:
            rm = pyvisa.ResourceManager("@py")
        self.ports = rm.list_resources()
        if not self.ports:
            WarnPopup(
                text="No VISA resources found!\nYou might need to install a VISA library.",
                title="No VISA resources!",
                do_not_pause=True,
            )
        self.comboBox_port.addItems(self.ports)

        self.layout().addWidget(label_port, 0, 0)
        self.layout().addWidget(self.comboBox_port, 0, 1, 1, 4)

        label_baud = QLabel("Baud-Rate:")
        self.lineEdit_baud = QLineEdit("9600")
        self.layout().addWidget(label_baud, 1, 0)
        self.layout().addWidget(self.lineEdit_baud, 1, 1)

        label_timeout = QLabel("Timeout (ms):")
        self.lineEdit_timeout = QLineEdit("2000")
        self.layout().addWidget(label_timeout, 1, 2)
        self.layout().addWidget(self.lineEdit_timeout, 1, 3)

        label_in_term = QLabel("In-Terminator:")
        self.lineEdit_in_term = QLineEdit("\\r\\n")
        self.layout().addWidget(label_in_term, 2, 0)
        self.layout().addWidget(self.lineEdit_in_term, 2, 1)

        label_out_term = QLabel("Out-Terminator:")
        self.lineEdit_out_term = QLineEdit("\\r\\n")
        self.layout().addWidget(label_out_term, 2, 2)
        self.layout().addWidget(self.lineEdit_out_term, 2, 3)

        label_error_retry = QLabel("Retries on error:")
        self.lineEdit_error_retry = QLineEdit("0")
        self.layout().addWidget(label_error_retry, 3, 0)
        self.layout().addWidget(self.lineEdit_error_retry, 3, 1)

        self.checkbox_retry_on_timeout = QCheckBox("retry on timeout")
        self.layout().addWidget(self.checkbox_retry_on_timeout, 3, 2, 1, 2)
        self.widgets_to_hide = [
            label_baud,
            self.lineEdit_baud,
            label_timeout,
            self.lineEdit_timeout,
            label_in_term,
            self.lineEdit_in_term,
            label_out_term,
            self.lineEdit_out_term,
            label_error_retry,
            self.lineEdit_error_retry,
            self.checkbox_retry_on_timeout,
        ]

    def get_settings(self):
        """ """
        if self.only_resource_name:
            return {"resource_name": self.comboBox_port.currentText()}
        return {
            "resource_name": self.comboBox_port.currentText(),
            "baud_rate": int(self.lineEdit_baud.text()),
            "timeout": int(self.lineEdit_timeout.text()),
            "read_termination": self.lineEdit_in_term.text()
            .replace("\\r", "\r")
            .replace("\\n", "\n"),
            "write_termination": self.lineEdit_out_term.text()
            .replace("\\r", "\r")
            .replace("\\n", "\n"),
            "retry_on_error": int(self.lineEdit_error_retry.text()),
            "retry_on_timeout": self.checkbox_retry_on_timeout.isChecked(),
        }

    def load_settings(self, settings_dict):
        """

        Parameters
        ----------
        settings_dict :


        Returns
        -------

        """
        if "connection" in settings_dict:
            settings_dict = settings_dict["connection"]
        if (
            "resource_name" in settings_dict
            and settings_dict["resource_name"] in self.ports
        ):
            self.comboBox_port.setCurrentText(settings_dict["resource_name"])
        if "baud_rate" in settings_dict:
            self.lineEdit_baud.setText(str(settings_dict["baud_rate"]))
        if "timeout" in settings_dict:
            self.lineEdit_timeout.setText(str(settings_dict["timeout"]))
        if "read_termination" in settings_dict:
            self.lineEdit_in_term.setText(
                settings_dict["read_termination"]
                .replace("\r", "\\r")
                .replace("\n", "\\n")
            )
        if "write_termination" in settings_dict:
            self.lineEdit_out_term.setText(
                settings_dict["write_termination"]
                .replace("\r", "\\r")
                .replace("\n", "\\n")
            )
        if "retry_on_error" in settings_dict:
            self.lineEdit_error_retry.setText(str(settings_dict["retry_on_error"]))
        if "retry_on_timeout" in settings_dict:
            self.checkbox_retry_on_timeout.setChecked(settings_dict["retry_on_timeout"])

    def set_only_resource_name(self):
        for widge in self.widgets_to_hide:
            widge.setHidden(True)
        self.only_resource_name = True


class Simple_Config(Device_Config):
    """ """

    def __init__(
        self,
        parent=None,
        device_name="",
        data="",
        settings_dict=None,
        config_dict=None,
        additional_info=None,
        comboBoxes=None,
        config_types=None,
        labels=None,
    ):
        config_channel_metadata = additional_info.get("config_channel_metadata", None)
        super().__init__(
            parent,
            device_name=device_name,
            data=data,
            settings_dict=settings_dict,
            config_dict=config_dict,
            additional_info=additional_info,
        )
        self.sub_widget = Simple_Config_Sub(
            settings_dict=settings_dict,
            parent=self,
            config_dict=config_dict,
            comboBoxes=comboBoxes,
            config_types=config_types,
            labels=labels,
            config_channel_metadata=config_channel_metadata,
            device_name=device_name,
        )
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sub_widget)
        self.extra_line = QFrame()
        self.extra_line.setFrameShape(QFrame.HLine)
        self.extra_line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(self.extra_line, 10, 0, 1, 5)
        self.layout().addWidget(self.scroll_area, 11, 0, 1, 5)
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout().addItem(self.spacer, 12, 0, 1, 5)
        self.load_settings()

    def get_settings(self):
        """ """
        self.sub_widget.get_settings()
        return super().get_settings()

    def get_config(self):
        """ """
        self.sub_widget.get_config()
        return super().get_config()


class Simple_Config_Sub(Device_Config_Sub):
    """ """

    config_changed = Signal()

    def __init__(
        self,
        settings_dict=None,
        parent=None,
        config_dict=None,
        comboBoxes=None,
        config_types=None,
        labels=None,
        config_channel_metadata=None,
        device_name="",
    ):
        super().__init__(
            settings_dict=settings_dict, parent=parent, config_dict=config_dict
        )
        settings_dict = settings_dict or {}
        config_dict = config_dict or {}
        config_channel_metadata = config_channel_metadata or {}
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        comboBoxes = comboBoxes or {}
        config_types = config_types or {}
        labels = labels or {}
        self.setting_checks = {}
        self.setting_floats = {}
        self.setting_strings = {}
        self.setting_combos = {}
        labels = labels or {}
        for name, val in settings_dict.items():
            if name == "connection":
                continue
            if name in comboBoxes:
                self.setting_combos[name] = QComboBox()
                self.setting_combos[name].addItems(comboBoxes[name])
                self.setting_combos[name].setCurrentText(val)
            elif name in config_types:
                if config_types[name] == "bool":
                    self.setting_checks[name] = QCheckBox(
                        labels[name] if name in labels else name
                    )
                    if isinstance(val, bool):
                        self.setting_checks[name].setChecked(val)
                elif config_types[name] == "float":
                    self.setting_floats[name] = QLineEdit(str(val))
                elif config_types[name] == "str":
                    self.setting_strings[name] = QLineEdit(str(val))
                else:
                    raise Exception(
                        f"Named config_type {config_types[name]} of {name} is not supported in Simple_Device_Config!"
                    )
            elif isinstance(val, bool):
                self.setting_checks[name] = QCheckBox(
                    labels[name] if name in labels else name
                )
                self.setting_checks[name].setChecked(val)
            elif isinstance(val, float) or isinstance(val, int):
                self.setting_floats[name] = QLineEdit(str(val))
            elif isinstance(val, str):
                self.setting_strings[name] = QLineEdit(val)
            else:
                raise Exception(
                    f"Type of {name} with value {val} not supported for simple device config!"
                )
        self.config_checks = {}
        self.config_floats = {}
        self.config_strings = {}
        self.config_combos = {}
        for name, val in config_dict.items():
            if name in comboBoxes:
                self.config_combos[name] = QComboBox()
                self.config_combos[name].addItems([str(x) for x in comboBoxes[name]])
                self.config_combos[name].setCurrentText(str(val))
            elif name in config_types:
                if config_types[name] == "bool":
                    self.config_checks[name] = QCheckBox(
                        labels[name] if name in labels else name
                    )
                    if isinstance(val, bool):
                        self.config_checks[name].setChecked(val)
                elif config_types[name] == "float":
                    self.config_floats[name] = QLineEdit(str(val))
                elif config_types[name] == "str":
                    self.config_strings[name] = QLineEdit(str(val))
                else:
                    raise Exception(
                        f"Named config_type {config_types[name]} of {name} is not supported in Simple_Device_Config!"
                    )
            elif isinstance(val, bool):
                self.config_checks[name] = QCheckBox(
                    labels[name] if name in labels else name
                )
                self.config_checks[name].setChecked(val)
            elif isinstance(val, float) or isinstance(val, int):
                self.config_floats[name] = QLineEdit(str(val))
            elif isinstance(val, str):
                self.config_strings[name] = QLineEdit(val)
            else:
                raise Exception(
                    f"Type of {name} with value {val} not supported for simple device config!"
                )
        for widge in self.setting_checks.values():
            widge.stateChanged.connect(lambda x=None: self.config_changed.emit())
        for widge in self.setting_combos.values():
            widge.currentTextChanged.connect(lambda x=None: self.config_changed.emit())
        for widge in self.setting_strings.values():
            widge.returnPressed.connect(lambda x=None: self.config_changed.emit())
        for widge in self.setting_floats.values():
            widge.returnPressed.connect(lambda x=None: self.config_changed.emit())
        for widge in self.config_checks.values():
            widge.stateChanged.connect(lambda x=None: self.config_changed.emit())
        for widge in self.config_combos.values():
            widge.currentTextChanged.connect(lambda x=None: self.config_changed.emit())
        for widge in self.config_strings.values():
            widge.returnPressed.connect(lambda x=None: self.config_changed.emit())
        for widge in self.config_floats.values():
            widge.returnPressed.connect(lambda x=None: self.config_changed.emit())

        col = 0
        row = 0
        self.setting_widgets = []
        for name, widge in self.setting_checks.items():
            self.layout().addWidget(widge, row, col, 1, 2)
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.setting_widgets.append(widge)
        for name, widge in self.setting_floats.items():
            if name in labels:
                label = QLabel(labels[name])
            else:
                label = QLabel(name)
            self.layout().addWidget(label, row, col)

            self.layout().addWidget(widge, row, col + 1)
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.setting_widgets.append([label, widge])
        for name, widge in self.setting_strings.items():
            if name in labels:
                label = QLabel(labels[name])
            else:
                label = QLabel(name)
            self.layout().addWidget(label, row, col)

            self.layout().addWidget(widge, row, col + 1)
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.setting_widgets.append([label, widge])
        for name, widge in self.setting_combos.items():
            if name in labels:
                label = QLabel(labels[name])
            else:
                label = QLabel(name)
            self.layout().addWidget(label, row, col)
            self.layout().addWidget(widge, row, col + 1)
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.setting_widgets.append([label, widge])

        self.config_widgets = []
        for name, widge in self.config_checks.items():
            self.layout().addWidget(widge, row, col, 1, 2)
            add_tooltip_from_name(
                [widge], f"{device_name}_{name}", config_channel_metadata
            )
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.config_widgets.append(widge)
        for name, widge in self.config_floats.items():
            if name in labels:
                label = QLabel(labels[name])
            else:
                label = QLabel(name)
            self.layout().addWidget(label, row, col)
            self.layout().addWidget(widge, row, col + 1)
            add_tooltip_from_name(
                [widge, label], f"{device_name}_{name}", config_channel_metadata
            )
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.config_widgets.append([label, widge])
        for name, widge in self.config_strings.items():
            if name in labels:
                label = QLabel(labels[name])
            else:
                label = QLabel(name)
            self.layout().addWidget(label, row, col)
            self.layout().addWidget(widge, row, col + 1)
            add_tooltip_from_name(
                [widge, label], f"{device_name}_{name}", config_channel_metadata
            )
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.config_widgets.append([label, widge])
        for name, widge in self.config_combos.items():
            if name in labels:
                label = QLabel(labels[name])
            else:
                label = QLabel(name)
            self.layout().addWidget(label, row, col)
            self.layout().addWidget(widge, row, col + 1)
            add_tooltip_from_name(
                [widge, label], f"{device_name}_{name}", config_channel_metadata
            )
            col += 2
            if col == 4:
                col = 0
                row += 1
            self.config_widgets.append([label, widge])
        self.line_frame = QFrame(self)
        self.line_frame.setFrameShape(QFrame.HLine)
        self.line_frame.setFrameShadow(QFrame.Sunken)
        self.line_frame.setObjectName("line_frame")
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.resize(max(self.width(), self.get_min_width_column() * 2), self.height())
        self.update_layout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_layout()

    def get_min_width_column(self):
        """ """
        min_width = 1
        for widge in self.setting_widgets + self.config_widgets:
            if isinstance(widge, list):
                width = sum([x.sizeHint().width() for x in widge])
            else:
                width = widge.sizeHint().width()
            min_width = max(min_width, width)
        return min_width

    def update_layout(self):
        while self.layout().count():
            item = self.layout().takeAt(0)
            self.layout().removeItem(item)
        width = self.width()
        column_width = self.get_min_width_column()
        columns = width // column_width
        columns = max(1, columns)
        positions = [
            (i // columns, i % columns) for i in range(len(self.setting_widgets))
        ]
        row = -1
        for i, widge in enumerate(self.setting_widgets):
            row, col = positions[i]
            if isinstance(widge, list):
                for j, widge in enumerate(widge):
                    self.layout().addWidget(widge, row, 2 * col + j)
            else:
                self.layout().addWidget(widge, row, 2 * col, 1, 2)
        # add a line if there was a row before
        if row >= 0:
            row += 1
            self.layout().addWidget(self.line_frame, row, 0, 1, columns * 2)
            self.line_frame.setHidden(False)
            offset = row + 1
        else:
            offset = 0
            self.line_frame.setHidden(True)

        positions = [
            (i // columns, i % columns) for i in range(len(self.config_widgets))
        ]
        row = 0
        for i, widge in enumerate(self.config_widgets):
            row, col = positions[i]
            if isinstance(widge, list):
                for j, widge in enumerate(widge):
                    self.layout().addWidget(widge, row + offset, 2 * col + j)
            else:
                self.layout().addWidget(widge, row + offset, 2 * col, 1, 2)
        self.layout().addItem(self.spacer, offset + row + 1, 0)

    def get_settings(self):
        """ """
        for name, widge in self.setting_checks.items():
            self.settings_dict[name] = widge.isChecked()
        for name, widge in self.setting_combos.items():
            self.settings_dict[name] = widge.currentText()
        for name, widge in self.setting_strings.items():
            self.settings_dict[name] = widge.text()
        for name, widge in self.setting_floats.items():
            try:
                self.settings_dict[name] = int(widge.text())
            except:
                self.settings_dict[name] = float(widge.text())
        return super().get_settings()

    def get_config(self):
        """ """
        for name, widge in self.config_checks.items():
            self.config_dict[name] = widge.isChecked()
        for name, widge in self.config_combos.items():
            self.config_dict[name] = widge.currentText()
        for name, widge in self.config_strings.items():
            self.config_dict[name] = widge.text()
        for name, widge in self.config_floats.items():
            try:
                self.config_dict[name] = int(widge.text())
            except:
                self.config_dict[name] = float(widge.text())
        return super().get_config()


def check_logged_in():
    if nomad_communication.token:
        return "NOMAD"
    if (
        extension_contexts.active_eln_context
        and extension_contexts.active_eln_context.extension_user
    ):
        return "ELN"
    return False


def add_tooltip_from_name(widgets, name, metadata_dict):
    if widgets and name in metadata_dict and metadata_dict[name]:
        for widge in widgets:
            widge.setToolTip(metadata_dict[name])
