import os.path
import subprocess

from main_classes.protocol_class import Measurement_Protocol

standard_string = 'import numpy as np\n'
standard_string += 'from ophyd.signal import EpicsSignal, EpicsSignalRO\n'
standard_string += 'from bluesky import RunEngine\n'
standard_string += 'from bluesky.callbacks.best_effort import BestEffortCallback\n'
standard_string += 'import bluesky.plan_stubs as bps\n'
standard_string += 'from bluesky.utils import install_kicker\n'
standard_string += 'from databroker import Broker\n\n'

standard_run_string = '\n\n\nif __name__ == "__main__":\n'
standard_run_string += '\tRE = RunEngine({})\n'
standard_run_string += '\tbec = BestEffortCallback()\n'
standard_run_string += '\tRE.subscribe(bec)\n'
standard_run_string += '\tdb = Broker.named("temp")\n'
standard_run_string += '\tRE.subscribe(db.insert)\n'

standard_save_string = '\theaders = db[uids]\n'
standard_save_string += '\tfor header in headers:\n'
standard_save_string += '\t\tprint(header.start)\n\n'
standard_save_string += '\t\tprint(header.table())\n'

def build_protocol(protocol:Measurement_Protocol, file_path):
    protocol_string = ''
    protocol_string += standard_string
    protocol_string += protocol.get_plan_string()
    protocol_string += standard_run_string
    protocol_string += f'\tuids = RE({protocol.name}_plan())\n'
    protocol_string += standard_save_string
    if not os.path.isdir(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w+') as file:
        file.write(protocol_string)

def run_protocol(protocol:Measurement_Protocol, file_path, sig_step=None, info_step=None):
    build_protocol(protocol, file_path)
    if sig_step is not None:
        sig_step.emit(0)
    total_time = 1
    for step in protocol.loop_steps:
        total_time += step.time_weight
    p = subprocess.Popen(['python', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    i = 1
    for line in iter(p.stdout.readline, b''):
        text = line.decode().rstrip()
        if text.startswith("starting loop_step "):
            print(text)
            if sig_step is not None:
                sig_step.emit(int(i/total_time * 100))
            i += 1
        else:
            if info_step is None:
                print(text)
            else:
                info_step.emit(text)
    if info_step is not None:
        info_step.emit('\n\n\n')
    if sig_step is not None:
        sig_step.emit(100)
