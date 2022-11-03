from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit


from utility import treeView_functions



class Loop_Step:
    """Main Class for all Loop_Steps.

    Attributes
    ----------
    step_type : str
        should be overwritten on inheritance, gives the type of Loop_Step
    has_children : bool
        set to True if a loop_step accepts children
    name : str
        specification of the loop_step (other than the type)
    full name : str
        consists of the type and name
    parent_step : str
        the loop_steps name which contains this step
    time_weight : int
        used for updating the progressBar for a running protocol
    used_devices : list
        list of the device-names used for this loopstep\
    """
    def __init__(self, name='', parent_step=None, step_info=None, **kwargs):
        self.step_type = 'Default'
        self.__save_dict__ = {}
        self.has_children = False
        self.children = []
        self.name = name
        self.full_name = f'{self.step_type} ({name})'
        self.parent_step = parent_step
        self.time_weight = 1
        self.used_devices = []
        if step_info and 'description' in step_info:
            self.description = step_info['description']
        else:
            self.description = ''

    def update_full_name(self):
        """Updates the full_name by combination of step_type and name"""
        self.full_name = f'{self.step_type} ({self.name})'

    def append_to_model(self, item_model, parent=None):
        """Ensures that the (full_)name of the loop_step is unique and
        updates name and full_name, then appends the step to the model."""
        if parent is None:
            parent = item_model
        if type(parent) is str:
            parent = item_model.itemFromIndex(treeView_functions.getItemIndex(item_model, parent))
        self.full_name = f'{self.step_type} ({self.name})'
        name = self.full_name
        if treeView_functions.getItemIndex(item_model, name) is not None:
            i = 1
            name = f'{name[:-1]}_{i})'
            while treeView_functions.getItemIndex(item_model, name) is not None:
                name = f'{name[:-3]}_{i})'
                i += 1
            self.name = name[len(self.step_type)+2:-1]
        item = QStandardItem(name)
        item.setData(name)
        parent.appendRow(item)
        index = treeView_functions.getItemIndex(item_model, name)
        item_model.setData(index, QSize(20,20), Qt.SizeHintRole)
        item.setDropEnabled(False)
        self.full_name = name
        return item

    def get_protocol_string(self, n_tabs=1):
        """Returns the string that is written into the protocol-file. To
        make use of the time_weight and status bar, it should start with
        printing, that the loop_step starts."""
        tabs = '\t'*n_tabs
        desc = self.description.replace("\n", f"\n{tabs}")
        protocol_string = f'\n{tabs}"""{desc}"""\n'
        protocol_string += f'{tabs}print("starting loop_step {self.full_name}")\n'
        protocol_string += f'{tabs}yield from bps.checkpoint()\n'
        return protocol_string

    def get_outer_string(self):
        return ''

    def get_add_main_string(self):
        return ''

    def update_variables(self):
        """Should update the variables_handling, if the loopstep
        provides variables."""
        pass

    def update_used_devices(self):
        """Should update `used_devices` to include all necessary devices."""
        pass

    def update_time_weight(self):
        """The time_weight of the children is included."""
        self.time_weight = 1


class Loop_Step_Container(Loop_Step):
    """Parent Class for loop_steps that should contain further steps
    (like e.g. a for-loop).

    Attributes
    ----------
    children : list of Loop_Step
        A list of the children inside this step (in the order, they are
        to be executed)
    """
    def __init__(self, name='', children=None, parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step=parent_step, step_info=step_info, **kwargs)
        self.step_type = 'Container'
        self.has_children = True
        if children is None:
            children = []
        self.children = children

    def append_to_model(self, item_model:QStandardItemModel, parent=None):
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
        meaning to append at the end."""
        if position < 0:
            self.children.append(child)
        else:
            self.children.insert(position, child)

    def remove_child(self, child):
        """Removes the specified child from the children."""
        self.children.remove(child)

    def get_protocol_string(self, n_tabs=1):
        """Returns the string that is written into the protocol-file. To
        make use of the time_weight and status bar, it should start with
        printing, that the loop_step starts.
        Here it is overwritten to include the strings of the children."""
        protocol_string = super().get_protocol_string(n_tabs)
        # protocol_string += self.get_children_strings(n_tabs+1)
        self.update_time_weight()
        return protocol_string

    def get_outer_string(self):
        outer_string = ''
        for child in self.children:
            outer_string += child.get_outer_string()
        return outer_string

    def get_add_main_string(self):
        add_main_string = ''
        for child in self.children:
            add_main_string += child.get_add_main_string()
        return add_main_string

    def update_time_weight(self):
        """The time_weight of the children is included."""
        self.time_weight = 1
        for child in self.children:
            self.time_weight += child.time_weight


    def get_children_strings(self, n_tabs=1):
        """Returns the protocol_strings of all the children."""
        child_string = ''
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
    name."""
    name_changed = pyqtSignal()
    add_other_step = pyqtSignal(dict)

    def __init__(self, parent=None, loop_step=None):
        super(Loop_Step_Config, self).__init__(parent)
        layout = QGridLayout()
        self.name_widget = Loop_Step_Name_Widget(self, loop_step.name, loop_step.description)
        self.loop_step = loop_step
        self.name_widget.name_changed.connect(self.change_name)
        layout.addWidget(self.name_widget, 0, 0, 1, 5)
        self.setLayout(layout)

    def change_name(self, name):
        """Changes the name of the loop_step, then emits the
        name_changed signal."""
        self.loop_step.name = name
        self.loop_step.update_full_name()
        self.name_changed.emit()

    def update_step_config(self):
        """Overwrite this for specific step-configuration. It should
        provide the loop_step object with all necessary data."""
        # self.loop_step.update_variables()
        self.name_widget.change_name()
        self.loop_step.description = self.name_widget.textEdit_desc.toPlainText()

class Loop_Step_Name_Widget(QWidget):
    """Simple class that provides the necessary widgets for the step's
    name."""
    name_changed = pyqtSignal(str)

    def __init__(self, parent=None, name='', description=''):
        super().__init__(parent)
        label = QLabel('Name:')
        self.lineEdit_name = QLineEdit(name, self)
        self.textEdit_desc = QTextEdit(description, self)
        self.textEdit_desc.setText(description)
        self.textEdit_desc.setPlaceholderText('Enter step description here.')

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.lineEdit_name, 0, 1)
        layout.addWidget(self.textEdit_desc, 1, 0, 1, 2)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.lineEdit_name.returnPressed.connect(self.change_name)

    def change_name(self):
        self.name_changed.emit(self.lineEdit_name.text())
