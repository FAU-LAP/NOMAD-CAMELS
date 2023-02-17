from PyQt5.QtWidgets import QDialog

from gui.pass_ask import Ui_Pass_Ask

class Pass_Ask(QDialog, Ui_Pass_Ask):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)