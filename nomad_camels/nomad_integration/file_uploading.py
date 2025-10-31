import os.path
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QGridLayout,
    QDialogButtonBox,
    QComboBox,
)
from PySide6.QtCore import QThread
import traceback
import logging
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.nomad_integration import nomad_communication


class UploadDialog(QDialog):
    """UI widget to handle uploading data to NOMAD."""

    def __init__(self, parent=None, file_set="", upload_path=""):
        super().__init__(parent)

        label_file = QLabel("File:")
        self.pathEdit_file = Path_Button_Edit(self, file_set)

        label_upload = QLabel("Upload:")
        self.combobox_upload = QComboBox()
        uploads = nomad_communication.get_user_upload_names(self)
        self.combobox_upload.addItems(uploads)

        label_upload_path = QLabel("Directory in upload:")
        if upload_path:
            self.lineEdit_upload_path = QLineEdit(upload_path)
        else:
            self.lineEdit_upload_path = QLineEdit("CAMELS_data")

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QGridLayout()

        layout.addWidget(label_file, 10, 0)
        layout.addWidget(self.pathEdit_file, 10, 1)
        layout.addWidget(label_upload, 11, 0)
        layout.addWidget(self.combobox_upload, 11, 1)

        layout.addWidget(label_upload_path, 13, 0)
        layout.addWidget(self.lineEdit_upload_path, 13, 1)

        layout.addWidget(self.button_box, 20, 0, 1, 2)

        self.setLayout(layout)
        if file_set:
            mid = os.path.basename(file_set) + " "
            self.pathEdit_file.setHidden(True)
            label_file.setHidden(True)
        else:
            mid = ""
        self.setWindowTitle(f"Upload {mid}to NOMAD")
        self.adjustSize()
        self.exec()

    def accept(self) -> None:
        """ "Before calling the super method, the upload is done."""
        f = self.pathEdit_file.get_path()
        upload = self.combobox_upload.currentText()
        path = self.lineEdit_upload_path.text()
        nomad_communication.upload_file(f, upload, path)
        super().accept()

class UploadThread(QThread):
    """
    QThread wrapper to run nomad_communication.upload_file in a background thread.
    Emits 'success' with the response object on success and 'error' with a string
    on failure.
    """

    def __init__(self, file_path, upload_name, upload_path, parent_widget=None):
        super().__init__(parent=parent_widget)
        self.file_path = file_path
        self.upload_name = upload_name
        self.upload_path = upload_path
        # keep a reference to the UI parent (MainWindow) to pass to ensure_login if needed
        self.parent_widget = parent_widget

    def run(self):
        try:
            # import inside thread to avoid any UI-thread import side effects
            from nomad_camels.nomad_integration import nomad_communication
            resp = nomad_communication.upload_file(
                self.file_path, self.upload_name, self.upload_path, parent=self.parent_widget
            )
        except Exception:
            tb = traceback.format_exc()
            logging.error(f"UploadThread failed:\n{tb}")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = UploadDialog()
    dialog.exec()
