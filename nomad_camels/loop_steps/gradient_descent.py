from PySide6.QtWidgets import QWidget

from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config

from nomad_camels.gui.gradient_descent_step import Ui_Grad_Desc
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.utility import variables_handling
from nomad_camels.bluesky_handling import builder_helper_functions
from nomad_camels.frontpanels.plot_definer import Plot_Info


class Gradient_Descent_Step(Loop_Step):
    """
    A step performing a gradient descent with a given channel to optimize a
    given function.


    Attributes
    ----------
    read_channels : list[str]
        A list of all the channels which are read for the optimization.
    extremum : str ('Minimum', 'Maximum')
        The extremum type that should be found.
    out_channel : str
        The channel which is used for the optimization.
    opt_func : str
        This string is evaluated by the given to give the target function.
    start_val : str, float
        Representation of where to start the algorithm.
    min_val : str, float
        The minimum value that should be given to the `set_channel`.
    max_val : str, float
        The maximum value that should be given to the `set_channel`.
    learning_rate : str, float
         A weight for the learning of the gradient descent.
         The next shift `delta_w` is calculated as:
         delta_w = -learning_rate * <current_gradient> + momentum * <last_delta_w>
    threshold : str, float
        If the difference between two measurements is smaller than this
        threshold, the algorithm recognizes the value as the optimum and stops.
    momentum : str, float
         (Default value = 0.8)
         A momentum to keep up the last direction.
         The next shift `delta_w` is calculated as:
         delta_w = -learning_rate * <current_gradient> + momentum * <last_delta_w>
    min_step : str, float
        The minimum step size.
    max_step : str, float
        The maximum step size.
    n_steps : str, int
        The maximum number of iterations until the algorithm should stop if it
        did not arrive at the threshold yet.
    plot_steps : bool
        Whether to plot the single steps of the algorithm at runtime.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Gradient Descent"
        step_info = step_info or {}
        self.read_channels = (
            step_info["read_channels"] if "read_channels" in step_info else []
        )
        self.extremum = step_info["extremum"] if "extremum" in step_info else "Minimum"
        self.out_channel = (
            step_info["out_channel"] if "out_channel" in step_info else ""
        )
        self.opt_func = step_info["opt_func"] if "opt_func" in step_info else ""
        self.start_val = step_info["start_val"] if "start_val" in step_info else ""
        self.min_val = step_info["min_val"] if "min_val" in step_info else ""
        self.max_val = step_info["max_val"] if "max_val" in step_info else ""
        self.learning_rate = (
            step_info["learning_rate"] if "learning_rate" in step_info else ""
        )
        self.threshold = step_info["threshold"] if "threshold" in step_info else ""
        self.momentum = step_info["momentum"] if "momentum" in step_info else ""
        self.min_step = step_info["min_step"] if "min_step" in step_info else ""
        self.max_step = step_info["max_step"] if "max_step" in step_info else ""
        self.n_steps = step_info["n_steps"] if "n_steps" in step_info else ""
        self.plot_steps = step_info["plot_steps"] if "plot_steps" in step_info else True

    def update_used_devices(self):
        """Uses all devices in self.read_channels and of self.out_channel"""
        self.used_devices = []
        set_device = variables_handling.channels[self.out_channel].device
        self.used_devices.append(set_device)
        for channel in self.read_channels:
            if channel in variables_handling.channels:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def get_outer_string(self):
        """Adds the plot, if self.plot_steps is True. The plot displays the
        formula to be optimized vs the out_channel."""
        if self.plot_steps:
            plot = Plot_Info(
                x_axis=self.out_channel,
                y_axes={"formula": [self.opt_func], "axis": ["left"]},
                title="gradient-descent",
            )
            return builder_helper_functions.plot_creator(
                [plot], f"create_plots_{self.name}"
            )[0]
        return ""

    def get_add_main_string(self):
        """Adds the call of creating the plots if self.plot_steps."""
        add_main_string = ""
        if self.plot_steps:
            stream = f'"{self.name}"'
            add_main_string += builder_helper_functions.get_plot_add_string(
                self.name, stream
            )
        return add_main_string

    def get_protocol_string(self, n_tabs=1):
        """Evaluates all / most of the values with the protocol's evaluator and
        calls the helper function gradient_descent to perform the algorithm."""
        tabs = "\t" * n_tabs
        func_text = f'"{self.opt_func}"'
        if self.extremum == "Maximum":
            func_text = f'"-({self.opt_func})"'

        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f"{tabs}channels = ["
        for i, channel in enumerate(self.read_channels):
            if channel not in variables_handling.channels:
                raise Exception(
                    f"Trying to read channel {channel} in {self.full_name}, but it does not exist!"
                )
            if i > 0:
                protocol_string += ", "
            name = variables_handling.channels[channel].name
            if "." in name:
                dev, chan = name.split(".")
                protocol_string += f'devs["{dev}"].{chan}'
            else:
                protocol_string += f'devs["{name}"]'
        protocol_string += "]\n"

        name = variables_handling.channels[self.out_channel].name
        if "." in name:
            dev, chan = name.split(".")
            setter = f'devs["{dev}"].{chan}'
        else:
            setter = f'devs["{name}"]'

        protocol_string += f'{tabs}yield from helper_functions.gradient_descent(eva.eval("{self.n_steps}"), eva.eval("{self.threshold}"), eva.eval("{self.start_val}"), {func_text}, eva, {setter}, channels, eva.eval("{self.min_step}"), eva.eval("{self.max_step}"), eva.eval("{self.min_val}"), eva.eval("{self.max_val}"), "{self.name}", eva.eval("{self.learning_rate}"), eva.eval("{self.momentum}"))\n'
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """Describes the kind of extremum, the opt_func and the out_channel."""
        short_string = super().get_protocol_short_string(n_tabs)[:-1]
        short_string += (
            f" - {self.extremum} of {self.opt_func} via {self.out_channel}\n"
        )
        return short_string


class Gradient_Descent_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: Gradient_Descent_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = Gradient_Descent_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)

    def update_step_config(self):
        """ """
        super().update_step_config()
        self.sub_widget.update_step_config()


class Gradient_Descent_Config_Sub(Ui_Grad_Desc, QWidget):
    """ """

    def __init__(self, loop_step: Gradient_Descent_Step, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loop_step = loop_step
        self.read_table = AddRemoveTable(
            title="Read Channels",
            headerLabels=[],
            tableData=loop_step.read_channels,
            comboBoxes=variables_handling.channels.keys(),
        )
        self.layout().addWidget(self.read_table, 20, 0, 1, 3)
        self.comboBox_extremum_type.addItems(["Minimum", "Maximum"])
        self.comboBox_extremum_type.setCurrentText(loop_step.extremum)

        out_box = []
        for channel in variables_handling.channels:
            if variables_handling.channels[channel].output:
                out_box.append(channel)
        self.comboBox_output_channel.addItems(out_box)
        if loop_step.out_channel in out_box:
            self.comboBox_output_channel.setCurrentText(loop_step.out_channel)
        self.lineEdit_opt_func.setText(loop_step.opt_func)
        self.lineEdit_starting_val.setText(loop_step.start_val)
        self.lineEdit_min_val.setText(loop_step.min_val)
        self.lineEdit_max_val.setText(loop_step.max_val)
        self.lineEdit_learning_rate.setText(loop_step.learning_rate)
        self.lineEdit_threshold.setText(loop_step.threshold)
        self.lineEdit_momentum.setText(loop_step.momentum)
        self.lineEdit_smallest_step.setText(loop_step.min_step)
        self.lineEdit_largest_step.setText(loop_step.max_step)
        self.lineEdit_max_n_steps.setText(loop_step.n_steps)
        self.checkBox_plot_steps.setChecked(loop_step.plot_steps)

    def update_step_config(self):
        """ """
        self.loop_step.extremum = self.comboBox_extremum_type.currentText()
        self.loop_step.out_channel = self.comboBox_output_channel.currentText()
        self.loop_step.opt_func = self.lineEdit_opt_func.text()
        self.loop_step.start_val = self.lineEdit_starting_val.text()
        self.loop_step.min_val = self.lineEdit_min_val.text()
        self.loop_step.max_val = self.lineEdit_max_val.text()
        self.loop_step.learning_rate = self.lineEdit_learning_rate.text()
        self.loop_step.threshold = self.lineEdit_threshold.text()
        self.loop_step.momentum = self.lineEdit_momentum.text()
        self.loop_step.min_step = self.lineEdit_smallest_step.text()
        self.loop_step.max_step = self.lineEdit_largest_step.text()
        self.loop_step.n_steps = self.lineEdit_max_n_steps.text()
        self.loop_step.read_channels = self.read_table.update_table_data()
        self.loop_step.plot_steps = self.checkBox_plot_steps.isChecked()
