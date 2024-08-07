import pytest
from unittest.mock import patch
from pytestqt import qtbot
from unittest.mock import MagicMock
from PySide6.QtWidgets import QApplication, QDialog
from nomad_camels.MainApp_v2 import MainWindow


@pytest.fixture(scope="function")
def app(qtbot):
    """Fixture for initializing the application and the MainWindow."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_ui_initialization(app):
    """Test to check if UI components are initialized correctly."""
    assert (
        app.windowTitle()
        == "NOMAD CAMELS - Configurable Application for Measurements, Experiments and Laboratory-Systems"
    )
    assert app.pushButton_pause.icon().isNull() is False
    assert app.pushButton_resume.icon().isNull() is False
    assert app.pushButton_stop.icon().isNull() is False


def test_signal_slots(app, qtbot):
    """Test to verify that signal-slot connections are properly set."""

    # Create a mock slot
    mock_slot = MagicMock()

    # Connect the signal to the mock slot
    app.protocol_stepper_signal.connect(mock_slot)

    # Emit the signal
    app.protocol_stepper_signal.emit(42)  # Assuming the signal emits an integer

    # Assert that the mock slot was called with the expected value
    mock_slot.assert_called_once_with(42)


def test_set_user(app):
    """Test setting the user."""
    app.userdata = {"user1": {}}
    app.set_user("user1")
    assert app.active_user == "user1"

    with pytest.raises(ValueError):
        app.set_user("non_existent_user")


def test_set_sample(app):
    """Test setting the sample."""
    app.sampledata = {"sample1": {}}
    app.set_sample("sample1")
    assert app.active_sample == "sample1"

    with pytest.raises(ValueError):
        app.set_sample("non_existent_sample")


def test_show_hide_log(app, qtbot):
    """Test showing and hiding the log."""
    app.textEdit_console_output.setHidden(False)
    app.pushButton_show_log.click()
    assert app.textEdit_console_output.isHidden()
    assert app.pushButton_show_log.text() == "Show Log"

    app.pushButton_show_log.click()
    assert not app.textEdit_console_output.isHidden()
    assert app.pushButton_show_log.text() == "Hide Log"


def test_check_password_protection(app, qtbot):
    """Test checking password protection."""
    app.preferences["password_protection"] = True
    app.preferences["password_hash"] = "test_hash"

    from nomad_camels.utility.password_widgets import Password_Dialog

    with patch(
        "nomad_camels.utility.password_widgets.Password_Dialog", autospec=True
    ) as mock_dialog:
        mock_dialog.return_value.exec = MagicMock(return_value=True)
        assert app.check_password_protection() is True

    with patch(
        "nomad_camels.utility.password_widgets.Password_Dialog", autospec=True
    ) as mock_dialog:
        mock_dialog.return_value.exec = MagicMock(return_value=False)
        assert app.check_password_protection() is False

    app.preferences["password_protection"] = False
    assert app.check_password_protection() is True
