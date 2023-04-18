---
layout: default
title: Instrument Drivers
parent: Programmer's Guide
nav_order: 1
---
# NOMAD-CAMELS Instrument Drivers
This is the officially maintained repository of the [NOMAD-CAMELS](https://fau-lap.github.io/NOMAD-CAMELS/) instrument drivers.\
[This list](/drivers_list.txt) contains all drivers that are supplied by the NOMAD-CAMELS development team. \
The [NOMAD-CAMELS measurement software](https://fau-lap.github.io/NOMAD-CAMELS/)  reads this file as a default to list the installable instruments. 
## 1. Writing New Instrument Drivers
Every instrument driver is an individual [PyPi](https://pypi.org/) package.
> &#9888; 
> Currently the drivers are located in [testPyPi.org](https://testPyPi.org/). &#9888;\
> This will be changed to [PyPi.org](https://PyPi.org/) once the devices are stable.

The source code of each driver can be found in this repository.
### 1.1. Folder structure
The driver should have the following folder structure
```
<parent_driver_name>
└─> dist (this is automatically created by python -m build)
    └─> nomad_camels_driver_<parent_driver_name>-X.Y.Z.tar.gz
    └─> nomad_camels_driver_<parent_driver_name>-X.Y.Z-py3-none-any.whl
└─> nomad_camels_driver_<parent_driver_name> (contains the actual device communication files)
    └─> <parent_driver_name>.py
    └─> <parent_driver_name>_ophyd.py
└─> LICENSE.txt
└─> pyproject.toml
└─> README.md
```
The `pyproject.toml` file contains most of the relevant information concerning the package that will be uploaded to PyPi ([see here for more information](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)). 
Most importantly the project name and version must be set in the `pyproject.toml` file.

<details>
  <summary>Code example: pyproject.toml file</summary>

{% highlight toml %}
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "nomad_camels_driver_keithley_237"
version = "0.1.4"
authors = [
    { name="FAIRmat - HU Berlin", email="nomad-camels@fau.de" }
]
description = "Device driver for the Keithley 237 SMU."
readme = "README.md"
requires-python = ">=3.9.6"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
    "Operating System :: Microsoft :: Windows",
]
dependencies = [
    "pyvisa",
]
[project.urls]
"GitHub Page" = "https://github.com/FAU-LAP/NOMAD-CAMELS"
"Documentation" = "https://fau-lap.github.io/NOMAD-CAMELS/"
{% endhighlight %}

</details>

### 1.2. Python files
The `<parent_driver_name>.py` file contains information about the possible instrument configurations and settings. This can be for example the current compliance of a voltage source or the integration time of a digital multimeter.\
#### 1.2.1 Simple Device Configurations
For simple instrument with only a few settings you do not need to write your own GUI for the settings but CAMELS can auto-generate the UI for you. An example file is displayed below:

<details>
  <summary>Code example: Use the auto-generated UI for instrument settings</summary>

{% highlight python %}
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

# This adds a simple GUI of the configuration settings that you add below. 
# This way you do NOT need to write our own GUI for the instrument settings.
# This can be used for simple instruments with only a few settings.
# For more complicated instruments (with e.g. multiple channels) it might be necessary to write a more advanced GUI
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
{% endhighlight %}

</details>


#### 1.2.2 Complex Device Configurations
If the instrument is more complex CAMELS can not auto generate the UI anymore. Here you need to write your own UI using for example QT Designer. The first three class definitions are relevant for this. 
<details>
  <summary>Code example: Use your own UI file to create settings for your instrument</summary>

{% highlight python %}
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

# This inherits from your UI and is used above to create the tab widget with all the settings you implemented.
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
{% endhighlight %}

</details>

Here is a more complex example which creates settings for two channels of a single instrument.
<details>
  <summary>Code example: Complex instrument</summary>

{% highlight python %}
from nomad_camels.main_classes import device_class
from keysight_b2912.keysight_b2912_channel_config import Ui_B2912_channel # You need to import the created UI file
from keysight_b2912.keysight_b2912_ophyd import Keysight_B2912 # Import the actual device communication
from PySide6.QtWidgets import QTabWidget

# Default settings of the instrument
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

# Similar to the simple device
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

# This inherits from the UI class you wrote for the UI config settings of the instrument
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
{% endhighlight %}

</details>

### 1.3. Building the Instrument Package
To create a new package that can be installed via pip from PyPi or testPyPi follow these steps.
1. Make sure you have `build` installed into your python environment with `pip install build`
2. Go to the `<parent_driver_name>` directory of the driver. So the parent directory containing the pyproject.toml 
3. Set the correct version number and metadata in your `pyproject.toml` file
4. Run the build command : `python -m build`. This creates the `dist/` folder and the distributions to upload to PyPi
5. Upload to testPyPi (PyPi) with 
    ```bash
    python -m twine upload --repository testpypi dist/nomad*
    ```
   &#9888; Change the repository used after the `--repository` flag to `pypi` to upload to PyPi

### 1.4. Install Instrument Package
To install simply run 
```bash
pip install --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nomad_camels_driver_<parent_driver_name>
```
where `nomad_camels_driver_<parent_driver_name>` is the driver name you gave your folder and project.\
The `--extra-index-url` flag allows dependencies to be installed from PyPi.\
The `--no-cache-dir` flag prevents any locally saved NOMAD-CAMELS version to be installed instead of the most recent remote version.\
> &#9888; The index-url must be changed of course when installing from PyPi &#9888;






### Advanced Driver Information

The directory should be named like the device.


`device`.py

This should include a class `subclass` which inherits from `main_classes.device_class.Device`.
The Arguments here should be set in the __init__ by the subclass (following) the documentation of the Device class.
For most devices, nothing further should be necessary in this class.
In the attribute `files`, you should list all files, needed for an IOC to support this device. These should be in the same directory.

The `subclass_config`, inheriting from `main_classes.device_class.Device_Config`.
It should provide the necessary configuration for the device and put this information into the device's `config`, `settings` and `ioc_settings` attributes.



`device_ophyd.py`
This should include a class (meaningfully named) inheriting from `ophyd.Device`.
Here you may set all the components the device has. Components are called 'channels' in CAMELS and is what you use to write and read to and from instruments. Those with a kind='normal' (or not specified) will appear as channels inside CAMELS. Those with kind='config' should be part of the configuration-Widget.
<p style="text-align:left;">
  <span style="color: grey;">
  <a href="../index.html">&larr; Back</a>
  </span>
  <span style="float:right;">
    <a href="quick_start.html">Next &rarr;</a><br>
  </span>
</p>
