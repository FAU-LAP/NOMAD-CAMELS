import sys
import os

sys.path.append(os.path.dirname(__file__).split("nomad_camels")[0])
import numpy as np
import threading
from collections import deque

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QApplication,
    QPushButton,
    QLabel,
    QLineEdit,
    QMenuBar,
    QGraphicsSceneMouseEvent,
)
from PySide6.QtCore import Signal, QObject, QTimer, QEvent, Qt
import PySide6
import pyqtgraph as pg
from pyqtgraph.GraphicsScene.mouseEvents import MouseClickEvent

import lmfit

from bluesky.callbacks.core import get_obj_fields, CallbackBase

from nomad_camels.gui.plot_options import Ui_Plot_Options
from nomad_camels.utility.fit_variable_renaming import replace_name
from nomad_camels.bluesky_handling.evaluation_helper import Evaluator
from nomad_camels.main_classes.plot_widget import LiveFit_Eva

# recognized by pyqtgraph: r, g, b, c, m, y, k, w
colors = ["w", "r", (0, 100, 255), "g", "c", "m", "y", "k"]
colors += ["orange", "purple", "brown", "pink", "gray", "olive", "navy", "teal"]


symbols = {
    "circle": "o",
    "square": "s",
    "triangle": "t",
    "diamond": "d",
    "plus": "+",
    "upwards triangle": "t1",
    "right triangle": "t2",
    "left triangle": "t3",
    "pentagon": "p",
    "hexagon": "h",
    "star": "star",
    "cross": "x",
    "arrow_up": "arrow_up",
    "arrow_right": "arrow_right",
    "arrow_down": "arrow_down",
    "arrow_left": "arrow_left",
    "crosshair": "crosshair",
}

linestyles = {
    "solid": Qt.PenStyle.SolidLine,
    "dashed": Qt.PenStyle.DashLine,
    "dash-dot": Qt.PenStyle.DashDotLine,
    "dash-dot-dot": Qt.PenStyle.DashDotDotLine,
    "dotted": Qt.PenStyle.DotLine,
    "none": Qt.PenStyle.NoPen,
}

# dark_mode = False
# pg.setConfigOptions(background="w", foreground="k")


# def activate_dark_mode():
#     """Changes the plot-style to dark-mode."""
#     global dark_mode
#     dark_mode = True
#     pg.setConfigOptions(background="k", foreground="w")


class PlotWidget(QWidget):
    """Class for creating a plot widget.

    Parameters
    ----------
    x_name : str
        The name of the x-axis variable
    y_names : Union[str, Tuple[str]]
        The name(s) of the y-axis variable(s)
    legend_keys : List[str], optional
        The keys for the legend, by default None
    xlim : Tuple[float, float], optional
        passed to Axes.set_xlim
    ylim : Tuple[float, float], optional
        passed to Axes.set_ylim
    epoch : {'run', 'unix'}, optional
        If 'run' t=0 is the time recorded in the RunStart document. If 'unix',
        t=0 is 1 Jan 1970 ("the UNIX epoch"). Default is 'run'.
    parent : QWidget, optional
        The parent widget, by default None
    namespace : Optional[Mapping[str, Any]]
        The namespace to use for the `Evaluator`, by default None
    ylabel : str, optional
        The y-axis label, by default ''
    xlabel : str, optional
        The x-axis label, by default ''
    title : str, optional
        The title of the plot, by default ''
    stream_name : str, optional
        The name of the stream to be used for the plot. Default is 'primary'
    fits : List[Dict[str, Union[str, bool, List[str], Tuple[float, float], Dict[str, Union[str, float]]]]], optional
        The fits for the plot, by default None
    do_plot : bool, optional
        Whether to show the plot, by default True
    **kwargs : Any, optional
        Additional keyword arguments to pass to `MultiLivePlot`

    Returns
    -------

    Attributes
    ----------
    ax : Axes
        The matplotlib axes of the plot
    x_name : str
        The name of the x-axis variable
    y_names : List[str]
        The name(s) of the y-axis variable(s)
    stream_name : str
        The name of the stream
    fits : List[Dict[str, Union[str, bool, List[str], Tuple[float, float], Dict[str, Union[str, float]]]]]
        The fits for the plot as they come from the fit/plot definer.
    liveFits : List[LiveFit_Eva]
        The live fit objects for the plot, handled by the liveFitPlots
    liveFitPlots : List[Fit_Plot_No_Init_Guess]
        The live fit plots for the plot, used to display the fits
    livePlot : MultiLivePlot
        The live plot, using the canvas etc.
    toolbar : NavigationToolbar2QT
        The toolbar for the plot
    pushButton_show_options : QPushButton
        The push button to show the plot options
    pushButton_autoscale : QPushButton
        The push button to autoscale the plot
    plot_options : Plot_Options
        The options widget for the plot
    options_open : bool
        Whether the options are currently open
    """

    closing = Signal()

    def __init__(
        self,
        x_name,
        y_names,
        *,
        legend_keys=None,
        xlim=None,
        ylim=None,
        epoch="run",
        parent=None,
        namespace=None,
        ylabel="",
        xlabel="",
        title="",
        stream_name="primary",
        fits=None,
        do_plot=True,
        multi_stream=False,
        y_axes=None,
        logX=False,
        logY=False,
        logY2=False,
        maxlen=np.inf,
        **kwargs,
    ):
        super().__init__(parent=parent)
        self.plot_widget = pg.PlotWidget()
        self.x_name = x_name
        self.y_names = y_names
        self.stream_name = stream_name
        self.fits = fits
        self.eva = Evaluator(namespace=namespace)
        self.liveFits = []
        self.liveFitPlots = []
        self.ax2_viewbox = None
        if y_axes and 2 in y_axes.values():
            self.ax2_viewbox = pg.ViewBox()
            plotItem = self.plot_widget.getPlotItem()
            # self.ax2_viewbox.setParentItem(plotItem)
            plotItem.scene().addItem(self.ax2_viewbox)
            plotItem.getAxis("right").linkToView(self.ax2_viewbox)
            self.ax2_viewbox.setXLink(plotItem)
            ax2 = pg.AxisItem("right")
            ax2.setLabel(self.y_names[0])
            ax2.linkToView(self.ax2_viewbox)
            plotItem.layout.addItem(ax2, 2, 3)

            def updateViews():
                self.ax2_viewbox.setGeometry(plotItem.vb.sceneBoundingRect())
                self.ax2_viewbox.linkedViewChanged(plotItem.vb, self.ax2_viewbox.XAxis)

            updateViews()
            plotItem.vb.sigResized.connect(updateViews)
        for fit in self.fits:
            if fit["use_custom_func"]:
                model = lmfit.models.ExpressionModel(fit["custom_func"])
                label = "custom"
            else:
                model = lmfit.models.lmfit_models[fit["predef_func"]]()
                label = fit["predef_func"]
            if fit["guess_params"]:
                init_guess = None
            else:
                init_guess = {}
                for i, param in enumerate(fit["initial_params"]["name"]):
                    init_guess[param] = fit["initial_params"]["initial value"][i]
            upper = {}
            lower = {}
            for i, param in enumerate(fit["initial_params"]["name"]):
                upper[param] = fit["initial_params"]["upper bound"][i] or np.inf
                lower[param] = fit["initial_params"]["lower bound"][i] or -np.inf
            params = model.make_params()
            if init_guess:
                for i, param in enumerate(fit["initial_params"]["name"]):
                    params[param].set(
                        init_guess[param], min=lower[param], max=upper[param]
                    )
            else:
                for i, param in enumerate(fit["initial_params"]["name"]):
                    params[param].set(min=lower[param], max=upper[param])
            name = f'{label}_{fit["y"]}_v_{fit["x"]}'
            name = replace_name(name)
            add_data = fit["additional_data"] or {}
            livefit = LiveFit_Eva(
                model,
                fit["y"],
                {"x": fit["x"]},
                self.eva,
                init_guess,
                name=name,
                additional_data=add_data,
                params=params,
                stream_name=stream_name,
            )
            self.liveFits.append(livefit)
            if y_axes and y_axes[fit["y"]] == 2:
                viewbox = self.ax2_viewbox
            else:
                viewbox = self.plot_widget.getPlotItem().vb
            self.liveFitPlots.append(
                LiveFitPlot(
                    livefit, viewbox, plotItem, display_values=fit["display_values"]
                )
            )

        self.livePlot = LivePlot(
            x_name=x_name,
            y_names=y_names,
            maxlen=maxlen,
            multi_stream=multi_stream,
            stream_name=stream_name,
            evaluator=self.eva,
            y_axes=y_axes,
            logX=logX,
            logY=logY,
            logY2=logY2,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            epoch=epoch,
            plot_item=self.plot_widget.getPlotItem(),
            ax2_viewbox=self.ax2_viewbox,
            fitPlots=self.liveFitPlots,
        )
        self.livePlot.new_data_signal.connect(self.show)
        self.livePlot.setup_done_signal.connect(self.make_toolbar)
        self.toolbar = None
        self.pushButton_show_options = QPushButton("Options")
        self.pushButton_show_options.clicked.connect(self.show_options)
        self.pushButton_clear = QPushButton("Clear Plot")
        self.pushButton_clear.clicked.connect(self.clear_plot)
        # self.plot_options = Plot_Options(self, self.livePlot)
        self.options_open = False
        label_n_data = QLabel("# data points:")
        self.lineEdit_n_data = QLineEdit(str(maxlen))
        self.lineEdit_n_data.returnPressed.connect(self.change_maxlen)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.plot_widget, 0, 0, 1, 4)
        self.layout().addWidget(self.pushButton_show_options, 2, 0)
        self.layout().addWidget(self.pushButton_clear, 2, 1)
        self.layout().addWidget(label_n_data, 2, 2)
        self.layout().addWidget(self.lineEdit_n_data, 2, 3)

    def make_toolbar(self):
        self.toolbar = QMenuBar()
        viewbox = self.plot_widget.getPlotItem().getViewBox()
        menu = viewbox.menu
        scene = viewbox.scene()
        # dummy mouseclickevent
        press_event = QGraphicsSceneMouseEvent(QEvent.GraphicsSceneMousePress)
        event = MouseClickEvent(press_event)
        scene.addParentContextMenus(viewbox, menu, event)
        actions = menu.actions()
        for action in actions:
            self.toolbar.addAction(action)
        self.layout().addWidget(self.toolbar, 1, 0, 1, 4)

    def change_maxlen(self):
        text = self.lineEdit_n_data.text()
        if not text or text.lower() in ["none", "inf", "np.inf"]:
            maxlen = np.inf
        else:
            try:
                maxlen = int(text)
            except ValueError:
                return
        self.livePlot.change_maxlen(maxlen)

    def show_options(self):
        pass

    def clear_plot(self):
        self.livePlot.clear_plot()
        for fit in self.liveFitPlots:
            fit.clear_plot()

    def closeEvent(self, event):
        self.closing.emit()
        super().closeEvent(event)


class Plot_Options(QWidget, Ui_Plot_Options):
    pass


class LivePlot(QObject, CallbackBase):
    new_data_signal = Signal()
    setup_done_signal = Signal()

    def __init__(
        self,
        x_name,
        y_names,
        plot_item,
        *,
        maxlen=np.inf,
        multi_stream=False,
        evaluator=None,
        stream_name="primary",
        y_axes=None,
        logX=False,
        logY=False,
        logY2=False,
        title="",
        xlabel=None,
        ylabel=None,
        epoch="run",
        ax2_viewbox=None,
        fitPlots=None,
        **kwargs,
    ):
        CallbackBase.__init__(self)
        QObject.__init__(self)
        self.__teleporter = Teleporter()
        self.__teleporter.name_doc_escape.connect(handle_teleport)
        self.plotItem = plot_item
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()

        def setup():
            nonlocal y_names, x_name, title, xlabel, ylabel, epoch
            with self.__setup_lock:
                if self.__setup_event.is_set():
                    return
                self.__setup_event.set()
            # set the labels
            self.use_abs = {"x": False, "y": False, "y2": False}
            self.plots = {}
            if x_name is not None:
                self.x, *others = get_obj_fields([x_name])
            else:
                self.x = "seq_num"
            self.ys = get_obj_fields(y_names)
            self.plotItem.setLabel("bottom", xlabel or x_name or "sequence #")
            self.plotItem.setLabel("left", ylabel or self.ys[0])
            if title:
                self.plotItem.setTitle(title)
            self._epoch_offset = None
            self._epoch = epoch

        self.x_data = []
        self.y_data = {}
        self.y_axes = y_axes or {}
        self.ax2_viewbox = None
        self.maxlen = maxlen
        self.stream_name = stream_name
        self.eva = evaluator
        self.y_names = y_names
        self.ys = get_obj_fields(y_names)
        for y in y_names:
            self.y_data[y] = []
        self.current_plots = {}
        self.legend = None
        self.desc = []
        self.multi_stream = multi_stream
        self.ax2_viewbox = ax2_viewbox
        self.__setup = setup
        self.fitPlots = fitPlots or []
        for fit in self.fitPlots:
            fit.parent_plot = self
        self.descs_fit_readying = {}
        self.line_number = 0
        self.n_plots = 0

    def __call__(self, name, doc, *, escape=False):
        if not escape and self.__teleporter is not None:
            self.__teleporter.name_doc_escape.emit(name, doc, self)
        else:
            return CallbackBase.__call__(self, name, doc)

    def start(self, doc):
        self.__setup()
        for i, y in enumerate(self.ys):
            try:
                color = colors[self.n_plots % len(colors)]
                if y in self.y_axes and self.y_axes[y] == 2:
                    self.current_plots[y] = plot = pg.PlotDataItem(
                        [],
                        [],
                        label=self.y_names[i],
                        symbol="o",
                        symbolPen=pg.mkPen(color=color),
                        symbolBrush=pg.mkBrush(color=color),
                        pen=pg.mkPen(color=color, width=2, style=linestyles["none"]),
                    )
                    self.ax2_viewbox.addItem(plot)
                else:
                    self.current_plots[y] = self.plotItem.plot(
                        [],
                        [],
                        label=self.y_names[i],
                        symbol="o",
                        symbolPen=pg.mkPen(color=color),
                        symbolBrush=pg.mkBrush(color=color),
                        pen=pg.mkPen(color=color, width=2, style=linestyles["none"]),
                    )
                self.n_plots += 1
            except Exception as e:
                print(e)
        self.legend = self.plotItem.addLegend()
        self.setup_done_signal.emit()
        for fit in self.fitPlots:
            fit.start(doc)

    def descriptor(self, doc):
        if doc["name"] == self.stream_name:
            self.desc.append(doc["uid"])
        elif doc["name"].startswith(f"{self.stream_name}_fits_readying_"):
            for fit in self.fitPlots:
                if (
                    doc["name"]
                    == f"{self.stream_name}_fits_readying_{fit.livefit.name}"
                ):
                    self.descs_fit_readying[doc["uid"]] = fit
        elif self.multi_stream and doc["name"].startswith(self.stream_name):
            self.desc.append(doc["uid"])

    def event(self, doc):
        if isinstance(doc, QEvent):
            try:
                pg.PlotWidget.event(self, doc)
            except Exception as e:
                print(e)
            return
        if doc["descriptor"] not in self.desc:
            if doc["descriptor"] in self.descs_fit_readying:
                self.descs_fit_readying[doc["descriptor"]].get_ready()
            return
        try:
            new_x = doc["data"][self.x]
        except KeyError:
            if self.x in ("time", "seq_num"):
                new_x = doc[self.x]
            else:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_x = self.eva.eval(self.x)
        if self.x == "time" and self._epoch == "run":
            new_x -= self._epoch_offset

        new_y = {}
        for y in self.ys:
            try:
                new_y[y] = doc["data"][y]
            except KeyError:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_y[y] = self.eva.eval(y)
        self.update_caches(new_x, new_y)
        for fit in self.fitPlots:
            fit.event(doc)
        self.update_plot()

    def update_caches(self, new_x, new_y):
        for y in new_y:
            self.y_data[y].append(new_y[y])
        self.x_data.append(new_x)

    def update_plot(self):
        for y in self.ys:
            self.current_plots[y].setData(self.x_data, self.y_data[y])
        self.new_data_signal.emit()

    def stop(self, doc):
        if not self.x_data:
            print(
                f"LivePlot did not get any data that corresponds to the x axis. {self.x}"
            )
        for y in self.y_data:
            if not self.y_data[y]:
                print(f"LivePlot did not get any data for {y}")
            if len(self.y_data[y]) != len(self.x_data):
                print(f"LivePlot has a length mismatch for {y}")
        for fit in self.fitPlots:
            fit.stop(doc)

    def clear_plot(self):
        for y in self.ys:
            self.current_plots[y].setData([], [])
        self.x_data = []
        for y in self.y_data:
            self.y_data[y] = []
        for fit in self.fitPlots:
            fit.clear_plot()
        self.update_plot()

    def change_maxlen(self, maxlen):
        self.maxlen = maxlen
        if maxlen < np.inf:
            self.x_data = deque(self.x_data, maxlen=maxlen)
            for y in self.y_data:
                self.y_data[y] = deque(self.y_data[y], maxlen=maxlen)
        else:
            self.x_data = list(self.x_data)
            for y in self.y_data:
                self.y_data[y] = list(self.y_data[y])


class LiveFitPlot(CallbackBase):
    def __init__(
        self,
        livefit,
        viewbox,
        plotItem,
        *,
        num_points=100,
        display_values=False,
        **kwargs,
    ):
        super().__init__()
        self.__teleporter = Teleporter()
        self.__teleporter.name_doc_escape.connect(handle_teleport)
        if len(livefit.independent_vars) != 1:
            raise NotImplementedError(
                "LiveFitPlot supports models with one independent variable only."
            )

        self.viewbox = viewbox
        self.plotItem = plotItem
        self.livefit = livefit
        self.display_values = display_values
        self.num_points = num_points
        self.kwargs = kwargs

        (self.__x_key,) = livefit.independent_vars.keys()
        self._has_been_run = False
        livefit.parent_plot = self
        self.x_data = []
        self.y_data = []
        self.plot = None
        self.x = None
        self.line_position = None
        self.text_objects = []
        self.color = "w"

        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()

        def setup():
            nonlocal livefit
            with self.__setup_lock:
                if self.__setup_event.is_set():
                    return
                self.__setup_event.set()
            (x,) = livefit.independent_vars.values()
            if x is not None:
                self.x, *others = get_obj_fields([x])
            else:
                self.x = "seq_num"
            y = livefit.y
            self.y, *others = get_obj_fields([y])

        self.__setup = setup

    def start(self, doc):
        self.__setup()
        self.x_data, self.y_data = [], []
        self.color = colors[self.parent_plot.n_plots % len(colors)]
        self.plot = pg.PlotDataItem(
            [],
            [],
            pen=pg.mkPen(color=self.color, width=2, style=linestyles["solid"]),
            symbol=None,
            symbolPen=pg.mkPen(color=self.color),
            symbolBrush=pg.mkBrush(color=self.color),
        )
        self.viewbox.addItem(self.plot)
        self.livefit.start(doc)
        (self.x,) = self.livefit.independent_vars.keys()
        self.parent_plot.n_plots += 1

    def get_ready(self):
        """Passes the command to the `_livefit`"""
        self.livefit.get_ready()

    def event(self, doc):
        """Passes the event to the `livefit`"""
        self.livefit.event(doc)

    def fit_has_result(self):
        if self.livefit.result is not None:
            x_data = self.livefit.independent_vars_data[self.__x_key]
            x_points = np.linspace(np.min(x_data), np.max(x_data), self.num_points)
            kwargs = {self.__x_key: x_points}
            kwargs.update(self.livefit.result.values)
            self.y_data = self.livefit.result.model.eval(**kwargs)
            self.x_data = x_points
            kwargs.update(self.livefit.result.init_values)
            self.update_plot()

    def clear_plot(self):
        if self.plot:
            self.plot.setData([], [])
        for text in self.text_objects:
            self.viewbox.removeItem(text)
        self.text_objects = []

    def update_plot(self):
        self.plot.setData(self.x_data, self.y_data)
        self.parent_plot.update_plot()
        if self.display_values:
            for text in self.text_objects:
                self.viewbox.removeItem(text)
            self.text_objects.clear()
            vals = self.livefit.result.values
            if self.line_position is None:
                self.line_position = self.parent_plot.line_number
                self.parent_plot.line_number += len(vals)
            for i, (name, value) in enumerate(vals.items()):
                text = pg.TextItem(f"{name}: {value:.3e}", color=self.color)
                text.setParentItem(self.plotItem)
                text.setPos(50, (i + self.line_position) * 20)
                self.text_objects.append(text)

    def __call__(self, name, doc, *, escape=False):
        if not escape and self.__teleporter is not None:
            self.__teleporter.name_doc_escape.emit(name, doc, self)
        else:
            return CallbackBase.__call__(self, name, doc)


class Teleporter(QObject):
    name_doc_escape = Signal(str, dict, object)


def handle_teleport(name, doc, obj):
    obj(name, doc, escape=True)


import sys
import numpy as np
import pyqtgraph as pg


class Plotter:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.plot = pg.PlotWidget()
        self.data = [0, 1]
        self.data2 = [0, 1]
        self.plot_item = self.plot.plot(self.data)
        self.plot_item2 = self.plot.plot(self.data2, pen=pg.mkPen(color="r", width=2))

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Update every 1000 ms

    def update(self):
        # Update the data
        self.data.append(np.random.random())
        self.data2.append(np.random.random())
        self.plot_item.setData(self.data)
        self.plot_item2.setData(self.data2)

    def run(self):
        self.plot.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    plotter = Plotter()
    plotter.run()
