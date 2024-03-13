from PySide6.QtWidgets import (
    QWidget,
    QTableWidgetItem,
    QLabel,
    QMessageBox,
    QLineEdit,
    QCheckBox,
    QGridLayout,
    QComboBox,
    QTextEdit,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QDialog,
)
from PySide6.QtCore import Qt

import databroker

from nomad_camels.utility import databroker_export, variables_handling
from nomad_camels.ui_widgets import path_button_edit, warn_popup


class Datbroker_Exporter(QDialog):
    """ """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Databroker Export - NOMAD CAMELS")

        file_label = QLabel("Filename:")
        data_path = variables_handling.meas_files_path
        self.file_box = path_button_edit.Path_Button_Edit(
            self, default_dir=data_path, save_file=True, file_extension="*.nxs"
        )
        session_label = QLabel("Session name:")
        self.lineEdit_session = QLineEdit()

        self.checkBox_export_csv = QCheckBox("export data to .csv")
        self.checkBox_export_json = QCheckBox("export metadata to .json")

        catalog_label = QLabel("Databroker catalog name:")
        catalog_name = "CAMELS_CATALOG"
        if "databroker_catalog_name" in variables_handling.preferences:
            catalog_name = variables_handling.preferences["databroker_catalog_name"]
        catalogs = list(databroker.catalog)
        self.catalog_box = QComboBox()
        self.catalog_box.addItems(catalogs)
        if catalog_name in catalogs:
            self.catalog_box.setCurrentText(catalog_name)

        run_label = QLabel("Run:")
        self.run_box = QComboBox()

        label_name = QLabel("Plan name:")
        label_time = QLabel("Time of run:")
        label_exit = QLabel("Exit status:")
        label_user = QLabel("User name:")
        label_overview = QLabel("Protocol overview")
        label_description = QLabel("Description")
        self.label_name = QLineEdit()
        self.label_time = QLineEdit()
        self.label_exit = QLineEdit()
        self.label_user = QLineEdit()
        self.label_name.setEnabled(False)
        self.label_time.setEnabled(False)
        self.label_exit.setEnabled(False)
        self.label_user.setEnabled(False)
        self.textedit_overview = QTextEdit()
        self.textedit_description = QTextEdit()
        self.textedit_description.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse
        )
        self.textedit_overview.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse
        )

        self.button_export = QPushButton("Export")
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.close)
        self.button_export.clicked.connect(self.export_data)

        layout = QGridLayout()
        layout.addWidget(file_label, 0, 0)
        layout.addWidget(self.file_box, 0, 1)
        layout.addWidget(session_label, 1, 0)
        layout.addWidget(self.lineEdit_session, 1, 1)
        layout.addWidget(self.checkBox_export_csv, 2, 0)
        layout.addWidget(self.checkBox_export_json, 2, 1)
        left = QWidget()
        left.setLayout(layout)
        layout.addItem(
            QSpacerItem(
                0,
                0,
                hData=QSizePolicy.Policy.Minimum,
                vData=QSizePolicy.Policy.Expanding,
            ),
            6,
            3,
        )

        layout = QGridLayout()
        layout.addWidget(catalog_label, 0, 2)
        layout.addWidget(self.catalog_box, 0, 3)
        layout.addWidget(run_label, 1, 2)
        layout.addWidget(self.run_box, 1, 3)

        layout.addWidget(label_name, 2, 2)
        layout.addWidget(label_time, 3, 2)
        layout.addWidget(label_exit, 4, 2)
        layout.addWidget(label_user, 5, 2)
        layout.addWidget(self.label_name, 2, 3)
        layout.addWidget(self.label_time, 3, 3)
        layout.addWidget(self.label_exit, 4, 3)
        layout.addWidget(self.label_user, 5, 3)
        layout.addWidget(label_description, 6, 2, 1, 2)
        layout.addWidget(self.textedit_description, 7, 2, 1, 2)
        mid = QWidget()
        mid.setLayout(layout)

        layout = QGridLayout()
        # layout.addWidget(label_description, 0, 4)
        # layout.addWidget(self.textedit_description, 1, 4, 1, 2)
        layout.addWidget(label_overview, 3, 4)
        layout.addWidget(self.textedit_overview, 4, 4, 1, 2)
        right = QWidget()
        right.setLayout(layout)

        layout = QGridLayout()
        layout.addWidget(left, 1, 0, 1, 3)
        layout.addWidget(mid, 0, 0)
        layout.addWidget(right, 0, 1, 1, 2)
        layout.addWidget(self.button_export, 5, 1)
        layout.addWidget(self.button_cancel, 5, 2)
        self.setLayout(layout)
        self.show()

        self.change_catalog()
        self.catalog_box.currentTextChanged.connect(self.change_catalog)
        self.change_run()
        self.run_box.currentTextChanged.connect(self.change_run)
        self.adjustSize()

    def export_data(self):
        self.setCursor(Qt.CursorShape.WaitCursor)
        filename = self.file_box.get_path()
        run = self.run_box.currentData()
        session = self.lineEdit_session.text()
        exp_csv = self.checkBox_export_csv.isChecked()
        exp_json = self.checkBox_export_json.isChecked()
        catalog = self.catalog_box.currentText()
        databroker_export.export_run(
            filename=filename,
            run_number=run,
            session_name=session,
            export_to_csv=exp_csv,
            export_to_json=exp_json,
            catalog_name=catalog,
        )
        self.setCursor(Qt.CursorShape.ArrowCursor)
        warn_popup.WarnPopup(self, "Successfully exported data!", "Data exported", True)
        self.accept()

    def change_catalog(self):
        self.setCursor(Qt.WaitCursor)
        catalog_name = self.catalog_box.currentText()
        if not catalog_name:
            return
        catalog = databroker.catalog[catalog_name]
        self.run_box.clear()
        run_time_names = []
        for run_name in list(catalog):
            run = catalog[run_name]
            run_time = run.metadata["start"]["time"]
            run_time = databroker_export.timestamp_to_ISO8601(run_time)
            run_time_names.append((run_time, run_name))
        for run in sorted(run_time_names, reverse=True):
            run_time, run_name = run
            self.run_box.addItem(f"{run_time} - {run_name}", userData=run_name)
        self.setCursor(Qt.ArrowCursor)

    def change_run(self):
        run_name = self.run_box.currentData()
        catalog_name = self.catalog_box.currentText()
        if run_name:
            catalog = databroker.catalog[catalog_name]
            run = catalog[run_name]
            metadata = run.metadata["start"]
            stopdata = run.metadata["stop"]
        else:
            metadata = {}
            stopdata = {}
        time = ""
        if "time" in metadata:
            time = databroker_export.timestamp_to_ISO8601(metadata["time"])
        self.label_time.setText(time)
        plan_name = ""
        if "plan_name" in metadata:
            plan_name = metadata["plan_name"]
        self.label_name.setText(plan_name)
        description = ""
        if "description" in metadata:
            description = metadata["description"]
        self.textedit_description.setText(description)
        user = ""
        if "user" in metadata:
            user = metadata["user"]["name"]
        self.label_user.setText(user)
        protocol_overview = ""
        if "protocol_overview" in metadata:
            protocol_overview = metadata["protocol_overview"]
        self.textedit_overview.setText(protocol_overview)
        exit_status = ""
        if stopdata and "exit_status" in stopdata:
            exit_status = stopdata["exit_status"]
        self.label_exit.setText(exit_status)

    def closeEvent(self, a0) -> None:
        discard_dialog = QMessageBox.question(
            self,
            "Discard Changes?",
            f"All changes will be lost!",
            QMessageBox.Yes | QMessageBox.No,
        )
        if discard_dialog != QMessageBox.Yes:
            a0.ignore()
            return
        super().closeEvent(a0)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    widge = Datbroker_Exporter()
    widge.show()
    app.exec()
