import sys
import os
import importlib
import re

from nomad_camels.utility import variables_handling
from nomad_camels.bluesky_handling import helper_functions

import copy

local_packages = {}
running_devices = {}

def load_local_packages(tell_local=False):
    global local_packages
    if local_packages:
        return local_packages
    local_instr_path = variables_handling.device_driver_path
    if not os.path.isdir(local_instr_path):
        return local_packages
    sys.path.append(local_instr_path)
    for f in os.listdir(local_instr_path):
        match = re.match(r'^(nomad[-_]{1}camels[-_]{1}driver[-_]{1})(.*)$', f)
        if match:
            package_path = f'{local_instr_path}/{f}'
            try:
                sys.path.append(package_path)
                package = importlib.import_module(match.group(2))
                device = package.subclass()
                if tell_local:
                    local_packages[f'local {device.name}'] = package
                else:
                    local_packages[device.name] = package
            except Exception as e:
                print(f, e)
    return local_packages


def get_channel_from_string(channel):
    dev, chan = channel.split('.')
    if dev not in running_devices:
        raise Exception(f'Device {dev} is needed, but not yet instantiated!')
    device = running_devices[dev]
    return getattr(device, chan)

def get_channels_from_string_list(channel_list):
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


def connection_check(ioc_settings, settings):
    if 'connection' not in ioc_settings:
        return
    conn = ioc_settings['connection']
    connTyp = conn['type']
    if connTyp == 'Local VISA':
        settings['resource_name'] = conn['resource_name']
        settings['baud_rate'] = conn['baud_rate']
        settings['read_termination'] = conn['read_termination']
        settings['write_termination'] = conn['write_termination']
        ioc_settings.clear()
    elif connTyp == '':
        ioc_settings.clear()

def start_devices_from_channel_list(channel_list):
    dev_list = set()
    for channel in channel_list:
        dev_list.add(variables_handling.channels[channel].device)
    dev_list = list(dev_list)
    devs, dev_data = instantiate_devices(dev_list)
    return devs, dev_data

def instantiate_devices(device_list):
    device_config = {}
    devices = {}
    for dev in device_list:
        # getting all the settings
        device = variables_handling.devices[dev]
        classname = device.ophyd_class_name
        config = copy.deepcopy(device.get_config())
        settings = copy.deepcopy(device.get_settings())
        ioc_settings = copy.deepcopy(device.get_ioc_settings())
        additional_info = copy.deepcopy(device.get_additional_info())
        if 'connection' in settings:
            settings.pop('connection')
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
        if not ioc_settings or ioc_settings['use_local_ioc']:
            ioc_name = variables_handling.preset
        else:
            ioc_name = ioc_settings['ioc_name']
        connection_check(ioc_settings, settings)
        if not ioc_settings and classname.endswith('_EPICS'):
            classname = classname[:-6]
        additional_info['device_class_name'] = classname
        extra_settings.update(settings)

        # instantiating ophyd-device
        if dev in running_devices:
            ophyd_device = running_devices[dev]
            ophyd_device.device_run_count += 1
        else:
            if not classname.endswith('_EPICS') and hasattr(device, 'ophyd_class_no_epics'):
                ophyd_device = device.ophyd_class_no_epics(f'{dev}:', name=dev, **extra_settings)
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
        if ioc_settings:
            device_config[dev]["ioc_settings"] = ioc_settings
        device_config[dev].update(additional_info)
    return devices, device_config

def close_devices(device_list):
    for dev in device_list:
        if dev not in running_devices:
            raise Warning(f'Trying to close device {dev}, but it is not even running!')
        ophyd_dev = running_devices[dev]
        ophyd_dev.device_run_count -= 1
        if ophyd_dev.device_run_count == 0:
            running_devices.pop(dev)
            if hasattr(ophyd_dev, 'finalize_steps') and callable(ophyd_dev.finalize_steps):
                ophyd_dev.finalize_steps()



