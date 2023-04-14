from PySide6.QtWidgets import QCheckBox

from nomad-camels.main_classes.loop_step import Loop_Step, Loop_Step_Config

from nomad-camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad-camels.ui_widgets.channels_check_table import Channels_Check_Table


class Set_Value_Popup(Loop_Step):
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = 'Set Value Popup'
        if step_info is None:
            step_info = {}
        self.variables = step_info['variables'] if 'variables' in step_info else []
        self.channels = step_info['channels'] if 'channels' in step_info else []
        self.free_variables = step_info['free_variables'] if 'free_variables' in step_info else False
        self.free_channels = step_info['free_channels'] if 'free_channels' in step_info else False

    def get_protocol_string(self, n_tabs=1):
        tabs = '\t' * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f'{tabs}boxes["values_{self.name}"].done = False\n'
        protocol_string += f'{tabs}boxes["values_{self.name}"].helper.executor.emit()\n'
        protocol_string += f'{tabs}while not boxes["values_{self.name}"].done:\n'
        protocol_string += f'{tabs}\tyield from bps.sleep(0.1)\n'
        protocol_string += f'{tabs}if boxes["values_{self.name}"].was_accepted:\n'
        protocol_string += f'{tabs}\tfor var, val in boxes["values_{self.name}"].set_variables.items():\n'
        protocol_string += f'{tabs}\t\tnamespace[var] = eva.eval(str(val))\n'
        protocol_string += f'{tabs}\tfor chan, val in boxes["values_{self.name}"].set_channels.items():\n'
        protocol_string += f'{tabs}\t\tdev, channel_name = boxes["values_{self.name}"].channel_devs[chan]\n'
        protocol_string += f'{tabs}\t\tyield from bps.abs_set(getattr(devs[dev], channel_name), eva.eval(str(val)), group="A")\n'
        protocol_string += f'{tabs}\tyield from bps.wait("A")\n'
        return protocol_string

    def get_add_main_string(self):
        add_main_string = super().get_add_main_string()
        add_main_string += f'\tboxes["values_{self.name}"] = helper_functions.Value_Box("", "Set Values!", {self.variables}, {self.channels}, {self.free_variables}, {self.free_channels}, devs=devs)\n'
        return add_main_string


class Set_Value_Popup_Config(Loop_Step_Config):
    def __init__(self, loop_step:Set_Value_Popup, parent=None):
        super().__init__(parent, loop_step)
        self.variables_table = AddRemoveTable(tableData=loop_step.variables,
                                              title='Variables', headerLabels=[])
        labels = ['use', 'channel']
        info_dict = {'channel': loop_step.channels}
        self.channels_table = Channels_Check_Table(self, labels,
                                                   info_dict=info_dict,
                                                   title='Channels',
                                                   only_output=True)
        self.checkBox_free_variables = QCheckBox('Allow free variable setting')
        self.checkBox_free_channels = QCheckBox('Allow free channel setting')

        self.layout().addWidget(self.checkBox_free_channels, 1, 0, 1, 5)
        self.layout().addWidget(self.checkBox_free_variables, 2, 0, 1, 5)
        self.layout().addWidget(self.channels_table, 3, 0, 1, 5)
        self.layout().addWidget(self.variables_table, 4, 0, 1, 5)

    def update_step_config(self):
        super().update_step_config()
        self.loop_step.variables = self.variables_table.update_table_data()
        self.loop_step.channels = self.channels_table.get_info()['channel']
        self.loop_step.free_channels = self.checkBox_free_channels.isChecked()
        self.loop_step.free_variables = self.checkBox_free_variables.isChecked()
