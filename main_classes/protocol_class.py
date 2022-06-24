from PyQt5.QtWidgets import QWidget, QCheckBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem

# from main_classes.loop_step import Loop_Step, Loop_Step_Container
# from loop_steps import for_while_loops, read_channels
from loop_steps import make_step_of_type
from gui.general_protocol_settings import Ui_Protocol_Settings

from utility.add_remove_table import AddRemoveTable
from utility import variables_handling


class Measurement_Protocol:
    """Class for the measurement protocols. It mainly contains
    loop_steps and plots."""
    def __init__(self, loop_steps=None, plots=None, channels=None, name='',
                 channel_metadata=None, metadata=None, use_nexus=False,
                 config_metadata=None):
        if plots is None:
            plots = {}
        if loop_steps is None:
            loop_steps = []
        if channels is None:
            channels = {}
        if channel_metadata is None:
            channel_metadata = {}
        if metadata is None:
            metadata = {}
        self.loop_steps = loop_steps
        self.loop_step_dict = {}
        for step in self.loop_steps:
            update_all_children(self.loop_step_dict, step)
        self.plots = plots
        self.filename = ''
        self.variables = {}
        self.loop_step_variables = {}
        self.channels = channels
        self.name = name
        self.channel_metadata = channel_metadata
        self.config_metadata = config_metadata
        self.metadata = metadata
        self.use_nexus = use_nexus

    def update_variables(self):
        """Update all the variables provided by loopsteps."""
        self.loop_step_variables.clear()
        for step in self.loop_steps:
            step.update_variables()

    def get_nexus_paths(self):
        """Get a dictionary containing the paths used for the output
        NeXus-file."""
        paths = {}
        for i, name in enumerate(self.metadata['Name']):
            paths[self.metadata['NeXus-path'][i]] = f'metadata_start/{name}'
        for i, name in enumerate(self.channel_metadata['Channel']):
            paths[self.channel_metadata['NeXus-path'][i]] = f'data/{name}'
        for i, name in enumerate(self.config_metadata['Configuration']):
            path = ''
            for dev in variables_handling.devices:
                if dev in name:
                    rn = name.split(dev)[1][1:]
                    device = variables_handling.devices[dev]
                    if rn in device.get_config() or rn in device.get_settings() or rn in device.get_passive_config():
                        path = f'metadata_start/device_config/{dev}/{name}'
                        break
            if not path:
                raise Exception(f"Cannot find {name} in any configuration!")
            paths[self.config_metadata['NeXus-path'][i]] = path
        return paths

    def add_loop_step(self, loop_step, position=-1, parent_step_name=None, model=None):
        """Adds a loop_step to the protocol (or the parent_step)at the specified
        position. Also appends the loop_step to the given model. The
        loop_step is added to the list as well as the dictionary.

        Parameters
        ----------
        loop_step : Loop_Step
            The loop_step object to be added.
        position : int, default -1
            the position where to add it to the list / parent,
            if -1 appends the loopstep to the end
        parent_step_name : str, None, default None
            name of the parent loop_step. If specified, the loop_step is
            added to the parrent instead of the main sequence
        model : QStandardItemModel
            if specified, the loop_step is also added to that model
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

    def add_loop_step_rec(self, loop_step, model=None, parent_step_name=None, position=-1):
        """Recursively adds the loop_step and all its children to the
        protocol. Steps are added to the list if they have no parent,
        otherwise to the parent. All are added to the dictionary."""
        if parent_step_name is None:
            self.add_loop_step(loop_step, model=model, parent_step_name=parent_step_name, position=position)
        else:
            if model is not None:
                loop_step.append_to_model(model, parent=parent_step_name)
            if loop_step not in self.loop_step_dict[parent_step_name].children:
                self.loop_step_dict[parent_step_name].add_child(loop_step, position)
            self.loop_step_dict.update({loop_step.full_name: loop_step})
        # if loop_step.has_children:
        for child in loop_step.children:
            self.add_loop_step_rec(child, parent_step_name=loop_step.full_name, model=model)

    def remove_loop_step(self, loop_step_name):
        """Removes the step with the given name from the sequence-list
        (or parent) and from the dictionary."""
        step = self.loop_step_dict.pop(loop_step_name)
        if step.parent_step is not None:
            self.loop_step_dict[step.parent_step].remove_child(step)
        else:
            self.loop_steps.remove(step)


    def load_loop_steps(self, loop_steps, model=None):
        """Takes a list of loop_steps, creates them (with the input data
        of each step) and adds them to the specified model."""
        for step in loop_steps:
            loop_step = self.make_step(step)
            self.add_loop_step_rec(loop_step, model=model)

    def make_step(self, step_info):
        """Creates the step specified with step_info (including the
        children), 'step_type' gives which subclass of Loop_Step shall
        be created."""
        children = None
        # if step_info['has_children']:
        children = []
        if 'children' in step_info:
            for child in step_info['children']:
                child_step = self.make_step(child)
                child_step.parent_step = step_info['full_name']
                children.append(child_step)
        st = make_step_of_type.make_step(step_info['step_type'], step_info, children)
        st.full_name = step_info['full_name']
        return st

    def load_plots(self, plots):  # Not needed?
        self.plots = plots

    def rearrange_loop_steps(self, step_list):
        """Takes a list of loopsteps, each entry consisting of a tuple
        of the loopstep name and its children, which is recursively the
        same kind of list. Re-populates the loop_step_dict and then puts
        the loop_steps in the correct order."""
        self.loop_step_dict = {}
        for step in self.loop_steps:
            update_all_children(self.loop_step_dict, step)
        self.loop_steps = []
        for step, children in step_list:
            self.loop_step_dict[step].children = []
            append_all_children(children, self.loop_step_dict[step], self.loop_step_dict)
            self.loop_steps.append(self.loop_step_dict[step])

    def get_plan_string(self):
        """Get the string for the protocol-plan, including the loopsteps."""
        plan_string = f'\n\n\ndef {self.name.replace(" ","_")}_plan_inner(devs, runEngine=None, stream_name="primary"):\n'
        plan_string += '\teva = Evaluator(namespace=namespace)\n'
        plan_string += '\trunEngine.subscribe(eva)\n'
        for step in self.loop_steps:
            plan_string += step.get_protocol_string(n_tabs=1)
        plan_string += f'\n\n\ndef {self.name.replace(" ","_")}_plan(devs, md=None, runEngine=None, stream_name="primary"):\n'
        plan_string += '\tyield from bps.open_run(md=md)\n'
        plan_string += f'\tyield from {self.name.replace(" ", "_")}_plan_inner(devs, runEngine, stream_name)\n'
        plan_string += '\tyield from bps.close_run()\n'
        return plan_string

    def get_add_main_string(self):
        add_main_string = 'def steps_add_main(RE):\n'
        add_main_string += '\treturner = {}\n'
        for step in self.loop_steps:
            add_main_string += step.get_add_main_string()
        add_main_string += '\treturn returner\n\n\n'
        return add_main_string

    def get_outer_string(self):
        outer_string = ''
        for step in self.loop_steps:
            outer_string += step.get_outer_string()
        return outer_string

    def get_used_devices(self):
        """Get a list of all devices needed by any loopstep."""
        devices = []
        for step in self.loop_steps:
            step.update_used_devices()
            devices += step.used_devices
        return list(set(devices))

def append_all_children(child_list, step, step_dict):
    """Takes a list of the kind specified in rearrange_loop_steps, does
    the same as the other function, but recursively for all the
    (grand-)children."""
    for child, grandchildren in child_list:
        child_step = step_dict[child]
        child_step.children = []
        append_all_children(grandchildren, child_step, step_dict)
        child_step.parent_step = step.full_name
        step.children.append(child_step)

def update_all_children(step_dict, step):
    """Similar to append_all_children, but only updating the step_dict
    with all the children."""
    step_dict.update({step.full_name: step})
    # if step.has_children:
    for child in step.children:
        update_all_children(step_dict, child)


class General_Protocol_Settings(QWidget, Ui_Protocol_Settings):
    """Widget for the configuration of the general protocol settings.
    Here plots may be defined and variables added to the protocol."""
    def __init__(self, parent=None, protocol=Measurement_Protocol()):
        super(General_Protocol_Settings, self).__init__(parent)
        self.setupUi(self)
        self.protocol = protocol
        self.lineEdit_filename.setText(self.protocol.filename)

        self.variable_model = QStandardItemModel()
        self.variable_model.setHorizontalHeaderLabels(['Name', 'Value',
                                                       'Data-Type'])
        self.tableView_variables.setModel(self.variable_model)
        self.load_variables()

        self.pushButton_add_variable.clicked.connect(lambda x: self.add_variable())
        self.pushButton_remove_variable.clicked.connect(self.remove_variable)

        self.variable_model.itemChanged.connect(self.check_variable)
        comboBoxes = {'plot-type': ['X-Y plot', 'Value-List', '2D plot']}
        subtables = {'Y-axes': []}
        cols = ['plot-type', 'X-axis', 'Y-axes', 'title', 'x-label', 'y-label']
        self.plot_table = AddRemoveTable(headerLabels=cols, title='Plots',
                                         comboBoxes=comboBoxes,
                                         subtables=subtables,
                                         tableData=self.protocol.plots,
                                         checkstrings=[1,2])
        self.layout().addWidget(self.plot_table, 1, 0, 1, 4)

        cols = ['Channel', 'NeXus-path']
        comboBoxes = {'Channel': list(variables_handling.channels.keys())}
        self.table_channel_NX_paths = AddRemoveTable(headerLabels=cols,
                                                     title='Channel-NeXus-Path',
                                                     comboBoxes=comboBoxes,
                                                     tableData=self.protocol.channel_metadata)
        self.layout().addWidget(self.table_channel_NX_paths, 6, 0, 1, 4)

        cols = ['Configuration', 'NeXus-path']
        configs = []
        for dev in variables_handling.devices:
            device = variables_handling.devices[dev]
            allconf = []
            allconf += list(device.get_passive_config().keys())
            allconf += list(device.get_config().keys())
            allconf += list(device.get_settings().keys())
            allconf += list(device.get_ioc_settings().keys())
            for key in allconf:
                configs.append(f'{device.name}_{key}')
        comboBoxes = {'Configuration': configs}
        self.table_config_NX_paths = AddRemoveTable(headerLabels=cols,
                                                    title='Config-NeXus-Path',
                                                    comboBoxes=comboBoxes,
                                                    tableData=self.protocol.config_metadata)
        self.layout().addWidget(self.table_config_NX_paths, 7, 0, 1, 4)

        cols = ['Name', 'NeXus-path', 'Value']
        self.table_metadata = AddRemoveTable(headerLabels=cols,
                                             title='NeXus-Metadata',
                                             tableData=self.protocol.metadata)
        self.layout().addWidget(self.table_metadata, 8, 0, 1, 4)

        self.checkBox_NeXus = QCheckBox('Use NeXus-output')
        self.checkBox_NeXus.clicked.connect(self.enable_nexus)
        self.layout().addWidget(self.checkBox_NeXus, 5, 0, 1, 4)
        self.checkBox_NeXus.setChecked(self.protocol.use_nexus)
        self.enable_nexus()

    def enable_nexus(self):
        """When the checkBox_NeXus is clicked, enables / disables the
        other widgets for the nexus-definition."""
        nx = self.checkBox_NeXus.isChecked()
        self.table_channel_NX_paths.setEnabled(nx)
        self.table_metadata.setEnabled(nx)


    def get_unique_name(self, name='name'):
        """Checks whether name already exists in the variables of the
        protocol and returns a unique name (with added _i)."""
        i = 1
        while name in self.protocol.variables:
            if '_' not in name:
                name += f'_{i}'
            else:
                name = f'{name.split("_")[0]}_{i}'
            i += 1
        return name

    def add_variable(self):
        """Add a variable to the list, given a unique name, then updates
        the protocol."""
        self.append_variable(self.get_unique_name('name'))
        self.update_variables()

    def append_variable(self, name='name', value='value'):
        """Append the variable with name and value to the item_model,
        also add an item that shows the datatype of the value."""
        name_item = QStandardItem(name)
        value_item = QStandardItem(value)
        type_item = QStandardItem(variables_handling.check_data_type(value))
        type_item.setEditable(False)
        self.variable_model.appendRow([name_item, value_item, type_item])

    def remove_variable(self):
        """Removes the selected variable."""
        try:
            index = self.tableView_variables.selectedIndexes()[0]
        except IndexError:
            raise Exception('You need to select a row first!')
        if index.row() >= 0:
            self.variable_model.removeRow(index.row())
            self.update_variables()

    def update_step_config(self):
        """Updates all the protocol settings."""
        self.protocol.filename = self.lineEdit_filename.text()
        self.plot_table.update_table_data()
        self.protocol.plots = self.plot_table.tableData
        self.protocol.metadata = self.table_metadata.update_table_data()
        self.protocol.channel_metadata = self.table_channel_NX_paths.update_table_data()
        self.protocol.config_metadata = self.table_config_NX_paths.update_table_data()
        self.update_variables()
        self.protocol.use_nexus = self.checkBox_NeXus.isChecked()

    def load_variables(self):
        """Called when starting, loads the variables from the protocol
        into the table."""
        for var in sorted(self.protocol.variables):
            self.append_variable(var, str(self.protocol.variables[var]))

    def check_variable(self):
        """If name of variable changed: check whether the variable is
        unique, if not change its name and raise an error.
        If value changed: re-evaluate the data-type.
        Update the protocol afterwards."""
        ind = self.tableView_variables.selectedIndexes()[0]
        item = self.variable_model.itemFromIndex(ind)
        if ind.column() == 0 and item.text() in self.protocol.variables:
            new_name = self.get_unique_name(item.text())
            item.setText(new_name)
            raise Exception('Variable names must be unique!')
        if ind.column() == 1:
            d_type = variables_handling.check_data_type(item.text())
            self.variable_model.item(ind.row(), 2).setText(d_type)
        self.update_variables()

    def update_variables(self):
        """Taking all the variables from the list into the protocol."""
        self.protocol.variables = {}
        for i in range(self.variable_model.rowCount()):
            name = self.variable_model.item(i, 0).text()
            value = variables_handling.get_data(self.variable_model.item(i, 1).text())
            self.protocol.variables.update({name: value})


