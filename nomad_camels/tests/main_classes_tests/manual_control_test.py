import pytest
import time
from unittest.mock import MagicMock, patch
from pytest_mock import mocker
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QCloseEvent

from nomad_camels.main_classes.manual_control import (
    Manual_Control,
    Manual_Control_Config,
)


@pytest.fixture(scope="module")
def app():
    """Fixture for creating a QApplication instance"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def manual_control(app):
    return Manual_Control(title="Test Control")


@pytest.fixture
def manual_control_config(app):
    return Manual_Control_Config(title="Test Control Config")


def test_manual_control_init(manual_control):
    assert manual_control.windowTitle() == "Test Control - NOMAD CAMELS"
    assert manual_control.name == "Test Control"
    assert manual_control.device is None
    assert manual_control.ophyd_device is None
    assert manual_control.device_list == []


def test_manual_control_close_event(manual_control):
    with patch(
        "nomad_camels.utility.device_handling.close_devices"
    ) as mock_close_devices:
        event = QCloseEvent()
        manual_control.closeEvent(event)
        mock_close_devices.assert_called_with([])
        assert event.isAccepted()


def test_manual_control_propagate_exception(manual_control):
    with pytest.raises(Exception, match="Test Exception"):
        manual_control.propagate_exception(Exception("Test Exception"))


def test_manual_control_start_device(app, manual_control):
    mock_device = MagicMock()
    mock_device.get_necessary_devices.return_value = ["device1", "device2"]
    mock_device.custom_name = "Test_Device"
    mock_device1 = MagicMock()
    mock_device1.custom_name = "device1"
    mock_device2 = MagicMock()
    mock_device2.custom_name = "device2"

    with patch(
        "nomad_camels.utility.variables_handling.devices",
        {"Test_Device": mock_device, "device1": mock_device1, "device2": mock_device2},
    ):
        manual_control.start_device("Test_Device")
        time.sleep(0.5)
        app.processEvents()
        assert manual_control.device == mock_device
        assert "device1" in manual_control.device_list
        assert "device2" in manual_control.device_list
        assert "Test_Device" in manual_control.device_list


def test_manual_control_start_multiple_devices(manual_control):
    device_names = ["device1", "device2"]
    with patch(
        "nomad_camels.utility.device_handling.InstantiateDevicesThread"
    ) as mock_thread:
        manual_control.start_multiple_devices(device_names)
        mock_thread.assert_called_with(device_names, False)
        assert not manual_control.isEnabled()


def test_manual_control_device_ready(manual_control):
    manual_control.instantiate_devices_thread = MagicMock()
    manual_control.instantiate_devices_thread.devices = {
        "Test Device": "ophyd_device_mock"
    }

    manual_control.device = MagicMock()
    manual_control.device.custom_name = "Test Device"

    manual_control.device_ready()
    assert manual_control.ophyd_device == "ophyd_device_mock"
    assert manual_control.isEnabled()


def test_manual_control_config_init(manual_control_config):
    assert manual_control_config.windowTitle() == "Test Control Config - NOMAD CAMELS"
    assert manual_control_config.control_type == "Manual_Control"
    assert manual_control_config.lineEdit_name.text() == "Manual_Control"


def test_manual_control_config_accept(manual_control_config):
    manual_control_config.lineEdit_name.setText("New Control Name")
    manual_control_config.accept()
    assert manual_control_config.control_data["name"] == "New Control Name"
    assert manual_control_config.control_data["control_type"] == "Manual_Control"


def test_manual_control_config_close_event(manual_control_config):
    event = QCloseEvent()
    with patch("PySide6.QtWidgets.QMessageBox.question", return_value=QMessageBox.Yes):
        manual_control_config.closeEvent(event)
        assert event.isAccepted()

    event = QCloseEvent()
    with patch("PySide6.QtWidgets.QMessageBox.question", return_value=QMessageBox.No):
        manual_control_config.closeEvent(event)
        assert not event.isAccepted()
