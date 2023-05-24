import os.path
import copy

# from nomad_camels.main_classes.protocol_class import Measurement_Protocol
import pathlib

from nomad_camels.utility import variables_handling, device_handling, load_save_functions

from nomad_camels.bluesky_handling.builder_helper_functions import plot_creator

standard_string = 'import numpy as np\n'
standard_string += 'import importlib\n'
standard_string += 'import bluesky\n'
standard_string += 'import ophyd\n'
standard_string += 'from bluesky import RunEngine\n'
standard_string += 'from bluesky.callbacks.best_effort import BestEffortCallback\n'
standard_string += 'import bluesky.plan_stubs as bps\n'
standard_string += 'import databroker\n'
# standard_string += 'from bluesky_widgets.qt.threading import wait_for_workers_to_quit\n'
standard_string += 'from PySide6.QtWidgets import QApplication, QMessageBox\n'
standard_string += 'from PySide6.QtCore import QCoreApplication, QThread\n'
standard_string += 'from epics import caput\n'
standard_string += 'import datetime\n'
standard_string += 'from nomad_camels.main_classes import plot_widget, list_plot, plot_2D\n'
standard_string += 'from nomad_camels.utility.databroker_export import broker_to_hdf5, broker_to_dict, broker_to_NX\n'
standard_string += 'from nomad_camels.utility import theme_changing\n'
standard_string += 'from nomad_camels.bluesky_handling.evaluation_helper import Evaluator\n'
standard_string += 'from nomad_camels.bluesky_handling import helper_functions\n'
# standard_string += 'RE = RunEngine()\n'
standard_string += 'darkmode = False\n'
standard_string += 'theme = "default"\n'
standard_string += 'protocol_step_information = {"protocol_step_counter": 0, "total_protocol_steps": 0, "protocol_stepper_signal": None}\n'

# standard_run_string = '\n\neva = Evaluator(namespace=namespace)\n\n\n'
standard_run_string = 'uids = []\n'
standard_run_string += 'def uid_collector(name, doc):\n'
standard_run_string += '\tuids.append(doc["uid"])\n\n\n'
standard_run_string += 'def run_protocol_main(RE, dark=False, used_theme="default", catalog=None, devices=None, md=None):\n'
standard_run_string += '\tdevs = devices or {}\n'
standard_run_string += '\tmd = md or {}\n'
standard_run_string += '\tglobal darkmode, theme, protocol_step_information\n'
standard_run_string += '\tdarkmode, theme = dark, used_theme\n'
# standard_run_string += '\tbec = BestEffortCallback()\n'
# standard_run_string += '\tRE.subscribe(bec)\n'

standard_start_string = '\n\n\ndef main():\n'
standard_start_string += '\tRE = RunEngine()\n'
standard_start_string += '\tbec = BestEffortCallback()\n'
standard_start_string += '\tRE.subscribe(bec)\n'
standard_start_string2 = '\t\tplot_etc = create_plots(RE)\n'
standard_start_string2 += '\t\tadditional_step_data = steps_add_main(RE, devs)\n'
standard_start_string2 += '\t\trun_protocol_main(RE=RE, catalog=catalog, devices=devs, md=md)\n'
standard_start_string3 = 'if __name__ == "__main__":\n'
standard_start_string3 += '\tmain()\n'
standard_start_string3 += '\tapp = QCoreApplication.instance()\n'
standard_start_string3 += '\tprint("protocol finished!")\n'
standard_start_string3 += '\tif app is not None:\n'
standard_start_string3 += '\t\tsys.exit(app.exec())\n'
# standard_start_string += '\treturn plot_dat, additional_step_data\n'

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


def build_protocol(protocol, file_path,
                   save_path='test.h5', catalog='CAMELS_CATALOG', userdata=None,
                   sampledata=None):
    """Creating the python file from a given `protocol`.

    Parameters
    ----------
    protocol :
        
    file_path :
        
    save_path :
         (Default value = 'test.h5')
    catalog :
         (Default value = 'CAMELS_CATALOG')
    userdata :
         (Default value = None)
    sampledata :
         (Default value = None)

    Returns
    -------

    
    """
    if not isinstance(save_path, pathlib.Path):
        save_path = pathlib.Path(save_path)
    if isinstance(save_path, pathlib.WindowsPath):
        save_path = save_path.as_posix()
    variables_handling.read_channel_names.clear()
    variables_handling.read_channel_sets.clear()
    device_import_string = '\n'
    devices_string = '\t\tdevs = {}\n\t\tdevice_config = {}\n'
    variable_string = '\nnamespace = {}\n'
    variable_string += 'all_fits = {}\n'
    variable_string += 'plots = []\n'
    variable_string += 'boxes = {}\n'
    additional_string_devices = ''
    final_string = ''
    for var, val in protocol.variables.items():
        if variables_handling.check_data_type(val) == 'String':
            val = f'"{val}"'
        if '(' in var or ')' in var:
            continue
        variable_string += f'{var} = {val}\n'
        variable_string += f'namespace["{var}"] = {var}\n'
    for var, val in protocol.loop_step_variables.items():
        if variables_handling.check_data_type(val) == 'String':
            val = f'"{val}"'
        if '(' in var or ')' in var:
            continue
        variable_string += f'{var} = {val}\n'
        variable_string += f'namespace["{var}"] = {var}\n'
    for dev in protocol.get_used_devices():
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
        device_handling.connection_check(ioc_settings, settings)
        if not ioc_settings and classname.endswith('_EPICS'):
            classname = classname[:-6]
        additional_info['device_class_name'] = classname
        if 'description' in additional_info:
            desc = additional_info['description'].replace('\n', '\n\t\t')
            devices_string += f'\t\t"""{dev} ({classname}):\n\t\t{desc}"""\n'
        devices_string += f'\t\tsettings = {settings}\n'
        if ioc_settings:
            devices_string += f'\t\tioc_settings = {ioc_settings}\n'
        devices_string += f'\t\tadditional_info = {additional_info}\n'
        devices_string += f'\t\t{dev} = {classname}("{dev}:", name="{dev}", '
        for key, value in extra_settings.items():
            devices_string += f'{key}={value}, '
        devices_string += '**settings)\n'
        devices_string += f'\t\tprint("connecting {dev}")\n'
        devices_string += f'\t\t{dev}.wait_for_connection()\n'
        devices_string += f'\t\tconfig = {config}\n'
        devices_string += f'\t\tconfigs = {dev}.configure(config)[1]\n'
        devices_string += f'\t\tdevice_config["{dev}"] = {{}}\n'
        devices_string += f'\t\tdevice_config["{dev}"].update(helper_functions.simplify_configs_dict(configs))\n'
        devices_string += f'\t\tdevice_config["{dev}"].update(settings)\n'
        if ioc_settings:
            devices_string += f'\t\tdevice_config["{dev}"]["ioc_settings"] = ioc_settings\n'
        devices_string += f'\t\tdevice_config["{dev}"].update(additional_info)\n'
        devices_string += f'\t\tdevs.update({{"{dev}": {dev}}})\n'
        device_import_string += f'from nomad_camels_driver_{device.name}.{device.name}_ophyd import {classname}\n'
        additional_string_devices += device.get_additional_string()
        final_string += device.get_finalize_steps()
    devices_string += '\t\tprint("devices connected")\n'
    devices_string += f'\t\tmd = {{"devices": device_config, "description": "{protocol.description}"}}\n'
    # devices_string += '\t\tmd.update({"program": "CAMELS", "version": "0.1"})\n'
    devices_string += '\t\tmd.update({"versions": {"NOMAD-CAMELS": "0.1", "EPICS": "7.0.6.2", "bluesky": bluesky.__version__, "ophyd": ophyd.__version__}})\n'
    if protocol.use_nexus:
        md_dict = {}
        for i, name in enumerate(protocol.metadata['Name']):
            md_dict[name] = protocol.metadata['Value'][i]
        devices_string += f'\t\tmd.update({md_dict})\n'
    plot_string, plotting = plot_creator(protocol.plots, multi_stream=True)
    # for device in protocol.get_used_devices():
    #     print(device)
    protocol_string = 'import sys\n'
    protocol_string += f'sys.path.append(r"{os.path.dirname(variables_handling.CAMELS_path)}")\n'
    protocol_string += f'sys.path.append(r"{os.path.dirname(variables_handling.CAMELS_path)}/nomad_camels")\n'
    protocol_string += f'sys.path.append(r"{variables_handling.device_driver_path}")\n\n'
    protocol_string += standard_string
    protocol_string += f'{variable_string}\n\n'
    protocol_string += device_import_string
    protocol_string += protocol.get_outer_string()
    protocol_string += protocol.get_plan_string()
    protocol_string += plot_string
    protocol_string += protocol.get_add_main_string()
    protocol_string += standard_run_string
    protocol_string += f'\tprotocol_step_information["total_protocol_steps"] = {protocol.get_total_steps()}\n'
    # protocol_string += '\ttry:\n'
    # protocol_string += '\tRE.subscribe(eva)\n\n'
    # protocol_string += devices_string
    protocol_string += additional_string_devices
    # if plotting:
    #     protocol_string += '\t\tplot_etc = create_plots(RE)\n'
    sampledata = sampledata or {'name': 'default_sample'}
    userdata = userdata or {'name': 'default_user'}
    protocol_string += user_sample_string(userdata, sampledata)
    protocol_string += f'\tmd["protocol_overview"] = "{protocol.get_short_string().encode("unicode_escape").decode()}"\n'
    protocol_string += '\twith open(__file__, "r") as f:\n'
    protocol_string += '\t\tmd["python_script"] = f.read()\n'
    protocol_string += '\tmd["variables"] = namespace\n'
    protocol_string += '\tRE.subscribe(uid_collector, "start")\n'
    # protocol_string += '\ttry:\n'
    protocol_string += f'\tRE({protocol.name}_plan(devs, md=md, runEngine=RE))\n'
    # protocol_string += '\tfinally:\n'
    # protocol_string += final_string or '\t\tpass\n'
    standard_save_string = '\tfinally:\n'
    standard_save_string += '\t\twhile RE.state not in ["idle", "panicked"]:\n'
    standard_save_string += '\t\t\timport time\n'
    standard_save_string += '\t\t\ttime.sleep(0.5)\n'
    standard_save_string += '\t\tif uids:\n'
    standard_save_string += '\t\t\truns = catalog[tuple(uids)]\n'
    if protocol.use_nexus:
        nexus_dict = protocol.get_nexus_paths()
        nexus_dict.update(standard_nexus_dict)
        standard_save_string += '\t\t\tdata = broker_to_dict(runs)\n'
        standard_save_string += f'\t\t\tnexus_mapper = {nexus_dict}\n'
        # TODO finish this
    else:
        standard_save_string += f'\t\t\tbroker_to_NX(runs, "{save_path}", plots,' \
                                f'session_name="{protocol.session_name}",' \
                                f'export_to_csv={protocol.export_csv},' \
                                f'export_to_json={protocol.export_json})\n\n\n'

    # protocol_string += standard_save_string
    protocol_string += standard_start_string
    protocol_string += '\ttry:\n'
    protocol_string += f'\t\tcatalog = databroker.catalog["{catalog}"]\n'
    protocol_string += '\texcept KeyError:\n'
    protocol_string += '\t\timport warnings\n'
    protocol_string += '\t\twarnings.warn("Could not find databroker catalog, using temporary catalog. If data is not transferred, it might get lost.")\n'
    protocol_string += '\t\tcatalog = databroker.temp().v2\n'
    protocol_string += '\tRE.subscribe(catalog.v1.insert)\n\n'
    protocol_string += '\tfrom nomad_camels.utility import tqdm_progress_bar\n'
    protocol_string += f'\ttqdm_bar = tqdm_progress_bar.ProgressBar({protocol.get_total_steps()})\n\n'
    protocol_string += '\tprotocol_step_information["protocol_stepper_signal"] = tqdm_bar\n'
    protocol_string += '\ttry:\n'
    protocol_string += devices_string
    protocol_string += standard_start_string2
    # protocol_string += '\tfinally:\n'
    protocol_string += standard_save_string
    protocol_string += final_string
    protocol_string += standard_start_string3
    if not os.path.isdir(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w+') as file:
        file.write(protocol_string)
    protocol_dict = load_save_functions.get_save_str(protocol)
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    load_save_functions.save_dictionary(file_path.with_suffix('.cprot'),
                                        protocol_dict)



def user_sample_string(userdata, sampledata):
    """Returns the string adding userdata and sampledata to the md.

    Parameters
    ----------
    userdata :
        
    sampledata :
        

    Returns
    -------

    """
    u_s_string = f'\tmd["user"] = {userdata}\n'
    u_s_string += f'\tmd["sample"] = {sampledata}\n'
    return u_s_string

