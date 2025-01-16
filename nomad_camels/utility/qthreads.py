"""
CURRENTLY DEPRECATED MODULE, NOTHING IS USED
This module contains various threads that may be run from the main UI."""

from PySide6.QtCore import QThread

import importlib

from nomad_camels.utility import variables_handling


# class Run_Protocol(QThread):
#     """
#     DEPRECATED
#     Runs the given protocol with a file at the given path."""
#     sig_step = Signal(int)
#     info_step = Signal(str)
#     protocol_done = Signal()
#
#     def __init__(self):
#         super().__init__()
#         self.protocol = None
#         self.path = None
#         self.popen = None
#         self.current_protocol = None
#         self.total_time = np.inf
#         self.counter = 0
#         self.paused = False
#         self.already_run = False
#         self.ready_to_run = False
#
#     def run(self) -> None:
#         """Runs the given `protocol` at `file_path`. If `sig_step` is
#         provided, the stdout will be written there. If `info_step` is
#         provided, it will update the completed-percentage with each starting
#         loopstep.
#
#         Parameters
#         ----------
#
#         Returns
#         -------
#
#         """
#         cmd = ['.desertenv/Scripts/pythonw', '-c', "from IPython import embed; embed()"]
#         flags = 0
#         if os.name == 'nt':
#             flags = subprocess.CREATE_NO_WINDOW
#         self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
#                                       stderr=subprocess.STDOUT,
#                                       stdin=subprocess.PIPE, bufsize=1,
#                                       creationflags=flags)
#         self.write_to_console('%gui qt5')
#         self.write_to_console('import sys')
#         self.write_to_console('import importlib')
#         self.write_to_console('from PySide6.QtWidgets import QApplication')
#         self.write_to_console('app = QApplication(sys.argv)')
#         self.write_to_console('import bluesky_handling.standard_imports')
#         self.ready_to_run = True
#         for line in iter(self.popen.stdout.readline, b''):
#             text = line.decode().rstrip()
#             if text.startswith("starting loop_step "):
#                 self.sig_step.emit(int(self.counter/self.total_time * 100))
#                 self.counter += 1
#             elif text.startswith("protocol finished!"):
#                 self.sig_step.emit(100)
#                 self.protocol_done.emit()
#             else:
#                 self.info_step.emit(text)
#         self.info_step.emit('\n\n\n')
#         self.sig_step.emit(100)
#
#     def run_protocol(self, path, prot_time):
#         """
#
#         Parameters
#         ----------
#         path :
#
#         prot_time :
#
#
#         Returns
#         -------
#
#         """
#         while not self.ready_to_run:
#             time.sleep(0.1)
#         name = os.path.basename(path)[:-3]
#         self.current_protocol = name
#         self.write_to_console(f'spec = importlib.util.spec_from_file_location("{name}", "{path}")')
#         self.write_to_console(f'{name}_mod = importlib.util.module_from_spec(spec)')
#         self.write_to_console(f'sys.modules[spec.name] = {name}_mod')
#         self.write_to_console(f'spec.loader.exec_module({name}_mod)')
#         self.counter = 0
#         self.total_time = prot_time
#         dark = variables_handling.dark_mode
#         theme = variables_handling.preferences['graphic_theme']
#         self.write_to_console(f'dat_{name} = {name}_mod.main(dark={dark}, used_theme="{theme}")')
#         self.already_run = True
#         # self.write_to_console(f'print(dat_{name})')
#
#     def pause(self):
#         """ """
#         # os.kill(self.p.pid, signal.SIGINT)
#         # self.popen.stdin.write('print("test")\n'.encode())
#         # self.popen.stdin.flush()
#         self.popen.send_signal(signal.CTRL_C_EVENT)
#         self.paused = True
#
#     def abort(self):
#         """ """
#         if not self.paused:
#             self.pause()
#         msg = f'{self.current_protocol}_mod.RE.abort()'
#         self.write_to_console(msg)
#         self.popen.terminate()
#         self.terminate()
#
#     def resume(self):
#         """ """
#         msg = f'{self.current_protocol}_mod.RE.resume()'
#         self.write_to_console(msg)
#
#     def write_to_console(self, msg):
#         """
#
#         Parameters
#         ----------
#         msg :
#
#
#         Returns
#         -------
#
#         """
#         if msg == 'exit()':
#             raise Exception('Exiting the shell is not allowed!')
#         if self.popen is not None:
#             self.popen.stdin.write(bytes(f'{msg}\n', 'utf-8'))
#             self.popen.stdin.flush()
#             self.info_step.emit(f'{msg}\n')
#
# class Run_Protocol_test(QThread):
#     """
#     DEPRECATED
#     Runs the given protocol with a file at the given path."""
#     sig_step = Signal(int)
#     info_step = Signal(str)
#     protocol_done = Signal()
#
#     def __init__(self, RE, main_fun):
#         super().__init__()
#         self.protocol = None
#         self.path = None
#         self.popen = None
#         self.current_protocol = None
#         self.total_time = np.inf
#         self.counter = 0
#         self.paused = False
#         self.already_run = False
#         self.ready_to_run = False
#         self.RE = RE
#         self.main_fun = main_fun
#
#     def run(self) -> None:
#         """Runs the given `protocol` at `file_path`. If `sig_step` is
#         provided, the stdout will be written there. If `info_step` is
#         provided, it will update the completed-percentage with each starting
#         loopstep.
#
#         Parameters
#         ----------
#
#         Returns
#         -------
#
#         """
#         # self.counter = 0
#         # self.total_time = prot_time
#         dark = variables_handling.dark_mode
#         theme = variables_handling.preferences['graphic_theme']
#         dat_ = self.main_fun(RE=self.RE, dark=dark, used_theme=theme)
#         # cmd = ['.desertenv/Scripts/pythonw', '-c', "from IPython import embed; embed()"]
#         # self.popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
#         #                               stderr=subprocess.STDOUT,
#         #                               stdin=subprocess.PIPE, bufsize=1,
#         #                               creationflags=subprocess.CREATE_NO_WINDOW)
#         # self.write_to_console('%gui qt5')
#         # self.write_to_console('import sys')
#         # self.write_to_console('import importlib')
#         # self.write_to_console('from PySide6.QtWidgets import QApplication')
#         # self.write_to_console('app = QApplication(sys.argv)')
#         # self.write_to_console('import bluesky_handling.standard_imports')
#         # self.ready_to_run = True
#         # for line in iter(self.popen.stdout.readline, b''):
#         #     text = line.decode().rstrip()
#         #     if text.startswith("starting loop_step "):
#         #         self.sig_step.emit(int(self.counter/self.total_time * 100))
#         #         self.counter += 1
#         #     elif text.startswith("protocol finished!"):
#         #         self.sig_step.emit(100)
#         #         self.protocol_done.emit()
#         #     else:
#         #         self.info_step.emit(text)
#         # self.info_step.emit('\n\n\n')
#         # self.sig_step.emit(100)
#
#     def run_protocol(self, path, prot_time):
#         """
#
#         Parameters
#         ----------
#         path :
#
#         prot_time :
#
#
#         Returns
#         -------
#
#         """
#         while not self.ready_to_run:
#             time.sleep(0.1)
#         name = os.path.basename(path)[:-3]
#         self.current_protocol = name
#         self.write_to_console(f'spec = importlib.util.spec_from_file_location("{name}", "{path}")')
#         self.write_to_console(f'{name}_mod = importlib.util.module_from_spec(spec)')
#         self.write_to_console(f'sys.modules[spec.name] = {name}_mod')
#         self.write_to_console(f'spec.loader.exec_module({name}_mod)')
#         self.counter = 0
#         self.total_time = prot_time
#         dark = variables_handling.dark_mode
#         theme = variables_handling.preferences['graphic_theme']
#         self.write_to_console(f'dat_{name} = {name}_mod.main(dark={dark}, used_theme="{theme}")')
#         self.already_run = True
#         # self.write_to_console(f'print(dat_{name})')
#
#     def pause(self):
#         """ """
#         # os.kill(self.p.pid, signal.SIGINT)
#         # self.popen.stdin.write('print("test")\n'.encode())
#         # self.popen.stdin.flush()
#         self.popen.send_signal(signal.CTRL_C_EVENT)
#         self.paused = True
#
#     def abort(self):
#         """ """
#         if not self.paused:
#             self.pause()
#         msg = f'{self.current_protocol}_mod.RE.abort()'
#         self.write_to_console(msg)
#         self.popen.terminate()
#         self.terminate()
#
#     def resume(self):
#         """ """
#         msg = f'{self.current_protocol}_mod.RE.resume()'
#         self.write_to_console(msg)
#
#     def write_to_console(self, msg):
#         """
#
#         Parameters
#         ----------
#         msg :
#
#
#         Returns
#         -------
#
#         """
#         if msg == 'exit()':
#             raise Exception('Exiting the shell is not allowed!')
#         if self.popen is not None:
#             self.popen.stdin.write(bytes(f'{msg}\n', 'utf-8'))
#             self.popen.stdin.flush()
#             self.info_step.emit(f'{msg}\n')


class Manual_Device_Thread(QThread):
    """DEPRECATED"""

    def __init__(self, device, ophyd_class):
        super().__init__()
        self.device = ophyd_class(
            f"{device.custom_name}:",
            name=f"manual_{device.custom_name}",
            **device.get_settings(),
        )
        self.device.wait_for_connection()
        self.device.configure(device.get_config())

    def update_config_settings(self, config=None, settings=None):
        """

        Parameters
        ----------
        config :
             (Default value = None)
        settings :
             (Default value = None)

        Returns
        -------

        """
        config = config or {}
        settings = settings or {}
        self.device.configure(config)
        self.device.update_settings(**settings)


class Additional_Imports_Thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.imports = []
        self.catalog = None
        self.catalog_temporary = False

    def run(self) -> None:
        """ """
        from bluesky_handling.run_engine_overwrite import RunEngineOverwrite
        from bluesky.callbacks.best_effort import BestEffortCallback
        import databroker
        from nomad_camels.frontpanels.manage_instruments import ManageInstruments
        from nomad_camels.nomad_integration import nomad_communication
        import pandas as pd
        from nomad_camels.ui_widgets import add_remove_table
        from nomad_camels.nomad_integration import entry_selection
        from nomad_camels.bluesky_handling import make_catalog
        import warnings
        from nomad_camels.frontpanels.settings_window import Settings_Window
        from nomad_camels.manual_controls.get_manual_controls import (
            New_Manual_Control_Dialog,
        )
        from nomad_camels.manual_controls.get_manual_controls import (
            get_control_by_type_name,
        )
        from nomad_camels.frontpanels.protocol_config import Protocol_Config
        from nomad_camels.ui_widgets.path_button_edit import Path_Button_Dialog
        import importlib, bluesky, ophyd, time
        from nomad_camels.nomad_integration import file_uploading
        from nomad_camels.utility import databroker_export, device_handling
        from nomad_camels.bluesky_handling import protocol_builder
        from nomad_camels.tools import device_driver_builder
        from nomad_camels.tools import EPICS_driver_builder
        from nomad_camels.tools import databroker_exporter
        from nomad_camels.bluesky_handling import helper_functions

        self.imports.append(RunEngineOverwrite)
        self.imports.append(BestEffortCallback)
        self.imports.append(databroker)
        self.imports.append(ManageInstruments)
        self.imports.append(nomad_communication)
        self.imports.append(pd)
        self.imports.append(add_remove_table)
        self.imports.append(entry_selection)
        self.imports.append(make_catalog)
        self.imports.append(warnings)
        self.imports.append(Settings_Window)
        self.imports.append(New_Manual_Control_Dialog)
        self.imports.append(get_control_by_type_name)
        self.imports.append(Protocol_Config)
        self.imports.append(Path_Button_Dialog)
        self.imports.append(importlib)
        self.imports.append(bluesky)
        self.imports.append(ophyd)
        self.imports.append(time)
        self.imports.append(device_handling)
        self.imports.append(file_uploading)
        self.imports.append(databroker_export)
        self.imports.append(protocol_builder)
        self.imports.append(device_driver_builder)
        self.imports.append(EPICS_driver_builder)
        self.imports.append(databroker_exporter)
        self.imports.append(helper_functions)

        try:
            self.catalog = databroker.catalog[
                variables_handling.preferences["databroker_catalog_name"]
            ]
        except KeyError:
            print("Could not find databroker catalog, using temporary")
            self.catalog = databroker.temp().v2
            self.catalog_temporary = True
