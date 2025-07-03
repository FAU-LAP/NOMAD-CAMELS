import importlib
import os.path
import sys
import databroker
import pytest

from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtWidgets import QMessageBox

from nomad_camels.frontpanels import protocol_config
from nomad_camels.bluesky_handling import make_catalog
from nomad_camels.utility import variables_handling
from nomad_camels.utility.treeView_functions import getItemIndex
from threading import Thread
import asyncio
from zmq.error import ZMQError
from bluesky.callbacks.zmq import RemoteDispatcher, Publisher
from nomad_camels.main_classes.plot_proxy import StoppableProxy as Proxy
from nomad_camels.tests.test_helper_functions import ensure_demo_in_devices

import socket

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


subprotocol_path = None


@pytest.fixture(scope="session", autouse=True)
def zmq_setup():
    """
    Sets up a single ZMQ proxy, dispatcher, and publisher for all tests.
    Yields a tuple (publisher, dispatcher) for use in tests.
    Stops the proxy at the end of the session.
    """
    try:
        proxy = Proxy(5577, 5578)
        proxy_created = True
    except ZMQError:
        proxy = None  # Use already running proxy.
        proxy_created = False

    def start_proxy():
        if proxy_created and proxy is not None:
            proxy.start()

    # Setup dispatcher and its thread.
    dispatcher = RemoteDispatcher("localhost:5578")

    def start_dispatcher():
        try:
            dispatcher.start()
        except asyncio.exceptions.CancelledError:
            pass  # Ignore cancellation errors on shutdown.

    # Setup publisher.
    publisher = Publisher("localhost:5577")

    # Start proxy and dispatcher in daemon threads.
    proxy_thread = Thread(target=start_proxy, daemon=True)
    dispatcher_thread = Thread(target=start_dispatcher, daemon=True)
    proxy_thread.start()
    dispatcher_thread.start()

    # Yield the shared objects for tests.
    yield publisher, dispatcher

    # Teardown: stop the proxy once all tests have finished.
    if proxy_created and proxy is not None:
        proxy.stop()


@pytest.fixture(autouse=True)
def mock_message_box(monkeypatch):
    """If a messagebox, e.g. asking whether to discard all changes to the
    protocol, pops up, it is automatically accepted"""

    def mock_question(*args, **kwargs):
        return QMessageBox.Yes

    monkeypatch.setattr(QMessageBox, "question", mock_question)


def test_change_dev_config(qtbot, tmp_path, zmq_setup):
    """Opens the config for "change device config" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import change_device_config

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_change_dev_config_protocol"
    )
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Change Device Config")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, change_device_config.Change_DeviceConf_Config)
    conf_widge.comboBox_device.setCurrentText("demo_instrument")
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_change_dev_config_protocol"
    assert "Change Device Config (Change_Device_Config)" in prot.loop_step_dict
    assert prot.loop_steps[0].device == "demo_instrument"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_for_loop(qtbot, tmp_path, zmq_setup):
    """Opens the config for a "For Loop" tries to configure it looping over a
    wait-step and tries to run a protocol with this step."""
    # ensure_demo_in_devices()
    from nomad_camels.loop_steps import for_while_loops

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_for_loop_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "For Loop")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, for_while_loops.For_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_start.setText("0")
    conf_widge.sub_widget.lineEdit_stop.setText("1")
    conf_widge.sub_widget.lineEdit_n_points.setText("11")

    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()
    prot = conf.protocol

    select_step_by_name(conf, "Wait (Wait)")

    def wait_for_move_in():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1

    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = "test_for_loop_protocol"
    assert "For Loop (For_Loop)" in prot.loop_step_dict
    assert prot.loop_steps[0].has_children
    assert prot.loop_steps[0].children[0].full_name == "Wait (Wait)"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_gradient_descent(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Gradient Descent" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import gradient_descent

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_gradient_descent_protocol"
    )
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Gradient Descent")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, gradient_descent.Gradient_Descent_Config)
    conf_widge.sub_widget.lineEdit_momentum.setText("1")
    conf_widge.sub_widget.lineEdit_threshold.setText("1e-3")
    conf_widge.sub_widget.lineEdit_max_val.setText("1")
    conf_widge.sub_widget.lineEdit_min_val.setText("1")
    conf_widge.sub_widget.lineEdit_opt_func.setText("demo_instrument_detectorY")
    conf_widge.sub_widget.lineEdit_max_n_steps.setText("25")
    conf_widge.sub_widget.lineEdit_largest_step.setText("1")
    conf_widge.sub_widget.lineEdit_smallest_step.setText("0.01")
    conf_widge.sub_widget.lineEdit_learning_rate.setText("1")
    conf_widge.sub_widget.lineEdit_starting_val.setText("0")
    conf_widge.sub_widget.comboBox_extremum_type.setCurrentText("Maximum")
    conf_widge.sub_widget.comboBox_output_channel.setCurrentText(
        "demo_instrument_motorY"
    )
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.loop_steps[0].read_channels.append("demo_instrument_detectorY")
    prot.name = "test_gradient_descent_protocol"
    assert "Gradient Descent (Gradient_Descent)" in prot.loop_step_dict
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


@pytest.mark.order(1)
def test_if_and_set_variables(qtbot, tmp_path, zmq_setup):
    """Opens the config for "If" tries to configure to run the correct way if
    the variables have the correct value, which is done by a "Set Variables" step."""
    from nomad_camels.loop_steps import set_variables

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_if_and_set_variables_protocol"
    )
    prot = conf.protocol
    qtbot.addWidget(conf)
    qtbot.mouseClick(
        conf.general_settings.pushButton_add_variable, Qt.MouseButton.LeftButton
    )
    conf.general_settings.variable_table.model.item(0, 0).setText("condition")
    conf.general_settings.variable_table.model.item(0, 1).setText("1")
    single_variable_if(qtbot, conf, 1)
    assert "If (If)" in prot.loop_step_dict
    assert "If_Sub (If_condition != 1)" in prot.loop_step_dict
    assert "Elif_Sub (If_condition == 1)" in prot.loop_step_dict
    assert "Else_Sub (If_Else)" in prot.loop_step_dict

    action = get_action_from_name(conf.add_actions, "Set Variables")
    action.trigger()

    def wait_selection():
        """ """
        select_step_by_name(conf, f"Set Variables (Set_Variables)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, set_variables.Set_Variables_Config
        )

    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(
        conf.loop_step_configuration_widget, set_variables.Set_Variables_Config
    )
    conf_widge.variables_table.add(["condition", "0"])

    single_variable_if(qtbot, conf, 0, 2, 1, 2)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)
    global subprotocol_path
    if subprotocol_path is None:
        subprotocol_path = str((tmp_path / (prot.name + ".cprot")).as_posix())


def test_nd_sweep(qtbot, tmp_path, zmq_setup):
    """ """
    """Opens the config for "Simple Sweep" tries to configure it for the
    demo instrument. Further it adds a plot and a fit to the sweep and tries to
    run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import nd_sweep
    from nomad_camels.frontpanels import plot_definer

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_nd_sweep_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "ND Sweep")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, nd_sweep.ND_Sweep_Config)
    qtbot.mouseClick(conf_widge.addSweepChannelButton, Qt.MouseButton.LeftButton)
    conf_widge.tabs[0].sweep_widget.lineEdit_start.setText("-10")
    conf_widge.tabs[0].sweep_widget.lineEdit_stop.setText("10")
    conf_widge.tabs[0].sweep_widget.lineEdit_n_points.setText("7")
    conf_widge.tabs[0].lineEdit_wait_time.setText("0.01")
    conf_widge.tabs[0].comboBox_sweep_channel.setCurrentText("demo_instrument_motorY")
    conf_widge.tabs[1].sweep_widget.lineEdit_start.setText("-10")
    conf_widge.tabs[1].sweep_widget.lineEdit_stop.setText("10")
    conf_widge.tabs[1].sweep_widget.lineEdit_n_points.setText("7")
    conf_widge.tabs[1].comboBox_sweep_channel.setCurrentText("demo_instrument_motorX")

    table = conf_widge.read_table.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_motorX", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    row = get_row_from_channel_table("demo_instrument_motorY", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    row = get_row_from_channel_table("demo_instrument_detectorComm", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)

    plot = plot_definer.Plot_Info(
        plt_type="2D plot",
        x_axis="demo_instrument_motorX",
        y_axes={"formula": ["demo_instrument_motorY"], "axis": ["left"]},
        z_axis="demo_instrument_detectorComm",
        browser_port=get_available_port(),
        checkbox_show_in_browser=True,
    )
    conf_widge.plot_widge.plot_data = [plot]

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_nd_sweep_protocol"
    assert "ND Sweep (ND_Sweep)" in prot.loop_step_dict
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_read_channels(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Read Channels" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import read_channels

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_read_channels_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, read_channels.Read_Channels_Config)
    table = conf_widge.sub_widget.read_table.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_detectorX", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_read_channels_protocol"
    assert "Read Channels (Read_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[0].channel_list == ["demo_instrument_detectorX"]
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


@pytest.mark.order(2)
def test_run_subprotocol(qtbot, tmp_path, zmq_setup, monkeypatch):
    """ """
    global subprotocol_path
    if subprotocol_path is None:
        raise ValueError(
            "No subprotocol for test found! Make sure the test_if_and_set_variables is run first and works."
        )

    from nomad_camels.loop_steps import run_subprotocol, read_channels
    from nomad_camels.utility.load_save_functions import standard_pref
    from nomad_camels.utility import variables_handling

    variables_handling.preferences = standard_pref

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_run_subprotocol_protocol"
    )
    qtbot.addWidget(conf)
    qtbot.mouseClick(
        conf.general_settings.pushButton_add_variable, Qt.MouseButton.LeftButton
    )
    conf.general_settings.variable_table.model.item(0, 0).setText("condition_out")
    conf.general_settings.variable_table.model.item(0, 1).setText("1")

    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    conf_widge.sub_widget.checkBox_read_variables.setChecked(True)

    action = get_action_from_name(conf.add_actions, "Run Subprotocol")
    action.trigger()

    def wait_selection():
        """ """
        select_step_by_name(conf, f"Run Subprotocol (Run_Subprotocol)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, run_subprotocol.Run_Subprotocol_Config
        )

    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, run_subprotocol.Run_Subprotocol_Config)
    conf_widge.path_button.set_path(subprotocol_path)
    conf_widge.input_table.add(vals=["condition", "4"])
    conf_widge.output_table.add(vals=["condition", "condition_out"])

    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()

    def wait_selection():
        """ """
        select_step_by_name(conf, f"Read Channels (Read_Channels)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, read_channels.Read_Channels_Config
        )

    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    conf_widge.sub_widget.checkBox_read_variables.setChecked(True)

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_run_subprotocol_protocol"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup

    # Import the original Prompt_Box so we can use it as a specification.
    from unittest.mock import MagicMock
    from nomad_camels.bluesky_handling.helper_functions import Prompt_Box

    # Create a fake prompt instance (the mock) with the same interface as Prompt_Box.
    fake_prompt = MagicMock(spec=Prompt_Box)
    fake_prompt.done_flag = False
    fake_prompt.helper = MagicMock()
    fake_prompt.helper.executor = MagicMock()

    # Define a side effect for the executor's emit() method:
    def fake_emit():
        fake_prompt.done_flag = True

    fake_prompt.helper.executor.emit.side_effect = fake_emit

    # Monkeypatch the Prompt_Box constructor so that whenever it is instantiated,
    # it returns our fake_prompt
    monkeypatch.setattr(
        "nomad_camels.bluesky_handling.helper_functions.Prompt_Box",
        lambda *args, **kwargs: fake_prompt,
    )

    savepath = run_test_protocol(
        tmp_path, prot, publisher, dispatcher, return_savepath=True
    )
    import h5py

    with h5py.File(savepath, "r") as f:
        # Check if the output variable is set correctly
        variable_data = f["CAMELS_entry"]["data"][
            "test_run_subprotocol_protocol_variable_signal"
        ]["condition_out"]
        assert len(variable_data) == 2
        assert variable_data[0] == 1
        assert variable_data[1] == 0


def test_set_channels(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Set Channels" tries to configure it for the
    demo instrument and tries to run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import set_channels

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_set_channels_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Set Channels")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, set_channels.Set_Channels_Config)
    table = conf_widge.sub_widget.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_motorX", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    table.item(row, 2).setText("1")
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_set_channels_protocol"
    assert "Set Channels (Set_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[0].channels_values == {
        "Channels": ["demo_instrument_motorX"],
        "Values": ["1"],
    }
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_simple_sweep_with_plot_and_fit(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Simple Sweep" tries to configure it for the
    demo instrument. Further it adds a plot and a fit to the sweep and tries to
    run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import simple_sweep
    from nomad_camels.frontpanels import plot_definer

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_simple_sweep_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Simple Sweep")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, simple_sweep.Simple_Sweep_Config)
    conf_widge.sweep_widget.lineEdit_start.setText("-10")
    conf_widge.sweep_widget.lineEdit_stop.setText("10")
    conf_widge.sweep_widget.lineEdit_n_points.setText("21")
    conf_widge.comboBox_sweep_channel.setCurrentText("demo_instrument_motorY")

    table = conf_widge.read_table.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_detectorY", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    row = get_row_from_channel_table("demo_instrument_motorY", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)

    fit = plot_definer.Fit_Info(
        True, "Gaussian", x="demo_instrument_motorY", y="demo_instrument_detectorY"
    )
    plot = plot_definer.Plot_Info(
        x_axis="demo_instrument_motorY",
        y_axes={"formula": ["demo_instrument_detectorY"], "axis": ["left"]},
        fits=[fit],
    )
    conf_widge.plot_widge.plot_data = [plot]

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_simple_sweep_protocol"
    assert "Simple Sweep (Simple_Sweep)" in prot.loop_step_dict
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_for_loop_set_var_with_plot_and_linear_fit(qtbot, tmp_path, zmq_setup):
    """Creates a For Loop from -1 to 1 that, on each iteration,
    sets the variable 'set_var' to the loop value and waits for 0.001s.
    The protocol is configured to plot 'set_var' versus the loop value
    and perform a linear fit that is expected to be perfect (slope=1, intercept=0)."""
    # Create the protocol config widget and set the protocol name.
    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText(
        "test_for_loop_set_var_protocol"
    )
    qtbot.addWidget(conf)

    # Add a global variable "set_var" (initial value is arbitrary here).
    qtbot.mouseClick(
        conf.general_settings.pushButton_add_variable, Qt.MouseButton.LeftButton
    )
    conf.general_settings.variable_table.model.item(0, 0).setText("set_var")
    conf.general_settings.variable_table.model.item(0, 1).setText("0")

    # --- Add For Loop step ---
    action = get_action_from_name(conf.add_actions, "For Loop")
    action.trigger()
    from nomad_camels.loop_steps import for_while_loops

    conf_widge_loop = conf.loop_step_configuration_widget
    assert isinstance(conf_widge_loop, for_while_loops.For_Loop_Step_Config)
    conf_widge_loop.sub_widget.lineEdit_start.setText("-1")
    conf_widge_loop.sub_widget.lineEdit_stop.setText("1")
    conf_widge_loop.sub_widget.lineEdit_n_points.setText("21")

    # --- Add child step: Set Variables ---
    action = get_action_from_name(conf.add_actions, "Set Variables")
    action.trigger()
    from nomad_camels.loop_steps import set_variables

    def wait_selection_sv():
        select_step_by_name(conf, "Set Variables (Set_Variables)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, set_variables.Set_Variables_Config
        )

    qtbot.waitUntil(wait_selection_sv)
    conf_widge_sv = conf.loop_step_configuration_widget
    # Configure the Set Variables step to assign the current for loop value to "set_var".
    # Here we assume that the expression "for_loop_value" is evaluated at runtime.
    conf_widge_sv.variables_table.add(["set_var", "For_Loop_Value"])

    # --- Read Channels ---
    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()
    from nomad_camels.loop_steps import read_channels

    def wait_selection_rc():
        select_step_by_name(conf, "Read Channels (Read_Channels)")
        conf.tree_click_sequence()
        assert isinstance(
            conf.loop_step_configuration_widget, read_channels.Read_Channels_Config
        )

    qtbot.waitUntil(wait_selection_rc)

    # --- Add child step: Wait ---
    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()

    from nomad_camels.loop_steps import wait_loop_step

    def wait_for_wait_widget():
        select_step_by_name(conf, "Wait (Wait)")
        conf.tree_click_sequence()
        return isinstance(
            conf.loop_step_configuration_widget, wait_loop_step.Wait_Loop_Step_Config
        )

    qtbot.waitUntil(wait_for_wait_widget)
    conf_widge_wait = conf.loop_step_configuration_widget
    assert isinstance(conf_widge_wait, wait_loop_step.Wait_Loop_Step_Config)
    conf_widge_wait.sub_widget.lineEdit_duration.setText("0.01")

    # --- Add a Plot definition with a linear fit ---
    from nomad_camels.frontpanels import plot_definer

    fit = plot_definer.Fit_Info(True, "Linear", x="For_Loop_Value", y="set_var")
    plot = plot_definer.Plot_Info(
        x_axis="For_Loop_Value",
        y_axes={"formula": ["set_var"], "axis": ["left"]},
        fits=[fit],
    )

    # Accept the protocol configuration.
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_for_loop_set_var_protocol"
    prot.plots.append(plot)

    def wait_for_move_in():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        print(len(prot.loop_steps))

    select_step_by_name(conf, "Set Variables (Set_Variables)")
    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    select_step_by_name(conf, "Read Channels (Read_Channels)")
    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    select_step_by_name(conf, "Wait (Wait)")
    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()

    # Build the catalog and run the protocol.
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)

    # --- After the protocol run, open the Nexus file and perform a linear fit ---
    # We assume that the protocol saves two datasets: one for the for-loop values
    # (named "for_loop_value") and one for the variable "set_var".
    import h5py
    import numpy as np

    if prot.use_nexus:
        file_ending = ".nxs"
    else:
        file_ending = ".h5"
    savepath = tmp_path / (prot.name + file_ending)
    with h5py.File(savepath, "r") as f:
        x_data = f[list(f.keys())[0]]["data"][
            "test_for_loop_set_var_protocol_variable_signal"
        ]["For_Loop_Value"][
            :
        ]  # for-loop (x-axis) values
        y_data = f[list(f.keys())[0]]["data"][
            "test_for_loop_set_var_protocol_variable_signal"
        ]["set_var"][
            :
        ]  # recorded set_var values
        slope_camels_fit = f[list(f.keys())[0]]["data"]["fits"][
            "Linear_set_var_v_For_Loop_Value_primary"
        ]["slope"][
            :
        ]  # linear fit values
        intercept_camels_fit = f[list(f.keys())[0]]["data"]["fits"][
            "Linear_set_var_v_For_Loop_Value_primary"
        ]["intercept"][
            :
        ]  # linear fit intercept

    # Compute a linear fit on the data.
    slope, intercept = np.polyfit(x_data, y_data, 1)
    # Check that the slope and intercept from the CAMELS fit are the same as the ones computed from the data.
    assert np.isclose(slope_camels_fit, slope, atol=0.05)
    assert np.isclose(intercept_camels_fit, intercept, atol=0.05)
    # Check that the slope is 1 and the intercept is 0 (within a small tolerance).
    assert np.isclose(slope, 1, atol=0.05)
    assert np.isclose(intercept, 0, atol=0.05)


def test_trigger_and_read_channels(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Read Channels" tries to configure it with a split
    triggering of the channels, then configures the trigger-step and tries to
    run a protocol with these steps."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import read_channels

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_trigger_protocol")
    qtbot.addWidget(conf)
    prot = conf.protocol
    variables_handling.current_protocol = prot
    action = get_action_from_name(conf.add_actions, "Read Channels")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, read_channels.Read_Channels_Config)
    conf_widge.sub_widget.checkBox_split_trigger.setChecked(True)
    conf_widge.sub_widget.checkBox_read_all.setChecked(True)

    action = get_action_from_name(conf.add_actions, "Trigger Channels")
    action.trigger()
    select_step_by_name(conf, "Trigger Channels (Trigger_Channels)")
    conf.tree_click_sequence()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, read_channels.Trigger_Channels_Config)

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        assert isinstance(prot.loop_steps[0], read_channels.Trigger_Channels_Step)

    qtbot.waitUntil(wait_for_move)

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = "test_trigger_protocol"
    assert "Read Channels (Read_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[1].read_all
    assert "Trigger Channels (Trigger_Channels)" in prot.loop_step_dict
    assert prot.loop_steps[0].read_step == "Read Channels (Read_Channels)"

    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_while_loop(qtbot, tmp_path, zmq_setup):
    """Opens the config for a "While Loop" and tries to configure it with the
    condition being `While_Loop_Count < 5`. Into the loop, a wait-step is added.
    Tries to run a protocol with this step."""
    from nomad_camels.loop_steps import for_while_loops

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_while_loop_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "While Loop")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, for_while_loops.While_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_condition.setText("While_Loop_Count < 5")

    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()
    prot = conf.protocol

    select_step_by_name(conf, "Wait (Wait)")

    def wait_for_move_in():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1

    qtbot.waitUntil(wait_for_move_in)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot.name = "test_while_loop_protocol"
    assert "While Loop (While_Loop)" in prot.loop_step_dict
    assert prot.loop_steps[0].has_children
    assert prot.loop_steps[0].children[0].full_name == "Wait (Wait)"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_wait(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Wait" tries to configure it to a wait time of
    1.0 second and tries to run a protocol with this step."""
    from nomad_camels.loop_steps import wait_loop_step

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_wait_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, wait_loop_step.Wait_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_duration.setText("1.0")
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_wait_protocol"
    assert "Wait (Wait)" in prot.loop_step_dict
    assert prot.loop_steps[0].wait_time == "1.0"
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def test_protocol_with_flyer(qtbot, tmp_path, zmq_setup):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import wait_loop_step

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_flyer_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Wait")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, wait_loop_step.Wait_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_duration.setText("3.0")

    from nomad_camels.frontpanels.flyer_window import FlyerWindow

    flyer_window = FlyerWindow()
    qtbot.addWidget(flyer_window)
    flyer_window.flyer_table.add("flyer1", 0.1)
    flyer_window.change_flyer_def(flyer_window.flyer_table.table_model.index(0, 0))
    flyer_window.flyer_def.lineEdit_name.setText("flyer1")
    flyer_window.flyer_def.lineEdit_read_rate.setText("0.1")
    flyer_window.flyer_def.channels_table.lineEdit_search.setText(
        "demo_instrument_detectorComm"
    )
    flyer_window.flyer_def.channels_table.change_search()
    flyer_window.flyer_def.channels_table.tableWidget_channels.item(0, 0).setCheckState(
        Qt.CheckState.Checked
    )
    with qtbot.waitSignal(flyer_window.accepted) as blocker:
        flyer_window.accept()
    conf.general_settings.flyer_button.flyer_data = flyer_window.flyer_data
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    prot = conf.protocol
    savepath = run_test_protocol(
        tmp_path, prot, publisher, dispatcher, return_savepath=True
    )
    import h5py

    with h5py.File(savepath, "r") as f:
        data = f["CAMELS_entry"]["data"]
        assert "flyer1" in data
        flyer_data = data["flyer1"]
        assert "demo_instrument_detectorComm" in flyer_data
        assert "time" in flyer_data
        assert len(flyer_data["time"]) > 20
        assert len(flyer_data["demo_instrument_detectorComm"]) == len(
            flyer_data["time"]
        )


def test_simple_sweep_with_plotly(qtbot, tmp_path, zmq_setup):
    """Opens the config for "Simple Sweep" tries to configure it for the
    demo instrument. Further it adds a plot and a fit to the sweep and tries to
    run a protocol with this step."""
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import simple_sweep
    from nomad_camels.frontpanels import plot_definer

    conf = protocol_config.Protocol_Config()
    conf.general_settings.lineEdit_protocol_name.setText("test_simple_sweep_protocol")
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, "Simple Sweep")
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge, simple_sweep.Simple_Sweep_Config)
    conf_widge.sweep_widget.lineEdit_start.setText("-10")
    conf_widge.sweep_widget.lineEdit_stop.setText("10")
    conf_widge.sweep_widget.lineEdit_n_points.setText("21")
    conf_widge.comboBox_sweep_channel.setCurrentText("demo_instrument_motorY")

    table = conf_widge.read_table.tableWidget_channels
    row = get_row_from_channel_table("demo_instrument_detectorY", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    row = get_row_from_channel_table("demo_instrument_motorY", table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)

    fit = plot_definer.Fit_Info(
        True, "Gaussian", x="demo_instrument_motorY", y="demo_instrument_detectorY"
    )
    plot = plot_definer.Plot_Info(
        x_axis="demo_instrument_motorY",
        y_axes={"formula": ["demo_instrument_detectorY"], "axis": ["left"]},
        fits=[fit],
        checkbox_show_in_browser=True,
        browser_port=get_available_port(),
    )
    conf_widge.plot_widge.plot_data = [plot]

    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = "test_simple_sweep_protocol"
    assert "Simple Sweep (Simple_Sweep)" in prot.loop_step_dict
    catalog_maker(tmp_path)
    publisher, dispatcher = zmq_setup
    run_test_protocol(tmp_path, prot, publisher, dispatcher)


def single_variable_if(qtbot, conf, wait_in=1, n_prompt=0, n_if=0, len_prot=0):
    """

    Parameters
    ----------
    qtbot :

    conf :

    wait_in :
         (Default value = 1)
    n_prompt :
         (Default value = 0)
    n_if :
         (Default value = 0)
    len_prot :
         (Default value = 0)

    Returns
    -------

    """
    from nomad_camels.loop_steps import if_step

    action = get_action_from_name(conf.add_actions, "If")
    action.trigger()

    def wait_selection():
        """ """
        if n_if:
            select_step_by_name(conf, f"If (If_{n_if})")
        else:
            select_step_by_name(conf, f"If (If)")
        conf.tree_click_sequence()
        assert isinstance(conf.loop_step_configuration_widget, if_step.If_Step_Config)

    qtbot.waitUntil(wait_selection)
    conf_widge = conf.loop_step_configuration_widget
    conf_widge.sub_widget.lineEdit_condition.setText("condition != 1")
    conf_widge.sub_widget.elif_table.add("condition == 1")
    conf_widge.sub_widget.checkBox_use_else.setChecked(True)
    nam = "Prompt" if 0 != wait_in else "Wait"
    action = get_action_from_name(conf.add_actions, nam)
    action.trigger()
    prot = conf.protocol

    if n_prompt > 0 and nam == "Prompt":
        select_step_by_name(conf, f"{nam} ({nam}_{n_prompt})")
        n_prompt += 1
    elif nam == "Wait" and n_if:
        select_step_by_name(conf, f"{nam} ({nam}_{n_if})")
    else:
        select_step_by_name(conf, f"{nam} ({nam})")

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_out, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot

    qtbot.waitUntil(wait_for_move)

    nam = "Prompt" if 1 != wait_in else "Wait"
    action = get_action_from_name(conf.add_actions, nam)
    action.trigger()
    if n_prompt > 0 and nam == "Prompt":
        select_step_by_name(conf, f"{nam} ({nam}_{n_prompt})")
        n_prompt += 1
    elif nam == "Wait" and n_if:
        select_step_by_name(conf, f"{nam} ({nam}_{n_if})")
    else:
        select_step_by_name(conf, f"{nam} ({nam})")

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_out, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_up, Qt.MouseButton.LeftButton)
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot

    qtbot.waitUntil(wait_for_move)

    action = get_action_from_name(conf.add_actions, "Prompt")
    action.trigger()
    if n_prompt == 0:
        n_prompt += 1
    select_step_by_name(conf, f"Prompt (Prompt_{n_prompt})")

    def wait_for_move():
        """ """
        qtbot.mouseClick(conf.pushButton_move_step_in, Qt.MouseButton.LeftButton)
        assert len(prot.loop_steps) == 1 + len_prot

    qtbot.waitUntil(wait_for_move)


def select_step_by_name(conf, name):
    """

    Parameters
    ----------
    conf :

    name :


    Returns
    -------

    """
    model = conf.treeView_protocol_sequence.model()
    conf.treeView_protocol_sequence.selectionModel().clearSelection()
    index = getItemIndex(model, name)
    conf.treeView_protocol_sequence.selectionModel().select(
        index, QItemSelectionModel.Select
    )
    conf.check_movability()


def get_row_from_channel_table(name, table):
    """

    Parameters
    ----------
    name :

    table :


    Returns
    -------

    """
    for i in range(table.rowCount()):
        row_name = table.item(i, 1).text()
        if name == row_name:
            return i


def catalog_maker(tmp_path):
    """

    Parameters
    ----------
    tmp_path :


    Returns
    -------

    """
    if tmp_path is None:
        tmp_path = ""
    if "test_catalog" not in list(databroker.catalog):
        make_catalog.make_yml(tmp_path, "test_catalog")


def run_test_protocol(tmp_path, protocol, publisher, dispatcher, return_savepath=False):
    """

    Parameters
    ----------
    tmp_path :

    protocol :


    Returns
    -------

    """
    from nomad_camels.bluesky_handling import protocol_builder

    file = tmp_path / (protocol.name + ".py")
    savepath = tmp_path / protocol.name
    protocol_builder.build_protocol(protocol, file, savepath, "test_catalog")
    sys.path.append(str(tmp_path))
    py_package = importlib.import_module(protocol.name)
    py_package.main(dispatcher=dispatcher, publisher=publisher)
    if protocol.use_nexus:
        file_ending = ".nxs"
    else:
        file_ending = ".h5"
    savepath = f"{savepath}{file_ending}"
    assert os.path.isfile(savepath)
    if return_savepath:
        return savepath


def get_action_from_name(actions, name):
    """

    Parameters
    ----------
    actions :

    name :


    Returns
    -------

    """
    for act in actions:
        if act.text() == name:
            return act
    return None
