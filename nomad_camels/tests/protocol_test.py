import importlib
import os.path
import sys
import databroker
from nomad_camels.frontpanels import protocol_config
from nomad_camels.bluesky_handling import make_catalog
from nomad_camels.frontpanels import instrument_installer
from nomad_camels.utility import variables_handling
from PySide6.QtCore import Qt


def test_change_dev_config(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import change_device_config
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Change Device Config')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      change_device_config.Change_DeviceConf_Config)
    conf_widge.comboBox_device.setCurrentText('demo_device')
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = 'test_change_dev_config_protocol'
    assert 'Change Device Config (Change_Device_Config)' in prot.loop_step_dict
    assert prot.loop_steps[0].device == 'demo_device'
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_for_loop():
    pass

def test_gradient_descent():
    pass

def test_if():
    pass

def test_nd_sweep():
    pass

def test_read_channels(qtbot, tmp_path):
    ensure_demo_in_devices()
    from nomad_camels.loop_steps import read_channels
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Read Channels')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      read_channels.Read_Channels_Config)
    table = conf_widge.sub_widget.read_table.tableWidget_channels
    row = get_row_from_channel_table('demo_device_detectorX', table)
    table.item(row, 0).setCheckState(Qt.CheckState.Checked)
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = 'test_read_channels_protocol'
    assert 'Read Channels (Read_Channels)' in prot.loop_step_dict
    assert prot.loop_steps[0].channel_list == ['demo_device_detectorX']
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)

def test_run_subprotocol():
    pass

def test_set_channels():
    pass

def test_set_variables():
    pass

def test_simple_sweep():
    pass

def test_trigger_channels():
    pass

def test_while_loop():
    pass

def test_wait(qtbot, tmp_path):
    from nomad_camels.loop_steps import wait_loop_step
    conf = protocol_config.Protocol_Config()
    qtbot.addWidget(conf)
    action = get_action_from_name(conf.add_actions, 'Wait')
    action.trigger()
    conf_widge = conf.loop_step_configuration_widget
    assert isinstance(conf_widge,
                      wait_loop_step.Wait_Loop_Step_Config)
    conf_widge.sub_widget.lineEdit_duration.setText('1.0')
    with qtbot.waitSignal(conf.accepted) as blocker:
        conf.accept()
    prot = conf.protocol
    prot.name = 'test_wait_protocol'
    assert 'Wait (Wait)' in prot.loop_step_dict
    assert prot.loop_steps[0].wait_time == '1.0'
    catalog_maker(tmp_path)
    run_test_protocol(tmp_path, prot)


def get_row_from_channel_table(name, table):
    for i in range(table.rowCount()):
        row_name = table.item(i, 1).text()
        if name == row_name:
            return i


def ensure_demo_in_devices():
    instr, packs = instrument_installer.getInstalledDevices(True, True)
    if 'demo_device' not in instr:
        instrument_installer.install_instrument('demo_device')
        instr, packs = instrument_installer.getInstalledDevices(True, True)
        assert 'demo_device' in instr
    if 'demo_device' not in variables_handling.devices:
        inst = packs['demo_device'].subclass()
        variables_handling.devices['demo_device'] = inst
    assert 'demo_device' in variables_handling.devices
    variables_handling.channels.clear()
    for key, dev in variables_handling.devices.items():
        for channel in dev.get_channels():
            variables_handling.channels.update({channel: dev.channels[channel]})


def catalog_maker(tmp_path):
    if 'test_catalog' not in list(databroker.catalog):
        make_catalog.make_yml(tmp_path, 'test_catalog')

def run_test_protocol(tmp_path, protocol):
    from nomad_camels.bluesky_handling import protocol_builder
    file = tmp_path / (protocol.name + '.py')
    savepath = tmp_path / (protocol.name + '.h5')
    protocol_builder.build_protocol(protocol, file, savepath, 'test_catalog')
    sys.path.append(str(tmp_path))
    py_package = importlib.import_module(protocol.name)
    py_package.main()
    assert os.path.isfile(savepath)

def get_action_from_name(actions, name):
    for act in actions:
        if act.text() == name:
            return act
    return None
