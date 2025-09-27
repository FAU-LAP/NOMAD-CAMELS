import os.path
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QSpacerItem,
    QGridLayout,
    QDialogButtonBox,
    QComboBox,
    QTextEdit,
    QSizePolicy,
    QMessageBox,
)
from PySide6.QtCore import Qt, QTimer
import yaml

from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.nomad_integration import nomad_communication
import re


def compute_combo_max_width(combo):
    fm = combo.fontMetrics()
    if not combo.count():
        return fm.horizontalAdvance("W" * 8) + 40
    else:
        max_width = max(
            fm.horizontalAdvance(combo.itemText(i)) for i in range(combo.count())
        )
        return max_width + 40


class EntrySelector(QDialog):
    def __init__(self, parent=None, selection="Sample", upload_id=None, entry_id=None):
        super().__init__(parent)
        self._window_title = f"Select {selection} - NOMAD CAMELS"
        self.setWindowTitle(self._window_title)

        self.upload_names = []
        self.upload_ids = []
        self.entry_names = []
        self.entry_types = []
        self.entry_ids = []
        self.entry_data = {}
        self.entry_metadata = {}
        self.last_upload_id = upload_id
        self.last_entry_id = entry_id
        self.reloading = False

        # --- widgets ---
        label_scope = QLabel("Entry Scope:")
        self.combo_scope = QComboBox()
        self.combo_scope.addItems(["all", "shared", "user"])
        self.combo_scope.setCurrentText("user")
        self.combo_scope.setToolTip(
            "all: every shared entry.\nshared: yours + shared to you.\nuser: only yours."
        )

        label_upload = QLabel("Upload:")
        self.upload_box = QComboBox()

        label_type = QLabel("Entry Type:")
        self.type_box = QComboBox()

        label_entry = QLabel("Entry:")
        self.entry_box = QComboBox()

        self.entry_info = QTextEdit()
        self.entry_info.setReadOnly(True)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.ok_button = self.button_box.button(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # --- layout ---
        layout = QGridLayout(self)
        layout.addWidget(label_scope, 0, 0)
        layout.addWidget(self.combo_scope, 1, 0)
        layout.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 0
        )
        layout.addWidget(label_upload, 3, 0)
        layout.addWidget(self.upload_box, 4, 0)
        layout.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 5, 0
        )
        layout.addWidget(label_type, 6, 0)
        layout.addWidget(self.type_box, 7, 0)
        layout.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding), 8, 0
        )
        layout.addWidget(label_entry, 10, 0)
        layout.addWidget(self.entry_box, 11, 0)
        layout.addWidget(self.entry_info, 0, 2, 12, 1)
        layout.addWidget(self.button_box, 20, 0, 1, 3)

        for w in (self.combo_scope, self.upload_box, self.type_box, self.entry_box):
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # --- signals ---
        self.combo_scope.currentTextChanged.connect(self.update_uploads)
        self.upload_box.currentTextChanged.connect(self.update_entries)
        self.type_box.currentTextChanged.connect(self.entry_filtering)
        self.entry_box.currentTextChanged.connect(self.entry_change)

        # start first load after widget is shown
        QTimer.singleShot(0, self.update_uploads)
        self.resize(800, 500)

    def update_uploads(self):
        self._block_ui("communicating with NOMAD…")
        try:
            uploads = nomad_communication.get_user_uploads(
                scope=self.combo_scope.currentText()
            )
            self.upload_names = [u.get("upload_name", u["upload_id"]) for u in uploads]
            self.upload_ids = [u["upload_id"] for u in uploads]
            self.upload_box.clear()
            for name in sorted(self.upload_names):
                self.upload_box.addItem(name)
            # restore last selection if any
            if self.last_upload_id:
                try:
                    idx = self.upload_ids.index(self.last_upload_id)
                    self.upload_box.setCurrentText(self.upload_names[idx])
                except ValueError:
                    pass
                self.last_upload_id = None
        except Exception as e:
            QMessageBox.critical(self, "Error fetching uploads", str(e))
        finally:
            self._unblock_ui()
        self.update_entries()

    def update_entries(self):
        if self.reloading:
            return
        self._block_ui("communicating with NOMAD…")
        try:
            name = self.upload_box.currentText()
            idx = self.upload_names.index(name)
            upload_id = self.upload_ids[idx]
            entries = nomad_communication.get_entries_from_upload(upload_id)
            self.entry_names.clear()
            self.entry_types.clear()
            self.entry_ids.clear()
            for ent in entries:
                md = ent.get("entry_metadata", {})
                n = md.get("entry_name")
                t = md.get("entry_type")
                e = md.get("entry_id")
                if n and t and e:
                    self.entry_names.append(n)
                    self.entry_types.append(t)
                    self.entry_ids.append(e)
            self.type_box.clear()
            for t in sorted(set(self.entry_types)):
                self.type_box.addItem(t)
        except Exception as e:
            QMessageBox.critical(self, "Error fetching entries", str(e))
        finally:
            self._unblock_ui()
        self.entry_filtering()

    def entry_filtering(self):
        if self.reloading:
            return
        if self.last_entry_id:
            try:
                idx = self.entry_ids.index(self.last_entry_id)
                last_type = self.entry_types[idx]
                self.type_box.setCurrentText(last_type)
            except ValueError:
                pass
        sel = self.type_box.currentText()
        filtered = [
            name for name, typ in zip(self.entry_names, self.entry_types) if typ == sel
        ]
        self.reloading = True
        self.entry_box.clear()
        self.entry_box.addItems(filtered)
        if self.last_entry_id:
            try:
                idx = self.entry_ids.index(self.last_entry_id)
                self.entry_box.setCurrentText(self.entry_names[idx])
            except ValueError:
                pass
            self.last_entry_id = None
        self.reloading = False

        # adjust combobox widths
        w = min(
            max(
                compute_combo_max_width(self.combo_scope),
                compute_combo_max_width(self.upload_box),
                compute_combo_max_width(self.type_box),
                compute_combo_max_width(self.entry_box),
            ),
            400,
        )
        for c in (self.combo_scope, self.upload_box, self.type_box, self.entry_box):
            c.setMaximumWidth(w)

        self.entry_change()

    def entry_change(self):
        if self.reloading:
            return
        self._block_ui()
        if self.entry_box.currentText():
            try:
                name = self.entry_box.currentText()
                idx = self.entry_names.index(name)
                eid = self.entry_ids[idx]
                archive = nomad_communication.get_entry_archive(entry_id=eid)
                data = archive.get("data", {})
                self.entry_metadata = archive.get("metadata", {})
                self.entry_data = data
                data_yaml_dump = yaml.dump(data)
                # 3. Regular Expression for finding base64 images in HTML <img> tags:
                # It looks for:
                # <img src="data:image/ANYTHING;base64,HUGE_BASE64_STRING" ...>
                # Group 1 captures the full matched string (the <img> tag).
                # Group 2 captures the file type (e.g., 'png', 'jpeg').
                # Group 3 captures the huge base64 string.
                # The '?' makes the quantifier non-greedy, stopping at the next ">".
                # The 's' flag (re.DOTALL) allows '.' to match newlines, important for huge strings.
                img_regex = re.compile(r'(<img\s+[^>]*src\s*=\s*["\']data:image/([^;]+);base64,([a-zA-Z0-9+/=]+)["\'][^>]*>)', re.DOTALL)
                cleaned_data_yaml_dump = img_regex.sub('Image', data_yaml_dump)
                self.entry_info.setText(cleaned_data_yaml_dump)
            except Exception as e:
                QMessageBox.critical(self, "Error fetching entry", str(e))
            finally:
                self._unblock_ui()
        else:
            self.entry_info.setText("No entry selected.")
            self._unblock_ui()

    def accept(self):
        # package return_data and close
        rd = self.entry_data.copy()
        rd["NOMAD_entry_metadata"] = self.entry_metadata
        if "name" not in rd and "Name" not in rd:
            rd["name"] = self.entry_box.currentText().split(".")[0]
        rd["ELN-service"] = "nomad"
        url = nomad_communication.nomad_url
        meta = rd["NOMAD_entry_metadata"]
        rd["full_identifier"] = (
            f"{url}/upload/id/{meta['upload_id']}/entry/id/{meta['entry_id']}"
        )
        rd["identifier"] = meta.get("lab_id", rd["full_identifier"])
        self.return_data = rd
        super().accept()

    def _block_ui(self, title=None):
        self.reloading = True
        self.setEnabled(False)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if title:
            self.setWindowTitle(title)

    def _unblock_ui(self):
        self.reloading = False
        self.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.setWindowTitle(self._window_title)
