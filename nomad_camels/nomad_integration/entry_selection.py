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
from PySide6.QtCore import Qt

import yaml

from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.nomad_integration import nomad_communication


class EntrySelector(QDialog):
    def __init__(self, parent=None, selection="Sample"):
        super().__init__(parent)
        self.reloading = False
        self.setWindowTitle(f"Select {selection}")
        self.entry_metadata = []
        self.entry_names = []
        self.entry_uploads = []
        self.entry_types = []
        self.entry_data = []

        label_entry_scope = QLabel("Entry Scope:")
        self.comboBox_entry_scope = QComboBox()
        self.comboBox_entry_scope.addItems(["shared", "user"])
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

        self.update_entries()
        self.entry_filtering()
        self.entry_change()
        self.upload_box.currentTextChanged.connect(self.entry_filtering)
        self.entry_type_box.currentTextChanged.connect(self.entry_filtering)
        self.entry_box.currentTextChanged.connect(self.entry_change)
        self.comboBox_entry_scope.currentTextChanged.connect(self.update_entries)

        self.return_data = {}

        self.adjustSize()

    def update_entries(self):
        self.setCursor(Qt.WaitCursor)
        self.setEnabled(False)
        entries = nomad_communication.get_entries(
            self.parent, owner=self.comboBox_entry_scope.currentText()
        )["data"]
        if not entries:
            raise Exception("No Entries found!")
        self.reloading = True
        self.entry_metadata.clear()
        self.entry_names.clear()
        self.entry_uploads.clear()
        self.entry_types.clear()
        self.entry_data.clear()
        for entry in entries:
            if "archive" not in entry:
                continue
            arch = entry["archive"]
            if "data" not in arch:
                continue
            self.entry_data.append(arch["data"])
            self.entry_metadata.append(arch["metadata"])
            self.entry_names.append(arch["metadata"]["entry_name"])
            self.entry_types.append(arch["metadata"]["entry_type"])
            if "upload_name" in arch["metadata"]:
                self.entry_uploads.append(arch["metadata"]["upload_name"])
            else:
                self.entry_uploads.append(arch["metadata"]["upload_id"])

        self.upload_box.clear()
        self.upload_box.addItems(sorted(list(set(self.entry_uploads))))

        self.entry_type_box.clear()
        self.entry_type_box.addItems(sorted(list(set(self.entry_types))))

        self.entry_box.clear()
        self.entry_box.addItems(sorted(self.entry_names))
        self.entry_filtering()
        self.entry_change()
        self.reloading = False
        self.setEnabled(True)
        self.setCursor(Qt.ArrowCursor)

    def entry_filtering(self):
        if self.reloading:
            return
        upload = self.upload_box.currentText()
        entry_type = self.entry_type_box.currentText()
        entries = []
        for i, entry in enumerate(self.entry_names):
            if upload == self.entry_uploads[i] and entry_type == self.entry_types[i]:
                entries.append(entry)
        self.entry_box.clear()
        self.entry_box.addItems(entries)

    def entry_change(self):
        if self.reloading:
            return
        self.entry_info.setText(yaml.dump(self.get_current_entry_data()))

    def get_current_entry_data(self, include_metadata=False):
        entry = self.entry_box.currentText()
        for i, ent in enumerate(self.entry_names):
            if ent == entry:
                if include_metadata:
                    data = dict(self.entry_data[i])
                    data["NOMAD_entry_metadata"] = dict(self.entry_metadata[i])
                    return data
                return dict(self.entry_data[i])
        return {}

    def accept(self):
        self.return_data = self.get_current_entry_data(True)
        if "name" not in self.return_data and "Name" not in self.return_data:
            self.return_data["name"] = self.entry_box.currentText().split(".")[0]
        self.return_data["ELN-service"] = "nomad"
        self.return_data["full_identifier"] = (
            f'upload/id/{self.return_data["NOMAD_entry_metadata"]["upload_id"]}/entry/id/{self.return_data["NOMAD_entry_metadata"]["entry_id"]}'
        )
        lab_id = self.return_data.get("lab_id", None)
        if lab_id:
            self.return_data["identifier"] = self.return_data["lab_id"]
        else:
            self.return_data["identifier"] = (
                f'upload/id/{self.return_data["NOMAD_entry_metadata"]["upload_id"]}/entry/id/{self.return_data["NOMAD_entry_metadata"]["entry_id"]}'
            )
        super().accept()
