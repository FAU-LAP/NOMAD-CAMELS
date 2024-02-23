from PySide6.QtWidgets import QMessageBox


class WarnPopup(QMessageBox):
    """ """

    def __init__(self, parent=None, text="", title="", info_icon=False):
        super().__init__(parent=parent)
        self.setText(text)
        self.setWindowTitle(f"{title} - NOMAD CAMELS")
        print(text)
        if info_icon:
            self.setIcon(QMessageBox.Information)
        else:
            self.setIcon(QMessageBox.Warning)
        self.exec()
