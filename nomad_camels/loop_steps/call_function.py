from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config
from nomad_camels.ui_widgets.channels_check_table import Call_Functions_Table
from nomad_camels.utility import variables_handling


class Call_Function(Loop_Step):
    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Call Function"
        if step_info is None:
            step_info = {}
        self.call_functions = (
            step_info["call_functions"] if "call_functions" in step_info else []
        )
        self.update_used_devices()

    def update_used_devices(self):
        self.used_devices = []
        for func in self.call_functions:
            device = func.split(".")[0]
            if device not in self.used_devices:
                self.used_devices.append(device)

    def get_protocol_string(self, n_tabs=1):
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        available_functions = variables_handling.get_non_channel_functions()
        for func in self.call_functions:
            if func not in available_functions:
                raise Exception(
                    f'Trying to call function "{func}" but it is not available!\nCheck whether you maybe renamed an instrument.'
                )
            dev, fun = func.split(".")
            protocol_string += f'{tabs}devs["{dev}"].{fun}()\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f"{short_string[:-1]} - {self.call_functions}\n"
        return short_string


class Call_Function_Config(Loop_Step_Config):
    def __init__(self, loop_step: Call_Function, parent=None):
        super().__init__(parent, loop_step)
        labels = ["call?", "function"]
        info = {"functions": self.loop_step.call_functions}
        self.table = Call_Functions_Table(
            headerLabels=labels, parent=self, info_dict=info, title="Functions"
        )
        self.layout().addWidget(self.table, 2, 0, 1, 5)

    def update_step_config(self):
        super().update_step_config()
        info = self.table.get_info()
        self.loop_step.call_functions = info["functions"]
