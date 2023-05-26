import threading
import numpy as np

import matplotlib.pyplot as plt
from bluesky.callbacks.mpl_plotting import LiveScatter
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QIcon

from nomad_camels.bluesky_handling.evaluation_helper import Evaluator

from nomad_camels.main_classes.plot_widget import MPLwidget

from nomad_camels.utility.plot_placement import place_widget
from pkg_resources import resource_filename

stdCols = plt.rcParams['axes.prop_cycle'].by_key()['color']

class PlotWidget_2D(QWidget):
    """ """
    closing = Signal()

    def __init__(self, x_name, y_name, z_name, *, xlim=None, ylim=None,
                 zlim=None, parent=None, namespace=None, zlabel='', ylabel='',
                 xlabel='', title='', stream_name='primary', **kwargs):
        super().__init__(parent=parent)
        canvas = MPLwidget()
        self.ax = canvas.axes
        self.stream_name = stream_name
        self.x_name = x_name
        self.y_name = y_name
        self.z_name = z_name
        eva = Evaluator(namespace=namespace)
        self.livePlot = LivePlot_2D(x_name, y_name, z_name, xlim=xlim,
                                    ylim=ylim, zlim=zlim, ax=self.ax,
                                    xlabel=xlabel, ylabel=ylabel, zlabel=zlabel,
                                    cmap='viridis', evaluator=eva,
                                    stream_name=stream_name, **kwargs)
        self.livePlot.new_data.connect(self.show)
        self.toolbar = NavigationToolbar2QT(canvas, self)

        self.pushButton_autoscale = QPushButton('Autoscale')
        self.pushButton_autoscale.clicked.connect(self.autoscale)

        layout = QGridLayout()
        layout.addWidget(canvas, 0, 1, 1, 3)
        layout.addWidget(self.toolbar, 1, 2, 1, 2)
        layout.addWidget(self.pushButton_autoscale, 1, 1)
        self.setLayout(layout)

        self.setWindowTitle(title or f'{z_name} 2D')
        self.setWindowIcon(QIcon(resource_filename('nomad_camels', 'graphics/camels_icon.png')))
        place_widget(self)

    def autoscale(self):
        """ """
        self.ax.autoscale()
        self.ax.figure.canvas.draw_idle()

    def clear_plot(self):
        """ """
        self.livePlot.clear_plot()

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


class LivePlot_2D(LiveScatter, QObject):
    """ """
    new_data = Signal()

    def __init__(self, x, y, z, *, xlim=None, ylim=None, zlim=None,
                 ax=None, xlabel='', ylabel='', zlabel='', cmap='viridis',
                 evaluator=None, stream_name='primary', **kwargs):
        LiveScatter.__init__(self, x, y, z, xlim=xlim, ylim=ylim, clim=zlim,
                             ax=ax, **kwargs)
        QObject.__init__(self)
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()
        self._minx, self._maxx, self._miny, self._maxy = (None,)*4
        self._xdata, self._ydata, self._Idata = [], [], []

        def setup():
            """ """
            # Run this code in start() so that it runs on the correct thread.
            nonlocal x, y, z, xlim, ylim, zlim, cmap, ax, kwargs  # noqa: E741
            with self.__setup_lock:
                if self.__setup_event.is_set():
                    return
                self.__setup_event.set()
            import matplotlib.colors as mcolors
            if ax is None:
                fig, ax = plt.subplots()
                fig.show()
            ax.cla()
            self.x = x
            self.y = y
            self.I = z  # noqa: E741
            ax.set_xlabel(xlabel or x)
            ax.set_ylabel(ylabel or y)
            ax.set_aspect('equal')
            self._sc = []
            self.ax = ax
            ax.margins(.1)
            self._xdata, self._ydata, self._Idata = [], [], []
            self._norm = mcolors.Normalize()

            self.xlim = xlim
            self.ylim = ylim
            if xlim is not None:
                ax.set_xlim(xlim)
            if ylim is not None:
                ax.set_ylim(ylim)
            if zlim is not None:
                self._norm.vmin, self._norm.vmax = zlim
            self.clim = zlim
            self.cmap = cmap
            self.kwargs = kwargs
            self.kwargs.setdefault('edgecolor', 'face')
            self.kwargs.setdefault('s', 50)

        self.__setup = setup
        self.zlabel = zlabel

        self.stream_name = stream_name
        self.eva = evaluator
        self.sc = None
        self.cb = None
        self.desc = ''

    def start(self, doc):
        """

        Parameters
        ----------
        doc :
            

        Returns
        -------

        """
        self.__setup()
        self._xdata.clear()
        self._ydata.clear()
        self._Idata.clear()
        sc = self.ax.scatter(self._xdata, self._ydata, c=self._Idata,
                             norm=self._norm, cmap=self.cmap, **self.kwargs)
        self._sc.append(sc)
        self.sc = sc
        self.cb = self.ax.figure.colorbar(sc, ax=self.ax)
        self.cb.set_label(self.zlabel or self.I)

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

    def event(self, doc):
        """

        Parameters
        ----------
        doc :
            

        Returns
        -------

        """
        if doc['descriptor'] != self.desc:
            return
        try:
            x = doc['data'][self.x]
        except KeyError:
            if self.x in ('time', 'seq_num'):
                x = doc[self.x]
            else:
                if not self.eva.is_to_date(doc['time']):
                    self.eva.event(doc)
                x = self.eva.eval(self.x)
        try:
            y = doc['data'][self.y]
        except KeyError:
            if not self.eva.is_to_date(doc['time']):
                self.eva.event(doc)
            y = self.eva.eval(self.y)
        try:
            I = doc['data'][self.I]
        except KeyError:
            if not self.eva.is_to_date(doc['time']):
                self.eva.event(doc)
            I = self.eva.eval(self.I)
        self.update(x, y, I)
        self.new_data.emit()

    def update(self, x, y, I):  # noqa: E741
        """

        Parameters
        ----------
        x :
            
        y :
            
        I :
            

        Returns
        -------

        """
        # if one is None all are
        if self._minx is None:
            self._minx = x
            self._maxx = x
            self._miny = y
            self._maxy = y

        self._xdata.append(x)
        self._ydata.append(y)
        self._Idata.append(I)
        offsets = np.vstack([self._xdata, self._ydata]).T
        self.sc.set_offsets(offsets)
        self.sc.set_array(np.asarray(self._Idata))

        if self.xlim is None:
            self._minx, self._maxx = np.minimum(x, self._minx), np.maximum(x, self._maxx)
            self.ax.set_xlim(self._minx, self._maxx)

        if self.ylim is None:
            self._miny, self._maxy = np.minimum(y, self._miny), np.maximum(y, self._maxy)
            self.ax.set_ylim(self._miny, self._maxy)

        if self.clim is None:
            clim = np.nanmin(self._Idata), np.nanmax(self._Idata)
            self.sc.set_clim(*clim)
        self.ax.figure.canvas.draw_idle()

    def clear_plot(self):
        """ """
        self._xdata.clear()
        self._ydata.clear()
        self._Idata.clear()
