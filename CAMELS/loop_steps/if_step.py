from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QGridLayout,\
    QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItemModel

from CAMELS.main_classes.loop_step import Loop_Step_Container, Loop_Step_Config
from CAMELS.utility.variable_tool_tip_box import Variable_Box
from CAMELS.utility.add_remove_table import AddRemoveTable


class If_Loop_Step(Loop_Step_Container):
    """A loopstep providing an if-case selection with a variable number
    of `elif`.

    Attributes
    ----------
    condition : str
        The condition which is used for the if-conditional
    use_else : bool
        whether to add an `else`-case
    elifs : list of str
        string-list of the conditions for a variable number of `elif`
    """
    def __init__(self, name='', children=None, parent_step=None, step_info=None,
                 **kwargs):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        self.step_type = 'If'
        self.has_children = False
        if step_info is None:
            step_info = {}
        self.condition = step_info['condition'] if 'condition' in step_info else '!'
        self.use_else = step_info['use_else'] if 'use_else' in step_info else False
        self.elifs = step_info['elifs'] if 'elifs' in step_info else []
        self.update_children()

    def append_to_model(self, item_model:QStandardItemModel, parent=None):
        """Overwritten, so that nothing can be dropped into the main step."""
        item = super(If_Loop_Step, self).append_to_model(item_model, parent)
        item.setDropEnabled(False)
        return item

    def update_children(self):
        """Updates the if-substeps provided by this step, giving them
        the names corresponding to the conditions."""
        if not self.children:
            self.children.append(If_Sub_Step(f'{self.name}_{self.condition}'))
        n_children = 1 + len(self.elifs) + (1 if self.use_else else 0)
        if self.use_else and not isinstance(self.children[-1], Else_Sub_Step):
            self.children.append(Else_Sub_Step(f'{self.name}_Else'))
        elif not self.use_else and isinstance(self.children[-1], Else_Sub_Step):
            self.children.pop()
        pops = []
        for i, child in enumerate(self.children):
            if i == 0:
                child.name = f'{self.name}_{self.condition}'
            elif self.use_else and i == len(self.children) - 1:
                child.name = f'{self.name}_Else'
            else:
                try:
                    child.name = f'{self.name}_{self.elifs[i-1]}'
                except IndexError:
                    pops.append(i)
        for i in reversed(pops):
            self.children.pop(i)
        diff = n_children - len(self.children)
        if diff > 0:
            for cond in self.elifs[-diff:]:
                if self.use_else:
                    self.children.insert(-1,
                                         Elif_Sub_Step(f'{self.name}_{cond}'))
                else:
                    self.children.append(Elif_Sub_Step(f'{self.name}_{cond}'))
        elif diff < 0:
            raise Exception('something went wrong with if-children!')

    def get_protocol_string(self, n_tabs=1):
        """Putting together the children of all if-substeps."""
        tabs = '\t' * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f'{tabs}if eva.eval("{self.condition}"):\n'
        protocol_string += self.children[0].get_children_strings(n_tabs+1)
        for i, el in enumerate(self.elifs):
            child = self.children[i+1]
            protocol_string += f'{tabs}elif eva.eval("{el}"):\n'
            protocol_string += child.get_children_strings(n_tabs+1)
        if self.use_else:
            protocol_string += f'{tabs}else:\n'
            protocol_string += self.children[-1].get_children_strings(n_tabs+1)
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        tabs = '\t' * n_tabs
        short_string = f'{tabs}if {self.condition}:\n'
        for child in self.children[0].children:
            short_string += child.get_protocol_short_string(n_tabs+1)
        for i, el in enumerate(self.elifs):
            short_string += f'{tabs}else if {el}:\n'
            for child in self.children[i+1].children:
                short_string += child.get_protocol_short_string(n_tabs+1)
        if self.use_else:
            short_string += f'{tabs}else:\n'
            for child in self.children[-1].children:
                short_string += child.get_protocol_short_string(n_tabs+1)
        return short_string





class If_Sub_Step(Loop_Step_Container):
    """Simple sub-step that represents the if-condition."""
    def __init__(self, name='', children=None, parent_step=None, step_info=None,
                 **kwargs):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        self.step_type = 'If_Sub'

    def append_to_model(self, item_model:QStandardItemModel, parent=None):
        """Overwritten, so that nothing can be dropped into the main step."""
        item = super().append_to_model(item_model, parent)
        item.setDragEnabled(False)
        item.setEnabled(False)
        return item

class Elif_Sub_Step(If_Sub_Step):
    """Simple sub-step that represents an elif-condition."""
    def __init__(self, name='', children=None, parent_step=None, step_info=None,
                 **kwargs):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        self.step_type = 'Elif_Sub'

class Else_Sub_Step(If_Sub_Step):
    """Simple sub-step that represents the else-condition."""
    def __init__(self, name='', children=None, parent_step=None, step_info=None,
                 **kwargs):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        self.step_type = 'Else_Sub'



class Sub_Step_Config(Loop_Step_Config):
    """Configuration for the substeps, disabling the name-widget."""
    def __init__(self, loop_step:Loop_Step_Container, parent=None):
        super().__init__(parent, loop_step)
        self.name_widget.setEnabled(False)


class If_Step_Config(Loop_Step_Config):
    """Configuration-Widget for the if-loop step."""
    def __init__(self, loop_step:If_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = If_Step_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)
        self.sub_widget.update_config.connect(self.update_step_config)

    def update_step_config(self):
        """Overwritten, so that the loopstep updates its substeps for
        correctly building the protocol sequence."""
        self.sub_widget.update_condition(True)
        self.loop_step.update_children()
        super().update_step_config()




class If_Step_Config_Sub(QWidget):
    """This widget consists of a line for the if-condition an
    AddRemoveTable for the elif-conditions and a checkbox for whether to
    use an else-case."""
    update_config = pyqtSignal()

    def __init__(self, loop_step:If_Loop_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step

        label = QLabel('Condition:')
        self.lineEdit_condition = Variable_Box(self)
        self.lineEdit_condition.setText(loop_step.condition)
        self.lineEdit_condition.textChanged.connect(self.update_condition)

        self.elif_table = AddRemoveTable(parent=self,
                                         headerLabels=[],
                                         tableData=self.loop_step.elifs,
                                         title='Elif-cases:',
                                         checkstrings=0, askdelete=True)
        self.elif_table.sizechange.connect(self.update_condition)

        self.checkBox_use_else = QCheckBox('Use Else')
        self.checkBox_use_else.setChecked(self.loop_step.use_else)
        self.checkBox_use_else.clicked.connect(self.else_change)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.lineEdit_condition, 0, 1)
        layout.addWidget(self.checkBox_use_else, 1, 0, 1, 2)
        layout.addWidget(self.elif_table, 2, 0, 1, 2)
        self.setLayout(layout)

    def else_change(self):
        """When removing the else-case, first ask the user if they are
        sure, since substeps will be deleted as well."""
        if self.loop_step.use_else:
            dialog = QMessageBox.question(self,
                                          'Remove Else case?',
                                          'Removing the Else-case also deletes its children',
                                          QMessageBox.Yes | QMessageBox.No)
            if dialog != QMessageBox.Yes:
                self.checkBox_use_else.setChecked(True)
                return
        self.update_condition()

    def update_condition(self, called=False):
        """Updating the loopstep. The signal is not emitted if the
        function is called from outside, so there is no infinite loop."""
        self.loop_step.use_else = self.checkBox_use_else.isChecked()
        self.loop_step.elifs = self.elif_table.update_table_data()
        self.loop_step.condition = self.lineEdit_condition.text()
        if not called:
            self.update_config.emit()
