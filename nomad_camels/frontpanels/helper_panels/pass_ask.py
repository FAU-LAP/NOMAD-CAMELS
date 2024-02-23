from PySide6.QtWidgets import QDialog

from nomad_camels.gui.pass_ask import Ui_Pass_Ask


class Pass_Ask(Ui_Pass_Ask, QDialog):
    """ """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
