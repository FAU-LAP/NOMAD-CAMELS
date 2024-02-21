from nomad_camels.gui.enterTextDialog import Ui_EnterTextDialog
from PySide6.QtWidgets import QDialog


class EnterTextDialog(Ui_EnterTextDialog, QDialog):
    """A simple QDialog-Box that has the value of the entered textbox in "self.value".

    - parent: parent-widget, passed to QDialog
    - window_title: The title of the pop-up window
    - label: The label shown in front of the QLineEdit

    Parameters
    ----------

    Returns
    -------

    """

    def __init__(self, parent=None, window_title="", label=""):
        super(EnterTextDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(window_title)
        self.label.setText(label)
        self.value = None

    def accept(self) -> None:
        """ """
        self.value = self.lineEdit_text.text()
        super().accept()
