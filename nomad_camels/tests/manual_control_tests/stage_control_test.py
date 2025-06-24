from PySide6.QtCore import Qt
from nomad_camels.manual_controls.stage_control.stage_control import (
    Stage_Control,
    Stage_Control_Config,
)
from nomad_camels.tests.test_helper_functions import ensure_demo_in_devices

expected_control_data = {
    "name": "Stage_Control",
    "control_type": "Stage_Control",
    "use_axis": [True, False, False],
    "axis_channel": ["demo_instrument_motorX", "", ""],
    "read_axis": [True, False, False],
    "read_channel": ["demo_instrument_motorX", "", ""],
    "axis_ref": ["None", "None", "None"],
    "axis_stop": ["None", "None", "None"],
    "manual_function": ["None", "None", "None"],
    "auto_reference": [False, False, False],
}


def test_stage_control_config(qtbot):
    """
    Test the Stage Control functionality by simulating a stage movement and verifying the position updates.
    """
    ensure_demo_in_devices()

    conf = Stage_Control_Config()
    conf.closeEvent = lambda event: None
    conf.axis_checkboxes[0].setChecked(True)  # Enable X axis
    conf.channels_combos[0].setCurrentText("demo_instrument_motorX")
    conf.read_checkboxes[0].setChecked(True)  # Enable reading for X axis
    conf.read_combos[0].setCurrentText("demo_instrument_motorX")
    qtbot.addWidget(conf)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    if conf.control_data != expected_control_data:
        if conf.control_data["axis_channel"] != expected_control_data["axis_channel"]:
            for i in range(len(conf.control_data["use_axis"])):
                if conf.control_data["use_axis"][i]:
                    continue
                conf.control_data["axis_channel"][i] = expected_control_data[
                    "axis_channel"
                ][i]
        if conf.control_data["read_channel"] != expected_control_data["read_channel"]:
            for i in range(len(conf.control_data["read_axis"])):
                if conf.control_data["read_axis"][i]:
                    continue
                conf.control_data["read_channel"][i] = expected_control_data[
                    "read_channel"
                ][i]
    assert conf.control_data == expected_control_data


def test_stage_control(qtbot):
    ensure_demo_in_devices()
    control = Stage_Control(control_data=expected_control_data, parent=None)
    qtbot.addWidget(control)
    qtbot.waitUntil(
        lambda: control.read_thread is not None and control.read_thread.isRunning(),
        timeout=5000,
    )
    qtbot.waitUntil(
        lambda: control.move_thread is not None and control.move_thread.isRunning(),
        timeout=5000,
    )
    assert control.read_thread.still_running
    assert control.move_thread.still_running
    with qtbot.waitSignal(control.lineEdit_stepX.textChanged) as blocker:
        control.lineEdit_stepX.setText("1.0")
    qtbot.waitUntil(lambda: control.control_data["stepSize_X"] == 1.0, timeout=5000)
    qtbot.mouseClick(control.pushButton_right, Qt.MouseButton.LeftButton)
    # wait until the move thread is done and the position is updated
    qtbot.waitUntil(lambda: control.read_channels[0].get() == 1.0, timeout=5000)
    qtbot.waitSignal(control.lineEdit_currentX.textChanged, timeout=5000)
    qtbot.waitUntil(
        lambda: float(control.lineEdit_currentX.text()) == 1.0, timeout=5000
    )
    control.lineEdit_manualX.setText("2.0")
    control.checkBox_manualActive.setChecked(True)
    qtbot.mouseClick(control, Qt.MouseButton.LeftButton)
    # now move manually
    qtbot.keyPress(
        control, Qt.Key.Key_Left, modifier=Qt.KeyboardModifier.ControlModifier
    )
    qtbot.waitUntil(lambda: float(control.lineEdit_currentX.text()) < 0.0, timeout=5000)
    qtbot.keyRelease(
        control, Qt.Key.Key_Left, modifier=Qt.KeyboardModifier.ControlModifier
    )

    qtbot.waitUntil(
        lambda: not control.move_thread.movers[0],
        timeout=5000,
    )
    last_position = control.read_channels[0].get()

    def check_position_stable():
        nonlocal last_position
        qtbot.wait(100)  # Wait a bit to ensure the position is stable
        same = control.read_channels[0].get() == last_position
        last_position = control.read_channels[0].get()
        return same

    qtbot.waitUntil(check_position_stable, timeout=5000)
    last_position = control.read_channels[0].get()

    # wait until the position is updated in the line edit
    qtbot.waitSignal(control.lineEdit_currentX.textChanged, timeout=5000)
    qtbot.waitUntil(
        lambda: abs(float(control.lineEdit_currentX.text()) - last_position) < 0.01,
        timeout=5000,
    )

    # now move manually and check whether stopping works
    qtbot.keyPress(
        control, Qt.Key.Key_Left, modifier=Qt.KeyboardModifier.ControlModifier
    )
    qtbot.waitUntil(
        lambda: float(control.lineEdit_currentX.text()) < last_position - 1,
        timeout=5000,
    )
    qtbot.mouseClick(control.pushButton_stop, Qt.MouseButton.LeftButton)
    qtbot.waitUntil(check_position_stable, timeout=5000)

    last_position = control.read_channels[0].get()
    qtbot.waitUntil(
        lambda: abs(float(control.lineEdit_currentX.text()) - last_position) < 0.01,
        timeout=5000,
    )

    # check whether the thread close properly
    control.move_thread.still_running = False
    control.read_thread.still_running = False
    qtbot.waitUntil(lambda: not control.move_thread.isRunning(), timeout=5000)
    qtbot.waitUntil(lambda: not control.read_thread.isRunning(), timeout=5000)
    control.close()
    assert control.move_thread is None
    assert control.read_thread is None
