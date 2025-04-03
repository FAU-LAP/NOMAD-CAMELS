import os.path
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QGridLayout,
    QDialogButtonBox,
    QComboBox,
    QTextEdit,
)
from PySide6.QtCore import Qt, QThread, Signal

import yaml

from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.nomad_integration import nomad_communication


class EntrySelector(QDialog):
    def __init__(self, parent=None, selection="Sample"):
        super().__init__(parent)
        self.reloading = False
        self._window_title = f"Select {selection} - NOMAD CAMELS"
        self.setWindowTitle(self._window_title)
        self.upload_names = []
        self.upload_ids = []
        self.entry_ids = []
        self.entry_names = []
        self.entry_types = []
        self.entry_data = {}
        self.entry_metadata = {}

        label_entry_scope = QLabel("Entry Scope:")
        self.comboBox_entry_scope = QComboBox()
        self.comboBox_entry_scope.addItems(["all", "shared", "user"])
        self.comboBox_entry_scope.setCurrentText("user")
        self.comboBox_entry_scope.setToolTip(
            "shared: Entries that belong to you or are shared with you.\nuser: Entries that belong to you."
        )

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        label_upload = QLabel("Upload:")
        self.upload_box = QComboBox()

        label_entry_type = QLabel("Entry Type:")
        self.entry_type_box = QComboBox()

        label_entry = QLabel("Entry:")
        self.entry_box = QComboBox()

        self.entry_info = QTextEdit()
        self.entry_info.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse
        )

        layout = QGridLayout()
        layout.addWidget(label_entry_scope, 0, 0)
        layout.addWidget(self.comboBox_entry_scope, 0, 1)
        layout.addWidget(label_upload, 1, 0)
        layout.addWidget(self.upload_box, 1, 1)
        layout.addWidget(label_entry_type, 2, 0)
        layout.addWidget(self.entry_type_box, 2, 1)
        layout.addWidget(label_entry, 10, 0)
        layout.addWidget(self.entry_box, 10, 1)
        layout.addWidget(self.entry_info, 0, 2, 12, 1)
        layout.addWidget(self.button_box, 20, 0, 1, 3)
        self.setLayout(layout)

        self._uploads_getter_thread = Upload_Getter_Thread(
            self, upload_names=self.upload_names, upload_ids=self.upload_ids
        )
        self._uploads_getter_thread.exception_signal.connect(self._propagate_exception)
        self._uploads_getter_thread.finished.connect(self._update_uploads_finished)

        self._entries_getter_thread = Entries_Getter_Thread(
            self,
            entry_types=self.entry_types,
            entry_names=self.entry_names,
            entry_ids=self.entry_ids,
        )
        self._entries_getter_thread.exception_signal.connect(self._propagate_exception)
        self._entries_getter_thread.finished.connect(self._update_entries_finished)

        self.update_uploads()
        self.entry_filtering()
        self.entry_change()
        self.upload_box.currentTextChanged.connect(self.update_entries)
        self.entry_type_box.currentTextChanged.connect(self.entry_filtering)
        self.entry_box.currentTextChanged.connect(self.entry_change)
        self.comboBox_entry_scope.currentTextChanged.connect(self.update_uploads)

        self.return_data = {}

        self.adjustSize()
        # self.resize(800, 600)

    def _propagate_exception(self, exception):
        """Propagate exceptions from the thread to the main thread."""
        raise exception

    def update_uploads(self):
        self.setEnabled(False)
        self.setCursor(Qt.WaitCursor)
        self.setWindowTitle("communicating with NOMAD...")
        self.reloading = True
        self._uploads_getter_thread.set_scope(self.comboBox_entry_scope.currentText())
        self._uploads_getter_thread.start()

    def _update_uploads_finished(self):
        self.upload_names = self._uploads_getter_thread.upload_names
        self.upload_ids = self._uploads_getter_thread.upload_ids

        self.upload_box.clear()
        self.upload_box.addItems(sorted(self.upload_names))

        self.reloading = False
        self.update_entries()

    def update_entries(self):
        if self.reloading:
            return
        self.setEnabled(False)
        self.setCursor(Qt.WaitCursor)
        self.setWindowTitle("communicating with NOMAD...")
        self.reloading = True
        upload_name = self.upload_box.currentText()
        index = self.upload_names.index(upload_name)
        upload_id = self.upload_ids[index]
        self._entries_getter_thread.set_upload_id(upload_id)
        self._entries_getter_thread.start()

    def _update_entries_finished(self):
        self.entry_names = self._entries_getter_thread.entry_names
        self.entry_types = self._entries_getter_thread.entry_types
        self.entry_ids = self._entries_getter_thread.entry_ids

        self.entry_type_box.clear()
        self.entry_type_box.addItems(sorted(list(set(self.entry_types))))

        self.reloading = False
        self.entry_filtering()
        self.setEnabled(True)
        self.setWindowTitle(self._window_title)
        self.setCursor(Qt.ArrowCursor)

    def entry_filtering(self):
        if self.reloading:
            return
        entry_type = self.entry_type_box.currentText()
        entries = []
        for i, entry in enumerate(self.entry_names):
            if entry_type == self.entry_types[i]:
                entries.append(entry)
        self.reloading = True
        self.entry_box.clear()
        self.entry_box.addItems(entries)
        self.reloading = False
        self.entry_change()

    def entry_change(self):
        if self.reloading:
            return
        self.update_current_entry_data()
        self.entry_info.setText(yaml.dump(self.entry_data))

    def update_current_entry_data(self):
        entry_name = self.entry_box.currentText()
        entry_id = self.entry_ids[self.entry_names.index(entry_name)]
        entry_archive = nomad_communication.get_entry_archive(
            parent=self, entry_id=entry_id
        )
        self.entry_data = dict(entry_archive.get("data", {}))
        self.entry_metadata = dict(entry_archive.get("metadata", {}))

    def accept(self):
        from nomad_camels.nomad_integration.nomad_communication import nomad_url

        self.return_data = self.entry_data
        self.return_data["NOMAD_entry_metadata"] = self.entry_metadata
        if "name" not in self.return_data and "Name" not in self.return_data:
            self.return_data["name"] = self.entry_box.currentText().split(".")[0]
        self.return_data["ELN-service"] = "nomad"
        self.return_data["full_identifier"] = (
            f'{nomad_url}/upload/id/{self.return_data["NOMAD_entry_metadata"]["upload_id"]}/entry/id/{self.return_data["NOMAD_entry_metadata"]["entry_id"]}'
        )
        lab_id = self.return_data.get("lab_id", None)
        if lab_id:
            self.return_data["identifier"] = self.return_data["lab_id"]
        else:
            self.return_data["identifier"] = (
                f'{nomad_url}/upload/id/{self.return_data["NOMAD_entry_metadata"]["upload_id"]}/entry/id/{self.return_data["NOMAD_entry_metadata"]["entry_id"]}'
            )
        super().accept()


class Entries_Getter_Thread(QThread):
    exception_signal = Signal(Exception)

    def __init__(
        self,
        parent=None,
        entry_names=None,
        entry_types=None,
        entry_ids=None,
        upload_id=None,
    ):
        super().__init__(parent)
        self.parent = parent
        self.entry_names = entry_names or []
        self.entry_types = entry_types or []
        self.entry_ids = entry_ids or []
        self.upload_id = upload_id or ""

    def set_upload_id(self, upload_id):
        """Update the current upload ID."""
        self.upload_id = upload_id

    def run(self):
        try:
            entries = nomad_communication.get_entries_from_upload(
                self.upload_id, self.parent
            )
            self.entry_names.clear()
            self.entry_types.clear()
            for entry in entries:
                if "entry_metadata" not in entry:
                    continue
                metadata = entry["entry_metadata"]
                if (
                    not "entry_name" in metadata
                    or not "entry_type" in metadata
                    or not metadata["entry_name"]
                    or not metadata["entry_type"]
                ):
                    continue
                self.entry_names.append(metadata["entry_name"])
                self.entry_types.append(metadata["entry_type"])
                self.entry_ids.append(metadata["entry_id"])
        except Exception as e:
            self.exception_signal.emit(e)


class Upload_Getter_Thread(QThread):
    exception_signal = Signal(Exception)

    def __init__(
        self,
        parent=None,
        scope="user",
        upload_names=None,
        upload_ids=None,
    ):
        super().__init__(parent)
        self.scope = scope
        self.parent = parent
        self.upload_names = upload_names or []
        self.upload_ids = upload_ids or []

    def set_scope(self, scope):
        """Update the scope of the thread."""
        self.scope = scope

    def run(self):
        try:
            uploads = nomad_communication.get_user_uploads(
                parent=self.parent, scope=self.scope
            )
            self.upload_ids.clear()
            self.upload_names.clear()
            for upload in uploads:
                if "upload_name" in upload:
                    self.upload_names.append(upload["upload_name"])
                else:
                    self.upload_names.append(upload["upload_id"])
                self.upload_ids.append(upload["upload_id"])
        except Exception as e:
            self.exception_signal.emit(e)
