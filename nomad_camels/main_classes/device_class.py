from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QComboBox,\
    QFrame, QCheckBox, QTextEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from ophyd import EpicsSignalRO
from ophyd import Device as OphydDevice
from ophyd.signal import SignalRO

from nomad_camels.main_classes.measurement_channel import Measurement_Channel


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

    def __init__(self, name='', virtual=False, tags=None, ophyd_device=None,
                 ophyd_class_name='', additional_info=None,
                 non_channel_functions=None, **kwargs):
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
        self.non_channel_functions = non_channel_functions or []
        self.ophyd_class_name = ophyd_class_name
        if ophyd_device is None:
            ophyd_device = OphydDevice
        # self.ophyd_device = ophyd_device
        self.ophyd_class = ophyd_device
        self.ophyd_instance = ophyd_device(name='test')
        self.get_channels()
        for comp in self.ophyd_instance.walk_components():
            name = comp.item.attr
            cls = comp.item.cls
            if name in self.ophyd_instance.configuration_attrs:
                if check_output(cls):
                    self.config.update({f'{name}': 0})
                else:
                    self.passive_config.update({f'{name}': 0})
        self.controls = {}

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
            funcs.append(f'{self.custom_name}.{func}')
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
        for chan_info in get_channels(self.ophyd_instance,
                                      include_metadata=True):
            chan, metadata = chan_info
            is_out = chan in outputs
            channel = Measurement_Channel(name=f'{self.custom_name}.{chan}',
                                          output=is_out,device=self.custom_name,
                                          metadata=metadata)
            self.channels.update({f'{self.custom_name}_{chan}': channel})
        return self.channels

    def get_additional_string(self):
        """returns a string that will be added into the protocol after
        connecting to the device.

        Returns
        -------
        additional_str : str
        """
        return ''

    def get_special_steps(self):
        """returns a dictionary containing containing device-specific
        loopsteps. The key is the loopstep's name, the value a list
        containing the Class of the step, and its config-widget.

        Returns
        -------
        steps : dict{'<step_name>': [Step_Class, Step_Config]}
        """
        return {}

def check_output(cls) -> bool:
    """Returns False if the give `cls` is an instance of a read-only Signal."""
    output = not issubclass(cls, EpicsSignalRO)
    output = output and not issubclass(cls, SignalRO)
    return output

def get_outputs(dev:OphydDevice):
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

def get_channels(dev:OphydDevice, include_metadata=False):
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
        if metadata is True, it will be a list of tuples conaining the channels'
        names and their metadata
    """
    channels = []
    for comp in dev.walk_components():
        name = comp.item.attr
        if name not in dev.configuration_attrs:
            if include_metadata:
                if hasattr(comp.item, 'kwargs') and 'metadata' in comp.item.kwargs:
                    metadata = comp.item.kwargs['metadata']
                else:
                    metadata = {}
                channels.append((name, metadata))
            else:
                channels.append(name)
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

    def __init__(self, parent=None, device_name='', data='', settings_dict=None,
                 config_dict=None, additional_info=None):
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

        label_title = QLabel(f'{device_name} - Configuration')
        title_font = QFont('MS Shell Dlg 2', 10)
        title_font.setWeight(QFont.Bold)
        label_title.setFont(title_font)

        self.label_custom_name = QLabel('Custom name:')
        self.lineEdit_custom_name = QLineEdit(data)

        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.textEdit_desc = QTextEdit(parent=self)
        self.textEdit_desc.setPlaceholderText('Enter your description here.')
        if additional_info and 'description' in additional_info:
            self.textEdit_desc.setText(additional_info['description'])

        self.label_connection = QLabel('Connection-type:')
        self.comboBox_connection_type = QComboBox()
        self.connector = Connection_Config()
        layout.addWidget(self.label_connection, 4, 0)
        layout.addWidget(self.comboBox_connection_type, 4, 1, 1, 2)
        layout.addWidget(self.connector, 6, 0, 1, 5)
        self.comboBox_connection_type.currentTextChanged.connect(self.connection_type_changed)

        layout.addWidget(label_title, 0, 0, 1, 5)
        layout.addWidget(self.label_custom_name, 1, 0)
        layout.addWidget(self.lineEdit_custom_name, 1, 1, 1, 2)
        layout.addWidget(self.textEdit_desc, 2, 0, 1, 5)
        layout.addWidget(self.line_2, 3, 0, 1, 5)

        self.settings_dict = settings_dict
        self.config_dict = config_dict
        self.additional_info = additional_info or {}
        self.lineEdit_custom_name.textChanged.connect(lambda x: self.name_change.emit(x))
        self.load_settings()


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
        if self.comboBox_connection_type.currentText() == 'Local VISA':
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
        self.settings_dict.update({'connection': {'type': self.comboBox_connection_type.currentText()}})
        self.settings_dict['connection'].update(self.connector.get_settings())
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
        self.additional_info['description'] = self.textEdit_desc.toPlainText()
        return self.additional_info


class Device_Config_Sub(QWidget):
    """ """
    def __init__(self, settings_dict=None, parent=None, config_dict=None):
        super().__init__()
        self.settings_dict = settings_dict or {}
        self.config_dict = config_dict or {}
        if settings_dict is None and config_dict is None:
            self.setLayout(QGridLayout())
            self.layout().addWidget(QLabel('Nothing to configure!'))

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


#
# class Prologix_Config(Connection_Config):
#     """Widget for the settings when the connection is via a Prologix
#     GPIB-Ethernet adapter.
#
#     Parameters
#     ----------
#
#     Returns
#     -------
#
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         layout = self.layout()
#         label_ip = QLabel('IP-Address:')
#         label_GPIB = QLabel('GPIB-Address:')
#         self.lineEdit_ip = QLineEdit()
#         self.lineEdit_GPIB = QLineEdit()
#         self.lineEdit_GPIB.textChanged.connect(self.connection_change.emit)
#         self.lineEdit_ip.textChanged.connect(self.connection_change.emit)
#
#         layout.addWidget(label_ip, 0, 0)
#         layout.addWidget(label_GPIB, 1, 0)
#         layout.addWidget(self.lineEdit_ip, 0, 1)
#         layout.addWidget(self.lineEdit_GPIB, 1, 1)
#
#     def get_settings(self):
#         """Returns the set IP-Address and GPIB-Address."""
#         return {'IP-Address': self.lineEdit_ip.text(),
#                 'GPIB-Address': self.lineEdit_GPIB.text()}
#
#     def load_settings(self, settings_dict):
#         """Loads the settings_dict, specifically the IP-Address and the
#         GPIB-Address.
#
#         Parameters
#         ----------
#         settings_dict :
#
#
#         Returns
#         -------
#
#         """
#         if 'IP-Address' in settings_dict:
#             self.lineEdit_ip.setText(settings_dict['IP-Address'])
#         if 'GPIB-Address' in settings_dict:
#             self.lineEdit_GPIB.setText(settings_dict['GPIB-Address'])
#
#
# class LAN_Config(Connection_Config):
#     """ """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         layout = self.layout()
#         label_ip = QLabel('IP-Address:')
#         self.lineEdit_ip = QLineEdit()
#         self.lineEdit_ip.textChanged.connect(self.connection_change.emit)
#
#         layout.addWidget(label_ip, 0, 0)
#         layout.addWidget(self.lineEdit_ip, 0, 1)
#
#     def get_settings(self):
#         """Returns the set IP-Address and GPIB-Address."""
#         return {'IP-Address': self.lineEdit_ip.text()}
#
#     def load_settings(self, settings_dict):
#         """Loads the settings_dict, specifically the IP-Address and the
#         GPIB-Address.
#
#         Parameters
#         ----------
#         settings_dict :
#
#
#         Returns
#         -------
#
#         """
#         if 'IP-Address' in settings_dict:
#             self.lineEdit_ip.setText(settings_dict['IP-Address'])
#


# class USB_Serial_Config(Connection_Config):
#     """ """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         label_port = QLabel('COM-Port:')
#         self.comboBox_port = QComboBox()
#         self.ports = get_ports()
#         self.comboBox_port.addItems(self.ports.keys())
#         self.comboBox_port.currentTextChanged.connect(self.change_desc)
#
#         self.label_desc = QLabel()
#         self.label_desc.setEnabled(False)
#         self.label_hwid = QLabel()
#         self.label_hwid.setEnabled(False)
#
#         self.layout().addWidget(label_port, 0, 0)
#         self.layout().addWidget(self.comboBox_port, 0, 1, 1, 4)
#         self.layout().addWidget(self.label_desc, 1, 0, 1, 2)
#         self.layout().addWidget(self.label_hwid, 1, 2, 1, 3)
#         self.change_desc()
#
#     def change_desc(self):
#         """ """
#         port = self.comboBox_port.currentText()
#         desc = self.ports[port]['description']
#         hwid = self.ports[port]['hardware']
#         self.label_desc.setText(desc)
#         self.label_hwid.setText(hwid)
#
#     def get_settings(self):
#         """ """
#         return {'Port': self.comboBox_port.currentText()}
#
#     def load_settings(self, settings_dict):
#         """
#
#         Parameters
#         ----------
#         settings_dict :
#
#
#         Returns
#         -------
#
#         """
#         if 'Port' in settings_dict and settings_dict['Port'] in self.ports.keys():
#             self.comboBox_port.setCurrentText(settings_dict['Port'])



class Local_VISA(Connection_Config):
    """ """
    def __init__(self, parent=None):
        super().__init__(parent)
        label_port = QLabel('Resource-Name:')
        self.comboBox_port = QComboBox()
        import pyvisa
        rm = pyvisa.ResourceManager()
        self.ports = rm.list_resources()
        self.comboBox_port.addItems(self.ports)

        self.layout().addWidget(label_port, 0, 0)
        self.layout().addWidget(self.comboBox_port, 0, 1, 1, 4)

        label_baud = QLabel('Baud-Rate:')
        self.lineEdit_baud = QLineEdit('9600')
        self.layout().addWidget(label_baud, 1, 0)
        self.layout().addWidget(self.lineEdit_baud, 1, 1)

        label_timeout = QLabel('Timeout (ms):')
        self.lineEdit_timeout = QLineEdit('2000')
        self.layout().addWidget(label_timeout, 1, 2)
        self.layout().addWidget(self.lineEdit_timeout, 1, 3)

        label_in_term = QLabel('In-Terminator:')
        self.lineEdit_in_term = QLineEdit('\\r\\n')
        self.layout().addWidget(label_in_term, 2, 0)
        self.layout().addWidget(self.lineEdit_in_term, 2, 1)

        label_out_term = QLabel('Out-Terminator:')
        self.lineEdit_out_term = QLineEdit('\\r\\n')
        self.layout().addWidget(label_out_term, 2, 2)
        self.layout().addWidget(self.lineEdit_out_term, 2, 3)

        label_error_retry = QLabel('Retries on error:')
        self.lineEdit_error_retry = QLineEdit('0')
        self.layout().addWidget(label_error_retry, 3, 0)
        self.layout().addWidget(self.lineEdit_error_retry, 3, 1, 1, 3)

    def get_settings(self):
        """ """
        return {'resource_name': self.comboBox_port.currentText(),
                'baud_rate': int(self.lineEdit_baud.text()),
                'timeout': int(self.lineEdit_timeout.text()),
                'read_termination': self.lineEdit_in_term.text().replace('\\r', '\r').replace('\\n', '\n'),
                'write_termination': self.lineEdit_out_term.text().replace('\\r', '\r').replace('\\n', '\n'),
                'retry_on_error': int(self.lineEdit_error_retry.text())}

    def load_settings(self, settings_dict):
        """

        Parameters
        ----------
        settings_dict :
            

        Returns
        -------

        """
        if 'connection' in settings_dict:
            settings_dict = settings_dict['connection']
        if 'resource_name' in settings_dict and settings_dict['resource_name'] in self.ports:
            self.comboBox_port.setCurrentText(settings_dict['resource_name'])
        if 'baud_rate' in settings_dict:
            self.lineEdit_baud.setText(str(settings_dict['baud_rate']))
        if 'timeout' in settings_dict:
            self.lineEdit_timeout.setText(str(settings_dict['timeout']))
        if 'read_termination' in settings_dict:
            self.lineEdit_in_term.setText(settings_dict['read_termination'].replace('\r', '\\r').replace('\n', '\\n'))
        if 'write_termination' in settings_dict:
            self.lineEdit_out_term.setText(settings_dict['write_termination'].replace('\r', '\\r').replace('\n', '\\n'))
        if 'retry_on_error' in settings_dict:
            self.lineEdit_error_retry.setText(str(settings_dict['retry_on_error']))



class Simple_Config(Device_Config):
    """ """
    def __init__(self, parent=None, device_name='', data='', settings_dict=None,
                 config_dict=None, additional_info=None,
                 comboBoxes=None, config_types=None, labels=None):
        super().__init__(parent, device_name=device_name, data=data,
                         settings_dict=settings_dict,
                         config_dict=config_dict,
                         additional_info=additional_info)
        self.sub_widget = Simple_Config_Sub(settings_dict=settings_dict,
                                            parent=self,
                                            config_dict=config_dict,
                                            comboBoxes=comboBoxes,
                                            config_types=config_types,
                                            labels=labels)
        self.layout().addWidget(self.sub_widget, 10, 0, 1, 5)
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
    def __init__(self, settings_dict=None, parent=None, config_dict=None,
                 comboBoxes=None, config_types=None, labels=None):
        super().__init__(settings_dict=settings_dict, parent=parent,
                         config_dict=config_dict)
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0,0,0,0)
        comboBoxes = comboBoxes or {}
        config_types = config_types or {}
        labels = labels or {}
        self.setting_checks = {}
        self.setting_floats = {}
        self.setting_strings = {}
        self.setting_combos = {}
        labels = labels or {}
        for name, val in settings_dict.items():
            if name == 'connection':
                continue
            if name in comboBoxes:
                self.setting_combos[name] = QComboBox()
                self.setting_combos[name].addItems(comboBoxes[name])
                self.setting_combos[name].setCurrentText(val)
            elif name in config_types:
                if config_types[name] == 'bool':
                    self.setting_checks[name] = QCheckBox(labels[name] if name in labels else name)
                    if isinstance(val, bool):
                        self.setting_checks[name].setChecked(val)
                elif config_types[name] == 'float':
                    self.setting_floats[name] = QLineEdit(str(val))
                elif config_types[name] == 'str':
                    self.setting_strings[name] = QLineEdit(str(val))
                else:
                    raise Exception(f'Named config_type {config_types[name]} of {name} is not supported in Simple_Device_Config!')
            elif isinstance(val, bool):
                self.setting_checks[name] = QCheckBox(labels[name] if name in labels else name)
                self.setting_checks[name].setChecked(val)
            elif isinstance(val, float) or isinstance(val, int):
                self.setting_floats[name] = QLineEdit(str(val))
            elif isinstance(val, str):
                self.setting_strings[name] = QLineEdit(val)
            else:
                raise Exception(f'Type of {name} with value {val} not supported for simple device config!')
        self.config_checks = {}
        self.config_floats = {}
        self.config_strings = {}
        self.config_combos = {}
        for name, val in config_dict.items():
            if name in comboBoxes:
                self.config_combos[name] = QComboBox()
                self.config_combos[name].addItems(comboBoxes[name])
                self.config_combos[name].setCurrentText(val)
            elif name in config_types:
                if config_types[name] == 'bool':
                    self.config_checks[name] = QCheckBox(labels[name] if name in labels else name)
                    if isinstance(val, bool):
                        self.config_checks[name].setChecked(val)
                elif config_types[name] == 'float':
                    self.config_floats[name] = QLineEdit(str(val))
                elif config_types[name] == 'str':
                    self.config_strings[name] = QLineEdit(str(val))
                else:
                    raise Exception(f'Named config_type {config_types[name]} of {name} is not supported in Simple_Device_Config!')
            elif isinstance(val, bool):
                self.config_checks[name] = QCheckBox(labels[name] if name in labels else name)
                self.config_checks[name].setChecked(val)
            elif isinstance(val, float) or isinstance(val, int):
                self.config_floats[name] = QLineEdit(str(val))
            elif isinstance(val, str):
                self.config_strings[name] = QLineEdit(val)
            else:
                raise Exception(f'Type of {name} with value {val} not supported for simple device config!')

        col = 0
        row = 0
        for name, widge in self.setting_checks.items():
            self.layout().addWidget(widge, row, col, 1, 2)
            col += 2
            if col == 4:
                col = 0
                row += 1
        for name, widge in self.setting_floats.items():
            if name in labels:
                self.layout().addWidget(QLabel(labels[name]), row, col)
            else:
                self.layout().addWidget(QLabel(name), row, col)

            self.layout().addWidget(widge, row, col+1)
            col += 2
            if col == 4:
                col = 0
                row += 1
        for name, widge in self.setting_strings.items():
            if name in labels:
                self.layout().addWidget(QLabel(labels[name]), row, col)
            else:
                self.layout().addWidget(QLabel(name), row, col)

            self.layout().addWidget(widge, row, col+1)
            col += 2
            if col == 4:
                col = 0
                row += 1
        for name, widge in self.setting_combos.items():
            if name in labels:
                self.layout().addWidget(QLabel(labels[name]), row, col)
            else:
                self.layout().addWidget(QLabel(name), row, col)
            self.layout().addWidget(widge, row, col+1)
            col += 2
            if col == 4:
                col = 0
                row += 1
        for name, widge in self.config_checks.items():
            self.layout().addWidget(widge, row, col, 1, 2)
            col += 2
            if col == 4:
                col = 0
                row += 1
        for name, widge in self.config_floats.items():
            if name in labels:
                self.layout().addWidget(QLabel(labels[name]), row, col)
            else:
                self.layout().addWidget(QLabel(name), row, col)
            self.layout().addWidget(widge, row, col+1)
            col += 2
            if col == 4:
                col = 0
                row += 1
        for name, widge in self.config_strings.items():
            if name in labels:
                self.layout().addWidget(QLabel(labels[name]), row, col)
            else:
                self.layout().addWidget(QLabel(name), row, col)
            self.layout().addWidget(widge, row, col+1)
            col += 2
            if col == 4:
                col = 0
                row += 1
        for name, widge in self.config_combos.items():
            if name in labels:
                self.layout().addWidget(QLabel(labels[name]), row, col)
            else:
                self.layout().addWidget(QLabel(name), row, col)
            self.layout().addWidget(widge, row, col+1)
            col += 2
            if col == 4:
                col = 0
                row += 1

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






#
# def get_ports():
#     """ """
#     import serial.tools.list_ports
#     ports = serial.tools.list_ports.comports()
#     port_dict = {}
#     for port, desc, hwid in sorted(ports):
#         port_dict[port] = {'description': desc, 'hardware': hwid}
#     return port_dict
#
