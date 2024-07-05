from PySide6.QtWidgets import QWidget, QCheckBox, QTextEdit, QMessageBox, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal

from nomad_camels.frontpanels.plot_definer import Plot_Button_Overview
from nomad_camels.loop_steps import make_step_of_type
from nomad_camels.gui.general_protocol_settings import Ui_Protocol_Settings

from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.utility import variables_handling


class Measurement_Protocol:
    """Class for the measurement protocols. It mainly contains
    loop_steps and plots.

    Attributes
    ----------
    description : str
        A string describing the protocol.
    export_csv : bool
        If True, the data will be exported to a csv file in the end.
    export_json : bool
        If True, the metadata will be exported to a json file in the end.
    session_name : str
        This name is appended to the entry in the hdf5-file, or used for the
        filenames of csv / json to make it easier for the user to recognize
        their measurements
    loop_steps : list[Loop_Step]
        A list of the steps performed by the protocol. This list also represents
        the order, in which the steps should be performed. The step's children
        steps are not included in this list.
    loop_step_dict : dict
        Keys are the steps' names with the steps being the value. The sub-steps
        are included here.
    plots : list[Plot_Info]
        Contains the information for the protocol's plots.
    filename : str
        The name of the produced datafile.
    variables : dict
        Name-value pairs of the protocol variables
    loop_step_variables : dict
        Name-value pairs of the variables provided by the steps (e.g. for loop)
    channels : dict
        Dictionary of the channel-names and channels used inside the protocol
    name : str
        The name of the protocol. This also appears in the main UI
    channel_metadata : dict
        Currently deprecated. Only used for specific nexus output.
    config_metadata : dict
        Currently deprecated. Only used for specific nexus output.
    metadata : dict
        Currently deprecated. Only used for specific nexus output.
    use_nexus : bool
        Currently deprecated. Only used for specific nexus output.
    """

    def __init__(
        self,
        loop_steps=None,
        plots=None,
        channels=None,
        name="",
        channel_metadata=None,
        metadata=None,
        use_nexus=False,
        config_metadata=None,
        **kwargs,
    ):
        if plots is None:
            plots = []
        if loop_steps is None:
            loop_steps = []
        if channels is None:
            channels = {}
        if channel_metadata is None:
            channel_metadata = {}
        if metadata is None:
            metadata = {}
        self.description = kwargs["description"] if "description" in kwargs else ""
        self.export_csv = kwargs["export_csv"] if "export_csv" in kwargs else False
        self.export_json = kwargs["export_json"] if "export_json" in kwargs else False
        self.session_name = kwargs["session_name"] if "session_name" in kwargs else ""
        self.skip_config = kwargs["skip_config"] if "skip_config" in kwargs else False
        self.h5_during_run = (
            kwargs["h5_during_run"] if "h5_during_run" in kwargs else True
        )
        self.loop_steps = loop_steps
        self.loop_step_dict = {}
        for step in self.loop_steps:
            update_all_children(self.loop_step_dict, step)
        self.plots = plots
        self.filename = ""
        self.variables = {}
        self.loop_step_variables = {}
        self.channels = channels
        self.name = name or "Protocol"
        self.channel_metadata = channel_metadata
        self.config_metadata = config_metadata
        self.metadata = metadata
        self.use_nexus = use_nexus

    def update_variables(self):
        """Update all the variables provided by loopsteps."""
        self.loop_step_variables.clear()
        for step in self.loop_steps:
            if not step.is_active:
                continue
            step.update_variables()

    def get_nexus_paths(self):
        """Get a dictionary containing the paths used for the output
        NeXus-file. Currently deprecated."""
        paths = {}
        for i, name in enumerate(self.metadata["Name"]):
            paths[self.metadata["NeXus-path"][i]] = f"metadata_start/{name}"
        for i, name in enumerate(self.channel_metadata["Channel"]):
            paths[self.channel_metadata["NeXus-path"][i]] = f"data/{name}"
        for i, name in enumerate(self.config_metadata["Configuration"]):
            path = ""
            for dev in variables_handling.devices:
                if dev in name:
                    rn = name.split(dev)[1][1:]
                    device = variables_handling.devices[dev]
                    if (
                        rn in device.get_config()
                        or rn in device.get_config()
                        or rn in device.get_passive_config()
                    ):
                        path = f"metadata_start/device_config/{dev}/{name}"
                        break
            if not path:
                raise Exception(f"Cannot find {name} in any configuration!")
            paths[self.config_metadata["NeXus-path"][i]] = path
        return paths

    def add_loop_step(self, loop_step, position=-1, parent_step_name=None, model=None):
        """Adds a loop_step to the protocol (or the parent_step)at the specified
        position. Also appends the loop_step to the given model. The
        loop_step is added to the list as well as the dictionary.

        Parameters
        ----------
        loop_step : Loop_Step
            The step that should be added
        position : int
            (Default value = -1)
            Where in the list to add the step
        parent_step_name : str, None
            (Default value = None)
            If the step is not in the outermost layer, its parent's name. Then
            `position` will not be for the protocol's list, but the parent's
            children-list.
        model : QAbstractItemModel, None
            (Default value = None)
            The item model that is used to display the steps.
        """
        if parent_step_name is None:
            if position < 0:
                self.loop_steps.append(loop_step)
            else:
                self.loop_steps.insert(position, loop_step)
        else:
            loop_step.parent_step = parent_step_name
            self.loop_step_dict[parent_step_name].add_child(loop_step, position)
        if model is not None:
            loop_step.append_to_model(model)
        self.loop_step_dict.update({loop_step.full_name: loop_step})

    def add_loop_step_rec(
        self, loop_step, model=None, parent_step_name=None, position=-1
    ):
        """Recursively adds the loop_step and all its children to the
        protocol. Steps are added to the list if they have no parent,
        otherwise to the parent. All are added to the dictionary.

        Parameters
        ----------
        loop_step : Loop_Step
            The step that should be added
        model : QAbstractItemModel, None
            (Default value = None)
            The item model that is used to display the steps.
        parent_step_name : str
            (Default value = None)
            If the step is not in the outermost layer, its parent's name. Then
            `position` will not be for the protocol's list, but the parent's
            children-list.
        position : int
            (Default value = -1)
            Where in the list to add the step
        """
        if parent_step_name is None:
            self.add_loop_step(
                loop_step,
                model=model,
                parent_step_name=parent_step_name,
                position=position,
            )
        else:
            if model is not None:
                loop_step.append_to_model(model, parent=parent_step_name)
            if loop_step not in self.loop_step_dict[parent_step_name].children:
                self.loop_step_dict[parent_step_name].add_child(loop_step, position)
            self.loop_step_dict.update({loop_step.full_name: loop_step})
        for child in loop_step.children:
            self.add_loop_step_rec(
                child, parent_step_name=loop_step.full_name, model=model
            )

    def remove_loop_step(self, loop_step_name):
        """Removes the step with the given name from the sequence-list
        (or parent) and from the dictionary.

        Parameters
        ----------
        loop_step_name : str
            The name of the step that is to be removed.
        """
        step = self.loop_step_dict.pop(loop_step_name)
        if step.parent_step is not None:
            self.loop_step_dict[step.parent_step].remove_child(step)
        else:
            self.loop_steps.remove(step)

    def load_loop_steps(self, loop_steps, model=None):
        """Takes a list of loop_steps, creates them (with the input data
        of each step) and adds them to the specified model.

        Parameters
        ----------
        loop_steps : list
            A list containing all the information (as dictionary) for creating
            the single steps.
        model : QAbstractItemModel, None
            (Default value = None)
            The item model that is used to display the steps.
        """
        for step in loop_steps:
            loop_step = self.make_step(step)
            self.add_loop_step_rec(loop_step, model=model)

    def make_step(self, step_info):
        """Creates the step specified with step_info (including the
        children), 'step_type' gives which subclass of Loop_Step shall
        be created.

        Parameters
        ----------
        step_info : dict
            This dictionary should hold all information needed to create the
            step. Specifically there should be "step_type" to decide on the
            class of step and "full_name" to give the step its name.


        Returns
        -------
        st : Loop_Step
            The created step
        """
        # children = None
        # if step_info['has_children']:
        children = []
        if "children" in step_info:
            for child in step_info["children"]:
                child_step = self.make_step(child)
                child_step.parent_step = step_info["full_name"]
                children.append(child_step)
        st = make_step_of_type.make_step(
            step_info["step_type"], step_info, children, protocol=self
        )
        st.full_name = step_info["full_name"]
        return st

    def rearrange_loop_steps(self, step_list):
        """Takes a list of loopsteps, each entry consisting of a tuple
        of the loopstep name and its children, which is recursively the
        same kind of list. Re-populates the loop_step_dict and then puts
        the loop_steps in the correct order.

        Parameters
        ----------
        step_list : list[(str, [list(str, ...)])]
            Contains tuples with the first entry being the names of the steps in
            the order they should be arranged to and the second entry being a
            list of the steps' children. That list should be structured the same
            way as this `step_list`.
        """
        self.loop_step_dict = {}
        for step in self.loop_steps:
            update_all_children(self.loop_step_dict, step)
        self.loop_steps = []
        for step, children in step_list:
            self.loop_step_dict[step].children = []
            append_all_children(
                children, self.loop_step_dict[step], self.loop_step_dict
            )
            self.loop_steps.append(self.loop_step_dict[step])

    def get_plan_string(self):
        """Get the string for the protocol-plan, including the loopsteps."""
        variables_handling.current_protocol = self
        plan_string = f'\n\n\ndef {self.name.replace(" ","_")}_plan_inner(devs, eva=None, stream_name="primary"):\n'
        prot_vars = dict(variables_handling.protocol_variables)
        if "StartTime" in prot_vars:
            prot_vars.pop("StartTime")
            prot_vars.pop("ElapsedTime")
        if prot_vars:
            plan_string += "\tglobal "
            for i, var in enumerate(prot_vars.keys()):
                if i > 0:
                    plan_string += ", "
                plan_string += var
            plan_string += "\n"
        for step in self.loop_steps:
            if not step.is_active:
                continue
            plan_string += step.get_protocol_string(n_tabs=1)
        plan_string += f'\n\n\ndef {self.name.replace(" ","_")}_plan(devs, md=None, runEngine=None, stream_name="primary"):\n'
        plan_string += "\teva = Evaluator(namespace=namespace)\n"
        plan_string += "\tsub_eva = runEngine.subscribe(eva)\n"
        plan_string += "\tyield from bps.open_run(md=md)\n"
        plan_string += f'\tyield from {self.name.replace(" ", "_")}_plan_inner(devs, eva, stream_name)\n'
        plan_string += (
            "\tyield from helper_functions.get_fit_results(all_fits, namespace, True)\n"
        )
        plan_string += "\tyield from bps.close_run()\n"
        plan_string += "\trunEngine.unsubscribe(sub_eva)\n"
        return plan_string

    def get_short_string(self):
        """Goes through all steps and creates an overview of what is happening
        in the protocol."""
        short_string = ""
        for step in self.loop_steps:
            if not step.is_active:
                continue
            short_string += step.get_protocol_short_string()
        return short_string

    def get_add_main_string(self):
        """Gets all the steps that should be executed in the protocol's main
        function."""
        add_main_string = "def steps_add_main(RE, devs):\n"
        add_main_string += "\treturner = {}\n"
        for step in self.loop_steps:
            if not step.is_active:
                continue
            add_main_string += step.get_add_main_string()
        add_main_string += "\treturn returner\n\n\n"
        return add_main_string

    def get_total_steps(self):
        """Returns the total number of steps (including repetitions for loops)"""
        total = 0
        for step in self.loop_steps:
            if not step.is_active:
                continue
            step.update_time_weight()
            total += step.time_weight
        return total

    def get_outer_string(self):
        """Strings outside of all other functions of the script, e.g. more
        functions to create step-specific plots."""
        outer_string = ""
        for step in self.loop_steps:
            if not step.is_active:
                continue
            outer_string += step.get_outer_string()
        return outer_string

    def get_used_devices(self):
        """Get a list of all devices needed by any loopstep."""
        devices = []
        for step in self.loop_steps:
            if not step.is_active:
                continue
            step.update_used_devices()
            devices += step.used_devices
        adds = []
        for dev in devices:
            adds += variables_handling.devices[dev].get_necessary_devices()
        devices += adds
        devices = list(set(devices))
        devices = sorted(devices, key=lambda x: x in adds, reverse=True)
        return devices


def append_all_children(child_list, step, step_dict):
    """Takes a list of the kind specified in rearrange_loop_steps, does
    the same as the other function, but recursively for all the
    (grand-)children.

    Parameters
    ----------
    child_list : list[(str, [list(str, ...)])]
        Contains tuples with the first entry being the names of the steps in
        the order they should be arranged to and the second entry being a
        list of the steps' children. That list should be structured the same
        way as this `child_list`.
    step : Loop_Step_Container
        The step to which the children should be appended.
    step_dict : dict
        A dictionary containing (among others) the steps of `child_list`.
    """
    for child, grandchildren in child_list:
        child_step = step_dict[child]
        child_step.children = []
        append_all_children(grandchildren, child_step, step_dict)
        child_step.parent_step = step.full_name
        step.children.append(child_step)


def update_all_children(step_dict, step):
    """Similar to append_all_children, but only updating the step_dict
    with all the children, i.e. writing them into the dictionary.

    Parameters
    ----------
    step_dict : dict
        Dictionary, where to write all the steps
    step : Loop_Step
        The step to be added to the dictionary. If it has child-steps, all of
        them will be added to the dictionary recursively.
    """
    step_dict.update({step.full_name: step})
    # if step.has_children:
    for child in step.children:
        update_all_children(step_dict, child)


class General_Protocol_Settings(Ui_Protocol_Settings, QWidget):
    """Widget for the configuration of the general protocol settings.
    Here plots may be defined and variables added to the protocol.

    Parameters
    ----------

    Returns
    -------

    """

    name_changed = Signal()

    def __init__(self, parent=None, protocol=Measurement_Protocol()):
        super(General_Protocol_Settings, self).__init__(parent)
        self.setupUi(self)
        self.protocol = protocol
        self.lineEdit_filename.setText(self.protocol.filename)
        self.lineEdit_protocol_name.setText(self.protocol.name)

        self.variable_table.set_protocol(self.protocol)
        self.variable_table.editable_names = True

        # self.variable_model = QStandardItemModel()
        # self.variable_model.setHorizontalHeaderLabels(["Name", "Value", "Data-Type"])
        # self.tableView_variables.setModel(self.variable_model)
        # self.load_variables()

        self.pushButton_add_variable.clicked.connect(lambda x: self.add_variable())
        self.pushButton_remove_variable.clicked.connect(self.remove_variable)

        # self.variable_model.itemChanged.connect(self.check_variable)

        self.plot_widge = Plot_Button_Overview(self, self.protocol.plots)

        cols = ["Channel", "NeXus-path"]
        comboBoxes = {"Channel": list(variables_handling.channels.keys())}
        self.table_channel_NX_paths = AddRemoveTable(
            headerLabels=cols,
            title="Channel-NeXus-Path",
            comboBoxes=comboBoxes,
            tableData=self.protocol.channel_metadata,
        )

        cols = ["Configuration", "NeXus-path"]
        configs = []
        for dev in variables_handling.devices:
            device = variables_handling.devices[dev]
            allconf = []
            allconf += list(device.get_passive_config().keys())
            allconf += list(device.get_config().keys())
            for key in allconf:
                configs.append(f"{device.name}_{key}")
        comboBoxes = {"Configuration": configs}
        self.table_config_NX_paths = AddRemoveTable(
            headerLabels=cols,
            title="Config-NeXus-Path",
            comboBoxes=comboBoxes,
            tableData=self.protocol.config_metadata,
        )

        cols = ["Name", "NeXus-path", "Value"]
        self.table_metadata = AddRemoveTable(
            headerLabels=cols, title="NeXus-Metadata", tableData=self.protocol.metadata
        )

        self.checkBox_NeXus = QCheckBox("Use NeXus-output")
        self.checkBox_NeXus.clicked.connect(self.enable_nexus)
        self.checkBox_NeXus.setChecked(self.protocol.use_nexus)
        self.lineEdit_protocol_name.textChanged.connect(self.name_change)
        self.name_change()

        self.textEdit_desc = QTextEdit(parent=self)
        self.textEdit_desc.setPlaceholderText("Enter your description here.")
        if self.protocol.description:
            self.textEdit_desc.setText(self.protocol.description)
        self.checkBox_csv_exp.setChecked(self.protocol.export_csv)
        self.checkBox_json_exp.setChecked(self.protocol.export_json)
        self.checkBox_no_config.setChecked(self.protocol.skip_config)
        self.checkBox_no_config.clicked.connect(self.enable_disable_config)

        self.radioButton_h5_during.setChecked(self.protocol.h5_during_run)
        self.radioButton_h5_after.setChecked(not self.protocol.h5_during_run)

        self.layout().addWidget(self.textEdit_desc, 5, 0, 1, 6)
        self.layout().addWidget(self.plot_widge, 6, 0, 1, 6)
        self.layout().addWidget(self.checkBox_NeXus, 7, 0, 1, 6)
        self.layout().addWidget(self.table_channel_NX_paths, 9, 0, 1, 6)
        self.layout().addWidget(self.table_config_NX_paths, 10, 0, 1, 6)
        self.layout().addWidget(self.table_metadata, 11, 0, 1, 6)

        self.checkBox_NeXus.setHidden(True)
        self.enable_nexus()
        self.update_variable_select()
        self.variable_table.selectionModel().selectionChanged.connect(
            self.update_variable_select
        )

    def enable_disable_config(self):
        disabling = self.checkBox_no_config.isChecked()
        if disabling:
            msgBox = QMessageBox()
            msgBox.setText(
                "Are you sure you want to disable configuration of the used instruments?\nThis may lead to unexpected behaviour of the instruments, if they are not configured correctly beforehand!"
            )
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.No)
            result = msgBox.exec()
            if result != QMessageBox.Yes:
                self.checkBox_no_config.setChecked(False)

    def enable_nexus(self):
        """When the checkBox_NeXus is clicked, enables / disables the
        other widgets for the nexus-definition.

        Parameters
        ----------

        Returns
        -------

        """
        nx = self.checkBox_NeXus.isChecked()
        self.table_channel_NX_paths.setHidden(not nx)
        self.table_metadata.setHidden(not nx)
        self.table_config_NX_paths.setHidden(not nx)

    # def get_unique_name(self, name="name"):
    #     """Checks whether name already exists in the variables of the
    #     protocol and returns a unique name (with added _i).

    #     Parameters
    #     ----------
    #     name :
    #          (Default value = 'name')

    #     Returns
    #     -------

    #     """
    #     i = 1
    #     while name in self.protocol.variables:
    #         if "_" not in name:
    #             name += f"_{i}"
    #         else:
    #             name = f'{name.split("_")[0]}_{i}'
    #         i += 1
    #     return name

    def add_variable(self):
        """Add a variable to the list, given a unique name, then updates
        the protocol.

        Parameters
        ----------

        Returns
        -------

        """
        self.variable_table.append_variable("name")
        self.variable_table.update_variables()
        self.update_variable_select()

    # def append_variable(self, name="name", value="value"):
    #     """Append the variable with name and value to the item_model,
    #     also add an item that shows the datatype of the value.

    #     Parameters
    #     ----------
    #     name :
    #          (Default value = 'name')
    #     value :
    #          (Default value = 'value')

    #     Returns
    #     -------

    #     """
    #     name_item = QStandardItem(name)
    #     value_item = QStandardItem(value)
    #     type_item = QStandardItem(variables_handling.check_data_type(value))
    #     type_item.setEditable(False)
    #     self.variable_model.appendRow([name_item, value_item, type_item])

    def remove_variable(self):
        """Removes the selected variable."""
        try:
            index = self.variable_table.selectedIndexes()[0]
        except IndexError:
            raise Exception("You need to select a row first!")
        if index.row() >= 0:
            self.variable_table.model.removeRow(index.row())
            self.variable_table.update_variables()

    def update_step_config(self):
        """Updates all the protocol settings."""
        self.protocol.filename = self.lineEdit_filename.text()
        self.protocol.name = self.lineEdit_protocol_name.text()
        self.protocol.description = self.textEdit_desc.toPlainText()
        self.protocol.plots = self.plot_widge.plot_data
        self.protocol.metadata = self.table_metadata.update_table_data()
        self.protocol.channel_metadata = self.table_channel_NX_paths.update_table_data()
        self.protocol.config_metadata = self.table_config_NX_paths.update_table_data()
        self.protocol.export_csv = self.checkBox_csv_exp.isChecked()
        self.protocol.export_json = self.checkBox_json_exp.isChecked()
        self.protocol.skip_config = self.checkBox_no_config.isChecked()
        self.variable_table.update_variables()
        self.protocol.use_nexus = self.checkBox_NeXus.isChecked()
        self.protocol.h5_during_run = self.radioButton_h5_during.isChecked()

    # def load_variables(self):
    #     """Called when starting, loads the variables from the protocol
    #     into the table.

    #     Parameters
    #     ----------

    #     Returns
    #     -------

    #     """
    #     for var in sorted(self.protocol.variables):
    #         self.append_variable(var, str(self.protocol.variables[var]))

    # def check_variable(self):
    #     """If name of variable changed: check whether the variable is
    #     unique, if not change its name and raise an error.
    #     If value changed: re-evaluate the data-type.
    #     Update the protocol afterwards.

    #     Parameters
    #     ----------

    #     Returns
    #     -------

    #     """
    #     ind = self.tableView_variables.selectedIndexes()
    #     if ind:
    #         ind = ind[0]
    #     else:
    #         return
    #     item = self.variable_model.itemFromIndex(ind)
    #     if ind.column() == 0:
    #         variables_handling.check_variable_name(item.text(), parent=self)
    #     if ind.column() == 0 and item.text() in self.protocol.variables:
    #         new_name = self.get_unique_name(item.text())
    #         item.setText(new_name)
    #         raise Exception("Variable names must be unique!")
    #     if ind.column() == 1:
    #         d_type = variables_handling.check_data_type(item.text())
    #         self.variable_model.item(ind.row(), 2).setText(d_type)
    #     self.update_variables()

    # def update_variables(self):
    #     """Taking all the variables from the list into the protocol."""
    #     self.protocol.variables = {}
    #     for i in range(self.variable_model.rowCount()):
    #         name = self.variable_model.item(i, 0).text()
    #         value = variables_handling.get_data(self.variable_model.item(i, 1).text())
    #         self.protocol.variables.update({name: value})
    #     variables_handling.protocol_variables = self.protocol.variables
    #     self.update_variable_select()

    def update_variable_select(self):
        if self.variable_table.selectedIndexes():
            self.pushButton_remove_variable.setEnabled(True)
        else:
            self.pushButton_remove_variable.setEnabled(False)

    def name_change(self):
        """ """
        name = self.lineEdit_protocol_name.text()
        self.label_title.setText(f"{name} - General Configuration")
        self.protocol.name = name
        self.name_changed.emit()
