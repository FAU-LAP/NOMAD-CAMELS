import signal
import os
import time

import numpy as np

from PySide6.QtCore import QThread, Signal

import subprocess

from nomad_camels.EPICS_handling import make_ioc
from nomad_camels.utility import variables_handling

import importlib
import sys


class Make_Ioc(QThread):
    """Called from the MainApp.
    It runs the steps from the make_ioc package to create a
    fully operational IOC."""
    sig_step = Signal(int)
    info_step = Signal(str)

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
    sig_step = Signal(int)
    info_step = Signal(str)
    protocol_done = Signal()

    def __init__(self):
        super().__init__()
        self.protocol = None
        self.path = None
        self.popen = None
        self.current_protocol = None
        self.total_time = np.inf
        self.counter = 0
        self.paused = False
        self.already_run = False
        self.ready_to_run = False

    def run(self) -> None:
        """Runs the given `protocol` at `file_path`. If `sig_step` is
        provided, the stdout will be written there. If `info_step` is
        provided, it will update the completed-percentage with each starting
        loopstep."""
        cmd = ['.desertenv/Scripts/pythonw', '-c', "from IPython import embed; embed()"]
        flags = 0
        if os.name == 'nt':
            flags = subprocess.CREATE_NO_WINDOW
        self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      stdin=subprocess.PIPE, bufsize=1,
                                      creationflags=flags)
        self.write_to_console('%gui qt5')
        self.write_to_console('import sys')
        self.write_to_console('import importlib')
        self.write_to_console('from PySide6.QtWidgets import QApplication')
        self.write_to_console('app = QApplication(sys.argv)')
        self.write_to_console('import bluesky_handling.standard_imports')
        self.ready_to_run = True
        for line in iter(self.popen.stdout.readline, b''):
            text = line.decode().rstrip()
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
        while not self.ready_to_run:
            time.sleep(0.1)
        name = os.path.basename(path)[:-3]
        self.current_protocol = name
        self.write_to_console(f'spec = importlib.util.spec_from_file_location("{name}", "{path}")')
        self.write_to_console(f'{name}_mod = importlib.util.module_from_spec(spec)')
        self.write_to_console(f'sys.modules[spec.name] = {name}_mod')
        self.write_to_console(f'spec.loader.exec_module({name}_mod)')
        self.counter = 0
        self.total_time = prot_time
        dark = variables_handling.dark_mode
        theme = variables_handling.preferences['graphic_theme']
        self.write_to_console(f'dat_{name} = {name}_mod.main(dark={dark}, used_theme="{theme}")')
        self.already_run = True
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

class Run_Protocol_test(QThread):
    """Runs the given protocol with a file at the given path."""
    sig_step = Signal(int)
    info_step = Signal(str)
    protocol_done = Signal()

    def __init__(self, RE, main_fun):
        super().__init__()
        self.protocol = None
        self.path = None
        self.popen = None
        self.current_protocol = None
        self.total_time = np.inf
        self.counter = 0
        self.paused = False
        self.already_run = False
        self.ready_to_run = False
        self.RE = RE
        self.main_fun = main_fun

    def run(self) -> None:
        """Runs the given `protocol` at `file_path`. If `sig_step` is
        provided, the stdout will be written there. If `info_step` is
        provided, it will update the completed-percentage with each starting
        loopstep."""
        # self.counter = 0
        # self.total_time = prot_time
        dark = variables_handling.dark_mode
        theme = variables_handling.preferences['graphic_theme']
        dat_ = self.main_fun(RE=self.RE, dark=dark, used_theme=theme)
        # cmd = ['.desertenv/Scripts/pythonw', '-c', "from IPython import embed; embed()"]
        # self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
        #                               stderr=subprocess.STDOUT,
        #                               stdin=subprocess.PIPE, bufsize=1,
        #                               creationflags=subprocess.CREATE_NO_WINDOW)
        # self.write_to_console('%gui qt5')
        # self.write_to_console('import sys')
        # self.write_to_console('import importlib')
        # self.write_to_console('from PySide6.QtWidgets import QApplication')
        # self.write_to_console('app = QApplication(sys.argv)')
        # self.write_to_console('import bluesky_handling.standard_imports')
        # self.ready_to_run = True
        # for line in iter(self.popen.stdout.readline, b''):
        #     text = line.decode().rstrip()
        #     if text.startswith("starting loop_step "):
        #         self.sig_step.emit(int(self.counter/self.total_time * 100))
        #         self.counter += 1
        #     elif text.startswith("protocol finished!"):
        #         self.sig_step.emit(100)
        #         self.protocol_done.emit()
        #     else:
        #         self.info_step.emit(text)
        # self.info_step.emit('\n\n\n')
        # self.sig_step.emit(100)

    def run_protocol(self, path, prot_time):
        while not self.ready_to_run:
            time.sleep(0.1)
        name = os.path.basename(path)[:-3]
        self.current_protocol = name
        self.write_to_console(f'spec = importlib.util.spec_from_file_location("{name}", "{path}")')
        self.write_to_console(f'{name}_mod = importlib.util.module_from_spec(spec)')
        self.write_to_console(f'sys.modules[spec.name] = {name}_mod')
        self.write_to_console(f'spec.loader.exec_module({name}_mod)')
        self.counter = 0
        self.total_time = prot_time
        dark = variables_handling.dark_mode
        theme = variables_handling.preferences['graphic_theme']
        self.write_to_console(f'dat_{name} = {name}_mod.main(dark={dark}, used_theme="{theme}")')
        self.already_run = True
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
    """
    Runs the given IOC in the background.

    Parameters
    ----------
    ioc_name : str, optional
        The name of the IOC to run, by default 'Default'

    Attributes
    ----------
    info_step : Signal
        A signal that is emitted when there is a new step to be shown
    popen : Popen
        A Popen object representing the subprocess running the IOC
    last_inputs : list
        A list of the last inputs received by the IOC
    curr_last : int
        The index of the last input received by the IOC
    """
    info_step = Signal(str)

    def __init__(self, ioc_name='Default'):
        super().__init__()
        self.ioc_name = ioc_name
        self.popen = None
        self.last_inputs = []
        self.curr_last = -1

    def run(self):
        flags = 0
        if os.name == 'nt':
            flags = subprocess.CREATE_NO_WINDOW
        self.popen = subprocess.Popen(['wsl', './EPICS_handling/run_ioc.cmd',
                                       self.ioc_name],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      stdin=subprocess.PIPE, bufsize=1,
                                      creationflags=flags)
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


class Manual_Device_Thread(QThread):
    def __init__(self, device, ophyd_class):
        super().__init__()
        if device.ioc_settings['use_local_ioc']:
            ioc = variables_handling.preset
        else:
            ioc = device.ioc_settings['ioc_name']
        self.device = ophyd_class(f'{ioc}:{device.custom_name}:',
                                  name=f'manual_{device.custom_name}',
                                  **device.get_settings())
        self.device.wait_for_connection()
        self.device.configure(device.get_config())

    def update_config_settings(self, config=None, settings=None):
        config = config or {}
        settings = settings or {}
        self.device.configure(config)
        self.device.update_settings(**settings)

