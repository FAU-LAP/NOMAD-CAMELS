import numpy as np

from bluesky.callbacks.mpl_plotting import QtAwareCallback

from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QGridLayout
from PySide6.QtCore import Qt, QEvent, QObject
from PySide6.QtGui import QIcon

from nomad_camels.bluesky_handling.evaluation_helper import Evaluator

from nomad_camels.utility.plot_placement import place_widget
from pkg_resources import resource_filename

from PySide6.QtCore import Signal as pySignal


class Values_List_Plot(QWidget):
    """ """
    closing = pySignal()

    def __init__(self, value_list, *, epoch='run', namespace=None, title='',
                 stream_name='primary', parent=None, **kwargs):
        super().__init__(parent=parent)
        self.table = QTableWidget()
        self.livePlot = Live_List(value_list, epoch=epoch,
                                  namespace=namespace,
                                  stream_name=stream_name, parent=self,
                                  table=self.table, **kwargs)
        self.livePlot.new_data.connect(self.show)

        layout = QGridLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle(title or f'{value_list[0]} ...')
        self.setWindowIcon(QIcon(resource_filename('nomad_camels', 'graphics/camels_icon.png')))
        self.stream_name = stream_name
        place_widget(self)

    def clear_plot(self):
        pass

    def autoscale(self):
        pass

    def closeEvent(self, a0):
        """

        Parameters
        ----------
        a0 :


        Returns
        -------

        """
        self.closing.emit()
        super().closeEvent(a0)




class Live_List(QtAwareCallback, QObject):
    new_data = pySignal()

    def __init__(self, value_list, table, *, epoch='run', namespace=None,
                 stream_name='primary', parent=None, **kwargs):
        QObject.__init__(self, parent=parent)
        QtAwareCallback.__init__(self, use_teleporter=kwargs.pop('use_teleporter', None))
        if isinstance(value_list, str):
            value_list = [value_list]
        self.value_list = value_list
        self.stream_name = stream_name
        self.table = table
        self.eva = Evaluator(namespace=namespace)

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
        self.desc = ''
        self.epoch_offset = 0
        self.epoch = epoch
        self.table.resizeColumnsToContents()

    def descriptor(self, doc):
        """

        Parameters
        ----------
        doc :
            

        Returns
        -------

        """
        if doc['name'] == self.stream_name:
            self.desc = doc['uid']

    def start(self, doc):
        """

        Parameters
        ----------
        doc :
            

        Returns
        -------

        """
        self.epoch_offset = doc['time']
        super().start(doc)

    def event(self, doc):
        """

        Parameters
        ----------
        doc :
            

        Returns
        -------

        """
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
        self.new_data.emit(None)