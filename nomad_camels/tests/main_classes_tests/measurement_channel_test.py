import pytest
from nomad_camels.utility import variables_handling
from nomad_camels.main_classes.measurement_channel import (
    Measurement_Channel,
    from_pv_name,
)


@pytest.fixture
def sample_channel():
    return Measurement_Channel(
        name="sample.name",
        output=True,
        device="sample_device",
        metadata={"key1": "value1", "key2": "value2"},
    )


def test_measurement_channel_init(sample_channel):
    assert sample_channel.name == "sample.name"
    assert sample_channel.output is True
    assert sample_channel.device == "sample_device"
    assert sample_channel.metadata == {"key1": "value1", "key2": "value2"}


def test_get_bluesky_name(sample_channel):
    expected_bluesky_name = "sample_device.name"
    assert sample_channel.get_bluesky_name() == expected_bluesky_name


def test_get_meta_str(sample_channel):
    expected_meta_str = "key1: value1\nkey2: value2"
    assert sample_channel.get_meta_str() == expected_meta_str


def test_from_pv_name():
    pv_name = "TEST:sample_device:name"
    expected_channel_name = "sample_device_name"
    assert from_pv_name(pv_name) == expected_channel_name
