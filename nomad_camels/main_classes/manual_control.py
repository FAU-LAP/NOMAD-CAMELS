from PySide6.QtWidgets import (
    QGridLayout,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QWidget,
)
from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtCore import Signal, Qt

from nomad_camels.utility import device_handling, variables_handling

from importlib import resources
from nomad_camels import graphics


class Manual_Control(QWidget):
    """
    Parent class for manual controls.

    This class provides the core functionality of a manual control in CAMELS.
    The parameters `device`, `device_list` and `ophyd_device` may or may not be
    used by the child class.

    Attributes
    ----------
    name : str
        The name of the manual control. It also determines the window title.
    device : str, None
        The device the manual control is using
    device_list : list
        A list of the devices, used. The specific implementation lies in the
        child classes.
    ophyd_device : ophyd.Device
        The device's representation in ophyd.
    """

    closing = Signal()

    def __init__(self, parent=None, title="Manual Control", control_data=None):
        super().__init__()
        # layout = QGridLayout()
        # self.setLayout(layout)
        self.control_data = control_data or {}

        self.setWindowTitle(f"{title} - NOMAD CAMELS")
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "CAMELS_Icon.png")))
        self.name = title
        self.device = None
        self.ophyd_device = None
        self.instantiate_devices_thread = None
        self.device_list = []
        self.show()

    # def close(self) -> bool:
    #     # device_handling.close_devices(self.device_list)
    #     self.closing.emit()
    #     return super().close()

    def closeEvent(self, a0: QCloseEvent) -> None:
        """Overwritten, so that `self.closing` is emitted, telling the main UI
        window that this manual control is no longer opened."""
        device_handling.close_devices(self.device_list)
        self.closing.emit()
        return super().closeEvent(a0)

    def propagate_exception(self, exception):
        """Propagates an exception to the main UI window.

        Parameters
        ----------
        exception : Exception
            The exception to be propagated.
        """
        raise exception

    def start_device(self, device_name):
        """Starts a device by using the
        `device_handling.InstantiateDevicesThread` class.

        Parameters
        ----------
        device_name : str
            The name of the device to be started.
        """
        self.device = variables_handling.devices[device_name]
        if self.device:
            self.device_list = self.device.get_necessary_devices()
            self.device_list = list(set(self.device_list))
            if self.device.name in self.device_list:
                self.device_list.remove(self.device.custom_name)
            self.device_list.append(self.device.custom_name)
            self.instantiate_devices_thread = device_handling.InstantiateDevicesThread(
                self.device_list
            )
            self.instantiate_devices_thread.successful.connect(self.device_ready)
            self.setCursor(Qt.WaitCursor)
            self.setEnabled(False)
            self.instantiate_devices_thread.exception_raised.connect(
                self.propagate_exception
            )
            self.instantiate_devices_thread.start()

    def start_multiple_devices(self, device_names, channels=False):
        """Starts multiple devices at once.

        Parameters
        ----------
        device_names : list
            A list of the names of the devices to be started, or the names of the channels, if `channels` is True.
        channels : bool
            Whether 'device_names' are channel names or device names.
        """
        self.instantiate_devices_thread = device_handling.InstantiateDevicesThread(
            device_names, channels
        )
        self.instantiate_devices_thread.successful.connect(self.device_ready)
        self.setEnabled(False)
        self.instantiate_devices_thread.exception_raised.connect(
            self.propagate_exception
        )
        self.instantiate_devices_thread.start()

    def device_ready(self):
        """Called when the devices are ready to be used, i.e. when the
        `instantiate_devices_thread` is finished."""
        self.device_list = self.instantiate_devices_thread.devices
        self.instantiate_devices_thread.quit()
        self.instantiate_devices_thread.wait()
        self.instantiate_devices_thread.deleteLater()
        self.instantiate_devices_thread = None
        if self.device:
            self.ophyd_device = self.device_list[self.device.custom_name]
        self.setCursor(Qt.ArrowCursor)
        self.setEnabled(True)


class Manual_Control_Config(QDialog):
    """ """

    def __init__(
        self,
        parent=None,
        control_data=None,
        title="Manual Control Config",
        control_type="",
    ):
        super().__init__(parent=parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        layout = QGridLayout()
        self.setLayout(layout)
        self.control_type = control_type or "Manual_Control"

        self.setWindowTitle(f"{title} - NOMAD CAMELS")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        name_label = QLabel("Name:")
        self.control_data = control_data or {}
        if "name" in self.control_data:
            name = self.control_data["name"]
        else:
            name = self.control_type
        self.lineEdit_name = QLineEdit(name)

        layout.addWidget(name_label, 0, 0)
        layout.addWidget(self.lineEdit_name, 0, 1)
        layout.addWidget(self.buttonBox, 11, 0, 1, 2)

    def accept(self):
        """ """
        name = self.lineEdit_name.text()
        if name in variables_handling.manual_controls:
            from nomad_camels.ui_widgets.warn_popup import WarnPopup

            WarnPopup(
                title="Manual Control Name Conflict",
                text=f'Manual control name "{name}" is already in use!',
                parent=self,
                info_icon=False,
            )
            return
        self.control_data["name"] = name
        self.control_data["control_type"] = self.control_type
        super().accept()

    def closeEvent(self, a0: QCloseEvent) -> None:
        """

        Parameters
        ----------
        a0: QCloseEvent :


        Returns
        -------

        """
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
