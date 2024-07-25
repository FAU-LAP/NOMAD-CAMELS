from PySide6.QtWidgets import QMessageBox


class WarnPopup(QMessageBox):
    """ """

    def __init__(
        self, parent=None, text="", title="", info_icon=False, do_not_pause=False
    ):
        super().__init__(parent=parent)
        self.setText(text)
        self.setWindowTitle(f"{title} - NOMAD CAMELS")
        print(text)
        self.clicked_by_user = False
        if info_icon:
            self.setIcon(QMessageBox.Information)
        else:
            self.setIcon(QMessageBox.Warning)
        self.accepted.connect(self.ok_clicked)
        if do_not_pause:
            self.show()
        else:
            self.exec()

    def ok_clicked(self):
        self.clicked_by_user = True
