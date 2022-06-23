import sys
import importlib
import os

from PyQt5.QtWidgets import QLabel, QComboBox, QCheckBox

from main_classes.loop_step import Loop_Step, Loop_Step_Config
from utility.path_button_edit import Path_Button_Edit
from utility import variables_handling
from utility.add_remove_table import AddRemoveTable

class Run_Subprotocol(Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, **kwargs)
        self.step_type = 'Run Subprotocol'
        if step_info is None:
            step_info = {}
        self.prot_path = step_info['prot_path'] if 'prot_path' in step_info else ''
        self.vars_in = step_info['vars_in'] if 'vars_in' in step_info else {}
        self.vars_out = step_info['vars_out'] if 'vars_out' in step_info else {}
        self.data_output = step_info['data_output'] if 'data_output' in step_info else 'sub-stream'
        self.own_plots = step_info['own_plots'] if 'own_plots' in step_info else True


    def get_protocol_string(self, n_tabs=1):
        tabs = '\t' * n_tabs
        prot_name = os.path.basename(self.prot_path)[:-3]
        protocol_string = f'{tabs}print("starting loop_step {self.full_name}")\n'
        stream = prot_name
        if self.data_output == 'main stream':
            stream = 'primary'
        protocol_string += f'{tabs}yield from {prot_name}_mod.{prot_name}_plan_inner(devs, runEngine, "{stream}")\n'
        return protocol_string

    def get_outer_string(self):
        prot_name = os.path.basename(self.prot_path)[:-3]
        outer_string = f'spec = importlib.util.spec_from_file_location("{prot_name}", "{self.prot_path}")\n'
        outer_string += f'{prot_name}_mod = importlib.util.module_from_spec(spec)\n'
        outer_string += f'sys.modules[spec.name] = {prot_name}_mod\n'
        outer_string += f'spec.loader.exec_module({prot_name}_mod)\n'
        return outer_string

    def get_add_main_string(self):
        prot_name = os.path.basename(self.prot_path)[:-3]
        add_main_string = ''
        if self.own_plots:
            add_main_string += f'\t{prot_name}_app, {prot_name}_plots = {prot_name}_mod.create_plots(RE)\n'
        return add_main_string


class Run_Subprotocol_Config(Loop_Step_Config):
    def __init__(self, loop_step:Run_Subprotocol, parent=None):
        super().__init__(parent, loop_step)
        label = QLabel('Select Protocol:')
        self.loop_step = loop_step
        self.path_button = Path_Button_Edit(self, loop_step.prot_path,
                                            variables_handling.preferences['py_files_path'])
        self.sub_vars = {}
        self.load_sub_vars()
        headerLabels = ['Variable', 'Value']
        comboBoxes = {'Variable': self.sub_vars.keys()}
        self.input_table = AddRemoveTable(headerLabels=headerLabels,
                                          tableData=loop_step.vars_in,
                                          title='Variables In',
                                          comboBoxes=comboBoxes,
                                          checkstrings=[1])
        headerLabels = ['Variable', 'Write to name']
        comboBoxes = {'Variable': self.sub_vars.keys()}
        self.output_table = AddRemoveTable(headerLabels=headerLabels,
                                          tableData=loop_step.vars_out,
                                          title='Variables Out',
                                          comboBoxes=comboBoxes)

        label_data = QLabel('Data Output:')
        self.comboBox_data_output = QComboBox()
        output_types = ['sub-stream', 'main stream', 'own file']
        self.comboBox_data_output.addItems(output_types)
        self.comboBox_data_output.setCurrentText(loop_step.data_output)

        self.checkBox_plots = QCheckBox('Use own plots')
        self.checkBox_plots.setChecked(loop_step.own_plots)

        self.layout().addWidget(label, 1, 0)
        self.layout().addWidget(self.path_button, 1, 1)
        self.layout().addWidget(label_data, 2, 0)
        self.layout().addWidget(self.comboBox_data_output, 2, 1)
        self.layout().addWidget(self.checkBox_plots, 3, 0, 1, 2)
        self.layout().addWidget(self.input_table, 5, 0, 1, 2)
        self.layout().addWidget(self.output_table, 6, 0, 1, 2)
        self.path_button.path_changed.connect(self.update_sub_vars)

    def update_sub_vars(self):
        self.load_sub_vars()
        comboBoxes = {'Variable': self.sub_vars.keys()}
        self.input_table.comboBoxes = comboBoxes
        self.input_table.load_table_data()
        self.output_table.comboBoxes = comboBoxes
        self.output_table.load_table_data()

    def load_sub_vars(self):
        prot_path = self.path_button.get_path()
        try:
            spec = importlib.util.spec_from_file_location("subprot", prot_path)
            subprot_mod = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = subprot_mod
            spec.loader.exec_module(subprot_mod)
            self.sub_vars = subprot_mod.namespace
        except:
            self.sub_vars = {}

    def update_step_config(self):
        super().update_step_config()
        self.loop_step.prot_path = self.path_button.get_path()
        self.loop_step.vars_in = self.input_table.update_table_data()
        self.loop_step.vars_out = self.output_table.update_table_data()
        self.loop_step.own_plots = self.checkBox_plots.isChecked()
        self.loop_step.data_output = self.comboBox_data_output.currentText()
