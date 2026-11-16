"""Dialog for pairing CAMELS with OASIS and enabling remote control."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from nomad_camels.api import remote_config

STATE_TEXT = {
    "stopped": "Not connected",
    "connecting": "Connecting ...",
    "online": "Connected",
    "retrying": "Connection lost, retrying",
    "unauthorized": "Rejected by OASIS",
    "replaced": "Stopped: another CAMELS uses this pairing",
    "outdated": "Stopped: update CAMELS",
}


class Remote_Control_Dialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("OASIS Remote Control - NOMAD CAMELS")
        self.setMinimumWidth(520)
        self.config = remote_config.load_config()

        intro = QLabel(
            "CAMELS opens an encrypted connection to OASIS. This computer needs no "
            "open port. Only protocols marked for OASIS remote control are visible."
        )
        intro.setWordWrap(True)

        # Pairing
        self.lineEdit_url = QLineEdit(self.config.oasis_url)
        self.lineEdit_url.setPlaceholderText("https://oasis.example.org/nomad-oasis")
        self.lineEdit_ca = QLineEdit(self.config.ca_file)
        self.lineEdit_ca.setPlaceholderText("only for a private certificate")
        browse = QPushButton("...")
        browse.setFixedWidth(30)
        browse.clicked.connect(self.browse_ca_file)
        ca_row = QHBoxLayout()
        ca_row.addWidget(self.lineEdit_ca)
        ca_row.addWidget(browse)
        self.lineEdit_code = QLineEdit()
        self.lineEdit_code.setPlaceholderText("XXXX-XXXX, from the OASIS device page")
        self.pushButton_pair = QPushButton("Pair")
        self.pushButton_pair.clicked.connect(self.pair)
        code_row = QHBoxLayout()
        code_row.addWidget(self.lineEdit_code)
        code_row.addWidget(self.pushButton_pair)

        pair_box = QGroupBox("Pairing")
        form = QFormLayout(pair_box)
        form.addRow("OASIS address", self.lineEdit_url)
        form.addRow("CA certificate", ca_row)
        form.addRow("Pairing code", code_row)

        # State
        self.label_device = QLabel()
        self.label_state = QLabel()
        self.label_state.setWordWrap(True)
        self.label_state.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.checkBox_enable = QCheckBox("Enable remote control")
        self.checkBox_enable.toggled.connect(self.set_enabled)
        self.pushButton_unpair = QPushButton("Unpair this computer")
        self.pushButton_unpair.clicked.connect(self.unpair)

        state_box = QGroupBox("Connection")
        state_layout = QFormLayout(state_box)
        state_layout.addRow("Device", self.label_device)
        state_layout.addRow("State", self.label_state)
        state_layout.addRow(self.checkBox_enable)
        state_layout.addRow(self.pushButton_unpair)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(intro)
        layout.addWidget(pair_box)
        layout.addWidget(state_box)
        layout.addWidget(buttons)

        main_window.remote_agent_state_signal.connect(self.show_state)
        self.update_view()

    def browse_ca_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "CA certificate", "", "Certificates (*.crt *.pem *.cer);;All files (*)"
        )
        if path:
            self.lineEdit_ca.setText(path)

    def update_view(self):
        paired = self.config.paired
        if paired:
            name = self.config.device_name or self.config.device_id
            self.label_device.setText(f"{name} ({self.config.device_id}) at {self.config.oasis_url}")
        else:
            self.label_device.setText("not paired")
        self.checkBox_enable.blockSignals(True)
        self.checkBox_enable.setChecked(self.config.enabled and paired)
        self.checkBox_enable.blockSignals(False)
        self.checkBox_enable.setEnabled(paired)
        self.pushButton_unpair.setEnabled(paired)
        self.pushButton_pair.setText("Pair again" if paired else "Pair")
        self.show_state(*self.main_window.remote_agent_state)

    def show_state(self, state, detail):
        text = STATE_TEXT.get(state, state)
        if detail and state != "online":
            text = f"{text}: {detail}"
        self.label_state.setText(text)

    def show_error(self, message):
        self.label_state.setText(f'<span style="color:#c0392b">{message}</span>')

    def pair(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.main_window.stop_remote_agent()
            self.config = remote_config.pair(
                self.lineEdit_url.text(),
                self.lineEdit_code.text(),
                self.lineEdit_ca.text().strip(),
            )
        except remote_config.RemoteConfigError as exc:
            QApplication.restoreOverrideCursor()
            self.config = remote_config.load_config()
            self.update_view()
            self.show_error(str(exc))
            return
        QApplication.restoreOverrideCursor()
        self.lineEdit_code.clear()
        self.lineEdit_url.setText(self.config.oasis_url)
        # Enable directly after pairing; the user paired to use it.
        self.config.enabled = True
        remote_config.save_config(self.config)
        self.update_view()
        self.main_window.start_remote_agent()

    def set_enabled(self, enabled):
        self.config = remote_config.load_config()
        self.config.enabled = bool(enabled)
        remote_config.save_config(self.config)
        if enabled:
            self.main_window.start_remote_agent()
        else:
            self.main_window.stop_remote_agent()
        self.update_view()

    def unpair(self):
        self.main_window.stop_remote_agent()
        self.config = remote_config.unpair()
        self.update_view()

    def done(self, result):
        try:
            self.main_window.remote_agent_state_signal.disconnect(self.show_state)
        except (RuntimeError, TypeError):
            pass
        super().done(result)
