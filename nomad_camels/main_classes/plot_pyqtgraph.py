import sys
import os

sys.path.append(os.path.dirname(__file__).split("nomad_camels")[0])
import numpy as np
import threading
from collections import deque

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMenuBar,
    QGraphicsSceneMouseEvent,
    QTableWidgetItem,
    QComboBox,
    QColorDialog,
)
from PySide6.QtCore import Signal, QObject, QEvent, Qt
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
dark_mode_colors = ["w", "r", (0, 100, 255), "g", "c", "m", "y", "k"]

matplotlib_default_colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]

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
    "none": None,
}

linestyles = {
    "solid": Qt.PenStyle.SolidLine,
    "dashed": Qt.PenStyle.DashLine,
    "dash-dot": Qt.PenStyle.DashDotLine,
    "dash-dot-dot": Qt.PenStyle.DashDotDotLine,
    "dotted": Qt.PenStyle.DotLine,
    "none": Qt.PenStyle.NoPen,
}

dark_mode = False
pg.setConfigOptions(background="w", foreground="k")
colors = matplotlib_default_colors


def activate_dark_mode():
    """Changes the plot-style to dark-mode."""
    global dark_mode, colors
    dark_mode = True
    pg.setConfigOptions(background="k", foreground="w")
    colors = dark_mode_colors


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
        ax2 = None
        if y_axes and 2 in y_axes.values():
            self.ax2_viewbox = pg.ViewBox()
            plotItem = self.plot_widget.getPlotItem()
            plotItem.scene().addItem(self.ax2_viewbox)
            ax2 = plotItem.getAxis("right")
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
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            epoch=epoch,
            plot_item=self.plot_widget.getPlotItem(),
            ax2_viewbox=self.ax2_viewbox,
            ax2_axis=ax2,
            fitPlots=self.liveFitPlots,
        )
        self.livePlot.plotItem.showGrid(True, True)
        self.livePlot.new_data_signal.connect(self.show)
        self.livePlot.setup_done_signal.connect(self.make_toolbar)
        self.toolbar = None
        self.pushButton_show_options = QPushButton("Show Options")
        self.pushButton_show_options.clicked.connect(self.show_options)
        self.pushButton_clear = QPushButton("Clear Plot")
        self.pushButton_clear.clicked.connect(self.clear_plot)
        self.plot_options = Plot_Options(self, self.livePlot)
        self.plot_options.checkBox_log_x.setChecked(logX)
        self.plot_options.checkBox_log_y.setChecked(logY)
        self.plot_options.checkBox_log_y2.setChecked(logY2)
        self.options_open = False
        label_n_data = QLabel("# data points:")
        self.lineEdit_n_data = QLineEdit(str(maxlen))
        self.lineEdit_n_data.returnPressed.connect(self.change_maxlen)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.plot_widget, 0, 1, 1, 4)
        self.layout().addWidget(self.pushButton_show_options, 2, 1)
        self.layout().addWidget(self.pushButton_clear, 2, 2)
        self.layout().addWidget(label_n_data, 2, 3)
        self.layout().addWidget(self.lineEdit_n_data, 2, 4)
        self.layout().addWidget(self.plot_options, 0, 0, 3, 1)
        self.plot_options.hide()
        self.adjustSize()

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
            if action.text() == "View All":
                action.triggered.connect(self.auto_range)
            self.toolbar.addAction(action)
        self.layout().addWidget(self.toolbar, 1, 1, 1, 4)
        self.plot_options.set_log()

    def auto_range(self):
        self.livePlot.plotItem.vb.autoRange()
        if self.ax2_viewbox:
            self.ax2_viewbox.autoRange()

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
        if self.options_open:
            self.pushButton_show_options.setText("Show Options")
            self.options_open = False
            self.plot_options.hide()
            self.adjustSize()
        else:
            self.pushButton_show_options.setText("Hide Options")
            self.options_open = True
            self.plot_options.show()
            self.plot_options.update_plot_items()

    def clear_plot(self):
        self.livePlot.clear_plot()
        for fit in self.liveFitPlots:
            fit.clear_plot()

    def closeEvent(self, event):
        self.closing.emit()
        super().closeEvent(event)


class Plot_Options(Ui_Plot_Options, QWidget):
    def __init__(self, parent=None, livePlot=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.livePlot = livePlot
        self.all_items = {}
        self.items_in_2 = []
        self.checkBox_log_x.setChecked(self.livePlot.plotItem.getAxis("bottom").logMode)
        self.checkBox_log_y.setChecked(self.livePlot.plotItem.getAxis("left").logMode)
        if self.livePlot.ax2_viewbox:
            self.checkBox_log_y2.setChecked(
                self.livePlot.plotItem.getAxis("right").logMode
            )
        self.checkBox_log_x.stateChanged.connect(self.set_log)
        self.checkBox_log_y.stateChanged.connect(self.set_log)
        self.checkBox_log_y2.stateChanged.connect(self.set_log)
        self.checkBox_use_abs_x.stateChanged.connect(self.set_log)
        self.checkBox_use_abs_y.stateChanged.connect(self.set_log)
        self.checkBox_use_abs_y2.stateChanged.connect(self.set_log)

    def update_plot_items(self):
        self.all_items.clear()
        self.items_in_2.clear()
        items_viewbox_1 = self.livePlot.plotItem.vb.allChildItems()
        for item in items_viewbox_1:
            if isinstance(item, pg.PlotDataItem):
                self.all_items[item.name()] = item
        if self.livePlot.ax2_viewbox:
            items_viewbox_2 = self.livePlot.ax2_viewbox.allChildItems()
            for item in items_viewbox_2:
                if isinstance(item, pg.PlotDataItem):
                    self.all_items[item.name()] = item
                    self.items_in_2.append(item.name())
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setMinimumWidth(400)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Name", "marker", "linestyle", "color"]
        )
        self.tableWidget.verticalHeader().setHidden(True)
        self.tableWidget.setRowCount(len(self.all_items))
        for i, (name, item) in enumerate(
            sorted(self.all_items.items(), key=lambda x: x[0].lower())
        ):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(name))

            markerwidge = QComboBox()
            markerwidge.addItems(symbols.keys())
            marker = item.opts["symbol"]
            if marker in symbols.values():
                marker = list(symbols.keys())[list(symbols.values()).index(marker)]
            markerwidge.setCurrentText(marker)
            markerwidge.currentTextChanged.connect(
                lambda text, n=i: self.change_symbol(text, n)
            )
            self.tableWidget.setCellWidget(i, 1, markerwidge)

            linestylewidge = QComboBox()
            linestylewidge.addItems(linestyles.keys())
            linestyle = item.opts["pen"].style()
            if linestyle in linestyles.values():
                linestyle = list(linestyles.keys())[
                    list(linestyles.values()).index(linestyle)
                ]
            linestylewidge.setCurrentText(linestyle)
            linestylewidge.currentTextChanged.connect(
                lambda text, item=item: item.setPen(
                    pg.mkPen(
                        color=item.opts["pen"].color(),
                        width=item.opts["pen"].width(),
                        style=linestyles[text],
                    )
                )
            )
            self.tableWidget.setCellWidget(i, 2, linestylewidge)

            color = item.opts["pen"].color()
            colorwidge = QPushButton(color.name())
            colorwidge.clicked.connect(lambda n=i: self.change_color(n))
            self.tableWidget.setCellWidget(i, 3, colorwidge)

    def change_symbol(self, symbol, row):
        name = self.tableWidget.item(row, 0).text()
        self.change_color(row, just_update=True)
        self.all_items[name].setSymbol(symbols[symbol])

    def change_color(self, row, just_update=False):
        if just_update:
            item = self.tableWidget.cellWidget(row, 3)
            color = item.text()
            name = self.tableWidget.item(row, 0).text()
            self.all_items[name].opts["pen"].setColor(color)
            self.all_items[name].setSymbolPen(pg.mkPen(color=color))
            self.all_items[name].setSymbolBrush(pg.mkBrush(color=color))
            return
        color = QColorDialog.getColor()
        if color.isValid():
            item = self.tableWidget.cellWidget(row, 3)
            item.setText(color.name())
            name = self.tableWidget.item(row, 0).text()
            self.all_items[name].opts["pen"].setColor(color)
            self.all_items[name].setSymbolPen(pg.mkPen(color=color))
            self.all_items[name].setSymbolBrush(pg.mkBrush(color=color))

    def set_log(self):
        x = self.checkBox_log_x.isChecked()
        self.checkBox_use_abs_x.setEnabled(x)
        y = self.checkBox_log_y.isChecked()
        self.checkBox_use_abs_y.setEnabled(y)
        y2 = self.checkBox_log_y2.isChecked()
        self.checkBox_use_abs_y2.setEnabled(y2)
        self.livePlot.use_abs["x"] = self.checkBox_use_abs_x.isChecked()
        self.livePlot.use_abs["y"] = self.checkBox_use_abs_y.isChecked()
        self.livePlot.use_abs["y2"] = self.checkBox_use_abs_y2.isChecked()
        for name, item in self.all_items.items():
            if name in self.items_in_2:
                item.setLogMode(x, y2)
            else:
                item.setLogMode(x, y)
        if self.livePlot.ax2_viewbox:
            self.livePlot.plotItem.getAxis("right").setLogMode(x, y2)
            self.livePlot.ax2_viewbox.setLogMode(x, y2)
            self.livePlot.ax2_axis.setLogMode(y2)
            self.livePlot.ax2_viewbox.enableAutoRange()
        self.livePlot.plotItem.setLogMode(x, y)
        self.livePlot.update_plot()


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
        title="",
        xlabel=None,
        ylabel=None,
        epoch="run",
        ax2_viewbox=None,
        ax2_axis=None,
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
        self.use_abs = {"x": False, "y": False, "y2": False}

        def setup():
            nonlocal y_names, x_name, title, xlabel, ylabel, epoch
            with self.__setup_lock:
                if self.__setup_event.is_set():
                    return
                self.__setup_event.set()
            # set the labels
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
        self.ax2_axis = ax2_axis
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
                        name=self.y_names[i],
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
                        name=self.y_names[i],
                        symbol="o",
                        symbolPen=pg.mkPen(color=color),
                        symbolBrush=pg.mkBrush(color=color),
                        pen=pg.mkPen(color=color, width=2, style=linestyles["none"]),
                    )
                self.n_plots += 1
            except Exception as e:
                print(e)
        self.legend = pg.LegendItem(
            offset=(1, 1), horSpacing=20, verSpacing=-5, pen="w" if dark_mode else "k"
        )
        self.legend.setParentItem(self.plotItem.vb)
        for plot in self.current_plots.values():
            self.legend.addItem(plot, plot.name())
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
        if self.plotItem.getAxis("bottom").logMode and self.use_abs["x"]:
            plot_x = np.abs(self.x_data)
        else:
            plot_x = self.x_data
        for y in self.ys:
            y_abs = False
            y2_abs = False
            if self.plotItem.getAxis("left").logMode and self.use_abs["y"]:
                y_abs = True
            if (
                self.ax2_viewbox
                and self.plotItem.getAxis("right").logMode
                and self.use_abs["y2"]
            ):
                y2_abs = True
            if self.y_axes.get(y, 1) == 2:
                plot_y = np.abs(self.y_data[y]) if y2_abs else self.y_data[y]
            else:
                plot_y = np.abs(self.y_data[y]) if y_abs else self.y_data[y]
            self.current_plots[y].setData(plot_x, plot_y)
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
            name=self.livefit.name,
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
        if self.display_values:
            for text in self.text_objects:
                self.viewbox.removeItem(text)
            self.text_objects.clear()
            legend = self.parent_plot.legend
            y0 = 0
            if legend is not None:
                legendRect = legend.boundingRect()
                legendPos = legend.scenePos()
                y0 = legendPos.y() + legendRect.height()
            vals = self.livefit.result.values
            if self.line_position is None:
                self.line_position = self.parent_plot.line_number
                self.parent_plot.line_number += len(vals)
            for i, (name, value) in enumerate(vals.items()):
                text = pg.TextItem(f"{name}: {value:.3e}", color=self.color)
                text.setParentItem(self.plotItem.vb)
                text.setPos(5, (i + self.line_position) * 20 + y0)
                self.text_objects.append(text)
        self.parent_plot.update_plot()

    def __call__(self, name, doc, *, escape=False):
        if not escape and self.__teleporter is not None:
            self.__teleporter.name_doc_escape.emit(name, doc, self)
        else:
            return CallbackBase.__call__(self, name, doc)


class Teleporter(QObject):
    name_doc_escape = Signal(str, dict, object)


def handle_teleport(name, doc, obj):
    obj(name, doc, escape=True)


class PlotWidget_2D(QWidget):
    """ """

    closing = Signal()

    def __init__(
        self,
        x_name,
        y_name,
        z_name,
        parent=None,
        namespace=None,
        xlabel="",
        ylabel="",
        zlabel="",
        title="",
        stream_name="primary",
        **kwargs,
    ):
        super().__init__(parent=parent)
        self.graphics_layout = pg.GraphicsLayoutWidget()
        self.plot = self.graphics_layout.addPlot(col=0, row=0)
        self.x_name = x_name
        self.y_name = y_name
        self.z_name = z_name
        self.plot.setLabel("bottom", xlabel or x_name)
        self.plot.setLabel("left", ylabel or y_name)
        self.stream_name = stream_name

        self.toolbar = None
        eva = Evaluator(namespace=namespace)
        self.livePlot = LivePlot_2D(
            x_name,
            y_name,
            z_name,
            plotItem=self.plot,
            graphics_layout=self.graphics_layout,
            cmap="viridis",
            evaluator=eva,
            stream_name=stream_name,
            **kwargs,
        )

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.graphics_layout, 0, 0)
        self.make_toolbar()
        self.adjustSize()

    def make_toolbar(self):
        self.toolbar = QMenuBar()
        viewbox = self.plot.getViewBox()
        menu = viewbox.menu
        scene = viewbox.scene()
        # dummy mouseclickevent
        press_event = QGraphicsSceneMouseEvent(QEvent.GraphicsSceneMousePress)
        event = MouseClickEvent(press_event)
        scene.addParentContextMenus(viewbox, menu, event)
        actions = menu.actions()
        for action in actions:
            self.toolbar.addAction(action)
        self.layout().addWidget(self.toolbar, 1, 0)

    def clear_plot(self):
        self.livePlot.clear_plot()

    def closeEvent(self, event):
        self.closing.emit()
        super().closeEvent(event)


class LivePlot_2D(QObject, CallbackBase):
    """ """

    new_data = Signal()

    def __init__(
        self,
        x,
        y,
        z,
        plotItem,
        graphics_layout,
        *,
        cmap="viridis",
        evaluator=None,
        stream_name="primary",
        **kwargs,
    ):
        CallbackBase.__init__(self)
        QObject.__init__(self)
        self.__teleporter = Teleporter()
        self.__teleporter.name_doc_escape.connect(handle_teleport)
        self.x = x
        self.y = y
        self.z = z
        self.x_data, self.y_data, self.z_data = [], [], []
        self.cmap = pg.colormap.get(cmap)
        self.eva = evaluator
        self.stream_name = stream_name
        self.kwargs = kwargs
        self.plotItem = plotItem
        self.graphics_layout = graphics_layout
        self.scatter_plot = None
        self.image = None
        self.hist = None
        self.desc = None
        self._epoch_offset = None
        self._epoch = "run"
        self._minx = self._miny = np.inf
        self._maxx = self._maxy = -np.inf

    def __call__(self, name, doc, *, escape=False):
        if not escape and self.__teleporter is not None:
            self.__teleporter.name_doc_escape.emit(name, doc, self)
        else:
            return CallbackBase.__call__(self, name, doc)

    def start(self, doc):
        self.x_data.clear()
        self.y_data.clear()
        self.z_data.clear()
        self.scatter_plot = pg.ScatterPlotItem(self.x_data, self.y_data)
        self.plotItem.addItem(self.scatter_plot)
        self.image = pg.ImageItem()
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.image)
        self.hist.autoHistogramRange()
        self.hist.gradient.setColorMap(self.cmap)
        self.hist.axis.setLabel(self.z)
        self.graphics_layout.addItem(self.hist, row=0, col=1)
        self.plotItem.addItem(self.image)
        self._epoch_offset = None
        self._epoch = "run"

    def descriptor(self, doc):
        if doc["name"] == self.stream_name:
            self.desc = doc["uid"]

    def event(self, doc):
        if doc["descriptor"] != self.desc:
            return
        try:
            x = doc["data"][self.x]
        except KeyError:
            if self.x in ("time", "seq_num"):
                x = doc[self.x]
            else:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                x = self.eva.eval(self.x)
        try:
            y = doc["data"][self.y]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            y = self.eva.eval(self.y)
        try:
            z = doc["data"][self.z]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            z = self.eva.eval(self.z)
        self.update(x, y, z)
        self.new_data.emit()

    def make_colormesh(self, x_shape=None, y_shape=None):
        if x_shape is None and y_shape is None:
            return None
        elif x_shape is not None and y_shape is None:
            y_shape = int(np.array(self.x_data).size / x_shape)
        elif x_shape is None and y_shape is not None:
            x_shape = int(np.array(self.y_data).size / y_shape)
        try:
            x = np.array(self.x_data).reshape((x_shape, y_shape))
            y = np.array(self.y_data).reshape((x_shape, y_shape))
            c = np.array(self.z_data).reshape((x_shape, y_shape))
            return x, y, c
        except Exception as e:
            return None

    def update(self, x, y, z):
        x_shape = None
        y_shape = None
        if np.isscalar(z):
            z = np.array([z])
        if np.isscalar(x):
            x = np.full(z.shape, x)
        if np.isscalar(y):
            y = np.full(z.shape, y)

        self.x_data.extend(x)
        self.y_data.extend(y)
        self.z_data.extend(z)
        x_shape = len(set(self.x_data))
        y_shape = len(set(self.y_data))
        z_normed = (self.z_data - np.min(self.z_data)) / (
            np.max(self.z_data) - np.min(self.z_data)
        )
        mesh = self.make_colormesh(x_shape, y_shape)
        if mesh:
            x, y, z = mesh
            self.image.clear()
            self.image.setImage(z)
            self.image.setRect(pg.QtCore.QRectF(x.min(), y.min(), x.ptp(), y.ptp()))
            self.image.setLookupTable(self.cmap.getLookupTable())
            self.scatter_plot.hide()
            self.image.show()
            self.hist.show()
        else:
            colors = self.cmap.map(z_normed)
            self.scatter_plot.setData(x=self.x_data, y=self.y_data, brush=colors)
            self.image.hide()
            self.scatter_plot.show()

    def clear_plot(self):
        pass
