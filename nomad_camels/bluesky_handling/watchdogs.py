from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QDialog,
    QCheckBox,
    QDialogButtonBox,
    QSpinBox,
    QLabel,
    QLineEdit,
)
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.utility import variables_handling


class Watchdog(QObject):
    condition_met = Signal(QObject)

    def __init__(
        self,
        channels=None,
        condition="",
        execute_at_condition=None,
        read_periodic=False,
        read_timer=10,
        active=True,
        name="watchdog",
        **kwargs,
    ):
        super().__init__()
        self.name = name
        self.channels = channels or []
        self.condition = condition
        self.execute_at_condition = execute_at_condition
        self.read_periodic = read_periodic
        self.read_timer = read_timer
        self.active = active
        self.timer = QTimer()
        self.eva = None
        self.timer.timeout.connect(self.read)
        self.subscriptions = {}
        self.was_triggered = False

    def read(self):
        # TODO periodic read
        # TODO plot again when again triggered
        pass

    def get_device_list(self):
        """Goes through the cannels and returns a list of all needed devices"""
        devices = []
        for channel in self.channels:
            chan = variables_handling.channels[channel]
            if chan.device not in devices:
                devices.append(chan.device)
        return devices

    def remove_device(self, device_name, ophyd_device):
        """Unsubscribes the respective channels corresponding to the device"""
        for channel in self.channels:
            chan = variables_handling.channels[channel]
            if chan.device == device_name:
                getattr(ophyd_device, chan.name.split(".")[-1]).unsubscribe(
                    self.subscriptions[channel]
                )
                self.subscriptions.pop(channel)
            if channel in self.eva.namespace:
                self.eva.namespace.pop(channel)

    def add_device(self, device_name, ophyd_device):
        """Subscribes the respective channels corresponding to the device"""
        for channel in self.channels:
            if channel in self.subscriptions:
                continue
            chan = variables_handling.channels[channel]
            if chan.device == device_name:
                sub = getattr(ophyd_device, chan.name.split(".")[-1]).subscribe(
                    self.callback
                )
                self.subscriptions[channel] = sub

    def callback(self, value, **kwargs):
        if "obj" in kwargs and hasattr(kwargs["obj"], "name"):
            self.eva.namespace[kwargs["obj"].name] = value
        try:
            condition = self.eva.eval(self.condition)
        except:
            print(f'Evaluating condition failed for watchdog "{self.name}"!')
            return
        if condition:
            if not self.was_triggered:
                self.condition_met.emit(self)
            self.was_triggered = True
            print("condition")


class Watchdog_Definer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.watchdogs = dict(variables_handling.watchdogs)
        tabledata = {"Name": list(self.watchdogs.keys())}
        self.watchdog_table = AddRemoveTable(
            headerLabels=["Name"], tableData=tabledata, editables=[]
        )
        self.last_item = None

        self.watchdog_view = Watchdog_View(self, self.watchdogs)

        self.dialog_button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.dialog_button_box.accepted.connect(self.accept)
        self.dialog_button_box.rejected.connect(self.reject)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.watchdog_table, 0, 0)
        self.layout().addWidget(self.watchdog_view, 0, 1)
        self.layout().addWidget(self.dialog_button_box, 5, 0, 1, 2)

        self.watchdog_table.table.selectionModel().selectionChanged.connect(
            self.update_watchdog_view
        )

    def update_watchdogs(self):
        current_watchers = []
        for i in range(self.watchdog_table.table_model.rowCount()):
            watchdog = self.watchdog_table.table_model.item(i, 0).text()
            current_watchers.append(watchdog)
            if watchdog not in self.watchdogs:
                self.watchdogs[watchdog] = Watchdog()
        removes = []
        for watcher in self.watchdogs:
            if watcher not in current_watchers:
                removes.append(watcher)
        for remove in removes:
            self.watchdogs.pop(remove)

    def update_watchdog_view(self):
        if self.last_item is not None:
            try:
                old_name = self.last_item.text()
                self.watchdogs.pop(old_name)
                self.last_item.setText(self.watchdog_view.name_box.text())
                watchdog = self.watchdog_view.get_data()
                self.watchdogs[watchdog.name] = watchdog
            except RuntimeError:
                pass
        indexes = self.watchdog_table.table.selectionModel().selectedIndexes()
        if len(indexes) == 0:
            return
        self.update_watchdogs()
        index = indexes[0]
        self.last_item = self.watchdog_table.table_model.itemFromIndex(index)
        selected_watchdog = self.last_item.text()
        self.watchdog_view.update_watchdog(selected_watchdog)
        self.watchdog_table.table.resizeColumnsToContents()

    def accept(self):
        self.update_watchdogs()
        self.update_watchdog_view()
        variables_handling.watchdogs = self.watchdogs
        super().accept()


class Watchdog_View(QWidget):
    def __init__(self, parent=None, watchdogs=None):
        super().__init__(parent)
        self.watchdog = None
        self.watchdogs = watchdogs
        self.condition_box = Variable_Box()
        self.channels_table = Channels_Check_Table(
            self, ["use", "channel"], title="connected channels"
        )

        self.label_protocol = QLabel("Execute at condition")
        self.protocol_selection = Path_Button_Edit(
            self,
            default_dir=variables_handling.preferences["py_files_path"],
            file_extension="*.cprot",
        )

        self.read_check = QCheckBox("force periodic read")
        self.read_timer = QSpinBox()
        self.label_name = QLabel("Name")
        self.name_box = QLineEdit()

        self.read_check.stateChanged.connect(self.read_check_changed)
        self.read_check.setChecked(False)
        self.read_timer.setValue(10)

        self.checkbox_active = QCheckBox("Watchdog Active")

        self.setLayout(QGridLayout())

        self.widgets = [
            self.condition_box,
            self.channels_table,
            self.protocol_selection,
            self.read_check,
            self.read_timer,
            self.label_name,
            self.name_box,
            self.checkbox_active,
        ]

        self.layout().addWidget(self.label_name, 0, 0)
        self.layout().addWidget(self.name_box, 0, 1)
        self.layout().addWidget(self.checkbox_active, 1, 0, 1, 2)
        self.layout().addWidget(self.condition_box, 2, 0, 1, 2)
        self.layout().addWidget(self.read_check, 3, 0)
        self.layout().addWidget(self.read_timer, 3, 1)
        self.layout().addWidget(self.channels_table, 4, 0, 1, 2)
        self.layout().addWidget(self.protocol_selection, 5, 0, 1, 2)

        self.update_watchdog(None)

    def update_watchdog(self, watchdog_name):
        if not watchdog_name in self.watchdogs:
            for widget in self.widgets:
                widget.setHidden(True)
            return
        for widget in self.widgets:
            widget.setHidden(False)
        self.watchdog = self.watchdogs[watchdog_name]
        self.condition_box.setText(self.watchdog.condition)
        self.channels_table.info_dict = {"channel": self.watchdog.channels}
        self.channels_table.build_channels_table()
        self.read_check.setChecked(self.watchdog.read_periodic)
        self.read_timer.setValue(self.watchdog.read_timer)
        self.checkbox_active.setChecked(self.watchdog.active)
        self.name_box.setText(self.watchdog.name)

    def read_check_changed(self):
        self.read_timer.setEnabled(self.read_check.isChecked())

    def get_data(self):
        if self.watchdog is None:
            return
        self.watchdog.condition = self.condition_box.text()
        self.watchdog.channels = self.channels_table.update_info()
        self.watchdog.channels = self.channels_table.info_dict["channel"]
        self.watchdog.read_periodic = self.read_check.isChecked()
        self.watchdog.read_timer = self.read_timer.value()
        self.watchdog.active = self.checkbox_active.isChecked()
        self.watchdog.name = self.name_box.text()
        self.watchdog.execute_at_condition = self.protocol_selection.get_path()
        return self.watchdog
