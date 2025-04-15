from traceback import format_tb, print_tb, format_exception
from PySide6.QtWidgets import QMessageBox, QTextEdit, QPushButton, QVBoxLayout
from PySide6.QtCore import QUrl

from PySide6.QtMultimedia import QSoundEffect

import logging

from bluesky.utils import RunEngineInterrupted

from nomad_camels.utility import variables_handling
from importlib import resources
from nomad_camels import graphics

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

    def __init__(self, exc_info, parent=None):
        tb = format_tb(exc_info[2])
        formatted_exc = "".join(format_exception(exc_info[0], exc_info[1], exc_info[2]))
        print_tb(exc_info[2])
        msg = str(exc_info[0].__name__)
        info_text = str(exc_info[1])
        logging.exception(formatted_exc)
        print(msg)
        print(info_text)
        super().__init__(parent)
        self.setWindowTitle("ERROR")
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)
        self.setText(msg)
        if info_text:
            self.setInformativeText(info_text)

        self.more_info_button = QPushButton("more information")
        self.more_info_button.clicked.connect(self.show_more_info)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setVisible(False)
        self.text_edit.setPlainText("".join(tb))

        self.layout().addWidget(self.more_info_button, 3, 0, 1, 5)
        self.layout().addWidget(self.text_edit, 2, 0, 1, 5)
        self.layout().addWidget(self.button(QMessageBox.Ok), 4, 0, 1, 5)
        self.showing_more_info = False
        self.adjustSize()

    def show_more_info(self):
        if self.showing_more_info:
            self.text_edit.setVisible(False)
            self.more_info_button.setText("more information")
            self.adjustSize()
            self.showing_more_info = False
        else:
            self.text_edit.setVisible(True)
            self.more_info_button.setText("hide additional information")
            self.text_edit.setMinimumHeight(500)
            self.text_edit.setMinimumWidth(800)
            self.showing_more_info = True
        self.adjustSize()


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
    if variables_handling.preferences["play_camel_on_error"]:
        try:
            effect = QSoundEffect()
            effect.setSource(
                QUrl.fromLocalFile(
                    str(resources.files(graphics) / "Camel-Groan-2-QuickSounds.com.wav")
                )
            )
            effect.play()
        except Exception as e:
            print(e)
    ErrorMessage(exc_info).exec()
