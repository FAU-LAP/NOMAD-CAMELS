from copy import deepcopy

from PyQt5.QtWidgets import QWidget, QAction, QToolButton, QMenu, QMessageBox, QShortcut, QUndoStack, QDialogButtonBox
from PyQt5.QtCore import QItemSelectionModel, Qt, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QCloseEvent, QKeyEvent, QIcon

from CAMELS.gui.protocol_view import Ui_Protocol_View
from CAMELS.main_classes.protocol_class import Measurement_Protocol, General_Protocol_Settings
from CAMELS.loop_steps import make_step_of_type
from CAMELS.utility import variables_handling, treeView_functions, drag_drop_tree_view
from CAMELS.commands import change_sequence

from pkg_resources import resource_filename


class Protocol_Config(QWidget, Ui_Protocol_View):
    accepted = pyqtSignal(Measurement_Protocol)
    closing = pyqtSignal()

    def __init__(self, protocol=Measurement_Protocol(), parent=None):
        super().__init__(parent=parent)
        protocol = deepcopy(protocol)
        self.setupUi(self)
        self.old_name = None
        if protocol.name != 'Protocol':
            self.old_name = protocol.name
        self.setWindowTitle(f'{protocol.name} - Measurement Protocol - CAMELS')
        self.setWindowIcon(QIcon(resource_filename('CAMELS','graphics/CAMELS_Icon_v2.ico')))
        self.configuration_main_widget.setHidden(True)
        self.general_settings = General_Protocol_Settings(protocol=protocol)
        self.meas_splitter.insertWidget(0, self.general_settings)

        self.toolButton_add_step.setPopupMode(QToolButton.InstantPopup)
        self.protocol = protocol
        self.loop_step_configuration_widget = None

        self.add_actions = []
        self.device_actions = []
        self.is_accepted = False

        self.item_model_sequence = QStandardItemModel(0,1)
        self.treeView_protocol_sequence = drag_drop_tree_view.Drag_Drop_TreeView()
        self.treeView_protocol_sequence.del_clicked.connect(self.remove_loop_step)
        self.sequence_main_widget.layout().addWidget(self.treeView_protocol_sequence, 5, 0, 1, 3)
        self.treeView_protocol_sequence.setModel(self.item_model_sequence)
        self.treeView_protocol_sequence.customContextMenuRequested.connect(self.sequence_right_click)
        self.treeView_protocol_sequence.dragdrop.connect(self.update_loop_step_order)

        self.pushButton_move_step_up.clicked.connect(lambda state: self.move_loop_step(-1,0))
        self.pushButton_move_step_down.clicked.connect(lambda state: self.move_loop_step(1,0))
        self.pushButton_move_step_in.clicked.connect(lambda state: self.move_loop_step(0,1))
        self.pushButton_move_step_out.clicked.connect(lambda state: self.move_loop_step(0,-1))
        self.treeView_protocol_sequence.clicked.connect(lambda x: self.tree_click_sequence(False))
        self.pushButton_remove_step.clicked.connect(lambda x: self.remove_loop_step(True))
        self.general_settings.name_changed.connect(self.change_name)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.accept)

        self.update_add_step_actions()

        self.layout().addWidget(self.buttonBox, 15, 0)

        self.inside_function = False
        self.undo_stack = QUndoStack(self)
        # QShortcut('Ctrl+z', self).activated.connect(self.undo)
        # QShortcut('Ctrl+y', self).activated.connect(self.redo)

        QShortcut('Ctrl+x', self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut).activated.connect(self.cut_shortcut)
        QShortcut('Ctrl+v', self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut).activated.connect(self.paste_shortcut)
        QShortcut('Ctrl+c', self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut).activated.connect(self.copy_shortcut)

        self.build_protocol_sequence()


    def update_add_step_actions(self):
        """Called when the devices change, updating the possible
        loopsteps to include new device steps."""
        self.add_actions.clear()
        self.device_actions.clear()
        for stp in sorted(make_step_of_type.step_type_config.keys(), key=lambda x: x.lower()):
            action = QAction(stp)
            action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
            self.add_actions.append(action)
        for stp in make_step_of_type.get_device_steps():
            action = QAction(stp)
            action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
            self.device_actions.append(action)
        self.toolButton_add_step.addActions(self.add_actions)
        if self.device_actions:
            self.toolButton_add_step.addActions(self.device_actions)



    def tree_click_sequence(self, general=False):
        """Called when clicking the treeView_protocol_sequence."""
        self.update_loop_step_order()
        self.get_step_config()
        self.protocol.update_variables()
        self.configuration_main_widget.setHidden(False)
        config = None
        if general:
            config = General_Protocol_Settings(self, self.protocol)
            self.enable_step_move(False)
            self.label_configuration.setText('Configuration: General Protocol Settings')
        else:
            index = self.treeView_protocol_sequence.selectedIndexes()[0]
            dat = self.item_model_sequence.itemFromIndex(index).data()
            if dat is not None:
                step = self.protocol.loop_step_dict[dat]
                config = make_step_of_type.get_config(step)
                enable = step.step_type not in make_step_of_type.non_addables
                self.enable_step_move(enable)
                self.label_configuration.setText(f'Configuration: {step.full_name}')
        if config is not None:
            if self.loop_step_configuration_widget is not None:
                self.configuration_main_widget.layout().removeWidget(self.loop_step_configuration_widget)
                self.loop_step_configuration_widget.deleteLater()
            self.loop_step_configuration_widget = config
            self.configuration_main_widget.layout().addWidget(self.loop_step_configuration_widget, 1, 0)
            if not general:
                self.loop_step_configuration_widget.name_changed.connect(self.change_step_name)

    def build_protocol_sequence(self):
        """Shows / builds the protocol sequence in the treeView
        dependent on the loop_steps in the current_protocol."""
        ind_seq = self.treeView_protocol_sequence.selectedIndexes()
        sel_data = ''
        if ind_seq:
            sel_data = self.item_model_sequence.data(ind_seq[0])
        variables_handling.current_protocol = self.protocol
        variables_handling.protocol_variables = self.protocol.variables
        variables_handling.loop_step_variables = self.protocol.loop_step_variables
        self.item_model_sequence.clear()
        for loop_step in self.protocol.loop_steps:
            loop_step.append_to_model(self.item_model_sequence)
        self.treeView_protocol_sequence.expandAll()
        self.sequence_main_widget.setEnabled(True)
        if sel_data is not None:
            new_index = treeView_functions.getItemIndex(self.item_model_sequence, sel_data)
            if new_index:
                self.treeView_protocol_sequence.selectionModel().select(new_index, QItemSelectionModel.Select)

    def enable_step_move(self, enable):
        self.pushButton_move_step_in.setEnabled(enable)
        self.pushButton_move_step_out.setEnabled(enable)
        self.pushButton_move_step_up.setEnabled(enable)
        self.pushButton_move_step_down.setEnabled(enable)

    def change_step_name(self):
        """Called when a loop_step changes its name, then updates the
        shown sequence, and also the protocol-data."""
        self.build_protocol_sequence()
        self.update_loop_step_order()

    def get_step_config(self):
        """Updates the data in the currently-to-configure loop_step."""
        if self.loop_step_configuration_widget is not None:
            self.loop_step_configuration_widget.update_step_config()


    def sequence_right_click(self, pos):
        """Opens a specific Menu on right click in the protocol-sequence.
        If selection is not on a loop_step, it consists only of Add Step,
        otherwise it consists of Delete Step."""
        # TODO other actions
        # TODO more beautiful?
        menu = QMenu()
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if inds:
            item = self.item_model_sequence.itemFromIndex(inds[0])
            below_actions = []
            above_actions = []
            into_actions = []
            row = inds[0].row()
            parent = item.parent()
            if parent is not None:
                parent = parent.data()
            for stp in sorted(make_step_of_type.step_type_config.keys(), key=lambda x: x.lower()):
                action = QAction(stp)
                action_a = QAction(stp)
                action_in = QAction(stp)
                action.triggered.connect(lambda state, x=stp, y=row+1, z=parent: self.add_loop_step(x, y, z))
                action_a.triggered.connect(lambda state, x=stp, y=row, z=parent: self.add_loop_step(x, y, z))
                action_in.triggered.connect(lambda state, x=stp, y=-1, z=item.data(): self.add_loop_step(x,y,z))
                below_actions.append(action)
                above_actions.append(action_a)
                into_actions.append(action_in)
            device_actions = []
            device_actions_a = []
            device_actions_in = []
            for stp in make_step_of_type.get_device_steps():
                action = QAction(stp)
                action_a = QAction(stp)
                action_in = QAction(stp)
                action.triggered.connect(lambda state, x=stp, y=row+1, z=parent: self.add_loop_step(x, y, z))
                action_a.triggered.connect(lambda state, x=stp, y=row, z=parent: self.add_loop_step(x, y, z))
                action_in.triggered.connect(lambda state, x=stp, y=-1, z=item.data(): self.add_loop_step(x,y,z))
                device_actions.append(action)
                device_actions_a.append(action_a)
                device_actions_in.append(action_in)
            insert_above_menu = QMenu('Insert Above')
            insert_above_menu.addActions(above_actions)
            insert_below_menu = QMenu('Insert Below')
            insert_below_menu.addActions(below_actions)
            if device_actions:
                insert_above_menu.addSeparator()
                insert_above_menu.addActions(device_actions_a)
                insert_below_menu.addSeparator()
                insert_below_menu.addActions(device_actions)
            if self.protocol.loop_step_dict[item.data()].has_children:
                add_in_menu = QMenu('Add Into')
                add_in_menu.addActions(into_actions)
                menu.addMenu(add_in_menu)
                if device_actions:
                    add_in_menu.addSeparator()
                    add_in_menu.addActions(device_actions_in)
            menu.addMenu(insert_above_menu)
            menu.addMenu(insert_below_menu)
            menu.addSeparator()
            cut_action = QAction('Cut')
            cut_action.triggered.connect(lambda state, x=item.data(): self.cut_loop_step(x))
            copy_action = QAction('Copy')
            copy_action.triggered.connect(lambda state, x=item.data(): self.copy_loop_step(x))
            paste_menu = QMenu('Paste')
            if variables_handling.copied_step is not None:
                paste_above = QAction('Paste Above')
                paste_above.triggered.connect(lambda state, x=True, y=row, z=parent: self.add_loop_step(copied_step=x, position=y, parent=z))
                paste_below = QAction('Paste Below')
                paste_below.triggered.connect(lambda state, x=True, y=row+1, z=parent: self.add_loop_step(copied_step=x, position=y, parent=z))
                if self.protocol.loop_step_dict[item.data()].has_children:
                    paste_into = QAction('Paste Into')
                    paste_into.triggered.connect(lambda state, x=True, y=-1, z=item.data(): self.add_loop_step(copied_step=x,position=y,parent=z))
                    paste_menu.addAction(paste_into)
                paste_menu.addActions([paste_above, paste_below])
            else:
                paste_menu.setEnabled(False)
            menu.addAction(cut_action)
            menu.addAction(copy_action)
            menu.addMenu(paste_menu)
            menu.addSeparator()
            if self.protocol.loop_step_dict[item.data()].step_type not in make_step_of_type.non_addables:
                del_action = QAction('Delete Step')
                del_action.triggered.connect(lambda x: self.remove_loop_step(True))
                menu.addAction(del_action)
        else:
            add_actions = []
            for stp in sorted(make_step_of_type.step_type_config, key=lambda x: x.lower()):
                action = QAction(stp)
                action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
                add_actions.append(action)
            device_actions = []
            for stp in make_step_of_type.get_device_steps():
                action = QAction(stp)
                action.triggered.connect(lambda state, x=stp: self.add_loop_step(x))
                device_actions.append(action)
            add_menu = QMenu('Add Step')
            add_menu.addActions(add_actions)
            if device_actions:
                add_menu.addSeparator()
                add_menu.addActions(device_actions)
            paste_action = QAction('Paste')
            if variables_handling.copied_step is not None:
                paste_action.triggered.connect(lambda state, x=True, y=-1, z=None: self.add_loop_step(copied_step=x, position=y, parent=z))
            else:
                paste_action.setEnabled(False)
            menu.addMenu(add_menu)
            menu.addAction(paste_action)
        menu.exec_(self.treeView_protocol_sequence.viewport().mapToGlobal(pos))

    def paste_shortcut(self):
        if variables_handling.copied_step is None:
            return
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if inds:
            ind = inds[0]
            item = self.item_model_sequence.itemFromIndex(ind)
            if self.protocol.loop_step_dict[item.data()].has_children:
                pos = -1
                parent = item.data()
            else:
                pos = ind.row() + 1
                parent = item.parent()
        else:
            pos = -1
            parent = None
        self.add_loop_step(copied_step=True, position=pos, parent=parent)

    def cut_shortcut(self):
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if not inds:
            return
        item = self.item_model_sequence.itemFromIndex(inds[0])
        self.cut_loop_step(item.data())

    def copy_shortcut(self):
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if not inds:
            return
        item = self.item_model_sequence.itemFromIndex(inds[0])
        self.copy_loop_step(item.data())

    def cut_loop_step(self, step_name):
        """Copies the given step, then removes it."""
        self.copy_loop_step(step_name)
        self.remove_loop_step(ask=False)

    def copy_loop_step(self, step_name):
        """Makes a deepcopy of the given step and stores it in
        copied_loop_step."""
        variables_handling.copied_step = deepcopy(self.protocol.loop_step_dict[step_name])

    def move_loop_step(self, up_down=0, in_out=0):
        """Moves a loop_step up or down in the sequence. It can also be
        moved in or out (into the loop_step above, it if accepts children).

        Parameters
        ----------
        up_down : int
            moves up if negative (lower row-number), down if positive
            (default is 0)
        in_out : int
            moves in if positive, out if negative, (default 0)
        """
        move_command = change_sequence.CommandMoveStep(self.treeView_protocol_sequence, self.item_model_sequence, up_down, in_out, self.protocol.loop_step_dict, self.update_loop_step_order)
        self.undo_stack.push(move_command)

    def add_loop_step(self, step_type='', position=-1, parent=None,
                      copied_step=False):
        """Add a loop_step of given step_type. Updates the current
        sequence into the protocol, then initializes the new step.

        Parameters
        ----------
        step_type : str
            gives the type of step to be added
        position : int, optional
            where to add the step, (default -1, append to the end)
        parent : Loop_Step, optional
            parent, where to add the new step, (default None, the step
            is added to the outermost layer of the protocol)
        copied_step : bool, optional
            if False, a new step of type step_type will be created,
            otherwise copied_loop_step will be inserted
        """

        self.update_loop_step_order()
        if copied_step:
            step = variables_handling.copied_step
        else:
            step = make_step_of_type.make_step(step_type)
        self.protocol.add_loop_step_rec(step, model=self.item_model_sequence, position=position, parent_step_name=parent)
        self.build_protocol_sequence()
        if copied_step:
            self.copy_loop_step(variables_handling.copied_step.full_name)
        new_ind = treeView_functions.getItemIndex(self.item_model_sequence, step.full_name)
        self.treeView_protocol_sequence.selectionModel().select(new_ind, QItemSelectionModel.Select)

    def remove_loop_step(self, ask=True):
        """After updating the loop_step order in the protocol, the
        selected loop step is deleted (if the messagebox is accepted)."""
        self.update_loop_step_order()
        ind = self.treeView_protocol_sequence.selectedIndexes()[0]
        name = self.item_model_sequence.itemFromIndex(ind).data()
        if name is not None:
            remove_dialog = None
            if self.protocol.loop_step_dict[name].step_type in make_step_of_type.non_addables:
                return
            if ask:
                remove_dialog = QMessageBox.question(self, 'Delete Step?', f'Are you sure you want to delete the step {name}?', QMessageBox.Yes | QMessageBox.No)
            if not ask or remove_dialog == QMessageBox.Yes:
                self.protocol.remove_loop_step(name)
                self.build_protocol_sequence()

    def update_loop_step_order(self):
        """Goes through all the loop_steps in the sequence, then
        rearranges them in the protocol."""
        self.general_settings.update_step_config()
        loop_steps = []
        for i in range(self.item_model_sequence.rowCount()):
            item = self.item_model_sequence.item(i, 0)
            sub_steps = treeView_functions.get_substeps(item)
            loop_steps.append((item.data(), sub_steps))
        self.protocol.rearrange_loop_steps(loop_steps)

    def accept(self) -> None:
        self.update_loop_step_order()
        self.get_step_config()
        self.check_protocol_name()
        self.accepted.emit(self.protocol)
        self.is_accepted = True
        self.close()

    def check_protocol_name(self):
        name = self.general_settings.lineEdit_protocol_name.text()
        if name in variables_handling.protocols and name != self.old_name:
            raise Exception(f'Protocol name "{name}" already in use!')

    def closeEvent(self, a0: QCloseEvent) -> None:
        name = self.general_settings.lineEdit_protocol_name.text()
        if not self.is_accepted:
            discard_dialog = QMessageBox.question(self, f'{name} - Discard Changes?',
                                                  f'All changes to {name} will be lost!',
                                                  QMessageBox.Yes | QMessageBox.No)
            if discard_dialog != QMessageBox.Yes:
                a0.ignore()
                return
        a0.accept()
        super().closeEvent(a0)
        self.closing.emit()

    def change_name(self):
        self.setWindowTitle(f'{self.protocol.name} - Measurement Protocol - CAMELS')

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return."""
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    widge = Protocol_Config()
    widge.show()
    sys.exit(app.exec())
