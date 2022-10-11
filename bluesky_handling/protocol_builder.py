import os.path
import subprocess
import copy

from main_classes.protocol_class import Measurement_Protocol
from utility import variables_handling

from bluesky_handling.builder_helper_functions import plot_creator

standard_string = 'import numpy as np\n'
standard_string += 'import importlib\n'
standard_string += 'from bluesky import RunEngine\n'
standard_string += 'from bluesky.callbacks.best_effort import BestEffortCallback\n'
standard_string += 'import bluesky.plan_stubs as bps\n'
standard_string += 'import databroker\n'
# standard_string += 'from bluesky_widgets.qt.threading import wait_for_workers_to_quit\n'
standard_string += 'from PyQt5.QtWidgets import QApplication\n'
standard_string += 'from PyQt5.QtCore import QCoreApplication\n'
standard_string += 'from epics import caput\n'
standard_string += 'import datetime\n'
standard_string += 'from CAMELS.main_classes import plot_widget, list_plot, plot_2D\n'
standard_string += 'from CAMELS.utility.databroker_export import broker_to_hdf5, broker_to_dict\n'
standard_string += 'from CAMELS.bluesky_handling.evaluation_helper import Evaluator\n'
standard_string += 'from CAMELS.bluesky_handling import helper_functions\n'
standard_string += 'RE = RunEngine()\n'

# standard_run_string = '\n\neva = Evaluator(namespace=namespace)\n\n\n'
standard_run_string = 'def main():\n'
standard_run_string += '\tbec = BestEffortCallback()\n'
standard_run_string += '\tRE.subscribe(bec)\n'

standard_start_string = '\n\n\nif __name__ == "__main__":\n'
standard_start_string += '\tmain()\n'

standard_nexus_dict = {'/ENTRY[entry]/operator/address': 'metadata_start/user/Address (affiliation)',
                       '/ENTRY[entry]/operator/affiliation': 'metadata_start/user/Affiliation',
                       '/ENTRY[entry]/operator/email': 'metadata_start/user/E-Mail',
                       '/ENTRY[entry]/operator/name': 'metadata_start/user/Name',
                       '/ENTRY[entry]/operator/orcid': 'metadata_start/user/ORCID',
                       '/ENTRY[entry]/operator/telephone_number': 'metadata_start/user/Phone',
                       '/ENTRY[entry]/start_time': 'metadata_start/time',
                       '/ENTRY[entry]/SAMPLE[sample]/data_identifier': 'metadata_start/sample/Identifier',
                       '/ENTRY[entry]/SAMPLE[sample]/sample_name': 'metadata_start/sample/Name',
                       '/ENTRY[entry]/SAMPLE[sample]/sample_history': 'metadata_start/sample/Preparation-Info',
                       "/ENTRY[entry]/PROCESS[process]/program": 'metadata_start/program',
                       "/ENTRY[entry]/PROCESS[process]/version": 'metadata_start/version',
                       "/ENTRY[entry]/SAMPLE[sample]/measured_data": 'data'}


def build_protocol(protocol:Measurement_Protocol, file_path,
                   save_path='test.h5', catalog='CAMELS_CATALOG', userdata=None,
                   sampledata=None):
    """Creating the python file from a given `protocol`.

    Parameters
    ----------
    protocol : Measurement_Protocol
        The protocol that should be build
    file_path : str, path
        The path, where the python file should be put
    save_path : str, default "test.h5"
        Path, where the datafile of the protocol should be put
    catalog : str, default "CAMELS_CATALOG"
        Name of the databroker-catalog that should be used
    userdata : dict, default None
        Should contain information about the user
    sampledata : dict, default None
        Should contain information about the sample
    """
    device_import_string = '\n'
    devices_string = '\n\t\tdevs = {}\n\t\tdevice_config = {}\n'
    variable_string = '\nnamespace = {}\n'
    variable_string += 'all_fits = {}\n'
    variable_string += 'plots = []\n'
    additional_string_devices = ''
    final_string = ''
    for var, val in variables_handling.protocol_variables.items():
        if variables_handling.check_data_type(val) == 'String':
            val = f'"{val}"'
        if '(' in var or ')' in var:
            continue
        variable_string += f'{var} = {val}\n'
        variable_string += f'namespace["{var}"] = {var}\n'
    for var, val in variables_handling.loop_step_variables.items():
        if variables_handling.check_data_type(val) == 'String':
            val = f'"{val}"'
        if '(' in var or ')' in var:
            continue
        variable_string += f'{var} = {val}\n'
        variable_string += f'namespace["{var}"] = {var}\n'
    for dev in protocol.get_used_devices():
        print(variables_handling.devices)
        device = variables_handling.devices[dev]
        classname = device.ophyd_class_name
        config = copy.deepcopy(device.get_config())
        settings = copy.deepcopy(device.get_settings())
        ioc_settings = copy.deepcopy(device.get_ioc_settings())
        if 'connection' in settings:
            settings.pop('connection')
        if 'idn' in settings:
            settings.pop('idn')
        devices_string += f'\t\tsettings = {settings}\n'
        devices_string += f'\t\tioc_settings = {ioc_settings}\n'
        if not ioc_settings or ioc_settings['use_local_ioc']:
            ioc_name = variables_handling.preset
        else:
            ioc_name = ioc_settings['ioc_name']
        devices_string += f'\t\t{dev} = {classname}("{ioc_name}:{dev}:", name="{dev}", **settings)\n'
        devices_string += f'\t\tprint("connecting {dev}")\n'
        devices_string += f'\t\t{dev}.wait_for_connection()\n'
        devices_string += f'\t\tconfig = {config}\n'
        devices_string += f'\t\tconfigs = {dev}.configure(config)[1]\n'
        devices_string += f'\t\tdevice_config["{dev}"] = {{}}\n'
        devices_string += f'\t\tdevice_config["{dev}"].update(configs)\n'
        devices_string += f'\t\tdevice_config["{dev}"]["settings"] = settings\n'
        devices_string += f'\t\tdevice_config["{dev}"]["ioc_settings"] = ioc_settings\n'
        devices_string += f'\t\tdevs.update({{"{dev}": {dev}}})\n'
        device_import_string += f'from {device.name}.{device.name}_ophyd import {classname}\n'
        additional_string_devices += device.get_additional_string()
        final_string += device.get_finalize_steps()
    devices_string += '\t\tprint("devices connected")\n'
    devices_string += '\t\tmd = {"device_config": device_config}\n'
    devices_string += '\t\tmd.update({"program": "CAMELS", "version": "0.1"})\n'
    devices_string += '\t\tmd["variables"] = namespace\n'
    if protocol.use_nexus:
        md_dict = {}
        for i, name in enumerate(protocol.metadata['Name']):
            md_dict[name] = protocol.metadata['Value'][i]
        devices_string += f'\t\tmd.update({md_dict})\n'
    plot_string, plotting = plot_creator(protocol.plots)
    # for device in protocol.get_used_devices():
    #     print(device)
    protocol_string = 'import sys\n'
    protocol_string += f'sys.path.append(r"{os.path.dirname(variables_handling.CAMELS_path)}")\n'
    protocol_string += f'sys.path.append("{variables_handling.device_driver_path}")\n\n'
    protocol_string += standard_string
    protocol_string += f'{variable_string}\n\n'
    protocol_string += device_import_string
    protocol_string += protocol.get_outer_string()
    protocol_string += protocol.get_plan_string()
    protocol_string += plot_string
    protocol_string += protocol.get_add_main_string()
    protocol_string += standard_run_string
    protocol_string += f'\tcatalog = databroker.catalog["{catalog}"]\n'
    protocol_string += '\tRE.subscribe(catalog.v1.insert)\n'
    protocol_string += '\ttry:\n'
    # protocol_string += '\tRE.subscribe(eva)\n\n'
    protocol_string += devices_string
    protocol_string += additional_string_devices
    if plotting:
        protocol_string += '\t\tplot_dat = create_plots(RE)\n'
    protocol_string += user_sample_string(userdata, sampledata)
    protocol_string += '\t\tadditional_step_data = steps_add_main(RE)\n'
    protocol_string += f'\t\tuids = RE({protocol.name}_plan(devs, md=md, runEngine=RE))\n'
    protocol_string += '\tfinally:\n'
    protocol_string += final_string or '\t\tpass\n'

    standard_save_string = '\n\n\truns = catalog[uids]\n'
    if protocol.use_nexus:
        nexus_dict = protocol.get_nexus_paths()
        nexus_dict.update(standard_nexus_dict)
        standard_save_string += '\tdata = broker_to_dict(runs)\n'
        standard_save_string += f'\tnexus_mapper = {nexus_dict}\n'
        # TODO finish this
    else:
        standard_save_string += f'\tbroker_to_hdf5(runs, "{save_path}")\n\n\n'
    standard_save_string += '\tapp = QCoreApplication.instance()\n'
    standard_save_string += '\tprint("protocol finished!")\n'
    standard_save_string += '\tif app is not None:\n'
    standard_save_string += '\t\tsys.exit(app.exec_())\n'
    standard_save_string += '\treturn plot_dat, additional_step_data\n'

    protocol_string += standard_save_string
    protocol_string += standard_start_string
    if not os.path.isdir(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w+') as file:
        file.write(protocol_string)

def user_sample_string(userdata, sampledata):
    """Returns the string adding userdata and sampledata to the md."""
    u_s_string = f'\t\tmd["user"] = {userdata}\n'
    u_s_string += f'\t\tmd["sample"] = {sampledata}\n'
    return u_s_string

