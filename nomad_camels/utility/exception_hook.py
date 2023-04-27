import os.path
from traceback import print_tb
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QUrl

from PySide6.QtMultimedia import QSoundEffect

import logging

from nomad_camels.utility.load_save_functions import appdata_path

from bluesky.utils import RunEngineInterrupted

from nomad_camels.utility import variables_handling
from pkg_resources import resource_filename

if not os.path.isfile(f'{appdata_path}/logging.log'):
	with open(f'{appdata_path}/logging.log', 'w'):
		pass
logging.basicConfig(filename=f'{appdata_path}/logging.log', level=logging.DEBUG)


class ErrorMessage(QMessageBox):
	"""A popUp-box describing the Error."""
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
	"""Use to overwrite sys.excepthook, so that an exception does not
	terminate the program, but simply shows a Message with the exception."""
	if issubclass(exc_info[0], KeyboardInterrupt):
		return
	elif issubclass(exc_info[0], RunEngineInterrupted):
		return
	logging.exception(str(exc_info))
	if variables_handling.preferences['play_camel_on_error']:
		effect = QSoundEffect()
		effect.setSource(QUrl.fromLocalFile(resource_filename('nomad_camels','graphics/Camel-Groan-2-QuickSounds.com.wav')))
		effect.play()
	ErrorMessage(exc_info[0].__name__, str(exc_info[1]) + '\n' + str(print_tb(exc_info[2]))).exec()
