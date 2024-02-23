from PySide6.QtWidgets import QWidget, QLabel, QGridLayout

from nomad_camels.main_classes.loop_step import Loop_Step_Config, Loop_Step
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box


class Export_Data_Step(Loop_Step):
    """
    A loopstep to export the measurement data at fixed points. Convenient to
    already start evaluation during long measurements.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Export Data"

    def get_protocol_string(self, n_tabs=1):
        """The protocol just calls `bps.wait(`wait_time`)`, where `wait_time` is
        evaluated by the protocol's evaluator."""
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f"{tabs}if uids:\n"
        protocol_string += f"{tabs}\truns uids:\n"
        protocol_string += (
            f"{tabs}broker_to_NX(runs, save_path, plots,"
            "session_name=session_name,"
            "export_to_csv=export_to_csv,"
            "export_to_json=export_to_json)\n"
        )
        protocol_string += f'{tabs}yield from bps.sleep(eva.eval("{self.wait_time}"))\n'
        return protocol_string


class Export_Data_Step_Config(Loop_Step_Config):
    """Displaying only what the step does."""

    def __init__(self, loop_step: Export_Data_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = QLabel(
            "This step exports the current measured data to"
            "the same directory where the final data will be"
            'saved. The filename will include "_intermediate"'
            "at the end."
        )
        self.layout().addWidget(self.sub_widget, 1, 0)
