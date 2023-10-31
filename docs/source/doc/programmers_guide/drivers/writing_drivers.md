# Writing New Instrument Drivers
There are two flavors of instrument drivers:

1. Drivers written only for your own use that are stored locally.
2. Drivers written for the entire CAMELS community that are made available through PyPi.

For the entire community to benefit, it's best to create a new [PyPi](https://pypi.org/) package for each instrument driver you write for CAMELS. It's not mandatory, but it helps make our project more accessible and useful for others as it is community-driven and open source.

The source code for existing drivers can be found in [this repository](https://github.com/FAU-LAP/CAMELS_drivers) on our GitHub.

The basic steps for creating both flavors of drivers are the same.


## 1. VISA-driver builder - Creating the core structure
The easiest way to create a new instrument driver for any kind of instrument is to open `CAMELS` and navigate to `Tools > VISA-driver builder`.

### 1.1. Basic Driver Settings
At the top enter the `Name` of the instrument, this should be lowercase and describe the instrument unambiguously. For example `keithley_2400`.\
Then enter the `Ophyd-Class-Name`. Best-practice is to have it be slightly different from `Name` and uppercase for the first letter of the Ophyd-Class-Name. For example `Keithley_2400`. 

If you communicate with the instrument via a **serial connection** enter the correct baud rate and read and write terminators. This is of course not relevant, if you communicate with the device via other ways such as .dlls, sockets, or ethernet connections. 

### 1.2. Instrument Channels
You now have the option to add four different types of channels to your instrument.
Channels are the core functionality of your instrument. Channels can be thought of like methods of a class that can be called to perform various tasks.

* `Read Channels`: Communicate with the instrument and read/return the value/data that you wish to save in to your measurement data. This channel type is used for values that can only be read from the instrument, e.g. a measured resistance.  They can be used in **measurements protocols** by using a `Read Channels` step.\
If you for example have a simple instrument that returns a voltage measurement when you send `VOLT?` to the device you would simply enter `VOLT?` in to the `Query-String` field. 
* `Set Channels`: These channels can set/output a value defined by the user, e.g. a voltage. These channels communicate with the instruments and write to the instrument and it is assumed that the state of instrument is modified in some way. If no return parser is set the message is simply written and nothing is read from the instrument. They can be used in measurements protocols by using a `Set Channels` step. In most cases it is not assumed that a `Set Channel` would return/save any data/information from the instrument. 

`Read Channels` and `Set Channels` can be used in measurement protocols (or manual controls) to read and set instruments. They are only executed when explicitly called in a protocol.

* `Config Channels - Read Only`: These may be used for values that are read only once from the instrument at the beginning of the measurement, but do not change its current state, e.g. the instrument identifier, as response from the `*IDN?` command.\

* `Config Channels`: These values are set at the beginning of a protocol and are configured in the instrument management (`Manage Instruments` window). These should be values, that are normally not changed, like the current and voltage compliance, exposure time or whether the instrument is used as a voltage or current source.

&#9888; Config Channels are **always** run once at the beginning of a measurement when the instrument is used. 
You can change instrument config channels during measurements, but the idea behind configs are settings that do not change within a single measurement. The value of the config channels are saved as metadata to the instrument at the beginning of the measurement. So take care when changing this during the measurement.


These four channels have several fields that you can fill out while creating your driver.

* **Name:** This will be the name of the channel, as it is also displayed in CAMELS.
* **Query-String: (Only for Read Channels)** The string sent to the instrument for querying some value (Input only, examples: `*IDN?`, `VOLT?`). This is useful for query commands that do not change.
* **Write-Format-String: (Only for Set Channels)** A string that formats the input value so that the instrument understands the set command. The value (that you entered in the measurement protocol) is passed to the string with `{value}`, i.e. for example: `"VOLT {value}"` where "{value}" will be replaced with the input value. So in the end if you set the value in the protocol to `1` the string that the instrument receives would be for example `"VOLT 1"`.
* **Return-Parser:** A regular expression which parses the string returned from the instrument. The regex must contain a capture group, so parenthesis around the value you want to extract. The first capture group from the regex will become the value. The actual code executed looks like this `re.match(parse, val).group(1)`, where `parse` is the regex string and `val` is the initial string read from the instrument.\
If this is `None`, for a set-channel, the instrument will only be written to, if it is not `None` a query is performed.

* **Return-Type:** The type to which the returned value from the "Return-Parser" should be converted. Supported are `str`, `float`, `int` and `bool`.
* **Unit:** The physical unit of the channel's measurement / output.
* **Description:** A description for the channel, making it clear in the metadata and for the user, what this channel does.
* **Input-Type:** This determines the input for a config-channel in the config window. Supporter are `str`, `float` (or any number-type) and `bool`.

When you are finished click `Build Driver` and select a folder where you want to save the driver.

This will automatically create the basic folder structure required to use the driver in CAMELS.

## 2. Folder structure
The basic folder structure for drivers is quite simple. For an instrument named `driver_name` it looks as follows.
```
nomad_camels_driver_<driver_name> (contains the actual device communication files)
└─> <driver_name>.py
└─> <driver_name>_ophyd.py
```
The `<driver_name>.py` file contains code regarding the configuration settings you find in the `Manage Instruments` window and sets up the instrument.

The `<driver_name>_ophyd.py` file contains code that describes how exactly you communicate with the instrument and defines the available channels. This file contains all commands that are sent to the instrument and specifies how the read data is treated.

# Drivers for PyPi
If you want to share your driver with others, all you have to do is create a PyPi package out of the folder you created above. 

You can ofcourse also fork our [driver repository](https://github.com/FAU-LAP/CAMELS_drivers) and create a pull request with the new driver you wrote and we will be happy to add your driver to PyPi for you. 
Or you can also send us 
To do this the driver should have the following folder structure:
```
<driver_name>
└─> dist (this is automatically created by python -m build)
    └─> nomad_camels_driver_<driver_name>-X.Y.Z.tar.gz
    └─> nomad_camels_driver_<driver_name>-X.Y.Z-py3-none-any.whl
└─> nomad_camels_driver_<driver_name> (contains the actual device communication files)
    └─> <driver_name>.py
    └─> <driver_name>_ophyd.py
└─> LICENSE.txt
└─> pyproject.toml
└─> README.md
```

The `pyproject.toml` file contains most of the relevant information concerning the package that will be uploaded to PyPi (see the [setuptools page](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)).

&#9888; Most importantly the project name and version must be set in the `pyproject.toml` file.


---

Here is an exemplary .toml file:

<details>
  <summary>Code example: pyproject.toml file for the  Keithley 237</summary>

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "nomad_camels_driver_keithley_237"
version = "0.1.4"
authors = [
    { name="FAIRmat - HU Berlin", email="nomad-camels@fau.de" }
]
description = "Instrument driver for the Keithley 237 SMU."
readme = "README.md"
requires-python = ">=3.9.6"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    "Operating System :: Microsoft :: Windows",
]
dependencies = [
    "pyvisa",
    "pyvisa-py"
]
[project.urls]
"GitHub Page" = "https://github.com/FAU-LAP/NOMAD-CAMELS"
"Documentation" = "https://fau-lap.github.io/NOMAD-CAMELS/"
```

</details>

---

(python_files)=
## 2. Python files
The `<driver_name>.py` file contains information about the possible instrument configurations and settings. This can be for example the current compliance of a voltage source or the integration time of a digital multimeter.

> &#9888; There is an inherent difference with how CAMELS treats "config" and "settings". The "config" is provided by the instrument's ophyd class similar to channels (see [below](write_ophyd_file)). The "settings" are handed to the instrument's `__init__`. Using the protocol-step "Change-Device-Config", only "config" can be changed. This step works with either providing a class `subclass_config_sub` in the driver or when the main `subclass_config` has an attribute `sub_widget` (as is the case for `Simple_Config`, see next section).


### 2.1 Simple Configurations
For **simple instruments** with only a **few settings** you do not need to write your own GUI for the settings but CAMELS can auto-generate the UI for you. \
An example file is displayed below:

---

<details>
  <summary>Code example: Use the auto-generated UI for instrument settings (for Keithley 237)</summary>

```python
from nomad_camels_driver_keithley_237.keithley_237_ophyd import Keithley_237 # Change this line!
from nomad_camels.main_classes import device_class

class subclass(device_class.Device):
    def __init__(self, **kwargs):
        # You can search for individual tags in the NOMAD-CAMELS GUI
        super().__init__(name='keithley_237', virtual=False, tags=['DMM', 'voltage', 'current',],       
                         directory='keithley_237', ophyd_device=Keithley_237, 
                         ophyd_class_name='Keithley_237', **kwargs)
        # These are the default values of the configuration settings  
        self.config['Four_wire'] = False
        self.config['Averages'] = "1"
        self.config['Integration_time'] = "20ms"
        self.config['Current_compliance_range'] = "Auto"
        self.config['Current_compliance'] = 1e-6
        self.config['Voltage_compliance_range'] = "Auto"
        self.config['Voltage_compliance'] = 10
        self.config['Bias_delay'] = 0
        self.config['Source_Type'] = "Voltage"
        self.config['Sweep_Hysteresis'] = False

"""This adds a simple GUI of the configuration settings that you add below. 
This way you do NOT need to write our own GUI for the instrument settings.
This can be used for simple instruments with only a few settings.
For more complicated instruments (with e.g. multiple channels) it might be necessary to write a more advanced GUI"""
class subclass_config(device_class.Simple_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        # Each dictionary entry become a combo box with the values ad drop down optins
        comboBoxes = {'Source_Type': ["Voltage", "Current", "Sweep Voltage", "Sweep Current"],
                      'Current_compliance_range': ["Auto", "1nA", "10nA", "100nA", "1uA",
                                             "10uA", "100uA", "1mA", "10mA", "100mA"],
                      'Voltage_compliance_range': ["Auto", "1.1V", "11V", "110V", "1100V"],
                      "Averages": ["1", "2", "4", "8", "16", "32"],
                      'Integration_time': ["20ms", "4ms", "0.4ms"],
                      }
        # Creates text fields in to which the user can write. 
        # It knows what type of field (bool, number, ...) it is from the default value above.
        labels = {'Source_Type': 'Source type',
                  'Current_compliance_range': 'Compliance range (A)',
                  'Voltage_compliance_range': 'Compliance range (V)',
                  'Integration_time': 'Integration time',
                  'Four_wire': 'Four wire',
                  'Current_compliance': 'Current compliance',
                  'Voltage_compliance': 'Voltage compliance',
                  'Bias_delay': 'Bias delay',
                  'Sweep_Hysteresis': 'Sweep Hysteresis',
                  }
        super().__init__(parent, 'Keithley 237', data, settings_dict,
                         config_dict, ioc_dict, additional_info, comboBoxes=comboBoxes, labels=labels)
        self.comboBox_connection_type.addItem('Local VISA')
        self.load_settings()
```

</details>

---

### 2.2 Complex Configurations
If the instrument is more complex CAMELS can not auto generate the UI anymore. Here you need to write your own UI using for example QT Designer. The first three class definitions are relevant for this.

---

<details>
  <summary>Code example: Use your own UI file to create settings for your instrument (for Andor Shamrock spectrograph)</summary>


```python
from CAMELS.main_classes import device_class
from .andor_shamrock_500_config import Ui_andor_shamrock500_config
from .andor_shamrock_500_ophyd import Andor_Shamrock_500
from PySide6.QtWidgets import QTabWidget


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='andor_shamrock_500', virtual=False,
                         tags=[ 'spectrometer', 'spectrum', 'Andor',],
                         directory='andor_shamrock_500', ophyd_device=Andor_Shamrock_500,
                         ophyd_class_name='Andor_Shamrock_500', **kwargs)

class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, config_dict=None, additional_info=None, **kwargs):
        super().__init__(parent, 'Andor Shamrock 500', data, settings_dict=settings_dict, config_dict=config_dict, additional_info=additional_info, no_ioc_connection=True, **kwargs)
        self.comboBox_connection_type.addItem('Windows dll')
        # self.comboBox_connection_type.addItem('Local VISA')
        self.tab_widget = QTabWidget()
        conf1 = {}
        for key, val in config_dict.items():
            if key.endswith('1'):
                conf1[key[:-1]] = val
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Here you add your own UI as a tab widget. This is the key part !!!!!  
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.channel_widge_1 = subclass_config_sub(config_dict=conf1, parent=parent, settings_dict=settings_dict)
        self.tab_widget.addTab(self.channel_widge_1, 'Settings')
        self.layout().addWidget(self.tab_widget, 20, 0, 1, 5)
        self.load_settings()

    def get_config(self):
        conf1 = self.channel_widge_1.get_config()
        for key, val in conf1.items():
            self.config_dict[f'{key}1'] = val
        return super().get_config()

"""This inherits from your UI and is used above to create the tab widget with all the settings you implemented."""
class subclass_config_sub(device_class.Device_Config_Sub, Ui_andor_shamrock500_config):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(parent=parent, config_dict=config_dict,
                         settings_dict=settings_dict)
        self.setupUi(self)
        if 'set_grating_number' in self.config_dict:
            self.set_grating_number.setValue(self.config_dict['set_grating_number'])
        if 'initial_wavelength' in self.config_dict:
            self.initial_wavelength.setValue(self.config_dict['initial_wavelength'])
        if 'input_port' in self.config_dict:
            self.input_port.setCurrentText(self.config_dict['input_port'])
        if 'output_port' in self.config_dict:
            self.output_port.setCurrentText(self.config_dict['output_port'])
        if 'select_camera' in self.config_dict:
            self.select_camera.setCurrentText(self.config_dict['select_camera'])
        if 'input_slit_size' in self.config_dict:
            self.input_slit_size.setValue(self.config_dict['input_slit_size'])
        if 'output_slit_size' in self.config_dict:
            self.output_slit_size.setValue(self.config_dict['output_slit_size'])

    def get_config(self):
        self.config_dict['set_grating_number'] = self.set_grating_number.value()
        self.config_dict['initial_wavelength'] = self.initial_wavelength.value()
        self.config_dict['input_port'] = self.input_port.currentText()
        self.config_dict['output_port'] = self.output_port.currentText()
        self.config_dict['select_camera'] = self.select_camera.currentText()
        self.config_dict['input_slit_size'] = self.input_slit_size.value()
        self.config_dict['output_slit_size'] = self.output_slit_size.value()
        return super().get_config()
```

</details>

---

Here is a more complex example which creates settings for two channels of a single instrument.
<details>
  <summary>Code example: Two separate channels (for Keysight 2912)</summary>

```python
from nomad_camels.main_classes import device_class
from keysight_b2912.keysight_b2912_channel_config import Ui_B2912_channel # You need to import the created UI file
from keysight_b2912.keysight_b2912_ophyd import Keysight_B2912 # Import the actual device communication
from PySide6.QtWidgets import QTabWidget

"""Default settings of the instrument"""
default_settings = {'source': 'Voltage',
                    'source_range': '2E-1 V',
                    'range_lower_lim': '2E-1 V',
                    'source_auto': True,
                    'low_terminal': 'Ground',
                    'current_auto_mode': True,
                    'current_lower_lim': '1E-8 A',
                    'current_range': '1E-8 A',
                    'voltage_range': '2E-1 V',
                    'voltage_auto_mode': True,
                    'voltage_lower_lim': '2E-1 V',
                    'resistance_range': '2 Ohm',
                    'resistance_upper_lim': '200E6 Ohm',
                    'output_protection': False,
                    'four_wire_meas': False,
                    'current_auto_range': True,
                    'voltage_auto_range': True,
                    'resistance_auto_range': True,
                    'resistance_compensation': False,
                    'voltage_compliance': 2,
                    'current_compliance': 2,
                    'NPLC': 1}

"""Similar to the simple device"""
class subclass(device_class.Device):
    def __init__(self, **kwargs):
        super().__init__(name='keysight_b2912', virtual=False, tags=['SMU', 'voltage', 'current', 'resistance'], directory='keysight_b2912', ophyd_device=Keysight_B2912, ophyd_class_name='Keysight_B2912', **kwargs)
        # This sets the default settings for each channel
        for key, val in default_settings.items():
            self.config[f'{key}1'] = val
            self.config[f'{key}2'] = val

class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None, config_dict=None, additional_info=None, **kwargs):
        super().__init__(parent, 'Keysight B2912', data, settings_dict=settings_dict, config_dict=config_dict, additional_info=additional_info, no_ioc_connection=True, **kwargs)
        self.comboBox_connection_type.addItem('Local VISA')
        self.tab_widget = QTabWidget()
        conf1 = {}
        conf2 = {}
        for key, val in config_dict.items():
            if key.endswith('1'):
                conf1[key[:-1]] = val
            elif key.endswith('2'):
                conf2[key[:-1]] = val
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Here you add your own UI as a tab widget. This is the key part !!!!!  
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.channel_widge_1 = subclass_config_sub(config_dict=conf1, parent=parent, settings_dict=settings_dict)
        self.channel_widge_2 = subclass_config_sub(config_dict=conf2, parent=parent, settings_dict=settings_dict)
        self.tab_widget.addTab(self.channel_widge_1, 'Channel 1')
        self.tab_widget.addTab(self.channel_widge_2, 'Channel 2')
        self.layout().addWidget(self.tab_widget, 20, 0, 1, 5)
        self.load_settings()

    def get_config(self):
        conf1 = self.channel_widge_1.get_config()
        conf2 = self.channel_widge_2.get_config()
        for key, val in conf1.items():
            self.config_dict[f'{key}1'] = val
        for key, val in conf2.items():
            self.config_dict[f'{key}2'] = val
        return super().get_config()

"""This inherits from the UI class you wrote for the UI config settings of the instrument"""
class subclass_config_sub(device_class.Device_Config_Sub, Ui_B2912_channel):
    def __init__(self, config_dict=None, parent=None, settings_dict=None):
        super().__init__(parent=parent, config_dict=config_dict,
                         settings_dict=settings_dict)
        self.setupUi(self)

        self.sources = ['Voltage', 'Current']
        self.comboBox_source.addItems(self.sources)
        if 'source' in config_dict and config_dict['source'] in self.sources:
            self.comboBox_source.setCurrentText(config_dict['source'])

        self.low_terminals = ['Ground', 'Float']
        self.comboBox_low_terminal.addItems(self.low_terminals)
        if 'low_terminal' in config_dict and config_dict['low_terminal'] in self.low_terminals:
            self.comboBox_low_terminal.setCurrentText(config_dict['source'])

        self.ranges_voltage = ['2E-1 V', '2 V', '20 V', '200 V']
        self.ranges_current = ['1E-8 A', '1E-7 A', '1E-6 A', '1E-5 A', '1E-4 A', '1E-3 A', '1E-2 A', '1E-1 A', '1 A', '1.5 A', '3 A', '10 A']
        self.ranges_resistance = ['2 Ohm', '20 Ohm', '200 Ohm', '2E3 Ohm', '20E3 Ohm', '200E3 Ohm', '2E6 Ohm', '20E6 Ohm', '200E6 Ohm']

        if 'source_auto' in self.config_dict:
            self.checkBox_source_auto.setChecked(self.config_dict['source_auto'])
        else:
            self.checkBox_source_auto.setChecked(True)

        self.load_source_options()
        self.checkBox_source_auto.clicked.connect(self.load_source_options)
        self.comboBox_source.currentTextChanged.connect(self.load_source_options)

        if 'output_protection' in config_dict:
            self.checkBox_output_protection.setChecked(config_dict['output_protection'])
        if 'current_compliance' in config_dict:
            self.lineEdit_current_compliance.setText(str(config_dict['current_compliance']))
        else:
            self.lineEdit_current_compliance.setText('0.1')
        if 'voltage_compliance' in config_dict:
            self.lineEdit_voltage_compliance.setText(str(config_dict['voltage_compliance']))
        else:
            self.lineEdit_voltage_compliance.setText('2')

        if 'NPLC' in config_dict:
            self.lineEdit_NPLC.setText(str(config_dict['NPLC']))
        else:
            self.lineEdit_NPLC.setText('1')

        if 'four_wire_meas' in config_dict:
            self.checkBox_four_wire_meas.setChecked(config_dict['four_wire_meas'])
        if 'current_auto_range' in config_dict:
            self.checkBox_current_auto_range.setChecked(config_dict['current_auto_range'])
        if 'voltage_auto_range' in config_dict:
            self.checkBox_voltage_auto_range.setChecked(config_dict['voltage_auto_range'])
        if 'resistance_auto_range' in config_dict:
            self.checkBox_resistance_auto_range.setChecked(config_dict['resistance_auto_range'])
        if 'resistance_compensation' in config_dict:
            self.checkBox_resistance_compensation.setChecked(config_dict['resistance_compensation'])

        auto_range_modes = ['Normal', 'Resolution', 'Speed']
        self.comboBox_voltage_auto_mode.addItems(auto_range_modes)
        self.comboBox_current_auto_mode.addItems(auto_range_modes)
        if 'voltage_auto_mode' in config_dict and config_dict['voltage_auto_mode'] in auto_range_modes:
            self.comboBox_voltage_auto_mode.setCurrentText(config_dict['voltage_auto_mode'])
        if 'current_auto_mode' in config_dict and config_dict['current_auto_mode'] in auto_range_modes:
            self.comboBox_current_auto_mode.setCurrentText(config_dict['current_auto_mode'])

        self.comboBox_current_lower_lim.addItems(self.ranges_current)
        if 'current_lower_lim' in self.config_dict and self.config_dict['current_lower_lim'] in self.ranges_current:
            self.comboBox_current_lower_lim.setCurrentText(self.config_dict['current_lower_lim'])
        self.comboBox_current_range.addItems(self.ranges_current)
        if 'current_range' in self.config_dict and self.config_dict['current_range'] in self.ranges_current:
            self.comboBox_current_range.setCurrentText(self.config_dict['current_range'])
        self.comboBox_voltage_lower_lim.addItems(self.ranges_voltage)
        if 'voltage_lower_lim' in self.config_dict and self.config_dict['voltage_lower_lim'] in self.ranges_voltage:
            self.comboBox_voltage_lower_lim.setCurrentText(self.config_dict['voltage_lower_lim'])
        self.comboBox_voltage_range.addItems(self.ranges_voltage)
        if 'voltage_range' in self.config_dict and self.config_dict['voltage_range'] in self.ranges_voltage:
            self.comboBox_voltage_range.setCurrentText(self.config_dict['voltage_range'])
        self.comboBox_resistance_range.addItems(self.ranges_resistance)
        if 'resistance_range' in self.config_dict and self.config_dict['resistance_range'] in self.ranges_resistance:
            self.comboBox_resistance_range.setCurrentText(self.config_dict['resistance_range'])
        self.comboBox_resistance_upper_lim.addItems(self.ranges_resistance)
        if 'resistance_upper_lim' in self.config_dict and self.config_dict['resistance_upper_lim'] in self.ranges_resistance:
            self.comboBox_resistance_upper_lim.setCurrentText(self.config_dict['resistance_upper_lim'])


    def load_source_options(self):
        src_v = True
        if self.comboBox_source.currentText() == 'Current':
            src_v = False
        auto_source = self.checkBox_source_auto.isChecked()
        self.comboBox_source_range.clear()
        self.comboBox_range_lower_lim.clear()
        if src_v:
            self.comboBox_source_range.addItems(self.ranges_voltage)
            self.comboBox_range_lower_lim.addItems(self.ranges_voltage)
            if 'source_range' in self.config_dict and self.config_dict['source_range'] in self.ranges_voltage:
                self.comboBox_source_range.setCurrentText(self.config_dict['source_range'])
            if 'range_lower_lim' in self.config_dict and self.config_dict['range_lower_lim'] in self.ranges_voltage:
                self.comboBox_range_lower_lim.setCurrentText(self.config_dict['range_lower_lim'])
        else:
            self.comboBox_source_range.addItems(self.ranges_current)
            self.comboBox_range_lower_lim.addItems(self.ranges_current)
            if 'source_range' in self.config_dict and self.config_dict['source_range'] in self.ranges_current:
                self.comboBox_source_range.setCurrentText(self.config_dict['source_range'])
            if 'range_lower_lim' in self.config_dict and self.config_dict['range_lower_lim'] in self.ranges_current:
                self.comboBox_range_lower_lim.setCurrentText(self.config_dict['range_lower_lim'])
        self.comboBox_source_range.setEnabled(not auto_source)
        self.comboBox_range_lower_lim.setEnabled(auto_source)


    def get_config(self):
        self.config_dict['source'] = self.comboBox_source.currentText()
        self.config_dict['low_terminal'] = self.comboBox_low_terminal.currentText()
        self.config_dict['source_range'] = self.comboBox_source_range.currentText()
        self.config_dict['range_lower_lim'] = self.comboBox_range_lower_lim.currentText()
        self.config_dict['current_auto_mode'] = self.comboBox_current_auto_mode.currentText()
        self.config_dict['current_lower_lim'] = self.comboBox_current_lower_lim.currentText()
        self.config_dict['current_range'] = self.comboBox_current_range.currentText()
        self.config_dict['voltage_range'] = self.comboBox_voltage_range.currentText()
        self.config_dict['voltage_auto_mode'] = self.comboBox_voltage_auto_mode.currentText()
        self.config_dict['voltage_lower_lim'] = self.comboBox_voltage_lower_lim.currentText()
        self.config_dict['resistance_range'] = self.comboBox_resistance_range.currentText()
        self.config_dict['resistance_upper_lim'] = self.comboBox_resistance_upper_lim.currentText()
        self.config_dict['source_auto'] = self.checkBox_source_auto.isChecked()
        self.config_dict['output_protection'] = self.checkBox_output_protection.isChecked()
        self.config_dict['four_wire_meas'] = self.checkBox_four_wire_meas.isChecked()
        self.config_dict['current_auto_range'] = self.checkBox_current_auto_range.isChecked()
        self.config_dict['voltage_auto_range'] = self.checkBox_voltage_auto_range.isChecked()
        self.config_dict['resistance_auto_range'] = self.checkBox_resistance_auto_range.isChecked()
        self.config_dict['resistance_compensation'] = self.checkBox_resistance_compensation.isChecked()
        self.config_dict['current_compliance'] = float(self.lineEdit_current_compliance.text())
        self.config_dict['voltage_compliance'] = float(self.lineEdit_voltage_compliance.text())
        self.config_dict['NPLC'] = float(self.lineEdit_NPLC.text())
        return super().get_config()

```

</details>

---
(write_ophyd_file)=
### 2.3 Ophyd File
The `<driver_name>_ophyd.py` file should contain a class inheriting from ophyd.Device (or one of its subclasses).
Each component with `kind='normal'` or `'hinted'` (or unspecified) of the defined device will appear as a channel in CAMELS. Components with `kind='config'` should be managed in the instrument settings in the UI.  
A quick way to get started is using the `custom_function_signal` module. These Signals inherit from ophyd's Signal and provide a way to use any python function for setting / reading the channel.  
The example below shows, how to use these. A function can be passed to the component directly, while a class method needs to be passed in the constructor.  
You may add a function `finalize_steps`. If this function exists, it will be called after a protocol. This function should be used to close / deinitialize the instrument if necessary.

<details>
  <summary>Code example for an ophyd file</summary>

```python
from ophyd import Device
from ophyd import Component as Cpt
from nomad_camels.bluesky_handling.custom_function_signal import Custom_Function_Signal, Custom_Function_SignalRO


def my_read_function():
    # do reading

def my_config_function(value):
    # do something


class Instrument_Name(Device):
    # This is an example for a channel that can only be read
    get_value = Cpt(Custom_Function_SignalRO, name='get_value',
                    metadata={'units': 'A'}, read_function=my_read_function)
    # Example of a set channel
    set_value = Cpt(Custom_Function_Signal, name='set_value',
                    metadata={'units': 'V'})

    # Example for a configuration attribute
    config_value = Cpt(Custom_Function_Signal, name='config_value',
                       kind='config', put_function=my_config_function)
    
    
    def __init__(self, prefix='', *, name, kind=None, read_attrs=None,
                 configuration_attrs=None, parent=None, **kwargs):
       super().__init__(prefix=prefix, name=name, kind=kind, read_attrs=read_attrs,
                        configuration_attrs=configuration_attrs, parent=parent, **kwargs)
       self.get_value.read_function = my_read_function
       self.set_value.put_function = self.my_set_method
       self.config_value.put_function = my_config_function
    
    def my_set_method(self):
        # do setting
    
    def finalize_steps(self):
        # do things to close the instrument

```
</details>


## 3. Building the Instrument Package
To create a new package that can be installed via pip from PyPi or testPyPi follow these steps.
1. Make sure you have `build` and `twine` installed into your python environment with
   ```
   pip install build
   ``` 
   and 
   ```
   pip install twine
   ``` 

2. Go to the `<driver_name>` directory of the driver. So the parent directory containing the pyproject.toml
3. Set the correct version number and metadata in your `pyproject.toml` file
4. Run the build command : 
   ```
   python -m build
   ```
   This creates the `dist/` folder and the distributions to upload to PyPi
5. Upload to PyPi with
    ```console
    python -m twine upload dist/nomad*
    ```

---

## 4. Automated Build and Upload
You can run the following script using microsoft PowerShell in the `$rootFolder` containing multiple instrument drivers in subdirectories.\
It runs the `python -m build` and `python -m twine upload dist/nomad*` commands in each subdirectory containing a `pyproject.toml` file.

```powershell
$rootFolder = "C:\Path\To\Root\Folder"
Get-ChildItem $rootFolder -Recurse -Directory | ForEach-Object {
    if (Test-Path "$($_.FullName)\pyproject.toml") {
        Push-Location $_.FullName
        python -m build
        python -m twine upload dist/nomad*
        Pop-Location
    }
}
```


---

## 5. Install Instrument Package
To install  run
```console
pip install nomad_camels_driver_<driver_name>
```
where `nomad_camels_driver_<driver_name>` is the driver name you gave your folder and project.\

