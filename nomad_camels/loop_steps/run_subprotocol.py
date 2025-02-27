import os

from PySide6.QtWidgets import QLabel, QComboBox, QCheckBox

from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
from nomad_camels.utility import variables_handling, load_save_functions
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.bluesky_handling import protocol_builder, builder_helper_functions
from nomad_camels.bluesky_handling import protocol_builder


class Run_Subprotocol(Loop_Step):
    """
    With this step, one may select another protocol to run inside the main one.

    Attributes
    ----------
    prot_path : str, path
        Path to the file of the subprotocol.
    vars_in : dict
        Variables of the subprotocol's namespace and the values they should get
        before the subprotocol is run. This can be used to e.g. give the
        subprotocol a new value for each run inside a loop.
    vars_out : dict
        Variables of the subprotocol and the name in the main protocol's
        namespace where they should be put. This can be used to e.g. store some
        value determined by the subprotocol for later use in the main protocol.
    data_output : str
        Whether the data is put into its own stream('sub-stream') or the primary
        stream ('main-stream').
    own_plots : bool
        If True, the plots specified by the protocol will also be shown.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Run Subprotocol"
        if step_info is None:
            step_info = {}
        self.prot_path = step_info["prot_path"] if "prot_path" in step_info else ""
        self.vars_in = step_info["vars_in"] if "vars_in" in step_info else {}
        self.vars_out = step_info["vars_out"] if "vars_out" in step_info else {}
        self.data_output = (
            step_info["data_output"] if "data_output" in step_info else "sub-stream"
        )
        self.own_plots = step_info["own_plots"] if "own_plots" in step_info else True

    def get_protocol_string(self, n_tabs=1, name=None):
        """Overwrites the signal for the progressbar and the number of steps in
        the subprotocol's module. Evaluates the input variables, then writes
        them into the subprotocol's namespace and starts the subprotocol's
        _plan_inner function. Afterwards the output variables are written to the
        main namespace."""
        protocol = load_save_functions.load_protocol(self.prot_path)
        if protocol.description and protocol.description not in self.description:
            self.description += f"\n\t{protocol.description}"
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += protocol_builder.sub_protocol_string(
            protocol_path=self.prot_path,
            n_tabs=n_tabs,
            variables_in=self.vars_in,
            variables_out=self.vars_out,
            data_output=self.data_output,
            new_stream=name,
        )
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """Specifies the name / path of the subprotocol."""
        short_string = super().get_protocol_short_string(n_tabs)
        short_string = f"{short_string[:-1]} - {self.prot_path} - {self.description}\n"
        return short_string

    def get_outer_string(self):
        """Imports the subprotocol as <protocol_name>_mod."""
        return protocol_builder.import_protocol_string(self.prot_path)
        # prot_name = os.path.basename(self.prot_path)[:-6]
        # py_file = f"{self.prot_path[:-6]}.py"
        # if not os.path.isfile(py_file):
        #     sub_protocol = load_save_functions.load_protocol(self.prot_path)
        #     protocol_builder.build_protocol(sub_protocol, py_file)
        # outer_string = f'spec = importlib.util.spec_from_file_location("{prot_name}", "{py_file}")\n'
        # outer_string += f"{prot_name}_mod = importlib.util.module_from_spec(spec)\n"
        # outer_string += f"sys.modules[spec.name] = {prot_name}_mod\n"
        # outer_string += f"spec.loader.exec_module({prot_name}_mod)\n"
        # return outer_string

    def get_add_main_string(self):
        """If using its own plots, adds them to the steps. In any case, the
        added steps from the subprotocol are added here as well."""
        return protocol_builder.make_plots_string_of_protocol(
            self.prot_path, self.own_plots, self.data_output, 1
        )
        # prot_name = os.path.basename(self.prot_path)[:-6]
        # add_main_string = ""
        # if self.own_plots:
        #     stream = f'"{prot_name}"'
        #     if self.data_output == "main stream":
        #         stream = '"primary"'
        #     add_main_string += builder_helper_functions.get_plot_add_string(
        #         prot_name, stream, True
        #     )
        # add_main_string += f'\treturner["{prot_name}_steps"] = {prot_name}_mod.steps_add_main(RE, devs)\n'
        # return add_main_string

    def update_used_devices(self):
        """Uses the devices that are used in the subprotocol."""
        sub_protocol = load_save_functions.load_protocol(self.prot_path)
        self.used_devices = sub_protocol.get_used_devices()

    def update_time_weight(self):
        """The time weight in the end is the weight of the subprotocol + 1."""
        super().update_time_weight()
        sub_protocol = load_save_functions.load_protocol(self.prot_path)
        self.time_weight += sub_protocol.get_total_steps()


class Run_Subprotocol_Config(Loop_Step_Config):
    """ """

    def __init__(self, loop_step: Run_Subprotocol, parent=None):
        super().__init__(parent, loop_step)
        label = QLabel("Select Protocol:")
        self.loop_step = loop_step
        self.path_button = Path_Button_Edit(
            self,
            loop_step.prot_path,
            variables_handling.preferences["py_files_path"],
            file_extension="*.cprot",
        )
        self.sub_vars = {}
        self.load_sub_vars()
        headerLabels = ["Variable", "Value"]
        comboBoxes = {"Variable": self.sub_vars.keys()}
        self.input_table = AddRemoveTable(
            headerLabels=headerLabels,
            tableData=loop_step.vars_in,
            title="Variables In",
            comboBoxes=comboBoxes,
            checkstrings=[1],
        )
        headerLabels = ["Variable", "Write to name"]
        comboBoxes = {"Variable": self.sub_vars.keys()}
        self.output_table = AddRemoveTable(
            headerLabels=headerLabels,
            tableData=loop_step.vars_out,
            title="Variables Out",
            comboBoxes=comboBoxes,
        )

        label_data = QLabel("Data Output:")
        self.comboBox_data_output = QComboBox()
        output_types = ["sub-stream", "main stream"]  # , 'own file']
        self.comboBox_data_output.addItems(output_types)
        self.comboBox_data_output.setCurrentText(loop_step.data_output)

        self.checkBox_plots = QCheckBox("Use own plots")
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
        """ """
        self.load_sub_vars()
        comboBoxes = {"Variable": self.sub_vars.keys()}
        self.input_table.comboBoxes = comboBoxes
        self.input_table.load_table_data()
        self.output_table.comboBoxes = comboBoxes
        self.output_table.load_table_data()

    def load_sub_vars(self):
        """ """
        self.sub_vars = {}
        prot_path = self.path_button.get_path()
        sub_protocol = load_save_functions.load_protocol(prot_path)
        if sub_protocol:
            self.sub_vars = sub_protocol.variables

    def update_step_config(self):
        """ """
        super().update_step_config()
        self.loop_step.prot_path = self.path_button.get_path()
        self.loop_step.vars_in = self.input_table.update_table_data()
        self.loop_step.vars_out = self.output_table.update_table_data()
        self.loop_step.own_plots = self.checkBox_plots.isChecked()
        self.loop_step.data_output = self.comboBox_data_output.currentText()
