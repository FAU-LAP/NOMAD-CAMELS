from PySide6.QtCore import QItemSelectionModel
from PySide6.QtGui import QUndoCommand


class CommandMoveStep(QUndoCommand):
    """
    Using a command for moving a step inside the protocol treeView to be able to
    reverse the action.

    Parameters
    ----------
    treeView : QTreeView
        The TreeView displaying the protocol sequence
    item_model : QStandardItemModel
        The treeview's item model
    up_down : int
        The direction in which to move the step, if positive it moves down, if
        negative it moves up.
    in_out : int
        The step is moved into the step above it, if positive, if negative it is
        moved out one layer.
    loop_step_dict : dict
        The dictionary of the loopsteps, used to find the parent steps
    update_func : function
        This function is called, when the command is finished, usually used to
        update the order of the steps in the protocol data.
    """

    def __init__(
        self, treeView, item_model, up_down, in_out, loop_step_dict, update_func
    ):
        super().__init__()
        self.treeView_protocol_sequence = treeView
        self.item_model_sequence = item_model
        self.up_down = up_down
        self.in_out = in_out
        self.loop_step_dict = loop_step_dict
        self.ind = self.treeView_protocol_sequence.selectedIndexes()[0]
        self.item = self.item_model_sequence.itemFromIndex(self.ind)
        self.update_func = update_func

    def redo(self):
        """Performs moving the step."""
        parent = self.item.parent()
        if parent is None:
            if (
                self.up_down != 0
                and (self.ind.row() > 0 or self.up_down > 0)
                and (
                    self.ind.row() < self.item_model_sequence.rowCount() - 1
                    or self.up_down < 0
                )
            ):
                row = self.item_model_sequence.takeRow(self.ind.row())
                self.item_model_sequence.insertRow(self.ind.row() + self.up_down, row)
            elif self.in_out > 0 and self.ind.row() > 0:
                above = self.item_model_sequence.item(self.ind.row() - 1, 0)
                step = self.loop_step_dict[above.data()]
                if step.step_type == "If":
                    above = above.child(above.rowCount() - 1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = self.item_model_sequence.takeRow(self.ind.row())
                    above.insertRow(above.rowCount(), row)
        else:
            if (
                self.up_down != 0
                and (self.ind.row() > 0 or self.up_down > 0)
                and (self.ind.row() < parent.rowCount() - 1 or self.up_down < 0)
            ):
                row = parent.takeRow(self.ind.row())
                parent.insertRow(self.ind.row() + self.up_down, row)
            elif self.in_out > 0 and self.ind.row() > 0:
                above = parent.child(self.ind.row() - 1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = parent.takeRow(self.ind.row())
                    above.insertRow(above.rowCount(), row)
            elif self.in_out < 0:
                grandparent = parent.parent()
                if grandparent is None:
                    grandparent = self.item_model_sequence
                parent_row = parent.index().row()
                row = parent.takeRow(self.ind.row())
                grandparent.insertRow(parent_row + 1, row)
        self.treeView_protocol_sequence.clearSelection()
        new_ind = self.item_model_sequence.indexFromItem(self.item)
        self.treeView_protocol_sequence.selectionModel().select(
            new_ind, QItemSelectionModel.Select
        )
        self.update_func()

    def undo(self):
        """Moves the step back to its original position."""
        parent = self.item.parent()
        up_down = -self.up_down
        in_out = -self.in_out
        ind = self.item_model_sequence.indexFromItem(self.item)
        if parent is None:
            if (
                up_down != 0
                and (ind.row() > 0 or up_down > 0)
                and (ind.row() < self.item_model_sequence.rowCount() - 1 or up_down < 0)
            ):
                row = self.item_model_sequence.takeRow(ind.row())
                self.item_model_sequence.insertRow(ind.row() + up_down, row)
            elif in_out > 0 and ind.row() > 0:
                above = self.item_model_sequence.item(ind.row() - 1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = self.item_model_sequence.takeRow(ind.row())
                    above.insertRow(above.rowCount(), row)
        else:
            if (
                up_down != 0
                and (ind.row() > 0 or up_down > 0)
                and (ind.row() < parent.rowCount() - 1 or up_down < 0)
            ):
                row = parent.takeRow(ind.row())
                parent.insertRow(ind.row() + up_down, row)
            elif in_out > 0 and ind.row() > 0:
                above = parent.child(ind.row() - 1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = parent.takeRow(ind.row())
                    above.insertRow(above.rowCount(), row)
            elif in_out < 0:
                grandparent = parent.parent()
                if grandparent is None:
                    grandparent = self.item_model_sequence
                parent_row = parent.index().row()
                row = parent.takeRow(ind.row())
                grandparent.insertRow(parent_row + 1, row)
        self.treeView_protocol_sequence.clearSelection()
        new_ind = self.item_model_sequence.indexFromItem(self.item)
        self.treeView_protocol_sequence.selectionModel().select(
            new_ind, QItemSelectionModel.Select
        )
        self.update_func()
