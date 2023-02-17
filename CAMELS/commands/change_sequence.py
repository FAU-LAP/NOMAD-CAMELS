from PyQt5.QtWidgets import QUndoCommand
from PyQt5.QtCore import QItemSelectionModel

class CommandMoveStep(QUndoCommand):
    def __init__(self, treeView, item_model, up_down, in_out, loop_step_dict, update_func):
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
        parent = self.item.parent()
        if parent is None:
            if self.up_down != 0 and (self.ind.row() > 0 or self.up_down > 0) and (self.ind.row() < self.item_model_sequence.rowCount()-1 or self.up_down < 0):
                row = self.item_model_sequence.takeRow(self.ind.row())
                self.item_model_sequence.insertRow(self.ind.row() + self.up_down, row)
            elif self.in_out > 0 and self.ind.row() > 0:
                above = self.item_model_sequence.item(self.ind.row()-1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = self.item_model_sequence.takeRow(self.ind.row())
                    above.insertRow(above.rowCount(), row)
        else:
            if self.up_down != 0 and (self.ind.row() > 0 or self.up_down > 0) and (self.ind.row() < parent.rowCount()-1 or self.up_down < 0):
                row = parent.takeRow(self.ind.row())
                parent.insertRow(self.ind.row() + self.up_down, row)
            elif self.in_out > 0 and self.ind.row() > 0:
                above = parent.child(self.ind.row()-1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = parent.takeRow(self.ind.row())
                    above.insertRow(above.rowCount(), row)
            elif self.in_out < 0:
                grandparent = parent.parent()
                if grandparent is None:
                    grandparent = self.item_model_sequence
                parent_row = parent.index().row()
                row = parent.takeRow(self.ind.row())
                grandparent.insertRow(parent_row+1, row)
        self.treeView_protocol_sequence.clearSelection()
        new_ind = self.item_model_sequence.indexFromItem(self.item)
        self.treeView_protocol_sequence.selectionModel().select(new_ind, QItemSelectionModel.Select)
        self.update_func()

    def undo(self):
        parent = self.item.parent()
        up_down = - self.up_down
        in_out = - self.in_out
        ind = self.item_model_sequence.indexFromItem(self.item)
        if parent is None:
            if up_down != 0 and (ind.row() > 0 or up_down > 0) and (ind.row() < self.item_model_sequence.rowCount()-1 or up_down < 0):
                row = self.item_model_sequence.takeRow(ind.row())
                self.item_model_sequence.insertRow(ind.row() + up_down, row)
            elif in_out > 0 and ind.row() > 0:
                above = self.item_model_sequence.item(ind.row()-1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = self.item_model_sequence.takeRow(ind.row())
                    above.insertRow(above.rowCount(), row)
        else:
            if up_down != 0 and (ind.row() > 0 or up_down > 0) and (ind.row() < parent.rowCount()-1 or up_down < 0):
                row = parent.takeRow(ind.row())
                parent.insertRow(ind.row() + up_down, row)
            elif in_out > 0 and ind.row() > 0:
                above = parent.child(ind.row()-1, 0)
                if self.loop_step_dict[above.data()].has_children:
                    row = parent.takeRow(ind.row())
                    above.insertRow(above.rowCount(), row)
            elif in_out < 0:
                grandparent = parent.parent()
                if grandparent is None:
                    grandparent = self.item_model_sequence
                parent_row = parent.index().row()
                row = parent.takeRow(ind.row())
                grandparent.insertRow(parent_row+1, row)
        self.treeView_protocol_sequence.clearSelection()
        new_ind = self.item_model_sequence.indexFromItem(self.item)
        self.treeView_protocol_sequence.selectionModel().select(new_ind, QItemSelectionModel.Select)
        self.update_func()