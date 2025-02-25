"""This module contains the classes for the plot widgets, based on pyqtgraph."""

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
    QApplication,
)
from PySide6.QtCore import Signal, QObject, QEvent, Qt, QCoreApplication
from PySide6.QtGui import QIcon, QColor
import PySide6
import pyqtgraph as pg
from pyqtgraph.GraphicsScene.mouseEvents import MouseClickEvent

import lmfit
from importlib import resources
from nomad_camels import graphics

from bluesky.callbacks.core import get_obj_fields, CallbackBase

from nomad_camels.gui.plot_options import Ui_Plot_Options
from nomad_camels.utility.fit_variable_renaming import replace_name
from nomad_camels.bluesky_handling.evaluation_helper import Evaluator
from nomad_camels.main_classes.plot_widget import LiveFit_Eva
from nomad_camels.utility.plot_placement import place_widget

# recognized by pyqtgraph: r, g, b, c, m, y, k, w
dark_mode_colors = ["w", "r", (0, 100, 255), "g", "c", "m", "y", "k"]

# these are the colors used by matplotlib, they are used as default colors in light mode
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

# these are the symbols recognized by pyqtgraph
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

# these are the linestyles recognized by pyqtgraph
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
    """Changes the plot-style to dark-mode, by changing the config options of pyqtgraph."""
    global dark_mode, colors
    dark_mode = True
    pg.setConfigOptions(background="k", foreground="w")
    colors = dark_mode_colors


class ListDeque_skip:
    def __init__(self, iterable=None, maxlen=None, skip_n_points=0):
        if iterable is None:
            iterable = []
        self.maxlen = maxlen
        self.skip_n_points = skip_n_points
        self.counter_value = 0
        if (
            maxlen is None
            or maxlen == np.inf
            or (isinstance(maxlen, str) and maxlen.lower() in ["none", "inf", "np.inf"])
        ):
            self.data = list(iterable)
        else:
            if not isinstance(maxlen, int):
                maxlen = int(maxlen)
            self.data = deque(iterable, maxlen=maxlen)

    def append(self, item):
        self.counter_value += 1
        if self.skip_n_points <= 0 or self.counter_value % self.skip_n_points == 0:
            self.data.append(item)

    def extend(self, iterable):
        self.data.extend(iterable)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return repr(self.data)

    def clear(self):
        self.data.clear()

    def pop(self):
        return self.data.pop()

    def popleft(self):
        if isinstance(self.data, deque):
            return self.data.popleft()
        else:
            raise AttributeError("'list' object has no attribute 'popleft'")

    def appendleft(self, item):
        if isinstance(self.data, deque):
            self.data.appendleft(item)
        else:
            raise AttributeError("'list' object has no attribute 'appendleft'")

    def extendleft(self, iterable):
        if isinstance(self.data, deque):
            self.data.extendleft(iterable)
        else:
            raise AttributeError("'list' object has no attribute 'extendleft'")

    def rotate(self, n=1):
        if isinstance(self.data, deque):
            self.data.rotate(n)
        else:
            raise AttributeError("'list' object has no attribute 'rotate'")

    def change_maxlen(self, maxlen):
        self.maxlen = maxlen
        if maxlen is None or maxlen == np.inf:
            self.data = list(self.data)
        else:
            self.data = deque(self.data, maxlen=maxlen)

    def change_skip_n_points(self, skip_n_points):
        self.skip_n_points = skip_n_points
        self.counter_value = 0


class PlotWidget(QWidget):
    """Class for creating a plot widget.

    Parameters
    ----------
    x_name : str
        The name of the x-axis variable
    y_names : Union[str, Tuple[str]]
        The name(s) of the y-axis variable(s)
    legend_keys : List[str]
        deprecated
    xlim : Tuple[float, float]
        deprecated
    ylim : Tuple[float, float]
        deprecated
    epoch : {'run', 'unix'}
        If 'run' t=0 is the time recorded in the RunStart document. If 'unix',
        t=0 is 1 Jan 1970 ("the UNIX epoch"). Default is 'run'.
    parent : QWidget, optional
        The parent widget, by default None
    namespace : Mapping[str, Any], optional
        The namespace to use for the `Evaluator`, by default None
    ylabel : str, optional
        The y-axis label, if empty the first y_name is used, by default ''
    xlabel : str, optional
        The x-axis label, if empty the x_name is used, by default ''
    title : str, optional
        The title of the plot, by default ''
    stream_name : str
        The name of the bluesky stream to be used for the plot. If multi_stream is True, streams including this name are used. Default is 'primary'
    fits : List[Dict[str, Union[str, bool, List[str], Tuple[float, float], Dict[str, Union[str, float]]]]], optional
        The fits for the plot, by default None
    do_plot : bool
        deprecated
    multi_stream : bool, optional
        Whether to use multiple streams, see stream name, by default False
    y_axes : Dict[str, int], optional
        The y-axis to use for each y_name, the ints should be 1 or 2, if 2, the respective y-value is plotted on the right axis, by default None
    logX : bool
        Whether to use a logarithmic x-axis, by default False
    logY : bool
        Whether to use a logarithmic y-axis, by default False
    logY2 : bool
        Whether to use a logarithmic y-axis for the right axis, by default False
    top_left_x : int, optional
        The x-coordinate of the top left corner of the plot widget, by default None
    top_left_y : int, optional
        The y-coordinate of the top left corner of the plot widget, by default None
    plot_width : int, optional
        The width of the plot widget, by default None
    plot_height : int, optional
        The height of the plot widget, by default None
    maxlen : int
        The maximum number of data points to show, by default np.inf
    use_bluesky : bool
    **kwargs : Any, optional
        Additional keyword arguments to pass to `MultiLivePlot`
    """

    closing = Signal()
    reopened = Signal()

    def __init__(
        self,
        x_name,
        y_names=None,
        *,
        legend_keys=None,
        xlim=None,
        ylim=None,
        epoch="run",
        parent=None,
        namespace=None,
        ylabel="",
        xlabel="",
        ylabel2="",
        title="",
        stream_name="primary",
        fits=None,
        do_plot=True,
        multi_stream=False,
        y_axes=None,
        logX=False,
        logY=False,
        logY2=False,
        manual_plot_position=False,
        top_left_x="",
        top_left_y="",
        plot_width="",
        plot_height="",
        maxlen=np.inf,
        use_bluesky=True,
        labels=(),
        first_hidden=None,
        show_in_browser=False,
        web_port=None,
        evaluator=None,
        **kwargs,
    ):
        super().__init__(parent=parent)
        self.plot_widget = pg.PlotWidget()
        self.x_name = x_name
        self.y_names = y_names or y_axes.keys()
        self.stream_name = stream_name
        self.fits = fits or []
        self.eva = evaluator
        self.liveFits = []
        self.liveFitPlots = []
        self.ax2_viewbox = None
        self.setWindowTitle(title or f"{x_name} vs. {y_names[0]}")
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "camels_icon.png")))

        ax2 = None
        plotItem = self.plot_widget.getPlotItem()
        if y_axes and 2 in y_axes.values():
            self.ax2_viewbox = pg.ViewBox()
            plotItem.scene().addItem(self.ax2_viewbox)
            ax2 = plotItem.getAxis("right")
            self.ax2_viewbox.setXLink(plotItem)
            ax2 = pg.AxisItem("right")
            ax2.setLabel(ylabel2 or self.y_names[0])
            ax2.linkToView(self.ax2_viewbox)
            plotItem.layout.addItem(ax2, 2, 3)

            # This makes the second y-axis move with the viewbox of the main plot
            def updateViews():
                self.ax2_viewbox.setGeometry(plotItem.vb.sceneBoundingRect())
                self.ax2_viewbox.linkedViewChanged(plotItem.vb, self.ax2_viewbox.XAxis)

            updateViews()
            plotItem.vb.sigResized.connect(updateViews)

        # create the fits
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
                show_in_browser=show_in_browser,
                web_port=web_port,
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

        # create the main plot, either with or without using bluesky callbacks
        if use_bluesky:
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
        else:
            self.livePlot = LivePlot_NoBluesky(
                self.plot_widget.getPlotItem(),
                ax2_viewbox=self.ax2_viewbox,
                ax2_axis=ax2,
                xlabel=xlabel,
                ylabel=ylabel,
                ylabel2=ylabel2,
                y_axes=y_axes,
                labels=labels,
                first_hidden=first_hidden,
            )
        self.livePlot.plotItem.showGrid(True, True)
        self.livePlot.new_data_signal.connect(self.show_again)
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
        label_skip_n_points = QLabel("skip n points:")
        self.lineEdit_skip_n_points = QLineEdit("0")
        self.lineEdit_skip_n_points.returnPressed.connect(self.change_skip_n_points)
        skip_tool_tip = "Skip n points in the plot before plotting the next value. This may be useful for long measurements to speed up plotting and free up memory."
        label_skip_n_points.setToolTip(skip_tool_tip)
        self.lineEdit_skip_n_points.setToolTip(skip_tool_tip)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.plot_widget, 0, 1, 1, 6)
        self.layout().addWidget(self.pushButton_show_options, 2, 1)
        self.layout().addWidget(self.pushButton_clear, 2, 2)
        self.layout().addWidget(label_n_data, 2, 5)
        self.layout().addWidget(self.lineEdit_n_data, 2, 6)
        self.layout().addWidget(label_skip_n_points, 2, 3)
        self.layout().addWidget(self.lineEdit_skip_n_points, 2, 4)
        self.layout().addWidget(self.plot_options, 0, 0, 3, 1)
        self.plot_options.hide()
        # self.setMinimumSize(500, 400)
        if manual_plot_position:
            place_widget(self, top_left_x, top_left_y, plot_width, plot_height)
        else:
            place_widget(self)
        # self.adjustSize()
        self.change_maxlen()

    def show_again(self):
        if not self.isVisible():
            self.show()
            self.reopened.emit()

    def make_toolbar(self):
        """Creates the toolbar for the plot widget. This toolbar is based on the context menu of the plot. The View All is connected with `auto_range`."""
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
        self.layout().addWidget(self.toolbar, 1, 1, 1, 6)
        self.plot_options.set_log()

    def auto_range(self):
        """Also call the auto range for the second y-axis if it exists."""
        self.livePlot.plotItem.vb.autoRange()
        if self.ax2_viewbox:
            self.ax2_viewbox.autoRange()

    def change_maxlen(self):
        """
        Changes the maximum number of data points to show in the plot. Reads the value from the line edit and sets it as the new maximum length.
        """
        text = self.lineEdit_n_data.text()
        if not text or text.lower() in ["none", "inf", "np.inf"]:
            maxlen = np.inf
        else:
            try:
                maxlen = int(text)
            except ValueError:
                return
        self.livePlot.change_maxlen(maxlen)

    def change_skip_n_points(self):
        text = self.lineEdit_skip_n_points.text()
        if not text:
            skip_n_points = 0
        else:
            try:
                skip_n_points = int(text)
            except ValueError:
                return
        self.livePlot.change_skip_n_points(skip_n_points)

    def show_options(self):
        """
        Shows or hides the plot options. If the options are shown, the button text is changed to "Hide Options", otherwise it is changed to "Show Options".
        """
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
        """
        Clears the plot and the fits.
        """
        self.livePlot.clear_plot()
        for fit in self.liveFitPlots:
            fit.clear_plot()

    def closeEvent(self, event):
        """
        Emits the closing signal when the widget is closed.
        """
        self.closing.emit()
        super().closeEvent(event)


class Plot_Options(Ui_Plot_Options, QWidget):
    """
    Class for the plot options widget. This widget is used to change the appearance of the plot, such as the color, linestyle, marker, and log-scale of the axes.

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget, by default None
    livePlot : LivePlot
        The LivePlot object connected to the plot widget, by default None
    """

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
        """
        Updates the items in the table widget to match the items in the plot.
        """
        self.all_items.clear()
        self.items_in_2.clear()
        items_viewbox_1 = self.livePlot.plotItem.vb.allChildItems()
        # get all PlotDataItems in the first y-axis
        for item in items_viewbox_1:
            if isinstance(item, pg.PlotDataItem):
                self.all_items[item.name()] = item
        # get all PlotDataItems in the second y-axis
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
            colorwidge.clicked.connect(lambda state, n=i: self.change_color(n))
            self.tableWidget.setCellWidget(i, 3, colorwidge)

    def change_symbol(self, symbol, row):
        """
        Changes the symbol of a PlotDataItem connected to the specified `row`.

        Parameters
        ----------
        symbol : str
            The new symbol
        row : int
            The row of the item in the table widget
        """
        name = self.tableWidget.item(row, 0).text()
        self.change_color(row, just_update=True)
        self.all_items[name].setSymbol(symbols[symbol])

    def change_color(self, row, just_update=False):
        """
        Changes the color of a PlotDataItem connected to the specified `row`.

        Parameters
        ----------
        row : int
            The row of the item in the table widget
        just_update : bool, (default: False)
            If True, only updates the color of the item to the one already set. If False, opens a color dialog to choose a new color.
        """
        item = self.tableWidget.cellWidget(row, 3)
        if just_update:
            color = QColor(item.text())
        else:
            color = QColorDialog.getColor()
            if not color.isValid():
                return
        item.setText(color.name())
        name = self.tableWidget.item(row, 0).text()
        self.all_items[name].opts["pen"].setColor(color)
        self.all_items[name].setSymbolPen(pg.mkPen(color=color))
        self.all_items[name].setSymbolBrush(pg.mkBrush(color=color))

    def set_log(self):
        """
        Sets the log-scale of the axes according to the checkboxes.
        """
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
    """
    Bluesky callback class for live plotting. This class is used to update the plot with new data.

    Parameters
    ----------
    x_name : str
        The name of the x-axis variable
    y_names : List[str]
        The name(s) of the y-axis variable(s)
    plot_item : pg.PlotItem
        The plot item to plot the data on
    maxlen : [int, np.inf], (default: np.inf)
        The maximum number of data points to show
    multi_stream : bool, (default: False)
        Whether to use multiple streams. If True, all streams including the `stream_name` are used.
    evaluator : Evaluator
        The evaluator object used to evaluate expressions.
    stream_name : str, (default: 'primary')
        The name of the bluesky stream to use for the plot.
    y_axes : Dict[str, int], (default: None)
        The y-axis to use for each y_name, the ints should be 1 or 2, if 2, the respective y-value is plotted on the right axis
    title : str, (default: '')
        The title of the plot
    xlabel : str, (default: '')
        The x-axis label, if empty the x_name is used
    ylabel : str, (default: '')
        The y-axis label, if empty the first y_name is used
    epoch : {'run', 'unix'}, (default: 'run')
        If 'run' t=0 is the time recorded in the RunStart document. If 'unix', t=0 is 1 Jan 1970 ("the UNIX epoch").
    ax2_viewbox : pg.ViewBox, (default: None)
        The viewbox for the second y-axis
    ax2_axis : pg.AxisItem, (default: None)
        The axis for the second y-axis
    fitPlots : List[LiveFitPlot], (default: [])
        The fit plots connected to the plot.
    """

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
        self.setup_is_done = False

        def setup():
            # this is the setup function, it is called when the first event is received
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
            self.setup_is_done = True

        self.x_data = ListDeque_skip(maxlen=maxlen)
        self.y_data = {}
        self.y_axes = y_axes or {}
        self.maxlen = maxlen
        self.stream_name = stream_name
        self.eva = evaluator
        self.y_names = y_names
        self.ys = get_obj_fields(y_names)
        for y in y_names:
            self.y_data[y] = ListDeque_skip(maxlen=maxlen)
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

    def add_plot(self, y):
        i = self.ys.index(y)
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

    def start(self, doc):
        """
        This method is called when the RunStart document is received. It sets up the plot and the fits.

        Parameters
        ----------
        doc : dict
            The RunStart document
        """
        self.__setup()
        for i, y in enumerate(self.ys):
            try:
                self.add_plot(y)
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
        self.eva.start(doc)

    def descriptor(self, doc):
        """
        This method is called when a new descriptor document is received. If the descriptor is relevant, (compared with `self.stream_name`), the uid of the descriptor is added to the list of relevant descriptors. If the descriptor is a fit descriptor, the fit stream is added to the list of fits.

        Parameters
        ----------
        doc : dict
            The descriptor document
        """
        if not self.setup_is_done:
            self.start(doc)
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
        """
        This method is called when a new event document is received. If the descriptor of the event is not in the list of relevant descriptors, the event is ignored. Otherwise, the data is extracted from the event and added to the plot.

        Parameters
        ----------
        doc : dict
            The event document
        """
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
        # Check to see if doc["data"] contains keys matching any on the self.ys strings or self.x
        if not (any(key in s for key in doc["data"] for s in self.ys)): #or self.x in doc["data"]):
            print("The data of the event does not match the data ")
            return
        try:
            new_x = doc["data"][self.x]
        except KeyError:
            if self.x in ("time", "seq_num"):
                new_x = doc[self.x]
            else:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_x = self.eva.eval(self.x, do_not_reraise=True)
        if self.x == "time" and self._epoch == "run":
            new_x -= self._epoch_offset

        new_y = {}
        for y in self.ys:
            try:
                new_y[y] = doc["data"][y]
            except KeyError:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                try:
                    new_y[y] = self.eva.eval(y, do_not_reraise=True)
                except ValueError as e:
                    print("Error getting data for plot", e)
                    return
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
        plot_x = np.asarray(plot_x)
        if plot_x.ndim > 1:
            plot_x = plot_x[-1]
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
            plot_y = np.asarray(plot_y)
            if plot_y.ndim > 1:
                plot_y = plot_y[-1]
            if not y in self.current_plots:
                self.add_plot(y)
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
        for y in self.current_plots:
            self.current_plots[y].setData([], [])
        self.x_data = ListDeque_skip(maxlen=self.maxlen)
        for y in self.y_data:
            self.y_data[y] = ListDeque_skip(maxlen=self.maxlen)
        for fit in self.fitPlots:
            fit.clear_plot()
        self.update_plot()

    def change_maxlen(self, maxlen):
        self.maxlen = maxlen
        self.x_data.change_maxlen(maxlen)
        for y in self.y_data:
            self.y_data[y].change_maxlen(maxlen)

    def change_skip_n_points(self, n):
        self.x_data.skip_n_points = n
        for y in self.y_data:
            self.y_data[y].skip_n_points = n


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
            x_points = np.linspace(
                np.min(x_data), np.max(x_data), max(self.num_points, len(x_data))
            )
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
            variables = self.livefit.result.var_names
            if self.line_position is None:
                self.line_position = self.parent_plot.line_number
                self.parent_plot.line_number += len(variables)
            for i, (name, value) in enumerate(vals.items()):
                if name not in variables:
                    continue
                if self.livefit.result.covar is not None:
                    error = np.sqrt(self.livefit.result.covar[i, i])
                    text = pg.TextItem(
                        f"{name}: {value:.3e} ± {error:.3e}", color=self.color
                    )
                else:
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
    reopened = Signal()

    def __init__(
        self,
        x_name,
        y_name,
        z_name,
        parent=None,
        evaluator=None,
        xlabel="",
        ylabel="",
        zlabel="",
        title="",
        maxlen=np.inf,
        stream_name="primary",
        manual_plot_position=False,
        top_left_x="",
        top_left_y="",
        plot_width="",
        plot_height="",
        **kwargs,
    ):
        super().__init__(parent=parent)
        self.setWindowTitle(
            title or f"{zlabel or z_name} vs. {xlabel or x_name}, {ylabel or y_name}"
        )
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "camels_icon.png")))
        self.graphics_layout = pg.GraphicsLayoutWidget()
        self.plot = self.graphics_layout.addPlot(col=0, row=0)
        self.x_name = x_name
        self.y_name = y_name
        self.z_name = z_name
        self.plot.setLabel("bottom", xlabel or x_name)
        self.plot.setLabel("left", ylabel or y_name)
        self.stream_name = stream_name

        self.toolbar = None
        eva = evaluator
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
        self.livePlot.new_data.connect(self.show_again)
        label_n_data = QLabel("# data points:")
        self.lineEdit_n_data = QLineEdit(str(maxlen))
        self.lineEdit_n_data.returnPressed.connect(self.change_maxlen)
        self.pushButton_clear = QPushButton("Clear Plot")
        self.pushButton_clear.clicked.connect(self.clear_plot)

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.graphics_layout, 0, 0, 1, 3)
        self.layout().addWidget(self.pushButton_clear, 2, 0)
        self.layout().addWidget(label_n_data, 2, 1)
        self.layout().addWidget(self.lineEdit_n_data, 2, 2)
        self.make_toolbar()
        if manual_plot_position:
            place_widget(self, top_left_x, top_left_y, plot_width, plot_height)
        else:
            place_widget(self)
        self.adjustSize()
        self.change_maxlen()

    def change_maxlen(self):
        """
        Changes the maximum number of data points to show in the plot. Reads the value from the line edit and sets it as the new maximum length.
        """
        text = self.lineEdit_n_data.text()
        if not text or text.lower() in ["none", "inf", "np.inf"]:
            maxlen = np.inf
        else:
            try:
                maxlen = int(text)
            except ValueError:
                return
        self.livePlot.change_maxlen(maxlen)

    def show_again(self):
        if not self.isVisible():
            self.show()
            self.reopened.emit()

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
        self.layout().addWidget(self.toolbar, 1, 0, 1, 3)

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
        self.dummy_image = pg.ImageItem()
        # Remove the old colorbar if it exists
        if hasattr(self, "color_bar") and self.color_bar is not None:
            self.graphics_layout.removeItem(self.color_bar)
        # Remove the old hist if it exists
        if hasattr(self, "hist") and self.hist is not None:
            self.graphics_layout.removeItem(self.hist)
        self.color_bar = pg.ColorBarItem(label=self.z, interactive=False)
        self.color_bar.setColorMap(self.cmap)
        self.color_bar.setImageItem(self.dummy_image)
        # self.color_bar.sigLevelsChanged.connect(self.update_scatter)
        self.plotItem.addItem(self.scatter_plot)
        self.image = pg.ImageItem()
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.image)
        self.hist.autoHistogramRange()
        self.hist.gradient.setColorMap(self.cmap)
        self.hist.axis.setLabel(self.z)
        self.graphics_layout.addItem(self.hist, row=0, col=1)
        self.hist.hide()
        self.color_bar.hide()
        self.graphics_layout.addItem(self.color_bar, row=0, col=2)
        self.plotItem.addItem(self.image)
        self._epoch_offset = None
        self._epoch = "run"

    def update_scatter(self):
        try:
            current_map = self.color_bar.getColorMap()
            colors = current_map.map(self.z_normed)
            self.scatter_plot.setData(x=self.x_data, y=self.y_data, brush=colors)
        except Exception as e:
            pass

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
                x = self.eva.eval(self.x, do_not_reraise=True)
        try:
            y = doc["data"][self.y]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            y = self.eva.eval(self.y, do_not_reraise=True)
        try:
            z = doc["data"][self.z]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            z = self.eva.eval(self.z, do_not_reraise=True)
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
        mesh = self.make_colormesh(x_shape, y_shape)
        
        if mesh:
            x, y, z = mesh
            if not self.x_data:
                return
            self.image.clear()
            self.image.setImage(z)
            self.image.setRect(pg.QtCore.QRectF(x.min(), y.min(), np.ptp(x), np.ptp(y)))
            self.image.setLookupTable(self.cmap.getLookupTable())
            self.scatter_plot.hide()
            self.color_bar.hide()
            self.image.show()
            self.hist.show()
        else:
            # Check for case that all z values are 0
            if np.all(np.array(self.z_data) == 0):
                self.z_normed = np.zeros(len(self.z_data))
            else:
                self.z_normed = (self.z_data - np.min(self.z_data)) / (
                    np.max(self.z_data) - np.min(self.z_data)
                )
            self.dummy_image.setImage(np.array([self.z_data]))
            self.color_bar.setLevels((np.min(self.z_data), np.max(self.z_data)))
            colors = self.cmap.map(self.z_normed)
            self.scatter_plot.setData(x=self.x_data, y=self.y_data, brush=colors)
            self.image.hide()
            self.hist.hide()
            self.scatter_plot.show()
            self.color_bar.show()

    def clear_plot(self):
        self.x_data.clear()
        self.y_data.clear()
        self.z_data.clear()
        self.update(self.x_data, self.y_data, self.z_data)

    def change_maxlen(self, maxlen):
        self.maxlen = maxlen
        if maxlen < np.inf:
            self.x_data = deque(self.x_data, maxlen=maxlen)
            self.y_data = deque(self.y_data, maxlen=maxlen)
            self.z_data = deque(self.z_data, maxlen=maxlen)
        else:
            self.x_data = list(self.x_data)
            self.y_data = list(self.y_data)
            self.z_data = list(self.z_data)


class LivePlot_NoBluesky(QObject):
    new_data_signal = Signal()
    setup_done_signal = Signal()

    def __init__(
        self,
        plotItem,
        xlabel,
        ylabel,
        ylabel2,
        y_axes,
        ax2_viewbox=None,
        ax2_axis=None,
        labels=(),
        first_hidden=None,
    ):
        super().__init__()
        self.plotItem = plotItem
        self.plotItem.setLabel("bottom", xlabel)
        self.plotItem.setLabel("left", ylabel)
        self.ax2_viewbox = ax2_viewbox
        self.ax2_axis = ax2_axis
        if self.ax2_axis:
            self.ax2_axis.setLabel("right", ylabel2)
        self.labels = labels
        self.maxlen = np.inf
        self.x_data = []
        self.y_data = {}
        self.y_axes = y_axes or {}
        self.first_hidden = first_hidden or []
        self.use_abs = {"x": False, "y": False, "y2": False}
        self.current_plots = {}
        self.n_plots = 0
        self.show_plot = True

    def add_data(self, x, ys, add=True):
        if not self.current_plots:
            if len(self.labels) != len(ys):
                self.labels = list(ys.keys())
            for i, y in enumerate(ys):
                try:
                    color = colors[self.n_plots % len(colors)]
                    if y in self.y_axes and self.y_axes[y] == 2:
                        self.current_plots[y] = plot = pg.PlotDataItem(
                            [],
                            [],
                            label=self.labels[i],
                            name=self.labels[i],
                            symbol=None,
                            symbolPen=pg.mkPen(color=color),
                            symbolBrush=pg.mkBrush(color=color),
                            pen=pg.mkPen(
                                color=color,
                                width=2,
                                style=linestyles[
                                    "none" if y in self.first_hidden else "solid"
                                ],
                            ),
                        )
                        self.ax2_viewbox.addItem(plot)
                    else:
                        self.current_plots[y] = self.plotItem.plot(
                            [],
                            [],
                            label=self.labels[i],
                            name=self.labels[i],
                            symbol=None,
                            symbolPen=pg.mkPen(color=color),
                            symbolBrush=pg.mkBrush(color=color),
                            pen=pg.mkPen(
                                color=color,
                                width=2,
                                style=linestyles[
                                    "none" if y in self.first_hidden else "solid"
                                ],
                            ),
                        )
                    if self.maxlen < np.inf:
                        self.y_data[y] = deque(maxlen=self.maxlen)
                    else:
                        self.y_data[y] = []
                    self.n_plots += 1
                except Exception as e:
                    print(e)
            self.setup_done_signal.emit()
        if add:
            self.x_data.append(x)
            for y in ys:
                if y in self.y_data:
                    self.y_data[y].append(ys[y])
        else:
            self.x_data = [x]
            self.y_data.clear()
            for y in ys:
                self.y_data[y] = [ys[y]]
        if self.show_plot:
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

    def update_plot(self):
        if self.plotItem.getAxis("bottom").logMode and self.use_abs["x"]:
            plot_x = np.abs(self.x_data)
        else:
            plot_x = self.x_data
        plot_x = np.asarray(plot_x)
        if plot_x.ndim > 1:
            plot_x = plot_x[-1]
        for y in self.labels:
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
            plot_y = np.asarray(plot_y)
            if plot_y.ndim > 1:
                plot_y = plot_y[-1]
            self.current_plots[y].setData(plot_x, plot_y)
        self.new_data_signal.emit()

    def clear_plot(self):
        for y in self.y_data:
            self.current_plots[y].setData([], [])
        self.x_data = []
        for y in self.y_data:
            self.y_data[y] = []
        self.update_plot()
