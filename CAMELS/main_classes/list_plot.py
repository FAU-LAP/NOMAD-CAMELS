import numpy as np

from bluesky.callbacks.mpl_plotting import QtAwareCallback

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QGridLayout
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon

from bluesky_handling.evaluation_helper import Evaluator

from utility.plot_placement import place_widget
from pkg_resources import resource_filename


class Values_List_Plot(QtAwareCallback, QWidget):
    def __init__(self, value_list, *, epoch='run', namespace=None, title='',
                 stream_name='primary', parent=None, **kwargs):
        QWidget.__init__(self, parent=parent)
        QtAwareCallback.__init__(self, use_teleporter=kwargs.pop('use_teleporter', None))
        layout = QGridLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        if isinstance(value_list, str):
            value_list = [value_list]
        self.value_list = value_list
        self.stream_name = stream_name
        self.eva = Evaluator(namespace=namespace)
        self.setWindowTitle(title or f'{value_list[0]} ...')

        self.table.setRowCount(len(value_list))
        self.table.setColumnCount(2)
        self.table.verticalHeader().setHidden(True)
        self.table.horizontalHeader().setHidden(True)
        self.val_items = []
        for i, val in enumerate(value_list):
            item = QTableWidgetItem(val)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 0, item)
            item = QTableWidgetItem(str(np.nan))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(i, 1, item)
            self.val_items.append(item)
        self.setWindowIcon(QIcon(resource_filename('graphics','CAMELS.svg')))
        self.desc = ''
        self.epoch_offset = 0
        self.epoch = epoch
        self.table.resizeColumnsToContents()
        place_widget(self)

    def descriptor(self, doc):
        if doc['name'] == self.stream_name:
            self.desc = doc['uid']

    def start(self, doc):
        self.epoch_offset = doc['time']
        super().start(doc)

    def event(self, doc):
        if isinstance(doc, QEvent):
            return QWidget.event(self, doc)
        if doc['descriptor'] != self.desc:
            return

        for i, val in enumerate(self.value_list):
            if val == 'time':
                new_val = doc['time']
                if self.epoch == 'run':
                    new_val -= self.epoch_offset
            else:
                try:
                    new_val = doc['data'][val]
                except KeyError:
                    if not self.eva.is_to_date(doc['time']):
                        self.eva.event(doc)
                    new_val = self.eva.eval(val)
            self.val_items[i].setText(f'{new_val:7e}')
        self.table.resizeColumnsToContents()
        self.show()
