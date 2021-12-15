from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDropEvent

from main_classes import loop_step

step_types = ['Default', 'Container']
container_types = ['Container']
def get_loop_step_from_type(step_type):
    if step_type == 'Default':
        return loop_step.Loop_Step('Default')
    elif step_type == 'Container':
        return loop_step.Loop_Step_Container('Container')
    else:
        return loop_step.Loop_Step('fail')



class Drag_Drop_TreeView(QTreeView):
    dragdrop = pyqtSignal()

    def __init__(self):
        super(Drag_Drop_TreeView, self).__init__()
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, e: QDropEvent) -> None:
        super(Drag_Drop_TreeView, self).dropEvent(e)
        self.dragdrop.emit()