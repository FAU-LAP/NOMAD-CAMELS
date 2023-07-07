import sys
import os
import importlib
import re

from nomad_camels.utility import variables_handling
from nomad_camels.bluesky_handling import helper_functions

import copy
import pathlib

local_packages = {}
running_devices = {}
last_path = ''

def load_local_packages(tell_local=False):
    """

    Parameters
    ----------
    tell_local :
         (Default value = False)

    Returns
    -------

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
    for f in pathlib.Path(local_instr_path).rglob('*'):
        match = re.match(r'^(nomad[-_]{1}camels[-_]{1}driver[-_]{1})(.*)$', f.name)
        if match:
            try:
                sys.path.append(str(f.parent))
                package = importlib.import_module(f'.{match.group(2)}', match.group(0))
                device = package.subclass()
                if tell_local:
                    local_packages[f'local {device.name}'] = package
                else:
                    local_packages[device.name] = package
            except Exception as e:
                print(f, e)
    return local_packages


def get_channel_from_string(channel):
    """

    Parameters
    ----------
    channel :
        

    Returns
    -------

    """
    dev, chan = channel.split('.')
    if dev not in running_devices:
        raise Exception(f'Device {dev} is needed, but not yet instantiated!')
    device = running_devices[dev]
    return getattr(device, chan)

def get_channels_from_string_list(channel_list):
    """

    Parameters
    ----------
    channel_list :
        

    Returns
    -------

    """
    channels = []
    for channel in channel_list:
        chan = channel
        if chan == 'None':
            channels.append(None)
            continue
        if channel in variables_handling.channels:
            chan = variables_handling.channels[channel]
        channels.append(get_channel_from_string(chan.name))
    return channels

def start_devices_from_channel_list(channel_list):
    """

    Parameters
    ----------
    channel_list :
        

    Returns
    -------

    """
    dev_list = set()
    for channel in channel_list:
        dev_list.add(variables_handling.channels[channel].device)
    dev_list = list(dev_list)
    devs, dev_data = instantiate_devices(dev_list)
    return devs, dev_data

def instantiate_devices(device_list):
    """

    Parameters
    ----------
    device_list :
        

    Returns
    -------

    """
    device_config = {}
    devices = {}
    for dev in device_list:
        # getting all the settings
        device = variables_handling.devices[dev]
        classname = device.ophyd_class_name
        config = copy.deepcopy(device.get_config())
        settings = copy.deepcopy(device.get_settings())
        additional_info = copy.deepcopy(device.get_additional_info())
        if 'connection' in settings:
            conn = settings.pop('connection')
            if 'type' in conn:
                conn.pop('type')
            settings.update(conn)
        if 'idn' in settings:
            settings.pop('idn')
        extra_settings = {}
        non_strings = []
        for key in settings:
            if key.startswith('!non_string!_'):
                extra_settings[key.replace('!non_string!_', '')] = settings[key]
                non_strings.append(key)
        for s in non_strings:
            settings.pop(s)
        additional_info['device_class_name'] = classname
        extra_settings.update(settings)

        # instantiating ophyd-device
        if dev in running_devices:
            ophyd_device = running_devices[dev]
            ophyd_device.device_run_count += 1
        else:
            ophyd_device = device.ophyd_class(f'{dev}:', name=dev, **extra_settings)
            ophyd_device.device_run_count = 1
            running_devices[dev] = ophyd_device
        print(f"connecting {dev}")
        ophyd_device.wait_for_connection()
        configs = ophyd_device.configure(config)[1]
        devices[dev] = ophyd_device

        # updating the config data
        device_config[dev] = {}
        device_config[dev].update(helper_functions.simplify_configs_dict(configs))
        device_config[dev].update(settings)
        device_config[dev].update(additional_info)
    return devices, device_config

def close_devices(device_list):
    """

    Parameters
    ----------
    device_list :
        

    Returns
    -------

    """
    for dev in reversed(device_list):
        if dev not in running_devices:
            raise Warning(f'Trying to close device {dev}, but it is not even running!')
        ophyd_dev = running_devices[dev]
        ophyd_dev.device_run_count -= 1
        if ophyd_dev.device_run_count == 0:
            running_devices.pop(dev)
            if hasattr(ophyd_dev, 'finalize_steps') and callable(ophyd_dev.finalize_steps):
                ophyd_dev.finalize_steps()



