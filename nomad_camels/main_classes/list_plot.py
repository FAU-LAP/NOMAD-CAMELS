import logging
import numpy as np

from bluesky.callbacks.core import CallbackBase

from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QGridLayout
from PySide6.QtCore import Qt, QEvent, QObject
from PySide6.QtGui import QIcon

from nomad_camels.bluesky_handling.evaluation_helper import Evaluator

from nomad_camels.utility.plot_placement import place_widget
from importlib import resources
from nomad_camels import graphics

from PySide6.QtCore import Signal as pySignal


class Values_List_Plot(QWidget):
    """ """

    closing = pySignal()
    reopened = pySignal()

    def __init__(
        self,
        value_list,
        *,
        epoch="run",
        namespace=None,
        title="",
        stream_name="primary",
        parent=None,
        plot_all_available=True,
        top_left_x=None,
        top_left_y=None,
        plot_width=None,
        plot_height=None,
        **kwargs,
    ):
        super().__init__(parent=parent)
        self.table = QTableWidget()
        self.livePlot = Live_List(
            value_list,
            epoch=epoch,
            namespace=namespace,
            stream_name=stream_name,
            parent=self,
            table=self.table,
            plot_all_available=plot_all_available,
            **kwargs,
        )
        self.livePlot.new_data.connect(self.show_again)

        layout = QGridLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        if title:
            self.setWindowTitle(title)
        elif value_list:
            self.setWindowTitle(f"{value_list[0]} ...")
        else:
            self.setWindowTitle("Current Value List")
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "CAMELS_Icon.png")))
        self.stream_name = stream_name
        place_widget(self, top_left_x, top_left_y, plot_width, plot_height)

    def show_again(self):
        if not self.isVisible():
            self.show()
            self.reopened.emit()

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


class Teleporter(QObject):
    name_doc_escape = pySignal(str, dict, object)


def handle_teleport(name, doc, obj):
    obj(name, doc, escape=True)


class Live_List(QObject, CallbackBase):
    new_data = pySignal()

    def __init__(
        self,
        value_list,
        table,
        *,
        epoch="run",
        namespace=None,
        stream_name="primary",
        parent=None,
        plot_all_available=False,
        **kwargs,
    ):
        CallbackBase.__init__(self)
        QObject.__init__(self)
        self.__teleporter = Teleporter()
        self.__teleporter.name_doc_escape.connect(handle_teleport)
        if isinstance(value_list, str):
            value_list = [value_list]
        self.value_list = value_list
        self.stream_name = stream_name
        self.table = table
        self.plot_all_available = plot_all_available
        self.eva = Evaluator(namespace=namespace)
        self.multi_stream = kwargs.get("multi_stream", False)

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
        self.add_items = {}
        self.desc = []
        self.epoch_offset = 0
        self.epoch = epoch
        self.table.resizeColumnsToContents()

    def add_to_table(self, name):
        i = len(self.val_items) + len(self.add_items)
        self.table.setRowCount(i + 1)
        item = QTableWidgetItem(name)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(i, 0, item)
        item = QTableWidgetItem(str(np.nan))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(i, 1, item)
        self.add_items[name] = item

    def descriptor(self, doc):
        """

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        if doc["name"] == self.stream_name:
            self.desc.append(doc["uid"])
        elif (
            self.multi_stream
            and doc["name"].startswith(self.stream_name)
            and not doc["name"][len(self.stream_name) :].startswith(
                "||subprotocol_stream||"
            )
            # check if the next part of the string after self.stream name is `||sub_stream||`,
            # if so it is a sub-stream inside a subprotocol and should be ignored
        ):
            self.desc.append(doc["uid"])

    def start(self, doc):
        """

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        self.epoch_offset = doc["time"]
        super().start(doc)
        self.eva.start(doc)

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
        if doc["descriptor"] not in self.desc:
            return

        for i, val in enumerate(self.value_list):
            if val == "time":
                new_val = doc["time"]
                if self.epoch == "run":
                    new_val -= self.epoch_offset
            else:
                try:
                    new_val = doc["data"][val]
                except KeyError:
                    if not self.eva.is_to_date(doc["time"]):
                        self.eva.event(doc)
                    try:
                        new_val = self.eva.eval(val)
                    except ValueError:
                        new_val = np.nan
                        logging.error(
                            f'Could not evaluate value "{val}" in Current Values Plot.'
                        )
            if isinstance(new_val, (int, float)):
                self.val_items[i].setText(f"{new_val:7e}")
            else:
                self.val_items[i].setText(str(new_val))
        if self.plot_all_available:
            for name, value in doc["data"].items():
                if name in self.value_list:
                    continue
                if name not in self.add_items:
                    self.add_to_table(name)
                try:
                    self.add_items[name].setText(f"{value:7e}")
                except:
                    self.add_items[name].setText(str(value))
        self.table.resizeColumnsToContents()
        self.new_data.emit()

    def __call__(self, name, doc, *, escape=False):
        """
        The call method of the callback. This method is called when a new event is received. If `__teleporter` is set, the event is sent to the `__teleporter`, otherwise the event is processed directly. The teleporter is necessary to send the event to a different thread, since Qt objects can only be accessed from the thread they were created in.

        Parameters
        ----------
        name : str
            The name of the event
        doc : dict
            The event document
        escape : bool, (default: False)
            If True, the event is always processed directly, otherwise it is sent to the teleporter
        """
        if not escape and self.__teleporter is not None:
            self.__teleporter.name_doc_escape.emit(name, doc, self)
        else:
            return CallbackBase.__call__(self, name, doc)
