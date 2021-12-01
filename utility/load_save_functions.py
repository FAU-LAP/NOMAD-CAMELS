import os.path
from os.path import isdir
from os import makedirs, getenv, listdir
from shutil import copyfile

from PyQt5.QtWidgets import QComboBox, QLineEdit, QWidget, QSplitter, QLabel, QPushButton, QTreeView, QListView, QMenuBar, QAction, QMenu, QStatusBar, QGridLayout, QFileDialog

from datetime import datetime
import json

appdata_path = f'{getenv("LOCALAPPDATA")}/CECS'
preset_path = f'{appdata_path}/Presets/'
backup_path = f'{preset_path}Backup/'
save_string_list = [QComboBox, QLineEdit, QTreeView, QListView]
save_dict_skip = [QWidget, QSplitter, QLabel, QPushButton, QMenu, QMenuBar, QAction, QStatusBar, QGridLayout]

def get_preset_list():
    """returns a two list of available presets, once for devices, once for measurements.
    (files with ".predev" or ".premeas" in "%localappdata%/CECS/Presets". If the directory does not exist, it is created."""
    if isdir(preset_path):
        names = listdir(preset_path)
        if 'Backup' not in names:
            makedirs(preset_path + 'Backup')
        predev = []
        premeas = []
        for name in names:
            if name.endswith('.predev'):
                predev.append(name[:-7])
            if name.endswith('.premeas'):
                premeas.append(name[:-8])
        return sorted(predev, key=lambda x: x.lower()), sorted(premeas, key=lambda x: x.lower())
    else:
        makedirs(preset_path)
        return get_preset_list()

def autosave_preset(preset:str, preset_data, devices=True):
    """Saves the given preset and makes a backup of the former one in the backup-folder.
    - preset: name of the preset to save
    - preset_data: all the data contained in the preset (usually the __save_dict__ of the MainApp)
    - devices: bool, whether to save it as .predev (if true) or .premeas (if false)"""
    if devices:
        preset_file = f'{preset}.predev'
    else:
        preset_file = f'{preset}.premeas'
    if preset_file in listdir(preset_path):
        make_backup(preset_file)
    with open(f'{preset_path}{preset_file}', 'w') as json_file:
        json.dump(preset_data, json_file)

def save_preset(path:str, preset_data:dict):
    """Saves the given preset_data under the specified path.
    If the path ends with '.predev', the following autosave_preset of the saved data will be called with devices=True, otherwise devices=False."""
    devs = False
    if path.endswith('.predev'):
        devs = True
    with open(path, 'w') as json_file:
        json.dump(preset_data, json_file)
    preset_name = path.split('/')[-1][:-7]
    autosave_preset(preset_name, preset_data, devs)


def make_backup(preset_file:str):
    """Puts a copy of the given preset_file into the backup-folder of the preset. The current datetime is added to the filename."""
    if preset_file.endswith('.predev'):
        backup_save_path = f'{backup_path}{preset_file[:-7]}_dev/'
    else:
        backup_save_path = f'{backup_path}{preset_file[:-8]}_meas/'
    if not isdir(backup_save_path):
        makedirs(backup_save_path)
    now = datetime.now()
    backup_name = f'{backup_save_path}{now.strftime("%Y-%m-%d_%H-%M-%S")}_{preset_file}'
    copyfile(f'{preset_path}{preset_file}', backup_name)

def load_save_dict(string_dict:dict, object_dict:dict, update_missing_key=False, remove_extra_key=False):
    """For all keys both given dictionaries have in common, the value of the object in object_dict will be updated to the corresponding value of the string in string_dict.
    - string_dict: dictionary with strings that should become the new values.
    - object_dict: dictionary with the objects that should be updated."""
    for key in string_dict:
        if key in object_dict:
            obj = object_dict[key]
            val = string_dict[key]
            if issubclass(type(obj), QComboBox):
                obj.setCurrentText(val)
            elif issubclass(type(obj), QLineEdit):
                obj.setText(val)
            elif hasattr(obj, '__save_dict__') or hasattr(obj, '__dict__'):
                load_save_dict(val, obj.__dict__)
            elif type(obj) is dict:
                load_save_dict(val, obj, True, True)
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
    """Utility function to create the string with which to save the object-data.
    If the object has the attribute __save_dict__, it is the return value.
    Objects of the types specified in save_dict_skip return None.
    QComboBox and QLineEdit return their current text.
    If None of the above, an object with the attribute __dict__ will return that, otherwise the string of obj is returned."""
    if hasattr(obj, '__save_dict__'):
        make_save_dict(obj)
        return obj.__save_dict__
    if type(obj) in save_dict_skip:
        return None
    if type(obj) in save_string_list:
        if issubclass(type(obj), QComboBox):
            return obj.currentText()
        if issubclass(type(obj), QLineEdit):
            return obj.text()
        return None
    if hasattr(obj, '__dict__') or type(obj) is dict:
        savedic = {}
        if hasattr(obj, '__dict__'):
            dictionary = obj.__dict__
        else:
            dictionary = obj
        for key in dictionary:
            savedic.update({key: get_save_str(dictionary[key])})
        return savedic
    elif type(obj) in [list, int, float, bool]:
        return obj
    return str(obj)

def make_save_dict(obj):
    """Utility function to update the __save_dict__ of the given obj.
    Goes through all the keys in __dict__ and calls get_save_str on the object.
    Thus working recursively if an attribute of obj also has a __save_dict__"""
    for key in obj.__dict__:
        if key == '__save_dict__':
            continue
        add_string = get_save_str(obj.__dict__[key])
        if add_string is not None:
            obj.__save_dict__.update({key: get_save_str(obj.__dict__[key])})

def get_most_recent_presets():
    """Goes through all files in the preset_path and returns the newest device-preset and measurement-preset.
    :returns
        - pred: name of the newest device-preset, returns None, if none found
        - prem: name of the neweset measurement-preset, returns None, if none found"""
    predevs = []
    premeas = []
    for name in listdir(preset_path):
        if name.endswith('.predev'):
            predevs.append(name)
        elif name.endswith('.premeas'):
            premeas.append(name)
    if predevs:
        pred = sorted(predevs, key=lambda x: os.path.getmtime(f'{preset_path}{x}'))[-1][:-7]
    else:
        pred = None
    if premeas:
        prem = sorted(premeas, key=lambda x: os.path.getmtime(f'{preset_path}{x}'))[-1][:-8]
    else:
        prem = None
    return pred, prem

def get_preferences():
    """If a file 'preferences.json' exists in the appdata, its content will be loaded and returned, if no file exists, it will be created with an empty dictionary."""
    if 'preferences.json' not in os.listdir(appdata_path):
        with open(f'{appdata_path}/preferences.json', 'w') as file:
            json.dump({}, file)
    with open(f'{appdata_path}/preferences.json', 'r') as file:
        prefs = json.load(file)
    return prefs

def save_preferences(prefs:dict):
    """Saves the given dictionary prefs as 'preferences.json' in the appdata."""
    with open(f'{appdata_path}/preferences.json', 'w') as file:
        json.dump(prefs, file)

