"""Provides helping functions to load and save all settings inside CAMELS.

Attributes
----------
    appdata_path : str, path
        The path to the local appdata of NOMAD CAMELS
    preset_path : str, path
        the path, where CAMELS saves the presets, a subfolder of `appdata_path`
    backup_path : str, path
        the path, where CAMELS saves backups of presets, a subfolder of
        `preset_path`
    save_string_list : list[class]
        a list of QWidget-classes, for which the current string they display should be
        saved
    save_dict_skip : list[class]
        a list of QWidget-classes, that should be ignored when saving
    standard_pref : dict
        dictionary of the default preferences used if nothing is changed by the
        user
"""

import os.path
import sys
from os.path import isdir
from os import makedirs, getenv, listdir
from shutil import copyfile
import importlib
from glob import glob
import platform

import numpy as np
import pandas as pd
from PySide6.QtWidgets import (
    QComboBox,
    QLineEdit,
    QWidget,
    QSplitter,
    QLabel,
    QPushButton,
    QTreeView,
    QListView,
    QMenuBar,
    QMenu,
    QStatusBar,
    QGridLayout,
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QTimer, Signal, SignalInstance

from datetime import datetime, timedelta
import json
import ophyd

from nomad_camels.main_classes import protocol_class, device_class, loop_step
from nomad_camels.utility.load_save_helper_functions import load_plots
from nomad_camels.utility.device_handling import load_local_packages
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from nomad_camels.bluesky_handling.watchdogs import Watchdog
from nomad_camels.bluesky_handling.evaluation_helper import Evaluator


os_name = platform.system()

if os_name == "Windows":
    # Use the APPDATA environment variable on Windows
    data_path = os.path.join(getenv("USERPROFILE"), "Documents", "NOMAD_CAMELS_data")
    appdata_path = os.path.join(getenv("LOCALAPPDATA"), "nomad_camels")
elif os_name == "Linux":
    # Use the XDG_DATA_HOME environment variable on Linux, defaulting to ~/.local/share
    data_path = os.path.join(
        getenv("XDG_DATA_HOME")
        or os.path.join(os.path.expanduser("~"), ".local", "share"),
        "nomad_camels_data",
    )
    appdata_path = os.path.join(
        getenv("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config"),
        "nomad_camels",
    )
elif os_name == "Darwin":
    # Use ~/Library/Application Support on MacOS
    data_path = os.path.join(
        os.path.expanduser("~"), "Library", "Application Support", "nomad_camels_data"
    )
    appdata_path = os.path.join(
        os.path.expanduser("~"), "Library", "Application Support", "nomad_camels"
    )
else:
    # Default to the home directory
    data_path = os.path.expanduser("~", "nomad_camels_data")
    appdata_path = os.path.expanduser("~", ".nomad_camels")


preset_path = os.path.join(appdata_path, "Presets")
backup_path = os.path.join(preset_path, "Backup")
save_string_list = [QComboBox, QLineEdit, QTreeView, QListView]
save_dict_skip = [
    QWidget,
    QSplitter,
    QLabel,
    QPushButton,
    QMenu,
    QMenuBar,
    QAction,
    QStatusBar,
    QGridLayout,
    QTimer,
    Evaluator,
    Signal,
    SignalInstance,
]

# Get the current operating system


standard_pref = {
    "autosave": True,
    "autosave_run": True,
    "backup_before_run": True,
    "dark_mode": False,
    "graphic_theme": "Fusion",
    "n_decimals": 3,
    "number_format": "mixed",
    "mixed_from": 3,
    "py_files_path": os.path.join(appdata_path, "python_files").replace("\\", "/"),
    "meas_files_path": data_path,
    "device_driver_path": os.path.join(
        os.getcwd(), "devices", "devices_drivers"
    ).replace("\\", "/"),
    "databroker_catalog_name": "CAMELS_CATALOG",
    "driver_repository": "https://github.com/FAU-LAP/CAMELS_drivers",
    "repo_branch": "main",
    "repo_directory": "",
    "play_camel_on_error": False,
    "auto_check_updates": False,
    "log_level": "Warning",
    "logfile_size": 1,
    "logfile_backups": 1,
    "NOMAD_URL": "",
    "backups": "smart",
    "backup_number": 30,
    "number_databroker_files": 30,
    "extension_path": os.path.join(os.getcwd(), "extensions").replace("\\", "/"),
    "extensions": [],
    "password_protection": False,
    "password_hash": "",
    "new_file_each_run": True,
    "enable_API": False,
    "API_port": "5000",
}


def update_config_path(path):
    global appdata_path, preset_path, backup_path
    appdata_path = path
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "config_path"), "w"
    ) as f:
        f.write(appdata_path)
    preset_path = os.path.join(appdata_path, "Presets")
    backup_path = os.path.join(preset_path, "Backup")
    standard_pref["py_files_path"] = os.path.join(appdata_path, "python_files").replace(
        "\\", "/"
    )
    if not os.path.isdir(appdata_path):
        makedirs(appdata_path)


def check_config_path():
    global appdata_path
    config_path_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "config_path"
    )
    if os.path.isfile(config_path_file):
        with open(config_path_file, "r") as f:
            appdata_path = f.read().strip()
    else:
        from nomad_camels.ui_widgets.path_button_edit import Path_Button_Dialog

        dialog = Path_Button_Dialog(
            path=appdata_path,
            default_dir=os.path.dirname(appdata_path),
            select_directory=True,
            title="Select path for configuration files",
            text="Please select where NOMAD CAMELS should save its configuration files",
        )
        if dialog.exec():
            appdata_path = dialog.path
        else:
            WarnPopup(
                text="No path selected, a default path will be used.\nYou can change the path in the settings.",
                title="No path selected",
                info_icon=True,
            )
    update_config_path(appdata_path)


def get_preset_list():
    """
    DEPRECATED

    returns a two list of available presets, once for devices, once
    for measurements. (files with ".predev" or ".premeas" in
    appdata_path. If the directory does not exist, it is created."""
    if isdir(preset_path):
        names = listdir(preset_path)
        if "Backup" not in names:
            makedirs(os.path.join(preset_path, "Backup"))
        presets = []
        for name in names:
            if name.endswith(".preset"):
                presets.append(name[:-7])
        return sorted(presets, key=lambda x: x.lower())
    else:
        makedirs(preset_path)
        return get_preset_list()


def autosave_preset(preset: str, preset_data, do_backup=True):
    """Saves the given preset and makes a backup of the former one in
    the backup-folder (if do_backup).

    Parameters
    ----------
    preset : str
        the name of the preset
    preset_data : dict
        data of the preset, formatted into a dictionary
    do_backup : bool, default=True
        if True, the old preset file will be copied into the backup folder, with
        timestamp
    """
    preset_file = f"{preset}.preset"
    if not os.path.isdir(preset_path):
        makedirs(preset_path)
    with open(
        os.path.join(preset_path, preset_file), "w", encoding="utf-8"
    ) as json_file:
        json.dump(preset_data, json_file, indent=2)
    if do_backup:
        make_backup(preset_file)


def save_preset(path, preset_data: dict):
    """Saves the given preset_data under the specified path.
    Further, `autosave_preset` is called.

    Parameters
    ----------
    path : str, path
        where to save the preset
    preset_data : dict
        the data of the preset, to be dumped as json
    """
    preset_name = path.split("/")[-1][:-7]
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(preset_data, json_file, indent=2)
    autosave_preset(preset_name, preset_data)


def save_dictionary(path, dictionary: dict):
    """
    Processes the given `dictionary` using `get_save_str`, then saves it as json
    to the given `path`.

    Parameters
    ----------
    path : str, path
        where to save the dictionary
    dictionary : dict
        the dictionary to be saved as json
    """
    save_dict = {}
    for key, val in dictionary.items():
        add_string = get_save_str(val)
        if add_string is not None:
            save_dict[key] = add_string
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as file:
        json.dump(save_dict, file, indent=2)


def make_backup(preset_file: str):
    """
    Puts a copy of the given `preset_file` into the backup-folder of
    the preset. The current datetime is added to the filename.

    Parameters
    ----------
    preset_file : str
        The name of the preset file. The file needs to be in the `preset_path`.
    """
    backup_save_path = os.path.join(backup_path, preset_file[:-7])
    if not isdir(backup_save_path):
        makedirs(backup_save_path)
    now = datetime.now()
    backup_name = os.path.join(
        backup_save_path, f'{now.strftime("%Y-%m-%d_%H-%M-%S")}_{preset_file}'
    )
    copyfile(os.path.join(preset_path, preset_file), backup_name)

    if not "backups" in variables_handling.preferences:
        return
    backups = sorted(glob(f"{backup_save_path}/*.preset"), key=os.path.getmtime)
    if variables_handling.preferences["backups"] == "number":
        if "backup_number" in variables_handling.preferences:
            backup_number = variables_handling.preferences["backup_number"]
            while len(backups) > backup_number:
                os.remove(backups.pop(0))
    elif variables_handling.preferences["backups"] == "smart":
        backups = [
            b
            for b in backups
            if datetime.fromtimestamp(os.path.getmtime(b)) < now - timedelta(days=7)
        ]
        for day in range(8, 31):
            day_ago = now - timedelta(days=day)
            daily_backups = [
                b
                for b in backups
                if datetime.fromtimestamp(os.path.getmtime(b)).date() == day_ago.date()
            ]
            while len(daily_backups) > 1:
                backup = daily_backups.pop(0)
                os.remove(backup)
                backups.remove(backup)
        backups = [
            b
            for b in backups
            if datetime.fromtimestamp(os.path.getmtime(b)) < now - timedelta(days=30)
        ]
        for month in range(1, 13):
            month_ago = now - timedelta(days=30 * month)
            monthly_backups = [
                b
                for b in backups
                if datetime.fromtimestamp(os.path.getmtime(b)).month == month_ago.month
            ]
            while len(monthly_backups) > 1:
                backup = monthly_backups.pop(0)
                os.remove(backup)
                backups.remove(backup)
        backups = [
            b
            for b in backups
            if datetime.fromtimestamp(os.path.getmtime(b)) < now - timedelta(days=365)
        ]
        if not backups:
            return
        for year in range(
            1, now.year - datetime.fromtimestamp(os.path.getmtime(backups[0])).year + 1
        ):
            year_ago = now - timedelta(days=365 * year)
            yearly_backups = [
                b
                for b in backups
                if datetime.fromtimestamp(os.path.getmtime(b)).year == year_ago.year
            ]
            while len(yearly_backups) > 1:
                backup = yearly_backups.pop(0)
                os.remove(backup)
                backups.remove(backup)


def load_save_dict(
    string_dict: dict,
    object_dict: dict,
    update_missing_key=False,
    remove_extra_key=False,
):
    """For all keys both given dictionaries have in common, the value of
    the object in object_dict will be updated to the corresponding value
    of the string in string_dict. Depending on the type of the objects already
    in `object_dict`, the values may be processed differently.
    The different possibilities are:

    - QComboBox: the value will be set as current text
    - QLineEdit: the value will be set as text
    - key=="protocols_dict": calls `load_protocols_dict`
    - key in ["active_devices_dict", "active_instruments"]: calls `load_devices_dict`
    - dict or hasattr "__save_dict__" or "__dict__": calls `load_save_dict` recursively
    - list: appends all the values in the list of the strings


    Parameters
    ----------
    string_dict : dict
        A dictionary containing mostly strings as loaded from a json as values.
    object_dict : dict
        The dictionary to be loaded into.
    update_missing_key : bool
        (Default value = False)
        If True, keys that are only in `string_dict`, but not in `object_dict`
        will be added as well.
    remove_extra_key : bool
        (Default value = False)
        If True, keys that are only in `object_dict`, but not in `string_dict`
        will be removed.
    """
    for key in string_dict:
        if key in object_dict:
            obj = object_dict[key]
            val = string_dict[key]
            if issubclass(type(obj), QComboBox):
                obj.setCurrentText(val)
            elif issubclass(type(obj), QLineEdit):
                obj.setText(val)
            elif key == "watchdogs":
                for w in val:
                    obj[w] = Watchdog(**val[w])
            elif key == "protocols_dict":
                load_protocols_dict(val, obj)
            elif key in ["active_devices_dict", "active_instruments"]:
                load_devices_dict(val, obj)
            elif isinstance(obj, dict):
                load_save_dict(val, obj, True, True)
            elif hasattr(obj, "__save_dict__") or hasattr(obj, "__dict__"):
                load_save_dict(val, obj.__dict__)
            elif type(obj) is list:
                obj.clear()
                for v in val:
                    obj.append(v)
        elif update_missing_key:
            object_dict.update({key: string_dict[key]})
    if remove_extra_key:
        rem_keys = []
        for key in object_dict:
            if key not in string_dict:
                rem_keys.append(key)
        for key in rem_keys:
            object_dict.pop(key)


def get_save_str(obj):
    """Utility function to create the string with which to save the
    object-data.
    If the object has the attribute __save_dict__, it is the return value.
    Objects of the types specified in save_dict_skip return None.
    QComboBox and QLineEdit return their current text.
    If `obj` is a dictionary or has the attribute `__dict__`, the values of the
    dictionary will be recursively read by `get_save_str`.
    Types str, bool and numbers are not converted.
    Arrays are converted to lists.

    Parameters
    ----------
    obj :
        The object that should be represented as string.

    Returns
    -------
    the string-representation of `obj`

    """
    if hasattr(obj, "__save_dict__"):
        make_save_dict(obj)
        return obj.__save_dict__
    if type(obj) in save_dict_skip:
        return None
    if isinstance(obj, ophyd.Device):
        return None
    if type(obj) in save_string_list:
        if issubclass(type(obj), QComboBox):
            return obj.currentText()
        if issubclass(type(obj), QLineEdit):
            return obj.text()
        return None
    if type(obj) is pd.DataFrame:
        obj.to_dict("list")
    if hasattr(obj, "__dict__") or type(obj) is dict:
        savedic = {}
        if isinstance(obj, dict):
            dictionary = obj
        else:
            dictionary = obj.__dict__
        for key in dictionary:
            if key == "py_package":
                continue
            savedic.update({key: get_save_str(dictionary[key])})
        return savedic
    if type(obj) in [int, float, bool, np.float64]:
        return obj
    if type(obj) is np.ndarray:
        obj = list(obj)
    if type(obj) is list:
        obj_list = []
        for p in obj:
            obj_list.append(get_save_str(p))
        return obj_list
    return str(obj)


def make_save_dict(obj):
    """Utility function to update the __save_dict__ of the given obj.
    Goes through all the keys in __dict__ and calls get_save_str on the
    object. Thus working recursively if an attribute of obj also has a
    `__save_dict__`.

    Parameters
    ----------
    obj :
        The object of which the `__save_dict__` should be updated.
    """
    for key in obj.__dict__:
        if key == "__save_dict__" or (
            isinstance(obj, device_class.Device)
            and key
            in [
                "controls",
                "ophyd_class",
                "ophyd_class_no_epics",
                "channels",
                "virtual",
                "tags",
                "files",
                "directory",
                "requirements",
                "ophyd_class_name",
                "connection",
            ]
        ):
            continue
        if key == "protocol" and isinstance(obj, loop_step.Loop_Step):
            continue
        add_string = get_save_str(obj.__dict__[key])
        if add_string is not None:
            obj.__save_dict__.update({key: get_save_str(obj.__dict__[key])})


def load_protocol(path):
    """
    Loads the protocol-json from the given `path` and converts it to a CAMELS
    Measurement_Protocol instance.

    Parameters
    ----------
    path : str, path
        the path, where protocol file can be found

    Returns
    -------
    Measurement_Protocol
        the protocol constructed from the data in the loaded file
    """
    prot_name = os.path.basename(path)[:-6]
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        prot_dict = json.load(f)
    prot_string_dict = {prot_name: prot_dict}
    sub_protocol = {}
    load_protocols_dict(prot_string_dict, sub_protocol)
    return sub_protocol[prot_name]


# def load_manuals_dict(string_dict, manuals_dict):
#     manuals_dict.clear()
#     for key, val in string_dict.items():
#         control_type = val['control_type']
#         control = get_manual_controls.get_control_by_type_name(control_type)


def load_protocols_dict(string_dict, prot_dict):
    """
    Specific function to construct protocols from a json string-dictionary.
    Loads the attributes of a Measurement_Protocol from the corresponding keys.

    Parameters
    ----------
    string_dict : dict{"<protocol_name>": dict}
        the dictionary with the information about the protocols (which is are
        dictinaries again)
    prot_dict : dict
        dictionary of the finished protocols
    """
    prot_dict.clear()
    for key in string_dict:
        prot_data = string_dict[key]
        prot = protocol_class.Measurement_Protocol()
        prot.name = key
        if "loop_steps" in prot_data:
            prot.load_loop_steps(prot_data["loop_steps"])
        if "plots" in prot_data:
            prot.plots = load_plots([], prot_data["plots"])
        if "filename" in prot_data:
            prot.filename = prot_data["filename"]
        if "variables" in prot_data:
            prot.variables = prot_data["variables"]
        if "metadata" in prot_data:
            prot.metadata = prot_data["metadata"]
        if "channel_metadata" in prot_data:
            prot.channel_metadata = prot_data["channel_metadata"]
        if "config_metadata" in prot_data:
            prot.config_metadata = prot_data["config_metadata"]
        if "use_nexus" in prot_data:
            prot.use_nexus = prot_data["use_nexus"]
        if "description" in prot_data:
            prot.description = prot_data["description"]
        if "export_json" in prot_data:
            prot.export_json = prot_data["export_json"]
        if "export_csv" in prot_data:
            prot.export_csv = prot_data["export_csv"]
        if "h5_during_run" in prot_data:
            prot.h5_during_run = prot_data["h5_during_run"]
        if "use_end_protocol" in prot_data:
            prot.use_end_protocol = prot_data["use_end_protocol"]
        if "end_protocol" in prot_data:
            prot.end_protocol = prot_data["end_protocol"]
        if "live_variable_update" in prot_data:
            prot.live_variable_update = prot_data["live_variable_update"]
        if "allow_live_comments" in prot_data:
            prot.allow_live_comments = prot_data["allow_live_comments"]
        prot_dict.update({key: prot})


def load_devices_dict(string_dict, devices_dict):
    """Specific function to load the dictionary of devices/instruments.
    Uses the instruments' name to import the corresponding module and create the
    instance of the instrument.

    Parameters
    ----------
    string_dict : dict{"<name>": dict}
        containing the names and information of the instruments
    devices_dict : dict
        the dictionary, where to put the loaded instruments
    """
    devices_dict.clear()
    local_packages = load_local_packages()

    path = f"{os.path.dirname(os.path.dirname(__file__))}/manual_controls/set_panel"
    sys.path.append(path)
    for key in string_dict:
        dev_data = string_dict[key]
        name = dev_data["name"]
        if name in local_packages:
            dev_lib = local_packages[name]
        else:
            try:
                dev_lib = importlib.import_module(f"nomad_camels_driver_{name}.{name}")
            except Exception as e:
                try:
                    dev_lib = importlib.import_module(f"{name}.{name}")
                except Exception as e2:
                    WarnPopup(
                        text=f'Could not import instrument module "{name}"\n{e}\n{e2}',
                        title="instrument import failed",
                    )
                    continue
                    # raise Exception(f'Could not import device module {name}\n{e}\n{e2}')
        dev = dev_lib.subclass()
        dev.name = name
        if "connection" in dev_data:
            dev.connection = dev_data["connection"]
        if "virtual" in dev_data:
            dev.virtual = dev_data["virtual"]
        if "tags" in dev_data:
            dev.tags = dev_data["tags"]
        if "files" in dev_data:
            dev.files = dev_data["files"]
        if "directory" in dev_data:
            dev.directory = dev_data["directory"]
        if "requirements" in dev_data:
            dev.requirements = dev_data["requirements"]
        if "settings" in dev_data:
            dev.settings = dev_data["settings"] or dev.settings
        if "config" in dev_data:
            dev.config = dev_data["config"] or dev.config
        if "custom_name" in dev_data:
            dev.custom_name = dev_data["custom_name"]
        if "additional_info" in dev_data:
            dev.additional_info = dev_data["additional_info"]
        devices_dict.update({key: dev})


def get_most_recent_presets(return_all=False):
    """Goes through all files in the `preset_path` and returns the newest preset.

    Returns
    -------
    preset : str
        the name of the newest preset
    """
    presets = []
    if not os.path.isdir(preset_path):
        makedirs(preset_path)
    for name in listdir(preset_path):
        if name.endswith(".preset"):
            presets.append(name)
    if preset_path is None:
        return None if not return_all else [None]
    if presets:
        presets = [
            x[:-7]
            for x in sorted(
                presets, key=lambda x: os.path.getmtime(os.path.join(preset_path, x))
            )
        ]
    else:
        return None if not return_all else [None]
    return presets[-1] if not return_all else presets


def get_preferences():
    """If a file 'preferences.json' exists in the `appdata_path`, its content
    will be loaded and returned, if no file exists, it will be created
    with an empty dictionary. Keys that are in the `standard_pref`, but not in
    the loaded preferences will be added with their default value.

    Returns
    -------
    prefs : dict
        the loaded preferences dictionary
    """
    check_config_path()
    pref_file = os.path.join(appdata_path, "preferences.json")
    if "preferences.json" not in os.listdir(appdata_path):
        with open(pref_file, "w", encoding="utf-8") as file:
            from nomad_camels.ui_widgets.path_button_edit import Path_Button_Dialog

            dialog = Path_Button_Dialog(
                path=data_path,
                default_dir=os.path.dirname(data_path),
                select_directory=True,
                title="Select data path",
                text="Please select the directory where the measurement data should be saved",
            )
            if dialog.exec():
                global standard_pref
                standard_pref["meas_files_path"] = dialog.path
            else:
                WarnPopup(
                    text="No data path selected, a default path will be used.\nYou can change the path in the settings.",
                    title="No data path selected",
                    info_icon=True,
                )
            json.dump(standard_pref, file, indent=2)
    with open(pref_file, "r", encoding="utf-8") as file:
        prefs = json.load(file)
    for key, value in standard_pref.items():
        if key not in prefs:
            prefs[key] = value
    return prefs


def save_preferences(prefs: dict):
    """Saves the given dictionary prefs as 'preferences.json' in the `appdata_path`

    Parameters
    ----------
    prefs : dict
        the preferences dictionary to be saved as json
    """
    with open(
        os.path.join(appdata_path, "preferences.json"), "w", encoding="utf-8"
    ) as file:
        json.dump(prefs, file, indent=2)
