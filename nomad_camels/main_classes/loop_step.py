from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QCheckBox,
)


from nomad_camels.utility import treeView_functions, variables_handling


class Loop_Step:
    """Main Class for all Loop_Steps.

    Parameters
    ----------
    name : str
        The custom name of the step.
    parent_step : Loop_Step, default None
        The step containing this step. If None, this step is in the outer layer.
    step_info : dict, default None
        Dictionary containing all the relevant information of the step.
    """

    def __init__(
        self, name="", parent_step=None, step_info=None, protocol=None, **kwargs
    ):
        self.step_type = "Default"
        self.__save_dict__ = {}
        self.has_children = False
        self.children = []
        self.name = name
        self.full_name = f"{self.step_type} ({name})"
        self.parent_step = parent_step
        self.time_weight = 1
        self.used_devices = []
        self.protocol = protocol or None
        if step_info and "description" in step_info:
            self.description = step_info["description"]
        else:
            self.description = ""
        if step_info and "is_active" in step_info:
            self.is_active = step_info["is_active"]
        else:
            self.is_active = True

    def update_full_name(self):
        """Updates the full_name by combination of step_type and name"""
        self.full_name = f"{self.step_type} ({self.name})"

    def append_to_model(self, item_model, parent=None):
        """Ensures that the full_name of the loop_step is unique and
        updates name and full_name, then appends the step to the model.

        Parameters
        ----------
        item_model : QStandardItemModel
            The item model that manages the view of the steps.
        parent : QStandardItem
            (Default value = None)
            The parent of the step inside the item modle
        """
        if parent is None:
            parent = item_model
            active = self.is_active
        else:
            p = parent if isinstance(parent, str) else parent.text()
            active = self.is_active and not p.startswith("# ")
        if type(parent) is str:
            parent = item_model.itemFromIndex(
                treeView_functions.getItemIndex(item_model, parent)
            )
        self.full_name = f"{self.step_type} ({self.name})"
        name = self.full_name
        if treeView_functions.getItemIndex(item_model, name) is not None:
            i = 1
            name = f"{name[:-1]}_{i})"
            while treeView_functions.getItemIndex(item_model, name) is not None:
                name = f"{name[:-3]}_{i})"
                i += 1
            self.name = name[len(self.step_type) + 2 : -1]
        if not active:
            name = f"# {name}"
        item = QStandardItem(name)
        item.setData(name)
        if not active:
            item.setForeground(Qt.gray)
        parent.appendRow(item)
        index = treeView_functions.getItemIndex(item_model, name)
        item_model.setData(index, QSize(20, 20), Qt.SizeHintRole)
        item.setDropEnabled(False)
        self.full_name = name
        return item

    def get_protocol_string(self, n_tabs=1):
        """Returns the string that is written into the protocol-file. To
        make use of the time_weight and status bar, it should start with
        printing, that the loop_step starts.

        Parameters
        ----------
        n_tabs : int
            (Default value = 1)
            Number of tabs for indentation inside the script

        Returns
        -------
        protocol_string : str
            The string representing the step
        """
        tabs = "\t" * n_tabs
        desc = self.description.replace("\n", f"\n{tabs}")
        protocol_string = f'\n{tabs}"""{desc}"""\n'
        # protocol_string += f'{tabs}print("starting loop_step {self.full_name}")\n'
        protocol_string += f'{tabs}protocol_step_information["protocol_stepper_signal"].emit(protocol_step_information["protocol_step_counter"] / protocol_step_information["total_protocol_steps"] * 100)\n'
        protocol_string += (
            f'{tabs}protocol_step_information["protocol_step_counter"] += 1\n'
        )
        protocol_string += f"{tabs}yield from bps.checkpoint()\n"
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """
        Gives a short overview of the step to quickly understand what the
        protocol does.

        Parameters
        ----------
        n_tabs : int
            (Default value = 0)
            Number of tabs for indentation inside the overview

        Returns
        -------
        short_string : str
            The string representing the step
        """
        tabs = "\t" * n_tabs
        short_string = f"{tabs}{self.step_type} '{self.name}'\n"
        return short_string

    def get_outer_string(self):
        """Returns the string for the protocol, where for example special plots
        for the step are created."""
        return ""

    def get_add_main_string(self):
        """Adds for example a call to the protocol function to the
        steps_add_main function of the script."""
        return ""

    def update_variables(self):
        """Should update the variables_handling, if the loopstep
        provides variables."""
        pass

    def update_used_devices(self):
        """Should update `used_devices` to include all necessary devices."""
        pass

    def update_time_weight(self):
        """The number of calls for this step. It is used to set the scaling for
        the progress bar of the protocol."""
        self.time_weight = 1


class Loop_Step_Container(Loop_Step):
    """Parent Class for loop_steps that should contain further steps
    (like e.g. a for-loop).

    Parameters
    ----------
    children : list of Loop_Step
        A list of the children inside this step (in the order, they are
        to be executed)
    """

    def __init__(
        self, name="", children=None, parent_step=None, step_info=None, **kwargs
    ):
        super().__init__(name, parent_step=parent_step, step_info=step_info, **kwargs)
        self.step_type = "Container"
        self.has_children = True
        if children is None:
            children = []
        self.children = children

    def append_to_model(self, item_model: QStandardItemModel, parent=None):
        """Overwrites this function to additionally append all children
        to the model."""
        item = super().append_to_model(item_model, parent)
        item.setDropEnabled(True)
        item.setEditable(False)
        for child in self.children:
            child.append_to_model(item_model, item)
        return item

    def add_child(self, child, position=-1):
        """Add a child-step at the specified position, default is -1,
        meaning to append at the end.

        Parameters
        ----------
        child : Loop_Step
            The child to be added.
        position : int
            (Default value = -1)
            The position, where to insert the child.
        """
        if position < 0:
            self.children.append(child)
        else:
            self.children.insert(position, child)

    def remove_child(self, child):
        """Removes the specified child from the children.

        Parameters
        ----------
        child : Loop_Step
            Child step to be removed.
        """
        self.children.remove(child)

    def get_protocol_string(self, n_tabs=1):
        """Returns the string that is written into the protocol-file. To
        make use of the time_weight and status bar, it should start with
        printing, that the loop_step starts.
        Here it is overwritten to include the strings of the children.
        """
        protocol_string = super().get_protocol_string(n_tabs)
        # protocol_string += self.get_children_strings(n_tabs+1)
        self.update_time_weight()
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """This is overwritten to include the strings from the children"""
        short_string = super().get_protocol_short_string(n_tabs)
        for child in self.children:
            short_string += child.get_protocol_short_string(n_tabs + 1)
        return short_string

    def get_outer_string(self):
        """This is overwritten to include the strings from the children"""
        outer_string = ""
        for child in self.children:
            outer_string += child.get_outer_string()
        return outer_string

    def get_add_main_string(self):
        """This is overwritten to include the strings from the children"""
        add_main_string = ""
        for child in self.children:
            add_main_string += child.get_add_main_string()
        return add_main_string

    def update_time_weight(self):
        """The time_weight of the children is included."""
        self.time_weight = 1
        for child in self.children:
            child.update_time_weight()
            self.time_weight += child.time_weight

    def get_children_strings(self, n_tabs=1):
        """Returns the protocol_strings of all the children.

        Parameters
        ----------
        n_tabs : int
            (Default value = 1)
            Number of tabs for indentation inside the script

        Returns
        -------
        child_string : str
            The string of all children's protocol strings.
        """
        child_string = ""
        for child in self.children:
            child_string += child.get_protocol_string(n_tabs)
        return child_string

    def update_variables(self):
        """Also updates the variables of the children."""
        for child in self.children:
            child.update_variables()

    def update_used_devices(self):
        """Includes the used devices of the children."""
        self.used_devices = []
        for child in self.children:
            child.update_used_devices()
            self.used_devices += child.used_devices
        self.used_devices = list(set(self.used_devices))


class Loop_Step_Config(QWidget):
    """Parent class for the configuration Widget of the loop_step.
    Provides the main layout and a lineEdit for changing the loop_steps
    name.

    Parameters
    ----------

    Returns
    -------

    """

    name_changed = Signal()
    add_other_step = Signal(dict)
    active_changed = Signal()

    def __init__(self, parent=None, loop_step=None):
        super(Loop_Step_Config, self).__init__(parent)
        layout = QGridLayout()
        self.name_widget = Loop_Step_Name_Widget(
            self, loop_step.name, loop_step.is_active
        )
        self.loop_step = loop_step
        self.name_widget.name_changed.connect(self.change_name)
        self.name_widget.active_changed.connect(self.change_active)
        layout.addWidget(self.name_widget, 0, 0, 1, 5)
        self.setLayout(layout)

        self.textEdit_desc = QTextEdit(loop_step.description, self)
        self.textEdit_desc.setPlaceholderText("Enter step description here.")

        layout.addWidget(self.textEdit_desc, 500, 0, 1, 5)

    def change_name(self, name):
        """Changes the name of the loop_step, then emits the
        name_changed signal.

        Parameters
        ----------
        name :


        Returns
        -------

        """
        self.loop_step.name = name
        self.loop_step.update_full_name()
        self.name_changed.emit()

    def change_active(self, active):
        """Changes if the step is active, or "commented out"."""
        self.loop_step.is_active = active
        self.active_changed.emit()

    def update_step_config(self):
        """Overwrite this for specific step-configuration. It should
        provide the loop_step object with all necessary data.

        Parameters
        ----------

        Returns
        -------

        """
        # self.loop_step.update_variables()
        self.name_widget.change_name()
        variables_handling.check_variable_name(self.loop_step.name, True, self)
        self.loop_step.description = self.textEdit_desc.toPlainText()


class Loop_Step_Name_Widget(QWidget):
    """Simple class that provides the necessary widgets for the step's
    name.

    Parameters
    ----------

    Returns
    -------

    """

    name_changed = Signal(str)
    active_changed = Signal(bool)

    def __init__(self, parent=None, name="", is_active=True):
        super().__init__(parent)
        label = QLabel("Name:")
        self.lineEdit_name = QLineEdit(name, self)
        self.checkBox_active = QCheckBox("active")
        self.checkBox_active.setChecked(is_active)

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.lineEdit_name, 0, 1)
        layout.addWidget(self.checkBox_active, 0, 2)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.lineEdit_name.returnPressed.connect(self.change_name)
        self.checkBox_active.clicked.connect(self.change_active)

    def change_active(self):
        self.active_changed.emit(self.checkBox_active.isChecked())

    def change_name(self):
        """ """
        self.name_changed.emit(self.lineEdit_name.text())
