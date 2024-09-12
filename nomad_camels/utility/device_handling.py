"""This package provides utility for everything regarding devices/instruments
connected to the main UI.

Attributes
----------
    local_packages : dict{"<driver_name>": python-module}
        the loaded modules of local instrument drivers
    running_devices : dict{"<device_name>": ophyd.Device}
        The devices that are already instantiated and currently running. All
        devices are given an attribute `device_run_count` which is increased by
        1 each time a function tries to instantiate a device that is already
        running. Closing the device decreases the run-count by 1. It is only
        really closed, once the run-count reaches 0.
    last_path : str, path
        The path that was last used to search for local drivers. This is used to
        only re-run loading the packages if something changed.
"""

import sys
import os
import importlib
import re

from nomad_camels.utility import variables_handling
from nomad_camels.bluesky_handling import helper_functions

import copy
import pathlib

from PySide6.QtCore import QThread, Signal

local_packages = {}
local_package_paths = {}
running_devices = {}
from_manual_controls = []
last_path = ""


def load_local_packages(tell_local=False):
    """
    Loads the packages of local instrument drivers and returns a dictionary with
    them. If `tell_local`, then the keys will be "local <driver_name>",
    otherwise just "<driver_name>".

    Parameters
    ----------
    tell_local : True
        (Default value = False)

    Returns
    -------
    dict
        Contains the packages with the driver name as keys.
    """
    global local_packages, last_path
    local_instr_path = variables_handling.device_driver_path
    if local_instr_path == last_path:
        if local_packages:
            return local_packages
    else:
        last_path = local_instr_path
        local_packages.clear()
    if not os.path.isdir(local_instr_path):
        return local_packages
    sys.path.append(local_instr_path)
    for f in pathlib.Path(local_instr_path).rglob("*"):
        match = re.match(r"^(nomad[-_]{1}camels[-_]{1}driver[-_]{1})(.*)$", f.name)
        if match:
            try:
                sys.path.append(str(f.parent))
                package = importlib.import_module(f".{match.group(2)}", match.group(0))
                device = package.subclass()
                if tell_local:
                    local_packages[f"local {device.name}"] = package
                else:
                    local_packages[device.name] = package
                local_package_paths[device.name] = str(f.parent)
            except Exception as e:
                print(f, e)
    for f in pathlib.Path("manual_controls").resolve().rglob("*"):
        match = re.match(r"^(nomad[-_]{1}camels[-_]{1}driver[-_]{1})(.*)$", f.name)
        if match:
            try:
                sys.path.append(str(f.parent))
                package = importlib.import_module(f".{match.group(2)}", match.group(0))
                device = package.subclass()
                if tell_local:
                    local_packages[f"local {device.name}"] = package
                else:
                    local_packages[device.name] = package
                local_package_paths[device.name] = str(f.parent)
                from_manual_controls.append(device.name)
            except Exception as e:
                print(f, e)
    return local_packages


def get_channel_from_string(channel):
    """
    Returns the component of the ophyd device that corresponds to the given
    channel. The device has to be instantiated at this point.

    Parameters
    ----------
    channel : str
        The name of the channel (i.e. "<device>.<channel>")

    Returns
    -------
    ophyd.Signal
        The signal / channel found from the string
    """
    dev, chan = channel.split(".")
    if dev not in running_devices:
        raise Exception(f"Device {dev} is needed, but not yet instantiated!")
    device = running_devices[dev]
    return getattr(device, chan)


def get_funtion_from_string(func_name):
    dev, func = func_name.split(".")
    if dev not in running_devices:
        raise Exception(f"Device {dev} is needed, but not yet instantiated!")
    device = running_devices[dev]
    return getattr(device, func)


def get_channels_from_string_list(channel_list, as_dict=False):
    """
    Goes through the given channel_list and if they are valid channels in
    CAMELS, their ophyd representation is called by `get_channel_from_string`.

    Parameters
    ----------
    channel_list : list[str]
        List of the channels in CAMELS-representation
        (i.e. "<device_name>_<channel_name>")
    as_dict : bool
        (Default value = False)
        if True, the returned channels will be a dictionary with the original
        list serving as keys

    Returns
    -------
    list[ophyd.Signal], dict
        A list of the ophyd representations of `channel_list`.
        If `as_dict` is True, it is a dictionary with the shape
        {'channel_name': ophyd.Signal}
    """
    if as_dict:
        channels = {}
    else:
        channels = []
    for channel in channel_list:
        chan = channel
        if chan == "None":
            channels.append(None)
            continue
        if channel in variables_handling.channels:
            chan = variables_handling.channels[channel]
        if as_dict:
            channels[channel] = get_channel_from_string(chan.name)
        else:
            channels.append(get_channel_from_string(chan.name))
    return channels


def get_functions_from_string_list(func_list):
    funcs = []
    for func in func_list:
        if func == "None":
            funcs.append(None)
            continue
        funcs.append(get_funtion_from_string(func))
    return funcs


def start_devices_from_channel_list(channel_list, skip_config=False):
    """
    Instantiates the ophyd devices that are needed by the given channels.
    Returns the ophyd devices and their metadata.

    Parameters
    ----------
    channel_list : list[str]
        List of the channels, for which the devices should be started.

    Returns
    -------
    devs : dict{"<device_name>": ophyd.Device}
        Dictionary of the started devices (or if they were already running,
        their currently running instance)
    dev_data : dict{"<device_name>": dict}
        Dictionary of the devices' metadata (i.e. config, settings...)
    """
    dev_list = set()
    for channel in channel_list:
        dev_list.add(variables_handling.channels[channel].device)
    dev_list = list(dev_list)
    devs, dev_data = instantiate_devices(dev_list, skip_config=skip_config)
    return devs, dev_data


def instantiate_devices(device_list, skip_config=False):
    """
    Starts the given devices, or increases their run-count by 1 and returns
    them together with their settings.

    Parameters
    ----------
    device_list : list[str]
        The devices (as they are named in CAMELS) that should be started

    Returns
    -------
    devices : dict{"<device_name>": ophyd.Device}
        Dictionary of the started devices (or if they were already running,
        their currently running instance)
    device_config : dict{"<device_name>": dict}
        Dictionary of the devices' metadata (i.e. config, settings...)
    """
    device_config = {}
    devices = {}
    started_devs = []
    try:
        for dev in device_list:
            # getting all the settings
            device = variables_handling.devices[dev]
            classname = device.ophyd_class_name
            if skip_config:
                config = {}
            else:
                config = copy.deepcopy(device.get_config())
            settings = copy.deepcopy(device.get_settings())
            additional_info = copy.deepcopy(device.get_additional_info())
            if "connection" in settings:
                conn = settings.pop("connection")
                if "type" in conn:
                    conn.pop("type")
                settings.update(conn)
            if "idn" in settings:
                settings.pop("idn")
            extra_settings = {}
            non_strings = []
            for key in settings:
                if key.startswith("!non_string!_"):
                    extra_settings[key.replace("!non_string!_", "")] = settings[key]
                    non_strings.append(key)
            for s in non_strings:
                settings.pop(s)
            additional_info["device_class_name"] = classname
            extra_settings.update(settings)

            extra_config = {}
            non_strings = []
            for key in config:
                if key.startswith("!non_string!_"):
                    extra_config[key.replace("!non_string!_", "")] = config[key]
                    non_strings.append(key)
            for s in non_strings:
                config.pop(s)
            config.update(extra_config)

            # instantiating ophyd-device
            print(f"connecting {dev}")
            if dev in running_devices:
                ophyd_device = running_devices[dev]
                ophyd_device.device_run_count += 1
            else:
                ophyd_device = device.ophyd_class(f"{dev}:", name=dev, **extra_settings)
                ophyd_device.device_run_count = 1
                running_devices[dev] = ophyd_device
            ophyd_device.wait_for_connection()
            configs = ophyd_device.configure(config)[1]
            devices[dev] = ophyd_device

            # updating the config data
            device_config[dev] = {"settings": {}}
            device_config[dev]["settings"].update(
                helper_functions.simplify_configs_dict(configs)
            )
            device_config[dev]["settings"].update(settings)
            device_config[dev].update(additional_info)
            device_config[dev]["instrument_camels_channels"] = {
                name: data.__dict__ for name, data in device.channels.items()
            }
            for watchdog in variables_handling.watchdogs.values():
                if dev in watchdog.get_device_list():
                    watchdog.add_device(dev, ophyd_device)
            started_devs.append(dev)
    except Exception as e:
        close_devices(started_devs)
        raise Exception(e)
    return devices, device_config


class InstantiateDevicesThread(QThread):
    """
    Thread for starting devices in the background.
    """

    exception_raised = Signal(Exception)
    successful = Signal()

    def __init__(self, device_list, channels=False, skip_config=False):
        super().__init__()
        self.channels = channels
        self.device_list = device_list
        self.skip_config = skip_config
        main_thread_devs = []
        if channels:
            for channel in device_list:
                if channel not in variables_handling.channels:
                    raise Warning(
                        f"Trying to use channel {channel}, but it is not defined!"
                    )
                chan = variables_handling.channels[channel]
                if chan.device not in variables_handling.devices:
                    raise Warning(
                        f"Trying to use channel {channel}, but the corresponding device {chan.device} is not defined!"
                    )
                dev = variables_handling.devices[chan.device]
                if dev.main_thread_only:
                    main_thread_devs.append(channel)
        else:
            for device in device_list:
                if device not in variables_handling.devices:
                    raise Warning(
                        f"Trying to start device {device}, but it is not even defined!"
                    )
                dev = variables_handling.devices[device]
                if dev.main_thread_only:
                    main_thread_devs.append(device)
                    for d in dev.get_necessary_devices():
                        if d not in main_thread_devs:
                            main_thread_devs.insert(0, d)
        for dev in main_thread_devs:
            self.device_list.remove(dev)
        if self.channels:
            self.devices, self.device_config = start_devices_from_channel_list(
                main_thread_devs, skip_config=skip_config
            )
        else:
            self.devices, self.device_config = instantiate_devices(
                main_thread_devs, skip_config=skip_config
            )
        # uncomment next line for testing purposes
        # self.run()

    def run(self):
        try:
            if self.channels:
                devices, device_config = start_devices_from_channel_list(
                    self.device_list, skip_config=self.skip_config
                )
            else:
                devices, device_config = instantiate_devices(
                    self.device_list, skip_config=self.skip_config
                )
            self.devices.update(devices)
            self.device_config.update(device_config)
            self.successful.emit()
        except Exception as e:
            self.exception_raised.emit(e)


def close_devices(device_list):
    """
    Closes the given devices (calling their `finalize_steps`), or decreases
    their run-count by 1.

    Parameters
    ----------
    device_list : list[str]
        The devices (as they are named in CAMELS) that should be closed
    """
    for dev in reversed(device_list):
        if dev not in running_devices:
            continue
            raise Warning(f"Trying to close device {dev}, but it is not even running!")
        ophyd_dev = running_devices[dev]
        ophyd_dev.device_run_count -= 1
        if ophyd_dev.device_run_count == 0:
            running_devices.pop(dev)
            if hasattr(ophyd_dev, "finalize_steps") and callable(
                ophyd_dev.finalize_steps
            ):
                ophyd_dev.finalize_steps()
            for watchdog in variables_handling.watchdogs.values():
                if dev in watchdog.get_device_list():
                    watchdog.remove_device(dev, ophyd_dev)
