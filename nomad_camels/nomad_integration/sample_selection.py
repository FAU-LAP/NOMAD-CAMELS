import os.path
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QGridLayout, QDialogButtonBox, QComboBox, QTextEdit
from PySide6.QtCore import Qt

import yaml

from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.nomad_integration import nomad_communication

class Sample_Selector(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        entries = nomad_communication.get_entries(parent)['data']
        if not entries:
            raise Exception('No Entries found!')
        self.entry_metadata = []
        self.entry_names = []
        self.entry_uploads = []
        self.entry_types = []
        self.entry_data = []
        for entry in entries:
            if 'archive' not in entry:
                continue
            arch = entry['archive']
            if 'data' not in arch:
                continue
            self.entry_data.append(arch['data'])
            self.entry_metadata.append(arch['metadata'])
            self.entry_names.append(arch['metadata']['entry_name'])
            self.entry_types.append(arch['metadata']['entry_type'])
            if 'upload_name' in arch['metadata']:
                self.entry_uploads.append(arch['metadata']['upload_name'])
            else:
                self.entry_uploads.append(arch['metadata']['upload_id'])

        label_upload = QLabel('Upload:')
        self.upload_box = QComboBox()
        self.upload_box.addItems(sorted(list(set(self.entry_uploads))))

        label_entry_type = QLabel('Entry Type:')
        self.entry_type_box = QComboBox()
        self.entry_type_box.addItems(sorted(list(set(self.entry_types))))

        label_entry = QLabel('Entry:')
        self.entry_box = QComboBox()
        self.entry_box.addItems(sorted(self.entry_names))

        self.entry_info = QTextEdit()
        self.entry_info.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(label_upload, 0, 0)
        layout.addWidget(self.upload_box, 0, 1)
        layout.addWidget(label_entry_type, 1, 0)
        layout.addWidget(self.entry_type_box, 1, 1)
        layout.addWidget(label_entry, 10, 0)
        layout.addWidget(self.entry_box, 10, 1)
        layout.addWidget(self.entry_info, 0, 2, 12, 1)
        layout.addWidget(self.button_box, 20, 0, 1, 3)
        self.setLayout(layout)

        self.entry_filtering()
        self.entry_change()
        self.upload_box.currentTextChanged.connect(self.entry_filtering)
        self.entry_type_box.currentTextChanged.connect(self.entry_filtering)
        self.entry_box.currentTextChanged.connect(self.entry_change)

        self.sample_data = {}

        self.adjustSize()

    def entry_filtering(self):
        upload = self.upload_box.currentText()
        entry_type = self.entry_type_box.currentText()
        entries = []
        for i, entry in enumerate(self.entry_names):
            if upload == self.entry_uploads[i] and entry_type == self.entry_types[i]:
                entries.append(entry)
        self.entry_box.clear()
        self.entry_box.addItems(entries)

    def entry_change(self):
        self.entry_info.setText(yaml.dump(self.get_current_entry_data()))

    def get_current_entry_data(self):
        entry = self.entry_box.currentText()
        for i, ent in enumerate(self.entry_names):
            if ent == entry:
                return self.entry_data[i]
        return {}


    def accept(self):
        self.sample_data = self.get_current_entry_data()
        if 'name' not in self.sample_data and 'Name' not in self.sample_data:
            self.sample_data['name'] = self.entry_box.currentText().split('.')[0]
        super().accept()
