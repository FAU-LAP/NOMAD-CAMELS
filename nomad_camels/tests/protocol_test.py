import importlib
import os.path
import sys
import databroker
from nomad_camels.frontpanels import protocol_config
from nomad_camels.bluesky_handling import make_catalog


def test_change_dev_config(qtbot):
    pass

def test_for_loop():
    pass

def test_gradient_descent():
    pass

def test_if():
    pass

def test_nd_sweep():
    pass

def test_prompt():
    pass

def test_read_channels():
    pass

def test_run_subprotocol():
    pass

def test_set_channels():
    pass

def test_set_value_popup():
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
    assert 'Wait (Wait)' in prot.loop_step_dict
    assert prot.loop_steps[0].wait_time == '1.0'
    make_catalog.make_yml(tmp_path, 'test_catalog')
    run_test_protocol(tmp_path, prot)




def run_test_protocol(tmp_path, protocol):
    from nomad_camels.bluesky_handling import protocol_builder
    protocol.name = 'test_wait_protocol'
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
