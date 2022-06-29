import signal
import os

import numpy as np

from PyQt5.QtCore import QThread, pyqtSignal

import subprocess

from EPICS_handling import make_ioc
from bluesky_handling import protocol_builder
from utility import variables_handling


class Make_Ioc(QThread):
    """Called from the MainApp.
    It runs the steps from the make_ioc package to create a
    fully operational IOC."""
    sig_step = pyqtSignal(int)
    info_step = pyqtSignal(str)

    def __init__(self, ioc_name='Default', device_data=None):
        """

        Parameters
        ----------
        ioc_name : str, default "Default"
            The name of the IOC. When calling from the function in
            MainApp, it is the name of the device-preset.
        device_data : dict, default None
            The data-dictionary for the devices (including settings etc.)
        """
        if device_data is None:
            device_data = {}
        super(Make_Ioc, self).__init__()
        self.ioc_name = ioc_name
        self.device_data = device_data

    def run(self):
        self.sig_step.emit(0)
        info = make_ioc.clean_up_ioc(self.ioc_name)
        self.info_step.emit(info)
        self.sig_step.emit(1)
        info = make_ioc.change_devices(self.device_data, self.ioc_name)
        self.info_step.emit(info)
        self.sig_step.emit(10)
        info = make_ioc.make_ioc(self.ioc_name, self.info_step, self.sig_step)
        # self.info_step.emit(info)
        self.sig_step.emit(100)


class Run_Protocol(QThread):
    """Runs the given protocol with a file at the given path."""
    sig_step = pyqtSignal(int)
    info_step = pyqtSignal(str)
    protocol_done = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.protocol = None
        self.path = None
        self.popen = None
        self.current_protocol = None
        self.total_time = np.inf
        self.counter = 0
        self.paused = False

    def run(self) -> None:
        """Runs the given `protocol` at `file_path`. If `sig_step` is
        provided, the stdout will be written there. If `info_step` is
        provided, it will update the completed-percentage with each starting
        loopstep."""
        args = []
        if variables_handling.dark_mode:
            args.append('--darkmode')
        cmd = ['camelsEnv/Scripts/python', '-c', "from IPython import embed; embed()"]
        self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      stdin=subprocess.PIPE, bufsize=1)
        self.write_to_console('%gui qt5')
        self.write_to_console('import sys')
        self.write_to_console('import importlib')
        self.write_to_console('from PyQt5.QtWidgets import QApplication')
        self.write_to_console('app = QApplication(sys.argv)')
        self.write_to_console('import bluesky_handling.standard_imports')
        for line in iter(self.popen.stdout.readline, b''):
            text = line.decode().rstrip()
            print(text)
            if text.startswith("starting loop_step "):
                self.sig_step.emit(int(self.counter/self.total_time * 100))
                self.counter += 1
            elif text.startswith("protocol finished!"):
                self.sig_step.emit(100)
                self.protocol_done.emit()
            else:
                self.info_step.emit(text)
        self.info_step.emit('\n\n\n')
        self.sig_step.emit(100)

    def run_protocol(self, path, prot_time):
        name = os.path.basename(path)[:-3]
        self.current_protocol = name
        self.write_to_console(f'spec = importlib.util.spec_from_file_location("{name}", "{path}")')
        self.write_to_console(f'{name}_mod = importlib.util.module_from_spec(spec)')
        self.write_to_console(f'sys.modules[spec.name] = {name}_mod')
        self.write_to_console(f'spec.loader.exec_module({name}_mod)')
        self.counter = 0
        self.total_time = prot_time
        self.write_to_console(f'dat_{name} = {name}_mod.main()')
        # self.write_to_console(f'print(dat_{name})')

    def pause(self):
        # os.kill(self.p.pid, signal.SIGINT)
        # self.popen.stdin.write('print("test")\n'.encode())
        # self.popen.stdin.flush()
        self.popen.send_signal(signal.CTRL_C_EVENT)
        self.paused = True

    def abort(self):
        if not self.paused:
            self.pause()
        msg = f'{self.current_protocol}_mod.RE.abort()'
        self.write_to_console(msg)
        self.popen.terminate()
        self.terminate()

    def resume(self):
        msg = f'{self.current_protocol}_mod.RE.resume()'
        self.write_to_console(msg)

    def write_to_console(self, msg):
        if msg == 'exit()':
            raise Exception('Exiting the shell is not allowed!')
        if self.popen is not None:
            self.popen.stdin.write(bytes(f'{msg}\n', 'utf-8'))
            self.popen.stdin.flush()
            self.info_step.emit(f'{msg}\n')


class Run_IOC(QThread):
    """Runs the given IOC in the background."""
    info_step = pyqtSignal(str)

    def __init__(self, ioc_name='Default'):
        super().__init__()
        self.ioc_name = ioc_name
        self.popen = None
        self.last_inputs = []
        self.curr_last = -1

    def run(self):
        self.popen = subprocess.Popen(['wsl', './EPICS_handling/run_ioc.cmd',
                                       self.ioc_name],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      stdin=subprocess.PIPE, bufsize=1)
        for line in iter(self.popen.stdout.readline, b''):
            text = line.decode().rstrip()
            self.info_step.emit(text)
        # while True:
        #     line = self.popen.stdout.readline()
        #     text = line.decode().rstrip()
        #     self.info_step.emit(text)

    def write_to_ioc(self, msg):
        if 'exit' in msg:
            raise Exception('Please stop the IOC only using the button!\n(The command "exit" is not allowed!)')
        self.last_inputs.append(msg)
        if self.popen is not None:
            self.popen.stdin.write(bytes(f'{msg}\n', 'utf-8'))
            self.popen.stdin.flush()


    def terminate(self) -> None:
        if self.popen is not None:
            self.popen.communicate(input=b'exit')
        super().terminate()
