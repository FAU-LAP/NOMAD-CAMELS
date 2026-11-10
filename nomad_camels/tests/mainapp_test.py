import json

import pytest
from unittest.mock import patch
from pytestqt import qtbot
from unittest.mock import MagicMock
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from nomad_camels.MainApp_v2 import MainWindow
from nomad_camels.main_classes.protocol_class import Measurement_Protocol
from nomad_camels.ui_widgets import add_remove_table
from nomad_camels.utility import load_save_functions, variables_handling
from nomad_camels.utility.load_save_functions import clean_sample_data



@pytest.fixture(scope="function")
def app(qtbot):
    """Fixture for initializing the application and the MainWindow."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    window = MainWindow(start_proxy_bool=False)
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
    """Test setting a sample."""
    app.sampledata = {"sample1": {"name": "sample1", "sample_id": ""}}

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

def sample(name, owner=None, description="", sample_id=""):
    entry = {"name": name, "sample_id": sample_id, "description": description}
    if owner is not None:
        entry["owner"] = owner
    return entry


def test_old_sample_without_owner_stays_shared():
    cleaned = clean_sample_data({"old": sample("old", description="keep")}, "user1")
    assert list(cleaned) == ["old, "]
    assert cleaned["old, "]["owner"] == ""
    assert cleaned["old, "]["description"] == "keep"
    assert cleaned["old, "]["display_name"] == "old"


def test_old_and_current_key_of_a_sample_are_merged():
    data = {
        "old": sample("old", owner="", description="keep"),
        "old, ": sample("old", owner=""),
    }
    cleaned = clean_sample_data(data, "user1")
    assert list(cleaned) == ["old, "]
    assert cleaned["old, "]["description"] == "keep"


def test_shared_sample_is_merged_into_the_sample_of_the_active_user():
    data = {
        "s1": sample("s1", description="from old version"),
        "s1, user1": sample("s1", owner="user1"),
    }
    cleaned = clean_sample_data(data, "user1")
    assert list(cleaned) == ["s1, user1"]
    assert cleaned["s1, user1"]["description"] == "from old version"


def test_shared_sample_stays_if_only_another_user_has_it():
    data = {"s1": sample("s1"), "s1, user2": sample("s1", owner="user2")}
    assert sorted(clean_sample_data(data, "user1")) == ["s1, ", "s1, user2"]


def test_samples_with_different_ids_are_not_merged():
    data = {
        "a": sample("s1", sample_id="1"),
        "b": sample("s1", sample_id="2"),
    }
    assert sorted(clean_sample_data(data, "user1")) == ["s1 / 1, ", "s1 / 2, "]


def test_owner_with_a_space_matches_the_cleaned_user_name():
    data = {
        "old": sample("old", owner="Some User"),
        "s1": sample("s1", owner="Some User", description="keep"),
        "s1, Some_User": sample("s1", owner="Some_User"),
    }
    cleaned = clean_sample_data(data, "Some_User")
    assert sorted(cleaned) == ["old, Some_User", "s1, Some_User"]
    assert cleaned["old, Some_User"]["owner"] == "Some_User"
    assert cleaned["s1, Some_User"]["description"] == "keep"


def test_cleaning_twice_changes_nothing():
    data = {"old": sample("old"), "new, user1": sample("new", owner="user1")}
    cleaned = clean_sample_data(data, "user1")
    assert clean_sample_data(cleaned, "user1") == cleaned


@pytest.fixture
def window(app):
    app.save_sample_data = lambda: None
    return app


def press_ok(window, delete=(), rename=None, add=None):
    """Runs edit_sample_info as if the user pressed OK in the dialog."""

    def fake_exec(dialog):
        model = dialog.table.table_model
        for row in reversed(range(model.rowCount())):
            name = model.item(row, 0).text()
            if name in delete:
                model.removeRow(row)
            elif rename and name in rename:
                model.item(row, 0).setText(rename[name])
        if add:
            dialog.table.add()
            model.item(model.rowCount() - 1, 0).setText(add)
        return True

    with patch.object(add_remove_table.AddRemoveDialoge, "exec", fake_exec):
        window.edit_sample_info()


def load(window, sampledata):
    window.sampledata = sampledata
    window.update_shown_samples()


def names(window):
    return sorted(entry["name"] for entry in window.sampledata.values())


def test_old_sample_survives_ok_next_to_a_new_sample(window):
    user = window.get_user_name_data()[0]
    load(window, {"old": sample("old"), f"new, {user}": sample("new", owner=user)})
    press_ok(window)
    assert names(window) == ["new", "old"]


def test_pressing_ok_creates_no_duplicate(window):
    load(window, {"old": sample("old", owner="")})
    press_ok(window)
    press_ok(window)
    assert list(window.sampledata) == ["old, "]


def test_deleted_shared_sample_does_not_come_back(window):
    load(window, {"old, ": sample("old", owner="")})
    press_ok(window, delete=("old",))
    assert window.sampledata == {}


def test_renamed_shared_sample_leaves_no_old_entry(window):
    load(window, {"old, ": sample("old", owner="")})
    press_ok(window, rename={"old": "renamed"})
    assert names(window) == ["renamed"]


def test_samples_of_other_users_are_not_touched(window):
    other = {"other, someone": sample("other", owner="someone")}
    load(window, {"mine, ": sample("mine", owner=""), **other})
    press_ok(window, delete=("mine",))
    assert sorted(window.sampledata) == ["other, someone"]


def test_old_sample_of_an_owner_with_a_space_is_visible_again(window):
    window.get_user_name_data = lambda: ("Some_User", {})
    load(window, {"old": sample("old", owner="Some User")})
    box = window.comboBox_sample
    assert [box.itemText(i) for i in range(box.count())] == ["old"]


def test_combobox_shows_a_merged_sample_once(window):
    user = window.get_user_name_data()[0]
    load(window, {"s1": sample("s1"), f"s1, {user}": sample("s1", owner=user)})
    box = window.comboBox_sample
    assert [box.itemText(i) for i in range(box.count())] == ["s1"]


def test_reported_case_stays_clean_after_saving_and_reloading(
    window, tmp_path, monkeypatch
):
    """Rows were duplicated on opening, OK failed with a ValueError, and the
    duplicates came back after removing them by hand."""
    user = window.get_user_name_data()[0]
    monkeypatch.setattr(load_save_functions, "appdata_path", str(tmp_path))
    del window.save_sample_data
    stored = {
        "active_sample": "old",
        "old": sample("old", owner="", description="keep"),
        "old, ": sample("old", owner=""),
        "s1": sample("s1"),
        f"s1, {user}": sample("s1", owner=user),
    }
    (tmp_path / "sampledata.json").write_text(json.dumps(stored), encoding="utf-8")

    window.load_sample_data()
    press_ok(window, add="new")
    window.load_sample_data()
    press_ok(window)
    window.load_sample_data()

    assert names(window) == ["new", "old", "s1"]
    saved = json.loads((tmp_path / "sampledata.json").read_text(encoding="utf-8"))
    saved.pop("active_sample")
    assert sorted(entry["name"] for entry in saved.values()) == ["new", "old", "s1"]


@pytest.mark.parametrize("given", ["s1", "id1", "s1 / id1"])
def test_api_selects_a_sample_by_name_or_id(window, given):
    load(window, {"other": sample("other"), "s1": sample("s1", sample_id="id1")})
    window.set_sample(given)
    assert window.comboBox_sample.currentText() == "s1 / id1"
    assert window.active_sample == "s1 / id1"


def test_api_does_not_select_a_sample_of_another_user(window):
    load(window, {"s1, someone": sample("s1", owner="someone")})
    with pytest.raises(ValueError):
        window.set_sample("s1")


def test_measurement_uses_the_sample_of_the_active_user(window):
    user = window.get_user_name_data()[0]
    load(
        window,
        {
            "s1, someone": sample("s1", owner="someone", description="other"),
            f"s1, {user}": sample("s1", owner=user, description="mine"),
        },
    )
    assert window.get_sample_name_data()[1]["description"] == "mine"


def test_answering_no_to_sample_not_found_cancels_the_protocol(window):
    load(window, {})
    window.run_engine = MagicMock()
    window.protocols_dict = {"prot": Measurement_Protocol(name="prot")}
    with patch.object(QMessageBox, "question", return_value=QMessageBox.No):
        window.run_protocol("prot")
    window.run_engine = None
    assert not window.pushButton_stop.isEnabled()
    assert not window.still_running


def test_answering_no_does_not_open_a_missing_protocol_file(window, tmp_path):
    load(window, {})
    window.preferences["py_files_path"] = str(tmp_path)
    window.protocols_dict = {"prot": Measurement_Protocol(name="prot")}
    with patch.object(QMessageBox, "question", return_value=QMessageBox.No):
        with patch.object(variables_handling, "open_link") as open_link:
            window.open_protocol("prot")
    open_link.assert_not_called()
