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
from nomad_camels.ui_widgets.warn_popup import WarnPopup
from nomad_camels.utility import variables_handling


class Watchdog(QObject):
    """
    A runtime watchdog that monitors one or more channels and evaluates
    a user‐defined condition. Emits `condition_met` when the condition
    transitions from False to True.
    """

    condition_met = Signal(QObject)

    def __init__(
        self,
        channels=None,
        condition="",
        execute_at_condition="",
        read_periodic=False,
        read_timer=10,
        active=True,
        name="watchdog",
    ):
        """
        Parameters
        ----------
        channels : list[str]
            Names of channels to subscribe to.
        condition : str
            A Python expression evaluated in the given namespace.
        execute_at_condition : str
            Path to a protocol to execute when condition is met.
        read_periodic : bool
            Whether to poll channel values on a timer and not only evaluate when they are updated.
        read_timer : int
            Polling interval in seconds, only used if `read_periodic` is True.
        active : bool
            Whether the watchdog is enabled.
        name : str
            Identifier for this watchdog.
        """
        super().__init__()
        self.name = name
        self.channels = channels or []
        self.condition = condition
        self.execute_at_condition = execute_at_condition
        self.read_periodic = read_periodic
        self.read_timer = read_timer
        self.active = active

        # Timer for periodic reads if requested
        self.timer = QTimer()
        self.timer.timeout.connect(self.read)

        self.eva = None  # Assigned at runtime
        self.subscriptions = {}  # channel_name -> subscription ID
        self.was_triggered = False  # Avoid repeated trigering
        self.plots = []  # Placeholder for associated plot objects
        self.ophyd_channels = []  # Ophyd channel objects

        # Start polling if requested
        if self.read_periodic:
            self.timer.start(self.read_timer * 1000)

    def get_definition(self):
        """
        Return a dict of this watchdog’s settings, used for saving and loading.
        """
        return {
            "channels": self.channels,
            "condition": self.condition,
            "execute_at_condition": self.execute_at_condition,
            "read_periodic": self.read_periodic,
            "read_timer": self.read_timer,
            "active": self.active,
            "name": self.name,
        }

    def read(self):
        """
        Manually trigger a read on each subscribed ophyd channel.
        Used by the internal QTimer.
        """
        for channel in self.ophyd_channels:
            channel.read()

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
            try:
                chan = variables_handling.channels[channel]
                if chan.device == device_name:
                    ophyd_channel = getattr(ophyd_device, chan.name.split(".")[-1])
                    ophyd_channel.unsubscribe(self.subscriptions[channel])
                    self.subscriptions.pop(channel)
                    self.ophyd_channels.remove(ophyd_channel)
                if channel in self.eva.namespace:
                    self.eva.namespace.pop(channel)
            except:
                pass

    def add_device(self, device_name, ophyd_device):
        """Subscribes the respective channels corresponding to the device"""
        if not self.active:
            return
        for channel in self.channels:
            # Skip if already subscribed
            if channel in self.subscriptions:
                continue
            chan = variables_handling.channels[channel]
            if chan.device == device_name:
                ophyd_channel = getattr(ophyd_device, chan.name.split(".")[-1])
                sub = ophyd_channel.subscribe(self.callback)
                self.subscriptions[channel] = sub
                self.ophyd_channels.append(ophyd_channel)

    def callback(self, value, **kwargs):
        """
        Receives updates from subscribed channels, evaluates
        the condition, and emits `condition_met` once when
        it transitions to True.
        """
        if not self.active:
            return
        if "obj" in kwargs and hasattr(kwargs["obj"], "name"):
            self.eva.namespace[kwargs["obj"].name] = value
        try:
            condition = self.eva.eval(self.condition)
        except:
            import logging

            logging.error(f"Error evaluating condition for watchdog {self.name}!")
            return
        if condition:
            if not self.was_triggered:
                self.condition_met.emit(self)
            self.was_triggered = True

    def update_settings(self):
        """
        Restart or stop the QTimer based on the
        current `read_periodic` and `read_timer` settings.
        """
        if self.timer.isActive():
            if not self.read_periodic:
                self.timer.stop()
            else:
                # Update interval if changed
                self.timer.setInterval(self.read_timer * 1000)
        elif self.read_periodic:
            # Start timer if newly enabled
            self.timer.start(self.read_timer * 1000)


class Watchdog_Definer(QDialog):
    """
    A dialog that allows users to add, remove, and configure
    Watchdog instances.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Define Watchdogs - NOMAD CAMELS")

        # Copy existing watchdogs to allow cancel/accept semantics
        self.watchdogs = dict(variables_handling.watchdogs)

        # Table for adding/removing watchdogs
        tabledata = {"Name": list(self.watchdogs.keys())}
        self.watchdog_table = AddRemoveTable(
            headerLabels=["Name"],
            tableData=tabledata,
            editables=[],
            add_tooltip="Add a new watchdog",
            remove_tooltip="Remove the selected watchdog",
        )
        self.last_item = None  # Track last selected table row

        # Edit a watchdog
        self.watchdog_view = Watchdog_View(self, self.watchdogs)

        # OK / Cancel buttons
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
        """
        Synchronize watchdogs with the entries in the watchdog table.

        - Collects current watcher names from the UI table.
        - Adds new Watchdog instances for any names not already tracked.
        - Removes watchdogs that have been deleted from the UI.
        """
        current_watchers = []  # List of names currently in the UI
        # Iterate over each row in the table model to collect names
        for i in range(self.watchdog_table.table_model.rowCount()):
            watchdog = self.watchdog_table.table_model.item(i, 0).text()
            current_watchers.append(watchdog)
            # If new, add it to the registry
            if watchdog not in self.watchdogs:
                self.watchdogs[watchdog] = Watchdog()

        # Determine which have been removed from the UI
        removes = []
        for watcher in self.watchdogs:
            if watcher not in current_watchers:
                removes.append(watcher)
        # Remove obsolete ones
        for remove in removes:
            self.watchdogs.pop(remove)

    def update_watchdog_view(self):
        """
        Update the detail view for the currently selected watchdog.

        - If there was a previously selected item (last_item), save its changes.
        - Refresh the watchdog list and detail view based on selection.
        """
        if self.last_item is not None:
            try:
                old_name = self.last_item.text()
                # Remove old entry, update its text, and re-add updated watchdog
                self.watchdogs.pop(old_name)
                self.last_item.setText(self.watchdog_view.name_box.text())
                watchdog = self.watchdog_view.get_data()
                self.watchdogs[watchdog.name] = watchdog
            except RuntimeError:
                pass

        # Get the current selection from the table
        indexes = self.watchdog_table.table.selectionModel().selectedIndexes()
        if len(indexes) == 0:
            return  # No selection, nothing to update

        self.update_watchdogs()
        index = indexes[0]
        self.last_item = self.watchdog_table.table_model.itemFromIndex(index)
        selected_watchdog = self.last_item.text()
        # Display selected watchdog details in the view
        self.watchdog_view.update_watchdog(selected_watchdog)
        # Adjust column widths to fit content
        self.watchdog_table.table.resizeColumnsToContents()

    def accept(self):
        """
        Finalize changes and apply watchdog settings.

        - Sync registry with UI table and detail view.
        - Store updated watchdogs in global variables.
        - Show a warning popup advising restart for full effect.
        """
        self.update_watchdogs()
        self.update_watchdog_view()
        variables_handling.watchdogs = self.watchdogs
        WarnPopup(
            self,
            "Watchdogs updated. Some functions might not work correctly right away. "
            "Restart CAMELS to make sure everything is working correctly.\n\n"
            "Watchdogs only read values of instruments that are being used by protocols or manual controls.\n"
            "(Further, channels that can only be read only work well if the instrument driver uses the Signals from CAMELS.)",
            "restart recommended, information",
            True,
        )
        super().accept()


class Watchdog_View(QWidget):
    """
    GUI component for viewing and editing a single Watchdog's settings.

    Contains widgets for condition expression, channel selection, read settings,
    activation checkbox, and optional protocol execution configuration.
    """

    def __init__(self, parent=None, watchdogs=None):
        """
        Initialize the Watchdog_View.

        Args:
            parent: Parent widget, if any.
            watchdogs: Dictionary of watchdog instances by name.
        """
        super().__init__(parent)
        self.setWindowTitle("Watchdogs - NOMAD CAMELS")
        self.watchdog = None
        self.watchdogs = watchdogs

        # Widget for entering the trigger condition
        self.condition_box = Variable_Box()
        # Table for selecting channels to monitor
        self.channels_table = Channels_Check_Table(
            self, ["use", "channel"], title="connected channels"
        )

        # Label and button for protocol script selection
        self.label_protocol = QLabel("Execute at condition:")
        self.protocol_selection = Path_Button_Edit(
            self,
            default_dir=variables_handling.preferences["py_files_path"],
            file_extension="*.cprot",
        )

        # Label for condition section
        self.label_condition = QLabel("Condition")
        # Checkbox and timer input for periodic reads
        self.read_check = QCheckBox("force periodic read")
        self.read_timer = QSpinBox()
        self.label_name = QLabel("Name")
        self.name_box = QLineEdit()

        self.read_check.stateChanged.connect(self.read_check_changed)
        self.read_check.setChecked(False)
        self.read_timer.setValue(10)

        self.checkbox_active = QCheckBox("Watchdog Active")

        # Arrange all widgets in a grid layout
        self.setLayout(QGridLayout())
        self.widgets = [
            self.condition_box,
            self.channels_table,
            self.protocol_selection,
            self.read_check,
            self.read_timer,
            self.label_name,
            self.label_condition,
            self.name_box,
            self.checkbox_active,
            self.label_protocol,
        ]

        # Place widgets in the desired grid positions
        self.layout().addWidget(self.label_name, 0, 0)
        self.layout().addWidget(self.name_box, 0, 1)
        self.layout().addWidget(self.checkbox_active, 1, 0, 1, 2)
        self.layout().addWidget(self.label_condition, 2, 0)
        self.layout().addWidget(self.condition_box, 2, 1)
        self.layout().addWidget(self.read_check, 3, 0)
        self.layout().addWidget(self.read_timer, 3, 1)
        self.layout().addWidget(self.channels_table, 4, 0, 1, 2)
        self.layout().addWidget(self.label_protocol, 5, 0, 1, 2)
        self.layout().addWidget(self.protocol_selection, 6, 0, 1, 2)

        # Initialize view with no selection
        self.update_watchdog(None)

    def update_watchdog(self, watchdog_name):
        """
        Populate the view with data from the specified watchdog.

        Args:
            watchdog_name: Name of the watchdog to display. If None or not found,
                           hides all widgets.
        """
        if watchdog_name not in self.watchdogs:
            # Hide all widgets if no valid watchdog selected
            for widget in self.widgets:
                widget.setHidden(True)
            return

        # Show widgets and load data into them
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
        self.protocol_selection.set_path(self.watchdog.execute_at_condition)

    def read_check_changed(self):
        """
        Enable or disable the read timer spin box based on the read checkbox state.
        """
        self.read_timer.setEnabled(self.read_check.isChecked())

    def get_data(self):
        """
        Retrieve updated settings from the view and apply them to the current watchdog.

        Returns:
            The updated Watchdog object, or None if no watchdog is loaded.
        """
        if self.watchdog is None:
            return None

        # Update watchdog fields from UI inputs
        self.watchdog.condition = self.condition_box.text()
        # Refresh channel list from table state
        self.watchdog.channels = self.channels_table.update_info()
        self.watchdog.channels = self.channels_table.info_dict["channel"]
        self.watchdog.read_periodic = self.read_check.isChecked()
        self.watchdog.read_timer = self.read_timer.value()
        self.watchdog.active = self.checkbox_active.isChecked()
        self.watchdog.name = self.name_box.text()
        self.watchdog.execute_at_condition = self.protocol_selection.get_path()
        # Apply any persistence or driver updates
        self.watchdog.update_settings()
        return self.watchdog
