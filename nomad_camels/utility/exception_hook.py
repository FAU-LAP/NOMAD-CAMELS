from traceback import print_tb
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QUrl

from PySide6.QtMultimedia import QSoundEffect

import logging

from bluesky.utils import RunEngineInterrupted

from nomad_camels.utility import variables_handling
from pkg_resources import resource_filename

# imported, so that it is run once, before the logging in
# `exception_hook` is connected
from nomad_camels.utility import logging_settings




class ErrorMessage(QMessageBox):
    """A popUp-box describing an Error.

    Parameters
    ----------
    msg : str
        the error message
    info_text : str
        A longer text, explaining the error (usually traceback)
    parent : QWidget
        The parent widget of this Messagebox
    """
    def __init__(self, msg, info_text='', parent=None):
        super().__init__(parent)
        self.setWindowTitle('ERROR')
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)
        self.setText(msg)
        print(msg)
        print(info_text)
        if info_text:
            self.setInformativeText(info_text)


def exception_hook(*exc_info):
    """Used to overwrite sys.excepthook, so that an exception does not
    terminate the program, but simply shows a Message with the exception.
    If the Exception is a KeyboardInterrupt, it does nothing, so that the
    interrupt may actually stop the program execution.

    Parameters
    ----------
    *exc_info : tuple(class, Exception, traceback)
        The information for the exception.
    """
    if issubclass(exc_info[0], KeyboardInterrupt):
        return
    elif issubclass(exc_info[0], RunEngineInterrupted):
        return
    logging.exception(f'{exc_info[1]} - {print_tb(exc_info[2])}')
    if variables_handling.preferences['play_camel_on_error']:
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(resource_filename('nomad_camels','graphics/Camel-Groan-2-QuickSounds.com.wav')))
        effect.play()
    ErrorMessage(exc_info[0].__name__, str(exc_info[1]) + '\n' + str(print_tb(exc_info[2]))).exec()
