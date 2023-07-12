"""This module takes care of all the settings regarding logging to a logfile.
The logfile is put into the `appdata_path`, a filehandler with specific
formatting is added to logging's app_log"""


import logging
from logging.handlers import RotatingFileHandler

from nomad_camels.utility.load_save_functions import appdata_path
from nomad_camels.utility import variables_handling
from nomad_camels.utility.load_save_functions import standard_pref

log_levels = {'All': logging.NOTSET,
              'Debug': logging.DEBUG,
              'Info': logging.INFO,
              'Warning': logging.WARNING,
              'Error': logging.ERROR,
              'Critical': logging.CRITICAL}


logfile = f'{appdata_path}/logging.log'
my_handler = RotatingFileHandler(logfile, mode='a')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
my_handler.setFormatter(log_formatter)

app_log = logging.getLogger('root')
app_log.addHandler(my_handler)

def update_log_settings():
    """Reads the logging settings from the current preferences and sets them for
    the logfile-handler. Including: the level of logging, the maximum size for
    the logfile, the number of old logfiles, when one is full. """
    prefs = variables_handling.preferences
    if 'log_level' in prefs and prefs['log_level']:
        log_level = prefs['log_level']
    else:
        log_level = standard_pref['log_level']
    if 'logfile_size' in prefs and prefs['logfile_size']:
        logfile_size = prefs['logfile_size']
    else:
        logfile_size = standard_pref['logfile_size']
    if 'logfile_backups' in prefs:
        logfile_backups = prefs['logfile_backups']
    else:
        logfile_backups = standard_pref['logfile_backups']

    my_handler.backupCount = logfile_backups
    my_handler.maxBytes = logfile_size * 1024 * 1024
    if log_level in log_levels:
        log_lv = log_levels[log_level]
    else:
        log_lv = logging.NOTSET
    my_handler.setLevel(log_lv)
    app_log.setLevel(log_lv)


update_log_settings()
