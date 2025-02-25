from PySide6.QtWidgets import QGridLayout, QCheckBox, QPushButton, QLineEdit
from PySide6.QtCore import QThread, Signal

import time
import copy

from nomad_camels.main_classes.manual_control import (
    Manual_Control,
    Manual_Control_Config,
)

from nomad_camels.utility import device_handling, variables_handling
from nomad_camels.bluesky_handling import evaluation_helper
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table


class Generic_Set_Read(Manual_Control):
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if "name" in control_data:
            name = control_data["name"]
        else:
            name = "Generic Set Read"
        super().__init__(parent, title=name)
        self.setWindowTitle(f"{name} - NOMAD CAMELS")
        self.control_data = control_data or {}

        self.channels = self.control_data.get("channels_dict", [])["channel"]
        handling_channels = {}
        for channel in self.channels:
            handling_channels[channel] = variables_handling.channels[channel]
        self.set_table = Channels_Check_Table(
            parent=self,
            headerLabels=["set?", "channel", "value"],
            only_output=True,
            title="Set Values",
            channels=handling_channels,
        )
        self.checkbox_auto_read = QCheckBox("auto read every ... s")
        self.checkbox_auto_read.setChecked(self.control_data.get("auto_read", False))
        self.checkbox_auto_read.setToolTip("automatically read the values")
        self.checkbox_auto_read.stateChanged.connect(self.auto_read_changed)

        self.lineEdit_auto_read = QLineEdit(
            str(self.control_data.get("auto_read_time", 1))
        )
        self.lineEdit_auto_read.setToolTip("time in seconds between readings")

        self.pushButton_read = QPushButton("read / update read time")
        self.pushButton_read.setToolTip(
            "manually trigger a reading if auto read is off\nupdate the time between readings if auto read is on"
        )
        self.pushButton_read.clicked.connect(self.update_reading)

        self.read_table = AddRemoveTable(
            editables=[],
            headerLabels=["channel", "value"],
            title="Read Values",
            parent=self,
        )
        self.read_table.addButton.setHidden(True)
        self.read_table.removeButton.setHidden(True)

        self.pushButton_set = QPushButton("set values")
        self.pushButton_set.clicked.connect(self.set_button_clicked)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.set_table, 0, 0, 3, 1)
        self.layout.addWidget(self.checkbox_auto_read, 0, 1)
        self.layout.addWidget(self.lineEdit_auto_read, 1, 1)
        self.layout.addWidget(self.read_table, 2, 1)
        self.layout.addWidget(self.pushButton_read, 3, 1)
        self.layout.addWidget(self.pushButton_set, 3, 0)

        self.start_multiple_devices(self.channels, True)

    def update_reading(self):
        if not self.checkbox_auto_read.isChecked():
            self.work_thread.manual_read = True
        self.work_thread.auto_read_time = float(self.lineEdit_auto_read.text())

    def auto_read_changed(self):
        self.work_thread.auto_read = self.checkbox_auto_read.isChecked()

    def set_button_clicked(self):
        self.work_thread.channel_values = copy.deepcopy(self.set_table.get_info())

    def update_read_table(self, results):
        self.read_table.tableData = results
        self.read_table.load_table_data()

    def exception_handler(self, ex):
        from PySide6.QtWidgets import QMessageBox

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"Error in the working thread of {self.name}!\nRestart?")
        msg.setInformativeText(f"{ex}\n\nRestart the thread?")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        if msg.exec() == QMessageBox.Yes:
            self.start_work_thread()

    def device_ready(self):
        self.ophyd_channels = device_handling.get_channels_from_string_list(
            self.channels
        )
        self.start_work_thread()
        super().device_ready()

    def start_work_thread(self):
        self.work_thread = Work_Thread(parent=self, channels=self.ophyd_channels)
        self.work_thread.auto_read = self.checkbox_auto_read.isChecked()
        self.work_thread.auto_read_time = float(self.lineEdit_auto_read.text())
        self.work_thread.exception_signal.connect(self.exception_handler)
        self.work_thread.data_signal.connect(self.update_read_table)
        self.work_thread.start()

    def close(self):
        self.work_thread.still_running = False
        return super().close()

    def closeEvent(self, a0):
        self.work_thread.still_running = False
        return super().closeEvent(a0)



class Work_Thread(QThread):

    exception_signal = Signal(Exception)
    data_signal = Signal(dict)

    def __init__(self, parent=None, channels=None):
        super().__init__(parent)
        self.channels = channels
        self.still_running = True
        self.channel_values = {}
        self.last_channel_values = {}
        self.auto_read = False
        self.auto_read_time = 1
        self.manual_read = False
        self.eva = evaluation_helper.Evaluator()

    def run(self):
        try:
            self.do_reading()
            wait_start_time = time.time()
            while self.still_running:
                if self.channel_values != self.last_channel_values:
                    channels = device_handling.get_channels_from_string_list(
                        self.channel_values["channel"]
                    )
                    values = self.channel_values["value"]
                    for i, channel in enumerate(channels):
                        channel.put(self.eva.eval(values[i]))
                    self.last_channel_values = copy.deepcopy(self.channel_values)
                if self.manual_read:
                    self.do_reading()
                    self.manual_read = False
                elif self.auto_read:
                    if time.time() - wait_start_time >= self.auto_read_time:
                        self.do_reading()
                        wait_start_time = time.time()
                else:
                    time.sleep(0.1)
        except Exception as e:
            self.exception_signal.emit(e)

    def do_reading(self):
        results = {"channel": [], "value": []}
        for channel in self.channels:
            name = channel.name
            value = channel.get()
            results["channel"].append(name)
            results["value"].append(value)
            self.eva.namespace[name] = value
        self.data_signal.emit(results)


class Generic_Set_Read_Config(Manual_Control_Config):
    def __init__(self, parent=None, control_data=None):
        super().__init__(
            parent=parent,
            control_data=control_data,
            title="Generic Set Read Configuration",
            control_type="Generic_Set_Read",
        )
        self.control_data = control_data or {}
        self.channels_table = Channels_Check_Table(
            parent=self,
            headerLabels=["use?", "channel"],
            title="Channels",
            info_dict=self.control_data.get("channels_dict", {}),
        )
        self.checkbox_auto_read = QCheckBox("auto read every ... s")
        self.checkbox_auto_read.setToolTip("automatically read the values")
        self.lineEdit_auto_read = QLineEdit("1")
        self.lineEdit_auto_read.setToolTip("time in seconds between readings")

        self.layout().addWidget(self.channels_table, 1, 0, 2, 1)
        self.layout().addWidget(self.checkbox_auto_read, 1, 1)
        self.layout().addWidget(self.lineEdit_auto_read, 2, 1)

    def accept(self):
        self.control_data["channels_dict"] = self.channels_table.get_info()
        self.control_data["auto_read"] = self.checkbox_auto_read.isChecked()
        self.control_data["auto_read_time"] = float(self.lineEdit_auto_read.text())
        super().accept()
