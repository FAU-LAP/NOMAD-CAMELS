"""This module takes care of all the settings regarding logging to a logfile.
The logfile is put into the `appdata_path`, a filehandler with specific
formatting is added to logging's app_log"""

import logging
import os
from logging.handlers import RotatingFileHandler

from nomad_camels.utility import load_save_functions
from nomad_camels.utility import variables_handling
from nomad_camels.utility.load_save_functions import standard_pref

log_levels = {
    "All": logging.NOTSET,
    "Debug": logging.DEBUG,
    "Info": logging.INFO,
    "Warning": logging.WARNING,
    "Error": logging.ERROR,
    "Critical": logging.CRITICAL,
}

my_handler = None


def update_log_settings():
    """Reads the logging settings from the current preferences and sets them for
    the logfile-handler. Including: the level of logging, the maximum size for
    the logfile, the number of old logfiles, when one is full."""
    global my_handler
    logfile = os.path.join(load_save_functions.appdata_path, "nomad_camels.log")
    if not os.path.isfile(logfile):
        if not os.path.isdir(load_save_functions.appdata_path):
            os.makedirs(load_save_functions.appdata_path)
        with open(logfile, "w") as f:
            pass
    app_log = logging.getLogger("root")
    if my_handler is None:
        my_handler = RotatingFileHandler(
            logfile,
            mode="a",
            maxBytes=standard_pref["logfile_size"] * 1024 * 1024,
            backupCount=standard_pref["logfile_backups"],
        )

        log_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        my_handler.setFormatter(log_formatter)

        app_log.addHandler(my_handler)

    my_handler.baseFilename = logfile

    prefs = variables_handling.preferences
    if "log_level" in prefs and prefs["log_level"]:
        log_level = prefs["log_level"]
    else:
        log_level = standard_pref["log_level"]
    if "logfile_size" in prefs and prefs["logfile_size"]:
        logfile_size = prefs["logfile_size"]
    else:
        logfile_size = standard_pref["logfile_size"]
    if "logfile_backups" in prefs:
        logfile_backups = prefs["logfile_backups"]
    else:
        logfile_backups = standard_pref["logfile_backups"]

    my_handler.backupCount = logfile_backups
    my_handler.maxBytes = logfile_size * 1024 * 1024
    if log_level in log_levels:
        log_lv = log_levels[log_level]
    else:
        log_lv = logging.NOTSET
    my_handler.setLevel(log_lv)
    app_log.setLevel(log_lv)


update_log_settings()
