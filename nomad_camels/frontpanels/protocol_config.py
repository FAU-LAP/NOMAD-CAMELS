from copy import deepcopy

from PySide6.QtWidgets import QWidget, QToolButton, QMenu, QMessageBox, QDialogButtonBox
from PySide6.QtCore import QItemSelectionModel, Qt, Signal
from PySide6.QtGui import (
    QStandardItemModel,
    QAction,
    QCloseEvent,
    QKeyEvent,
    QShortcut,
    QIcon,
    QUndoStack,
)

from nomad_camels.gui.protocol_view import Ui_Protocol_View
from nomad_camels.main_classes.protocol_class import (
    Measurement_Protocol,
    General_Protocol_Settings,
)
from nomad_camels.loop_steps import make_step_of_type
from nomad_camels.utility import variables_handling, treeView_functions
from nomad_camels.ui_widgets import drag_drop_tree_view
from nomad_camels.commands import change_sequence

from importlib import resources
from nomad_camels import graphics


loop_step_display_order = [
    "Read Channels",
    "Set Channels",
    "For Loop",
    "Simple Sweep",
    "Wait",
    "Run Subprotocol",
    "If",
    "Set Variables",
    "Execute Python File",
    "ND Sweep",
    "Change Device Config",
    "While Loop",
    "Gradient Descent",
    "API Call",
    "Set Value Popup",
    "Trigger Channels",
    "Prompt",
    "Call Function",
]

channel_action_list = [
    "Read Channels",
    "Set Channels",
    "Trigger Channels",
]
loop_action_list = [
    "For Loop",
    "While Loop",
    "Simple Sweep",
    "ND Sweep",
]
additional_action_list = [
    "Execute Python File",
    "API Call",
    "Change Device Config",
    "Gradient Descent",
    "Prompt",
    "Call Function",
    "Set Value Popup",
]


class Protocol_Config(Ui_Protocol_View, QWidget):
    """ """

    accepted = Signal(Measurement_Protocol)
    closing = Signal()

    def __init__(self, protocol=None, parent=None):
        super().__init__(parent=parent)
        self.old_name = None
        if protocol is None:
            protocol = Measurement_Protocol()
        else:
            protocol = deepcopy(protocol)
            self.old_name = protocol.name
        self.setupUi(self)
        self.setWindowTitle(f"{protocol.name} - Measurement Protocol - NOMAD CAMELS")
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "camels_icon.png")))
        self.configuration_main_widget.setHidden(True)
        self.general_settings = General_Protocol_Settings(protocol=protocol)
        self.meas_splitter.insertWidget(0, self.general_settings)

        self.toolButton_add_step.setPopupMode(QToolButton.InstantPopup)
        self.protocol = protocol
        self.loop_step_configuration_widget = None

        self.add_actions = []
        self.device_actions = []
        self.is_accepted = False

        self.item_model_sequence = QStandardItemModel(0, 1)
        self.treeView_protocol_sequence = drag_drop_tree_view.Drag_Drop_TreeView()
        self.treeView_protocol_sequence.del_clicked.connect(self.remove_loop_step)
        self.sequence_main_widget.layout().addWidget(
            self.treeView_protocol_sequence, 5, 0, 1, 3
        )
        self.treeView_protocol_sequence.setModel(self.item_model_sequence)
        self.treeView_protocol_sequence.customContextMenuRequested.connect(
            self.sequence_right_click
        )
        self.treeView_protocol_sequence.dragdrop.connect(self.update_loop_step_order)

        self.pushButton_move_step_up.clicked.connect(
            lambda state: self.move_loop_step(-1, 0)
        )
        self.pushButton_move_step_down.clicked.connect(
            lambda state: self.move_loop_step(1, 0)
        )
        self.pushButton_move_step_in.clicked.connect(
            lambda state: self.move_loop_step(0, 1)
        )
        self.pushButton_move_step_out.clicked.connect(
            lambda state: self.move_loop_step(0, -1)
        )
        self.treeView_protocol_sequence.clicked.connect(
            lambda x: self.tree_click_sequence()
        )
        self.pushButton_remove_step.clicked.connect(
            lambda x: self.remove_loop_step(True)
        )
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

        QShortcut(
            "Ctrl+x", self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut
        ).activated.connect(self.cut_shortcut)
        QShortcut(
            "Ctrl+v", self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut
        ).activated.connect(self.paste_shortcut)
        QShortcut(
            "Ctrl+c", self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut
        ).activated.connect(self.copy_shortcut)
        QShortcut(
            "Ctrl+k", self.sequence_main_widget, context=Qt.WidgetWithChildrenShortcut
        ).activated.connect(self.comment_shortcut)

        self.build_protocol_sequence()
        self.check_movability()

    def update_add_step_actions(self):
        """Called when the devices change, updating the possible
        loopsteps to include new device steps.

        Parameters
        ----------

        Returns
        -------

        """
        self.add_actions.clear()
        self.device_actions.clear()
        for stp in sorted(
            make_step_of_type.step_type_config.keys(),
            key=lambda x: loop_step_display_order.index(x),
        ):
            action = QAction(stp)
            action.triggered.connect(lambda state=None, x=stp: self.add_loop_step(x))
            self.add_actions.append(action)
        for stp in make_step_of_type.get_device_steps():
            action = QAction(stp)
            action.triggered.connect(lambda state=None, x=stp: self.add_loop_step(x))
            self.device_actions.append(action)
        self.toolButton_add_step.addActions(self.add_actions)
        if self.device_actions:
            self.toolButton_add_step.addActions(self.device_actions)

    def tree_click_sequence(self):
        """Called when clicking the treeView_protocol_sequence."""
        self.update_loop_step_order()
        self.get_step_config()
        self.protocol.update_variables()
        self.configuration_main_widget.setHidden(False)
        config = None
        index = self.treeView_protocol_sequence.selectedIndexes()
        if not index:
            return
        index = index[0]
        dat = self.item_model_sequence.itemFromIndex(index).data()
        if dat is not None:
            step = self.protocol.loop_step_dict[dat]
            config = make_step_of_type.get_config(step)
            enable = step.step_type not in make_step_of_type.non_addables
            self.enable_step_move(enable)
            self.label_configuration.setText(f"Configuration: {step.full_name}")
        if config is not None:
            if self.loop_step_configuration_widget is not None:
                self.configuration_main_widget.layout().removeWidget(
                    self.loop_step_configuration_widget
                )
                self.loop_step_configuration_widget.deleteLater()
            self.loop_step_configuration_widget = config
            self.configuration_main_widget.layout().addWidget(
                self.loop_step_configuration_widget, 1, 0
            )
            self.loop_step_configuration_widget.name_changed.connect(
                self.change_step_name
            )
            self.loop_step_configuration_widget.active_changed.connect(
                self.change_step_name
            )
        self.check_movability()

    def build_protocol_sequence(self):
        """Shows / builds the protocol sequence in the treeView
        dependent on the loop_steps in the current_protocol.

        Parameters
        ----------

        Returns
        -------

        """
        ind_seq = self.treeView_protocol_sequence.selectedIndexes()
        sel_data = ""
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
            new_index = treeView_functions.getItemIndex(
                self.item_model_sequence, sel_data
            )
            if new_index:
                self.treeView_protocol_sequence.selectionModel().select(
                    new_index, QItemSelectionModel.Select
                )

    def enable_step_move(self, enable):
        """

        Parameters
        ----------
        enable :


        Returns
        -------

        """
        self.pushButton_move_step_in.setEnabled(enable)
        self.pushButton_move_step_out.setEnabled(enable)
        self.pushButton_move_step_up.setEnabled(enable)
        self.pushButton_move_step_down.setEnabled(enable)

    def change_step_name(self):
        """Called when a loop_step changes its name, then updates the
        shown sequence, and also the protocol-data.

        Parameters
        ----------

        Returns
        -------

        """
        self.build_protocol_sequence()
        self.update_loop_step_order()

    def get_step_config(self):
        """Updates the data in the currently-to-configure loop_step."""
        if self.loop_step_configuration_widget is not None:
            self.loop_step_configuration_widget.update_step_config()

    def sequence_right_click(self, pos):
        """Opens a specific Menu on right click in the protocol-sequence.
        If selection is not on a loop_step, it consists only of Add Step,
        otherwise it consists of Delete Step.

        Parameters
        ----------
        pos :


        Returns
        -------

        """
        # TODO other actions
        # TODO more beautiful?
        menu = QMenu()
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if inds:
            item = self.item_model_sequence.itemFromIndex(inds[0])
            below_actions = []
            above_actions = []
            into_actions = []
            replace_actions = []
            row = inds[0].row()
            parent = item.parent()
            if parent is not None:
                parent = parent.data()
            for stp in sorted(
                make_step_of_type.step_type_config.keys(),
                key=lambda x: loop_step_display_order.index(x),
            ):
                action = QAction(stp)
                action_a = QAction(stp)
                action_in = QAction(stp)
                action.triggered.connect(
                    lambda state=None, x=stp, y=row + 1, z=parent: self.add_loop_step(
                        x, y, z
                    )
                )
                action_a.triggered.connect(
                    lambda state=None, x=stp, y=row, z=parent: self.add_loop_step(
                        x, y, z
                    )
                )
                action_in.triggered.connect(
                    lambda state=None, x=stp, y=-1, z=item.data(): self.add_loop_step(
                        x, y, z
                    )
                )
                below_actions.append(action)
                above_actions.append(action_a)
                into_actions.append(action_in)
                if (
                    not self.protocol.loop_step_dict[item.data()].has_children
                    or not self.protocol.loop_step_dict[item.data()].children
                    or stp in make_step_of_type.steps_with_children
                ):
                    action_replace = QAction(stp)
                    action_replace.triggered.connect(
                        lambda state=None, x=stp, y=row, z=parent: self.replace_loop_step(
                            x, y, z
                        )
                    )
                    replace_actions.append(action_replace)
            device_actions = []
            device_actions_a = []
            device_actions_in = []
            for stp in make_step_of_type.get_device_steps():
                action = QAction(stp)
                action_a = QAction(stp)
                action_in = QAction(stp)
                action.triggered.connect(
                    lambda state=None, x=stp, y=row + 1, z=parent: self.add_loop_step(
                        x, y, z
                    )
                )
                action_a.triggered.connect(
                    lambda state=None, x=stp, y=row, z=parent: self.add_loop_step(
                        x, y, z
                    )
                )
                action_in.triggered.connect(
                    lambda state=None, x=stp, y=-1, z=item.data(): self.add_loop_step(
                        x, y, z
                    )
                )
                device_actions.append(action)
                device_actions_a.append(action_a)
                device_actions_in.append(action_in)

            # -------------- Above actions -----------------------------
            insert_above_menu = QMenu("Insert Above")
            insert_above_menu_channels = QMenu("Channels")
            insert_above_menu_loops = QMenu("Loops")
            insert_above_menu_additional = QMenu("Additional")
            # Filter out specific steps with a list of the .text of the QAction and then remove them from the list
            duplicate_actions = above_actions[:]
            for action in above_actions:
                if action.text() in channel_action_list:
                    insert_above_menu_channels.addAction(action)
                    # Remove from the list
                    duplicate_actions.remove(action)
                elif action.text() in loop_action_list:
                    insert_above_menu_loops.addAction(action)
                    # Remove from the list
                    duplicate_actions.remove(action)
                elif action.text() in additional_action_list:
                    insert_above_menu_additional.addAction(action)
                    # Remove from the list
                    duplicate_actions.remove(action)
            insert_above_menu.addMenu(insert_above_menu_channels)
            insert_above_menu.addMenu(insert_above_menu_loops)
            if len(duplicate_actions) > 0:
                insert_above_menu.addActions(duplicate_actions)
            insert_above_menu.addMenu(insert_above_menu_additional)

            # -------------- Below actions -----------------------------
            insert_below_menu = QMenu("Insert Below")
            insert_below_menu_channels = QMenu("Channels")
            insert_below_menu_loops = QMenu("Loops")
            insert_below_menu_additional = QMenu("Additional")
            # Filter out specific steps with a list of the .text of the QAction and then remove them from the list for the below menu
            duplicate_actions = below_actions[:]
            for action in below_actions:
                if action.text() in channel_action_list:
                    insert_below_menu_channels.addAction(action)
                    # Remove from the list
                    duplicate_actions.remove(action)
                elif action.text() in loop_action_list:
                    insert_below_menu_loops.addAction(action)
                    # Remove from the list
                    duplicate_actions.remove(action)
                elif action.text() in additional_action_list:
                    insert_below_menu_additional.addAction(action)
                    # Remove from the list
                    duplicate_actions.remove(action)
            insert_below_menu.addMenu(insert_below_menu_channels)
            insert_below_menu.addMenu(insert_below_menu_loops)
            if len(duplicate_actions) > 0:
                insert_below_menu.addActions(duplicate_actions)
            insert_below_menu.addMenu(insert_below_menu_additional)
            # -------------- Add in actions -----------------------------
            # insert_below_menu.addActions(below_actions)
            if device_actions:
                insert_above_menu.addSeparator()
                insert_above_menu.addActions(device_actions_a)
                insert_below_menu.addSeparator()
                insert_below_menu.addActions(device_actions)
            if self.protocol.loop_step_dict[item.data()].has_children:
                add_in_menu = QMenu("Add Into")
                add_in_menu_channels = QMenu("Channels")
                add_in_menu_loops = QMenu("Loops")
                add_in_menu_additional = QMenu("Additional")
                # Filter out specific steps with a list of the .text of the QAction and then remove them from the list
                duplicate_actions = into_actions[:]
                for action in into_actions:
                    if action.text() in channel_action_list:
                        add_in_menu_channels.addAction(action)
                        # Remove from the list
                        duplicate_actions.remove(action)
                    elif action.text() in loop_action_list:
                        add_in_menu_loops.addAction(action)
                        # Remove from the list
                        duplicate_actions.remove(action)
                    elif action.text() in additional_action_list:
                        add_in_menu_additional.addAction(action)
                        # Remove from the list
                        duplicate_actions.remove(action)
                add_in_menu.addMenu(add_in_menu_channels)
                add_in_menu.addMenu(add_in_menu_loops)
                if len(duplicate_actions) > 0:
                    add_in_menu.addActions(duplicate_actions)
                add_in_menu.addMenu(add_in_menu_additional)
                menu.addMenu(add_in_menu)
                if device_actions:
                    add_in_menu.addSeparator()
                    add_in_menu.addActions(device_actions_in)
            replace_menu = QMenu("Replace with")
            replace_menu.addActions(replace_actions)
            menu.addMenu(insert_above_menu)
            menu.addMenu(insert_below_menu)
            menu.addMenu(replace_menu)
            menu.addSeparator()
            cut_action = QAction("Cut\tCtrl + X")
            cut_action.triggered.connect(
                lambda state=None, x=item.data(): self.cut_loop_step(x)
            )
            copy_action = QAction("Copy\tCtrl + C")
            copy_action.triggered.connect(
                lambda state=None, x=item.data(): self.copy_loop_step(x)
            )
            paste_menu = QMenu("Paste\tCtrl + V")
            if variables_handling.copied_step is not None:
                paste_above = QAction("Paste Above")
                paste_above.triggered.connect(
                    lambda state=None, x=True, y=row, z=parent: self.add_loop_step(
                        copied_step=x, position=y, parent=z
                    )
                )
                paste_below = QAction("Paste Below")
                paste_below.triggered.connect(
                    lambda state=None, x=True, y=row + 1, z=parent: self.add_loop_step(
                        copied_step=x, position=y, parent=z
                    )
                )
                if self.protocol.loop_step_dict[item.data()].has_children:
                    paste_into = QAction("Paste Into")
                    paste_into.triggered.connect(
                        lambda state=None, x=True, y=-1, z=item.data(): self.add_loop_step(
                            copied_step=x, position=y, parent=z
                        )
                    )
                    paste_menu.addAction(paste_into)
                paste_menu.addActions([paste_above, paste_below])
            else:
                paste_menu.setEnabled(False)
            menu.addAction(cut_action)
            menu.addAction(copy_action)
            menu.addMenu(paste_menu)
            if (
                self.protocol.loop_step_dict[item.data()].step_type
                not in make_step_of_type.non_addables
            ):
                del_action = QAction("Delete Step\tDel")
                del_action.triggered.connect(lambda x: self.remove_loop_step(True))
                menu.addAction(del_action)
            menu.addSeparator()
            if item.text().startswith("# "):
                comment_action = QAction("Enable step\tCtrl + K")
            else:
                comment_action = QAction("Disable step\tCtrl + K")
            comment_action.triggered.connect(
                lambda state=None, x=item.data(): self.comment_loop_step(x)
            )
            menu.addAction(comment_action)
        else:
            add_actions = []
            for stp in sorted(
                make_step_of_type.step_type_config,
                key=lambda x: loop_step_display_order.index(x),
            ):
                action = QAction(stp)
                action.triggered.connect(
                    lambda state=None, x=stp: self.add_loop_step(x)
                )
                add_actions.append(action)
            device_actions = []
            for stp in make_step_of_type.get_device_steps():
                action = QAction(stp)
                action.triggered.connect(
                    lambda state=None, x=stp: self.add_loop_step(x)
                )
                device_actions.append(action)
            add_menu = QMenu("Add Step")
            add_menu.addActions(add_actions)
            if device_actions:
                add_menu.addSeparator()
                add_menu.addActions(device_actions)
            paste_action = QAction("Paste")
            if variables_handling.copied_step is not None:
                paste_action.triggered.connect(
                    lambda state=None, x=True, y=-1, z=None: self.add_loop_step(
                        copied_step=x, position=y, parent=z
                    )
                )
            else:
                paste_action.setEnabled(False)
            menu.addMenu(add_menu)
            menu.addAction(paste_action)
        menu.exec_(self.treeView_protocol_sequence.viewport().mapToGlobal(pos))

    def paste_shortcut(self):
        """ """
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
                if item.parent():
                    parent = item.parent().data()
                else:
                    parent = None
        else:
            pos = -1
            parent = None
        self.add_loop_step(copied_step=True, position=pos, parent=parent)

    def cut_shortcut(self):
        """ """
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if not inds:
            return
        item = self.item_model_sequence.itemFromIndex(inds[0])
        self.cut_loop_step(item.data())

    def copy_shortcut(self):
        """ """
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if not inds:
            return
        item = self.item_model_sequence.itemFromIndex(inds[0])
        self.copy_loop_step(item.data())

    def comment_shortcut(self):
        inds = self.treeView_protocol_sequence.selectedIndexes()
        if not inds:
            return
        item = self.item_model_sequence.itemFromIndex(inds[0])
        self.comment_loop_step(item.data())

    def cut_loop_step(self, step_name):
        """Copies the given step, then removes it.

        Parameters
        ----------
        step_name :


        Returns
        -------

        """
        self.copy_loop_step(step_name)
        self.remove_loop_step(ask=False)

    def copy_loop_step(self, step_name):
        """Makes a deepcopy of the given step and stores it in
        copied_loop_step.

        Parameters
        ----------
        step_name :


        Returns
        -------

        """
        variables_handling.copied_step = deepcopy(
            self.protocol.loop_step_dict[step_name]
        )

    def check_movability(self):
        """ """
        ind = self.treeView_protocol_sequence.selectedIndexes()
        if not ind:
            self.enable_step_move(False)
            self.pushButton_remove_step.setEnabled(False)
            return
        ind = ind[0]
        item = self.item_model_sequence.itemFromIndex(ind)
        self.pushButton_remove_step.setEnabled(True)
        parent = item.parent()
        if ind.row() > 0:
            self.pushButton_move_step_up.setEnabled(True)
            if parent is not None:
                above = parent.child(ind.row() - 1, 0)
            else:
                above = self.item_model_sequence.item(ind.row() - 1, 0)
            self.pushButton_move_step_in.setEnabled(True)
            if above is not None:
                step = self.protocol.loop_step_dict[above.data()]
                if step.step_type == "If":
                    above = above.child(above.rowCount() - 1, 0)
                if not self.protocol.loop_step_dict[above.data()].has_children:
                    self.pushButton_move_step_in.setEnabled(False)
        else:
            self.pushButton_move_step_up.setEnabled(False)
            self.pushButton_move_step_in.setEnabled(False)
        if ind.row() < self.item_model_sequence.rowCount() - 1:
            self.pushButton_move_step_down.setEnabled(True)
        else:
            self.pushButton_move_step_down.setEnabled(False)
        if parent is None:
            self.pushButton_move_step_out.setEnabled(False)
        else:
            self.pushButton_move_step_out.setEnabled(True)

    def move_loop_step(self, up_down=0, in_out=0):
        """Moves a loop_step up or down in the sequence. It can also be
        moved in or out (into the loop_step above, it if accepts children).

        Parameters
        ----------
        up_down :
             (Default value = 0)
        in_out :
             (Default value = 0)

        Returns
        -------


        """
        move_command = change_sequence.CommandMoveStep(
            self.treeView_protocol_sequence,
            self.item_model_sequence,
            up_down,
            in_out,
            self.protocol.loop_step_dict,
            self.update_loop_step_order,
        )
        self.undo_stack.push(move_command)
        self.tree_click_sequence()

    def comment_loop_step(self, step_name):
        step = self.protocol.loop_step_dict[step_name]
        step.is_active = not step.is_active
        self.build_protocol_sequence()

    def add_loop_step(self, step_type="", position=-1, parent=None, copied_step=False):
        """Add a loop_step of given step_type. Updates the current
        sequence into the protocol, then initializes the new step.

        Parameters
        ----------
        step_type :
             (Default value = '')
        position :
             (Default value = -1)
        parent :
             (Default value = None)
        copied_step :
             (Default value = False)

        Returns
        -------
        step : Loop_Step
            the newly added loop_step

        """

        self.update_loop_step_order()
        if copied_step:
            step = variables_handling.copied_step
        else:
            step = make_step_of_type.make_step(step_type, protocol=self.protocol)
        self.protocol.add_loop_step_rec(
            step,
            model=self.item_model_sequence,
            position=position,
            parent_step_name=parent,
        )
        self.build_protocol_sequence()
        if copied_step:
            self.copy_loop_step(variables_handling.copied_step.full_name)
        new_ind = treeView_functions.getItemIndex(
            self.item_model_sequence, step.full_name
        )
        self.treeView_protocol_sequence.selectionModel().select(
            new_ind, QItemSelectionModel.Select
        )
        self.tree_click_sequence()
        return step

    def remove_loop_step(self, ask=True):
        """After updating the loop_step order in the protocol, the
        selected loop step is deleted (if the messagebox is accepted).

        Parameters
        ----------
        ask :
             (Default value = True)

        Returns
        -------

        """
        self.update_loop_step_order()
        ind = self.treeView_protocol_sequence.selectedIndexes()[0]
        name = self.item_model_sequence.itemFromIndex(ind).data()
        if name is not None:
            remove_dialog = None
            if (
                self.protocol.loop_step_dict[name].step_type
                in make_step_of_type.non_addables
            ):
                return
            if ask:
                remove_dialog = QMessageBox.question(
                    self,
                    "Delete Step?",
                    f"Are you sure you want to delete the step {name}?",
                    QMessageBox.Yes | QMessageBox.No,
                )
            if not ask or remove_dialog == QMessageBox.Yes:
                self.protocol.remove_loop_step(name)
                self.build_protocol_sequence()
                self.check_movability()

    def replace_loop_step(self, step_type="", position=-1, parent=None):
        """ """
        ind = self.treeView_protocol_sequence.selectedIndexes()[0]
        children_names = treeView_functions.get_substeps(
            self.item_model_sequence.itemFromIndex(ind)
        )
        children_steps = []
        for child in children_names:
            children_steps.append(self.protocol.loop_step_dict[child[0]])
        self.remove_loop_step(ask=False)
        step = self.add_loop_step(step_type, position, parent)
        step.children = children_steps
        self.build_protocol_sequence()

    def update_loop_step_order(self):
        """Goes through all the loop_steps in the sequence, then
        rearranges them in the protocol.

        Parameters
        ----------

        Returns
        -------

        """
        self.general_settings.update_step_config()
        loop_steps = []
        for i in range(self.item_model_sequence.rowCount()):
            item = self.item_model_sequence.item(i, 0)
            sub_steps = treeView_functions.get_substeps(item)
            loop_steps.append((item.data(), sub_steps))
        self.protocol.rearrange_loop_steps(loop_steps)

    def accept(self) -> None:
        """ """
        self.update_loop_step_order()
        self.get_step_config()
        self.check_protocol_name()
        self.check_file_name()
        self.accepted.emit(self.protocol)
        self.is_accepted = True
        self.close()

    def check_file_name(self):
        """check if the filename contains any characters that might cause problems"""
        name = self.general_settings.lineEdit_filename.text()
        invalid_characters = [
            "/",
            "\\",
            ":",
            "*",
            "?",
            '"',
            "<",
            ">",
            "|",
            "+",
            "%",
            "&",
            "#",
            "@",
            "!",
            "$",
            "^",
            "`",
            "~",
        ]
        invals = []
        for char in invalid_characters:
            if char in name:
                invals.append(char)
        if invals:
            raise Exception(
                f"Filename contains invalid characters:\n{' '.join(invals)}"
            )

    def check_protocol_name(self):
        """ """
        name = self.general_settings.lineEdit_protocol_name.text()
        if name in variables_handling.protocols and name != self.old_name:
            raise Exception(f'Protocol name "{name}" already in use!')
        variables_handling.check_variable_name(name, True, self)

    def closeEvent(self, a0: QCloseEvent) -> None:
        """

        Parameters
        ----------
        a0: QCloseEvent :


        Returns
        -------

        """
        name = self.general_settings.lineEdit_protocol_name.text()
        if not self.is_accepted:
            discard_dialog = QMessageBox.question(
                self,
                f"{name} - Discard Changes?",
                f"All changes to {name} will be lost!",
                QMessageBox.Yes | QMessageBox.No,
            )
            if discard_dialog != QMessageBox.Yes:
                a0.ignore()
                return
        a0.accept()
        super().closeEvent(a0)
        self.closing.emit()

    def change_name(self):
        """ """
        self.setWindowTitle(
            f"{self.protocol.name} - Measurement Protocol - NOMAD CAMELS"
        )

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return.

        Parameters
        ----------
        a0: QKeyEvent :


        Returns
        -------

        """
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widge = Protocol_Config()
    widge.show()
    sys.exit(app.exec())
