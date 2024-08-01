from pytest_mock import mocker
from unittest.mock import MagicMock
from nomad_camels.main_classes.device_class import Device


def test_device_initialization():
    device = Device(name="TestDevice", virtual=True, tags=["test", "virtual"])

    assert device.name == "TestDevice"
    assert device.virtual is True
    assert device.tags == ["test", "virtual"]
    assert device.settings == {}
    assert device.config == {}
    assert device.passive_config == {}
    assert device.channels == {}
    assert device.config_channels == {}
    assert device.non_channel_functions == []
    assert device.main_thread_only is False
    assert device.controls == {}


def test_get_channels(mocker):
    mock_device = MagicMock()
    mock_device.configuration_attrs = []
    mocker.patch(
        "nomad_camels.main_classes.device_class.OphydDevice", return_value=mock_device
    )
    mock_get_outputs = mocker.patch(
        "nomad_camels.main_classes.device_class.get_outputs", return_value=[]
    )
    mock_get_channels = mocker.patch(
        "nomad_camels.main_classes.device_class.get_channels", return_value=([], [])
    )

    device = Device(name="TestDevice")
    channels = device.get_channels()

    assert mock_get_outputs.called
    assert mock_get_channels.called
    assert channels == {}


def test_get_additional_info():
    device = Device(additional_info={"info_key": "info_value"})
    assert device.get_additional_info() == {"info_key": "info_value"}


def test_get_finalize_steps():
    device = Device(name="TestDevice")
    steps_str = device.get_finalize_steps()

    expected_str = "\t\tif 'TestDevice' in devs and hasattr(devs['TestDevice'], 'finalize_steps') and callable(devs['TestDevice'].finalize_steps):\n"
    expected_str += "\t\t\tdevs['TestDevice'].finalize_steps()\n"

    assert steps_str == expected_str


from nomad_camels.main_classes.device_class import (
    check_output,
    get_channels,
    get_outputs,
)
from ophyd import Signal, SignalRO


def test_check_output():
    assert check_output(Signal) is True
    assert check_output(SignalRO) is False


def test_get_outputs(mocker):
    mock_device = MagicMock()
    mock_device.walk_components.return_value = [
        MagicMock(item=MagicMock(attr="signal1", cls=MagicMock()))
    ]
    mocker.patch(
        "nomad_camels.main_classes.device_class.check_output", return_value=True
    )

    outputs = get_outputs(mock_device)
    assert "signal1" in outputs


def test_get_channels(mocker):
    mock_device = MagicMock()
    mock_device.walk_components.return_value = [
        MagicMock(item=MagicMock(attr="channel1", cls=MagicMock()))
    ]
    mock_device.configuration_attrs = []

    channels, config_channels = get_channels(
        mock_device, include_metadata=False, include_config=True
    )

    assert "channel1" in channels
