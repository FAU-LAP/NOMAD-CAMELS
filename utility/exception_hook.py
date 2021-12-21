from traceback import print_tb
from PyQt5.QtWidgets import QMessageBox

import logging

from utility.load_save_functions import appdata_path

logging.basicConfig(filename=f'{appdata_path}/logging.log', level=logging.DEBUG)


class ErrorMessage(QMessageBox):
	def __init__(self, msg, info_text='', parent=None):
		super().__init__(parent)
		self.setWindowTitle('ERROR')
		self.setIcon(QMessageBox.Warning)
		self.setStandardButtons(QMessageBox.Ok)
		self.setText(msg)
		if info_text:
			self.setInformativeText(info_text)


def exception_hook(*exc_info):
	logging.exception(str(exc_info))
	ErrorMessage(exc_info[0].__name__, str(exc_info[1]) + '\n' + str(print_tb(exc_info[2]))).exec_()