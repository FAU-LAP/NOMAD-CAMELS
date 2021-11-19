from traceback import print_tb
from PyQt5.QtWidgets import QMessageBox

class ErrorMessage(QMessageBox):
	def __init__(self, msg, info_text='', parent=None):
		super().__init__(parent)
		self.setWindowTitle('ERROR')
		self.setIcon(QMessageBox.Warning)
		self.setStandardButtons(QMessageBox.Ok)
		self.setText(msg)
		if info_text:
			self.setInformativeText(info_text)


def exception_hook(exctype, value, tb):
	ErrorMessage(exctype.__name__, str(value) + '\n' + str(print_tb(tb))).exec_()