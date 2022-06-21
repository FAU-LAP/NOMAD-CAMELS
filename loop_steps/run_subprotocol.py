from PyQt5.QtWidgets import QLabel

from main_classes.loop_step import Loop_Step, Loop_Step_Config
from utility.path_button_edit import Path_Button_Edit
from utility import variables_handling

class Run_Subprotocol(Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, **kwargs)
        self.step_type = 'Run Subprotocol'
        if step_info is None:
            step_info = {}
        self.prot_path = step_info['prot_path'] if 'prot_path' in step_info else ''

    def get_protocol_string(self, n_tabs=1):
        tabs = '\t' * n_tabs
        protocol_string = f'{tabs}print("starting loop_step {self.full_name}")\n'
        protocol_string += f'{tabs}import importlib\n'
        protocol_string += f'{tabs}spec = importlib.util.spec_from_file_location("subprot", "{self.prot_path}")\n'
        protocol_string += f'{tabs}subprot_mod = importlib.util.module_from_spec(spec)\n'
        protocol_string += f'{tabs}sys.modules[spec.name] = subprot_mod\n'
        protocol_string += f'{tabs}spec.loader.exec_module(module)\n'
        protocol_string += f'{tabs}subprot.main()\n'
        return protocol_string



class Run_Subprotocol_Config(Loop_Step_Config):
    def __init__(self, loop_step:Run_Subprotocol, parent=None):
        super().__init__(parent, loop_step)
        label = QLabel('Select Protocol:')
        self.loop_step = loop_step
        self.path_button = Path_Button_Edit(self, loop_step.prot_path, variables_handling.preferences['py_files_path'])
        self.path_button.path_changed.connect(self.update_path)
        self.layout().addWidget(label, 1, 0)
        self.layout().addWidget(self.path_button, 2, 0)

    def update_path(self):
        self.loop_step.prot_path = self.path_button.get_path()
