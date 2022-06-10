import sys
from collections import ChainMap
import threading

import matplotlib.pyplot as plt
from bluesky.callbacks.mpl_plotting import LivePlot
from bluesky.callbacks.core import get_obj_fields
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,\
    NavigationToolbar2QT

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QPushButton

dark_mode = False
def activate_dark_mode():
    """Changes the plot-style to dark-mode."""
    global dark_mode
    dark_mode = True
    plt.style.use('dark_background')


class MPLwidget(FigureCanvasQTAgg):
    def __init__(self):
        fig, ax = plt.subplots()
        self.axes = ax
        self.axes.grid()
        super().__init__(fig)

class PlotWidget(QWidget):
    def __init__(self, x_name=None, y_names=(), *, legend_keys=None, xlim=None, ylim=None, epoch='run', parent=None, namespace=None, **kwargs):
        super().__init__(parent)
        canvas = MPLwidget()
        self.livePlot = MultiLivePlot(y_names, x_name, legend_keys=legend_keys,
                                      xlim=xlim, ylim=ylim, epoch=epoch,
                                      ax=canvas.axes, namespace=namespace,
                                      **kwargs)
        self.toolbar = NavigationToolbar2QT(canvas, self)
        self.pushButton_show_options = QPushButton('Show Options')
        self.pushButton_show_options.clicked.connect(self.show_options)

        layout = QGridLayout()
        layout.addWidget(canvas, 0, 1, 1, 2)
        layout.addWidget(self.toolbar, 1, 2)
        layout.addWidget(self.pushButton_show_options, 1, 1)
        self.setLayout(layout)

        self.options_open = False
        self.show()

    def show_options(self):
        if self.options_open:
            self.pushButton_show_options.setText('Show Options')
            self.options_open = False
        else:
            self.pushButton_show_options.setText('Hide Options')
            self.options_open = True


class MultiLivePlot(LivePlot):
    def __init__(self, ys=(), x=None, *, legend_keys=None, xlim=None, ylim=None,
                 ax=None, epoch='run', xlabel='', ylabel='', namespace=None,
                 **kwargs):
        super().__init__(y=ys[0], x=x, legend_keys=legend_keys, xlim=xlim, ylim=ylim,
                         ax=ax, epoch=epoch, **kwargs)
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()
        self.eva = Evaluator(namespace=namespace)
        if isinstance(ys, str):
            ys = [ys]

        def setup():
            # Run this code in start() so that it runs on the correct thread.
            nonlocal ys, x, legend_keys, xlim, ylim, ax, epoch, kwargs, xlabel,\
                ylabel
            with self.__setup_lock:
                if self.__setup_event.is_set():
                    return
                self.__setup_event.set()
            if ax is None:
                fig, ax = plt.subplots()
            self.ax = ax

            if legend_keys is None:
                legend_keys = ys
            self.legend_keys = legend_keys
            if x is not None:
                self.x, *others = get_obj_fields([x])
            else:
                self.x = 'seq_num'
            self.ys = get_obj_fields(ys)
            self.ax.set_ylabel(ylabel or ys[0])
            self.ax.set_xlabel(xlabel or x or 'sequence #')
            if xlim is not None:
                self.ax.set_xlim(*xlim)
            if ylim is not None:
                self.ax.set_ylim(*ylim)
            self.ax.margins(.1)
            self.kwargs = kwargs
            self.lines = []
            self.legend = None
            # self.legend_title = " :: ".join([name for name in self.legend_keys])
            self._epoch_offset = None  # used if x == 'time'
            self._epoch = epoch

        self.__setup = setup
        self._epoch_offset = 0
        self.x_data = []
        self.y_data = {}
        self.y_names = ys
        self.ys = get_obj_fields(ys)
        for y in ys:
            self.y_data[y] = []
        self.current_lines = {}

    def start(self, doc):
        self.__setup()
        # The doc is not used; we just use the signal that a new run began.
        self._epoch_offset = doc['time']  # used if self.x == 'time'
        self.x_data = []
        self.y_data = {}
        for y in self.ys:
            self.y_data[y] = []
        # label = " :: ".join(
            # [str(doc.get(name, name)) for name in self.legend_keys])
        kwargs = ChainMap(self.kwargs, {'ls': 'None', 'marker': 'x'})
        self.current_lines = {}
        for i, y in enumerate(self.ys):
            try:
                self.current_lines[y], = self.ax.plot([], [],
                                                      label=self.legend_keys[i],
                                                      **kwargs)
            except Exception as e:
                print(e)
        self.lines.append(self.current_lines)
        legend = self.ax.legend(loc=0)
        try:
            # matplotlib v3.x
            self.legend = legend.set_draggable(True)
        except AttributeError:
            # matplotlib v2.x (warns in 3.x)
            self.legend = legend.draggable(True)

    def event(self, doc):
        """Unpack data from the event and call self.update()."""
        # This outer try/except block is needed because multiple event
        # streams will be emitted by the RunEngine and not all event
        # streams will have the keys we want.
        # This inner try/except block handles seq_num and time, which could
        # be keys in the data or accessing the standard entries in every
        # event.
        try:
            new_x = doc['data'][self.x]
        except KeyError:
            if self.x in ('time', 'seq_num'):
                new_x = doc[self.x]
            else:
                raise
        new_y = {}
        for y in self.ys:
            try:
                new_y[y] = doc['data'][y]
            except KeyError:
                if not self.eva.is_to_date(doc['time']):
                    self.eva.event(doc)
                new_y[y] = self.eva.eval(y)


        # Special-case 'time' to plot against against experiment epoch, not
        # UNIX epoch.
        if self.x == 'time' and self._epoch == 'run':
            new_x -= self._epoch_offset

        self.update_caches(new_x, new_y)
        self.update_plot()
        # super().event(doc)

    def update_caches(self, x, ys):
        for y in ys:
            self.y_data[y].append(ys[y])
        self.x_data.append(x)

    def update_plot(self):
        for y, line in self.current_lines.items():
            line.set_data(self.x_data, self.y_data[y])
        # Rescale and redraw.
        self.ax.relim(visible_only=True)
        self.ax.autoscale_view(tight=True)
        self.ax.figure.canvas.draw_idle()

    def stop(self, doc):
        if not self.x_data:
            print('MultiLivePlot did not get any data that corresponds to the '
                  'x axis. {}'.format(self.x))
        for y in self.y_data:
            if not self.y_data[y]:
                print('MultiLivePlot did not get any data that corresponds to the '
                      'y axis. {}'.format(y))
            if len(self.y_data[y]) != len(self.x_data):
                print('MultiLivePlot has a different number of elements for x ({}) and'
                      'y ({}, {})'.format(len(self.x_data), len(self.y_data), y))


if __name__ == '__main__':
    from bluesky import RunEngine
    from bluesky.plans import scan
    from ophyd.sim import motor, det
    from bluesky_handling.evaluation_helper import Evaluator

    motor.delay = 1e-3

    def plan():
        for i in range(4, 5):
            yield from scan([det], motor, -5, 5, 3**i)

    RE = RunEngine()
    app = QApplication(sys.argv)
    # myapp = PlotWidget(run_engine=RE, x_name='motor', y_names=['det'], title='test', xlabel='aaaa', ylabel='bbbb')
    myapp = PlotWidget('motor', ['det', 'det**2'])
    myapp.show()
    RE.subscribe(myapp.livePlot)
    RE(plan())
    sys.exit(app.exec_())