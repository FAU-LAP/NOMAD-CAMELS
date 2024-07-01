import sys
from collections import ChainMap
import threading
import numpy as np
import lmfit
from collections import deque

import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from bluesky.callbacks.mpl_plotting import LivePlot, LiveFitPlot
from bluesky.callbacks import LiveFit
from bluesky.callbacks.core import get_obj_fields
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QApplication,
    QPushButton,
    QTableWidgetItem,
    QColorDialog,
    QComboBox,
    QLabel,
    QLineEdit,
)
from PySide6.QtCore import Signal, QObject, Qt, QCoreApplication
from PySide6.QtGui import QIcon

from nomad_camels.gui.plot_options import Ui_Plot_Options
from nomad_camels.utility.fit_variable_renaming import replace_name
from nomad_camels.bluesky_handling.evaluation_helper import Evaluator
from ophyd import SignalRO, Device, Component, BlueskyInterface, Kind
from bluesky import plan_stubs as bps

from nomad_camels.utility.plot_placement import place_widget

from importlib import resources
from nomad_camels import graphics
from nomad_camels.ui_widgets.warn_popup import WarnPopup

stdCols = plt.rcParams["axes.prop_cycle"].by_key()["color"]

dark_mode = False


def activate_dark_mode():
    """Changes the plot-style to dark-mode."""
    global dark_mode
    dark_mode = True
    plt.style.use("dark_background")


class MPLwidget(FigureCanvasQTAgg):
    """Custom QT widget for displaying matplotlib plots.

    This class inherits from matplotlib's FigureCanvasQTAgg to create a custom
    QT widget for displaying matplotlib plots. In the init method, a new figure
    and axes are created using matplotlib.pyplot.subplots(). The grid is then
    displayed on the axes.

    Parameters
    ----------

    Returns
    -------

    """

    def __init__(self):
        fig, ax = plt.subplots()
        self.axes = ax
        self.axes.grid()
        super().__init__(fig)


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
        canvas = MPLwidget()
        if isinstance(y_names, str):
            y_names = [y_names]
        self.ax = canvas.axes
        self.x_name = x_name
        self.y_names = y_names
        self.stream_name = stream_name
        self.fits = fits or []
        self.liveFits = []
        self.liveFitPlots = []
        eva = Evaluator(namespace=namespace)
        self.ax2 = self.ax.twinx() if y_axes and 2 in y_axes.values() else None
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
                eva,
                init_guess,
                name=name,
                additional_data=add_data,
                params=params,
                stream_name=stream_name,
            )
            self.liveFits.append(livefit)
            if y_axes and y_axes[fit["y"]] == 2:
                ax = self.ax2
                ax_is2 = True
            else:
                ax = self.ax
                ax_is2 = False
            if fit["y"] in y_names:
                col = stdCols[y_names.index(fit["y"])]
            else:
                col = "black"
            self.liveFitPlots.append(
                Fit_Plot_No_Init_Guess(
                    livefit,
                    ax=ax,
                    legend_keys=[name],
                    ax_is2=ax_is2,
                    color=col,
                    display_values=fit["display_values"],
                )
            )
        self.livePlot = MultiLivePlot(
            y_names,
            x_name,
            legend_keys=legend_keys,
            xlim=xlim,
            ylim=ylim,
            epoch=epoch,
            ax=canvas.axes,
            evaluator=eva,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            stream_name=stream_name,
            do_plot=do_plot,
            fitPlots=self.liveFitPlots,
            y_axes=y_axes,
            multi_stream=multi_stream,
            ax2=self.ax2,
            **kwargs,
        )
        self.livePlot.new_data.connect(self.show)
        self.toolbar = NavigationToolbar2QT(canvas, self)

        self.pushButton_show_options = QPushButton("Show Options")
        self.pushButton_show_options.clicked.connect(self.show_options)
        self.pushButton_autoscale = QPushButton("Autoscale")
        self.pushButton_autoscale.clicked.connect(self.autoscale)
        self.pushButton_clear = QPushButton("Clear Plot")
        self.pushButton_clear.clicked.connect(self.clear_plot)
        self.plot_options = Plot_Options(self, self.ax, self.livePlot, self.ax2)
        label_n_data = QLabel("# data points:")
        self.lineEdit_n_data = QLineEdit(str(maxlen))
        self.lineEdit_n_data.returnPressed.connect(self.change_maxlen)

        layout = QGridLayout()
        layout.addWidget(canvas, 0, 1, 1, 6)
        layout.addWidget(self.toolbar, 1, 4)
        layout.addWidget(self.pushButton_show_options, 1, 1)
        layout.addWidget(self.pushButton_autoscale, 1, 2)
        layout.addWidget(self.pushButton_clear, 1, 3)
        layout.addWidget(label_n_data, 1, 5)
        layout.addWidget(self.lineEdit_n_data, 1, 6)
        layout.addWidget(self.plot_options, 0, 0, 2, 1)
        self.setLayout(layout)

        self.setWindowTitle(title or f"{x_name} vs. {y_names[0]}")
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "camels_icon.png")))

        self.plot_options.hide()
        self.options_open = False
        if do_plot:
            self.show()
            self.plot_options.checkBox_log_x.setChecked(logX)
            self.plot_options.checkBox_log_y.setChecked(logY)
            self.plot_options.checkBox_log_y2.setChecked(logY2)
            self.plot_options.set_log()
        place_widget(self)
        self.change_maxlen()

    def change_maxlen(self):
        """ """
        text = self.lineEdit_n_data.text()
        if (
            not text
            or text == "None"
            or text == "none"
            or text == "inf"
            or text == "np.inf"
        ):
            maxlen = np.inf
        else:
            try:
                maxlen = int(text)
            except:
                return
        self.livePlot.change_maxlen(maxlen)

    def clear_plot(self):
        """Clear the plot by removing the data from the plot and clearing all
        fit plots.

        Parameters
        ----------

        Returns
        -------

        """
        self.livePlot.clear_plot()
        for fit_plot in self.liveFitPlots:
            fit_plot.clear_plot()

    def autoscale(self):
        """Autoscale the plot's x and y axis."""
        self.ax.autoscale()
        self.ax.figure.canvas.draw_idle()

    def show_options(self):
        """Show or hide the options for the plot.
        Toggles between 'Show Options' and 'Hide Options' on the button press.

        Parameters
        ----------

        Returns
        -------

        """
        if self.options_open:
            self.pushButton_show_options.setText("Show Options")
            self.options_open = False
            self.plot_options.hide()
        else:
            self.pushButton_show_options.setText("Hide Options")
            self.options_open = True
            self.plot_options.show()
            self.plot_options.setup_table()
        self.adjustSize()

    def closeEvent(self, a0):
        """
        Overwrite the closeEvent to emit the closing signal before closing the
        window.

        Parameters
        ----------
        a0 :


        Returns
        -------

        """
        self.closing.emit()
        super().closeEvent(a0)


class LiveFit_Eva(LiveFit):
    """LiveFit_Eva is a subclass of LiveFit that adds the ability to evaluate the
    independent variables before fitting. It uses the given evaluator for that.

    Parameters
    ----------

    Returns
    -------


    """

    def __init__(
        self,
        model,
        y,
        independent_vars,
        evaluator,
        init_guess=None,
        additional_data=None,
        *,
        name="",
        params=None,
        stream_name="primary",
    ):
        super().__init__(
            model=model, y=y, independent_vars=independent_vars, init_guess=init_guess
        )
        self.eva = evaluator
        self.name = f"{name}_{stream_name}"
        self.params = params
        name = replace_name(name)
        # self.ophyd_fit = Fit_Ophyd(name, name=name, params=params,
        #                            parent_fit=self)
        self.stream_name = stream_name
        self.timestamp = None
        self.parent_plot = None
        self.__stale = True
        self.ready_to_read = False
        self.results = {}
        if isinstance(additional_data, list):
            self.additional_data = {}
            for d in additional_data:
                self.additional_data[d] = []
        else:
            self.additional_data = additional_data or {}
        self.read_ready = Fit_Signal(f"{self.name}_read_ready")

    def _reset(self):
        """Resets the fit, also sets the `ready_to_read` to False."""
        super()._reset()
        self.ready_to_read = False

    def event(self, doc):
        """Handles new events received by the fit. Evaluates the independent variables using the evaluator
        and updates the fit with the new data.

        Parameters
        ----------
        doc :


        Returns
        -------


        """
        idv = {}
        for k, v in self.independent_vars.items():
            try:
                new_x = doc["data"][v]
            except KeyError:
                if v in ("time", "seq_num"):
                    new_x = doc[v]
                else:
                    if not self.eva.is_to_date(doc["time"]):
                        self.eva.event(doc)
                    new_x = self.eva.eval(v)
            idv[k] = new_x

        try:
            y = doc["data"][self.y]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            y = self.eva.eval(self.y)
        # Always stash the data for the next time the fit is updated.
        self.update_caches(y, idv)
        self.timestamp = doc["time"]
        self.__stale = True

    def get_ready(self):
        """This function is used to set the ready_to_read attribute to True."""
        self.ready_to_read = True

    def update_fit(self):
        """Update the fit by evaluating the model with the current data.

        This method updates the fit by evaluating the current data using the
        model defined by the user. The method uses the `params` attribute, if
        available, to pass on the parameters to the fitting method. If the fit
        is not stale (i.e. no new data has arrived since the last update) the
        method will return without doing anything. Otherwise, the method updates
        the `result` attribute with the fit result and the `ophyd_fit` with the
        updated data. It also calls the `fit_has_result` method on the parent
        plot.
        Before doing anything, it will wait for `ready_to_read` to be True.

        Parameters
        ----------

        Returns
        -------

        """
        while not self.ready_to_read:
            yield from bps.sleep(0.1)
        if not self.__stale:
            return None
        kwargs = {}
        kwargs.update(self.independent_vars_data)
        kwargs.update(self.init_guess)
        try:
            if self.params:
                self.result = self.model.fit(self.ydata, params=self.params, **kwargs)
            else:
                self.result = self.model.fit(self.ydata, **kwargs)
        except Exception as e:
            print(f"Error in fit {self.name}: {e}")
            return None
        self.results[f"{self.timestamp}"] = self.result
        for d in self.additional_data:
            self.additional_data[d].append(self.eva.eval(d))
        self.__stale = False
        # self.ophyd_fit.update_data(self.result, self.timestamp)
        self.parent_plot.fit_has_result()


class Fit_Signal(SignalRO):
    """A subclass of ophyd.SignalRO for storing fit results

    This class is a subclass of ophyd.SignalRO, which is used to store the
    results of a fit.
    It has an additional method `update_data` that updates the readback value
    and timestamp metadata of the signal.

    Parameters
    ----------

    Returns
    -------


    """

    def __init__(
        self,
        name,
        value=0.0,
        timestamp=None,
        parent=None,
        labels=None,
        kind="hinted",
        tolerance=None,
        rtolerance=None,
        metadata=None,
        cl=None,
        attr_name="",
    ):
        super().__init__(
            name=name,
            value=value,
            timestamp=timestamp,
            parent=parent,
            labels=labels,
            kind=kind,
            tolerance=tolerance,
            rtolerance=rtolerance,
            metadata=metadata,
            cl=cl,
            attr_name=attr_name,
        )

    def update_data(self, result, timestamp):
        """Updates the readback value and timestamp metadata of the signal.
        Called by the parent's `update_data` function.

        Parameters
        ----------
        result :

        timestamp :


        Returns
        -------

        """
        self._readback = result
        self._metadata["timestamp"] = timestamp


class Fit_Ophyd(Device):
    """A device that extends the functionality of the Device class from Ophyd.
    It is included in the LiveFit_Eva class.

    Parameters
    ----------

    Returns
    -------


    """

    a = Component(Fit_Signal, name="a")
    b = Component(Fit_Signal, name="b")
    c = Component(Fit_Signal, name="c")
    d = Component(Fit_Signal, name="d")
    e = Component(Fit_Signal, name="e")
    f = Component(Fit_Signal, name="f")
    g = Component(Fit_Signal, name="g")
    h = Component(Fit_Signal, name="h")
    i = Component(Fit_Signal, name="i")
    j = Component(Fit_Signal, name="j")
    k = Component(Fit_Signal, name="k")
    l = Component(Fit_Signal, name="l")
    m = Component(Fit_Signal, name="m")
    n = Component(Fit_Signal, name="n")
    o = Component(Fit_Signal, name="o")
    p = Component(Fit_Signal, name="p")
    q = Component(Fit_Signal, name="q")
    r = Component(Fit_Signal, name="r")
    covar = Component(Fit_Signal, name="covar")
    read_ready = Component(Fit_Signal, name="read_ready")

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        params=None,
        parent_fit=None,
        **kwargs,
    ):
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        self.params = params.keys()
        self.order = [
            self.a,
            self.b,
            self.c,
            self.d,
            self.e,
            self.f,
            self.g,
            self.h,
            self.i,
            self.j,
            self.k,
            self.l,
            self.m,
            self.n,
            self.o,
            self.p,
            self.q,
            self.r,
        ]
        self.used_comps = [self.covar]
        for i, p in enumerate(self.params):
            self.used_comps.append(self.order[i])
        self.parent_fit = parent_fit

    def update_data(self, result, timestamp):
        """Update the data of all the components.
        For each fit parameter, the corresponding component is updated.

        Parameters
        ----------
        result : lmfit.model.ModelResult
            The result of the fit.

        timestamp : float
            The timestamp of the fit. Used to update the timestamp metadata of
            the components.

        Returns
        -------


        """
        self.used_comps = [self.covar]
        for i, comp in enumerate(self.params):
            if comp in result.best_values:
                self.order[i].update_data(result.best_values[comp], timestamp)
                self.used_comps.append(self.order[i])
                self.order[i].name = f"{self.name}_{comp}"
        if result is not None and result.covar is not None:
            self.covar.update_data(result.covar, timestamp)
        else:
            self.covar.update_data(None, timestamp)

    def read(self):
        """Overwrites the `read` method from `Device`.
        Stops reading, as soon as the number of parameters is reached.
        """
        res = BlueskyInterface.read(self)
        i = 1
        for _, component in self._get_components_of_kind(Kind.normal):
            res.update(component.read())
            i += 1
            if i > len(self.params):
                break
        return res


class Fit_Plot_No_Init_Guess(LiveFitPlot):
    """A subclass of LiveFitPlot that doesn't plot the initial guess for the fit."""

    def __init__(
        self,
        livefit,
        *,
        num_points=100,
        legend_keys=None,
        xlim=None,
        ylim=None,
        ax=None,
        ax_is2=False,
        display_values=False,
        **kwargs,
    ):
        # super().__init__(livefit, num_points=num_points, legend_keys=legend_keys,
        #                  xlim=xlim, ylim=ylim, ax=ax, **kwargs)
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()
        self.display_values = display_values
        if len(livefit.independent_vars) != 1:
            raise NotImplementedError(
                "LiveFitPlot supports models with one " "independent variable only."
            )

        def setup():
            # Run this code in start() so that it runs on the correct thread.
            nonlocal legend_keys, xlim, ylim, ax, kwargs, livefit
            with self.__setup_lock:
                if self.__setup_event.is_set():
                    return
                self.__setup_event.set()
            self.ax = ax
            # if legend_keys is None:
            #     legend_keys = []
            # self.legend_keys = ['scan_id'] + legend_keys
            (x,) = livefit.independent_vars.values()
            if x is not None:
                self.x, *others = get_obj_fields([x])
            else:
                self.x = "seq_num"
            y = livefit.y
            self.y, *others = get_obj_fields([y])
            if xlim is not None:
                self.ax.set_xlim(*xlim)
            if ylim is not None:
                self.ax.set_ylim(*ylim)
            # self.ax.margins(.1)
            self.kwargs = kwargs
            self.lines = []
            # self.legend = None
            # self.legend_title = " :: ".join([name for name in self.legend_keys])
            # self._epoch_offset = None  # used if x == 'time'
            # self._epoch = epoch

        (self.__x_key,) = livefit.independent_vars.keys()  # this never changes
        # x, = livefit.independent_vars.values()  # this may change
        self.num_points = num_points
        self._livefit = livefit
        self._xlim = xlim
        self._has_been_run = False
        livefit.parent_plot = self
        self.x_data = []
        self.y_data = []
        self.current_line = None
        self.x = None
        self.ax_is2 = ax_is2
        self.__setup = setup
        self.line_position = None
        self.text_objects = []

    def start(self, doc):
        """Overwrites the `start` method of LiveFitPlot to not display the
        init_guess_line.

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        # LivePlot.start(self, doc)
        self.__setup()
        # The doc is not used; we just use the signal that a new run began.
        # self._epoch_offset = doc['time']  # used if self.x == 'time'
        self.x_data, self.y_data = [], []
        (self.current_line,) = self.ax.plot([], [], **self.kwargs)
        self.lines.append(self.current_line)
        # legend = self.ax.legend(loc=0, title=self.legend_title)
        # try:
        #     # matplotlib v3.x
        #     self.legend = legend.set_draggable(True)
        # except AttributeError:
        #     # matplotlib v2.x (warns in 3.x)
        #     self.legend = legend.draggable(True)
        self.livefit.start(doc)
        (self.x,) = self.livefit.independent_vars.keys()  # in case it changed
        # Put fit above other lines (default 2) but below text (default 3).
        [line.set_zorder(2.5) for line in self.lines]
        # if self.legend_keys:
        #     self.current_line.set_label(self.legend_keys[-1])
        # legend = self.ax.legend(loc=0, title='')
        # if not self.ax_is2:
        #     try:
        #         legend.set_draggable(True)
        #     except AttributeError:
        #         legend.draggable(True)
        # else:
        #     self.ax.get_legend().remove()

    def get_ready(self):
        """Passes the command to the `_livefit`"""
        self._livefit.get_ready()

    def event(self, doc):
        """Passes the event to the `livefit`

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        self.livefit.event(doc)

    def fit_has_result(self):
        """If the `livefit` has a result, a resulting line is calculated, and the
        plot is updated.
        Called by LiveFit_Eva.update_fit().

        Parameters
        ----------

        Returns
        -------

        """
        if self.livefit.result is not None:
            # Evaluate the model function at equally-spaced points.
            # To determine the domain of x, use xlim if available. Otherwise,
            # use the range of x points measured up to this point.
            if self._xlim is None:
                x_data = self.livefit.independent_vars_data[self.__x_key]
                xmin, xmax = np.min(x_data), np.max(x_data)
            else:
                xmin, xmax = self._xlim
            x_points = np.linspace(xmin, xmax, self.num_points)
            kwargs = {self.__x_key: x_points}
            kwargs.update(self.livefit.result.values)
            self.y_data = self.livefit.result.model.eval(**kwargs)
            self.x_data = x_points
            # update kwargs to initial guess
            kwargs.update(self.livefit.result.init_values)
            self.update_plot()
        # Intentionally override LivePlot.event. Do not call super().

    def clear_plot(self):
        """Empties the data of the current plot line."""
        if self.current_line:
            self.current_line.set_data([], [])

    def update_plot(self):
        """Sets the current x and y data, then calls the `parent_plot` to update."""
        self.current_line.set_data(self.x_data, self.y_data)
        self.parent_plot.update_plot()
        if self.display_values:
            for text_object in self.text_objects:
                text_object.remove()
            self.text_objects.clear()
            vals = self.livefit.result.values
            if self.line_position is None:
                self.line_position = self.parent_plot.line_number
                self.parent_plot.line_number += len(vals)
            color = self.current_line.get_color()
            for i, (key, value) in enumerate(vals.items()):
                text_object = self.parent_plot.ax.text(
                    0.05,
                    0.95 - (i + self.line_position) * 0.05,
                    f"{key}: {value:.2e}",
                    transform=self.ax.transAxes,
                    verticalalignment="top",
                    color=color,
                )
                self.text_objects.append(text_object)


class Plot_Options(Ui_Plot_Options, QWidget):
    """Widget for setting the options of a plot.

    Parameters
    ----------
    parent : QWidget, optional
        The parent widget.
    ax : matplotlib.axes.Axes, optional
        The axes to plot on.
    livePlot : LivePlot, optional
        The LivePlot to set the options for.
    ax2 : matplotlib.axes.Axes, optional
        The second (y) axes to plot on.
    """

    def __init__(self, parent=None, ax=None, livePlot=None, ax2=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ax = ax
        self.ax2 = ax2
        self.livePlot = livePlot
        self.livePlot.setup_done.connect(self.setup_table)
        self.checkBox_log_x.clicked.connect(self.set_log)
        self.checkBox_log_y.clicked.connect(self.set_log)
        self.checkBox_log_y2.clicked.connect(self.set_log)
        self.checkBox_use_abs_x.clicked.connect(self.set_log)
        self.checkBox_use_abs_y.clicked.connect(self.set_log)
        self.checkBox_use_abs_y2.clicked.connect(self.set_log)
        self.color_widges = []
        self.marker_widges = []
        self.linestyle_widges = []
        self.axis_widges = []
        self.marker_dict = {}
        self.linestyle_dict = {}

    def setup_table(self, x=None, y=None):
        """Sets up the table with the current lines in the plot."""
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setMinimumWidth(400)
        self.tableWidget.setHorizontalHeaderLabels(
            ["Name", "marker", "color", "linestyle", "y-axis"]
        )
        self.tableWidget.verticalHeader().setHidden(True)
        for i, line in enumerate(self.ax.lines):
            if not self.marker_dict:
                self.marker_dict = {v: k for k, v in line.markers.items()}
                self.linestyle_dict = {
                    "".join(v.split("_")[2:]): k for k, v in line.lineStyles.items()
                }
            self.tableWidget.insertRow(i)
            item = QTableWidgetItem(line.get_label())
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 0, item)

            markerwidge = QComboBox()
            markerwidge.addItems(self.marker_dict.keys())
            markerwidge.setCurrentText(line.markers[line.get_marker()])
            markerwidge.currentTextChanged.connect(lambda x, n=i: self.change_marker(n))
            self.marker_widges.append(markerwidge)
            self.tableWidget.setCellWidget(i, 1, markerwidge)

            colorwidge = QPushButton(line.get_color())
            colorwidge.clicked.connect(lambda n=i: self.change_color(n))
            self.color_widges.append(colorwidge)
            self.tableWidget.setCellWidget(i, 2, colorwidge)

            linestylewidge = QComboBox()
            linestylewidge.addItems(self.linestyle_dict.keys())
            # print(line.get_linestyle)
            linestylewidge.setCurrentText(
                "".join(line.lineStyles[line.get_linestyle()].split("_")[2:])
            )
            linestylewidge.currentTextChanged.connect(
                lambda x, n=i: self.change_linestyle(n)
            )
            self.linestyle_widges.append(linestylewidge)
            self.tableWidget.setCellWidget(i, 3, linestylewidge)

            # axiswidge = QComboBox()
            # axiswidge.addItems(['1', '2'])
            # axiswidge.setCurrentText('1')
            # axiswidge.currentTextChanged.connect(lambda x, n=i: self.change_axis(n))
            # self.axis_widges.append(axiswidge)
            # self.tableWidget.setCellWidget(i, 4, axiswidge)
        self.tableWidget.resizeColumnsToContents()

    def change_linestyle(self, row):
        """Changes the linestyle of the selected line in the plot.

        Parameters
        ----------
        row : int
            The row of the line in the table.
        """
        linestyle = self.linestyle_widges[row].currentText()
        name = self.ax.lines[row].get_label()
        self.livePlot.current_lines[name].set_linestyle(self.linestyle_dict[linestyle])
        self.ax.lines[row].set_linestyle(self.linestyle_dict[linestyle])
        self.ax.figure.canvas.draw_idle()

    def change_marker(self, row):
        """

        Parameters
        ----------
        row :


        Returns
        -------

        """
        marker = self.marker_widges[row].currentText()
        name = self.ax.lines[row].get_label()
        self.livePlot.current_lines[name].set_marker(self.marker_dict[marker])
        self.ax.lines[row].set_marker(self.marker_dict[marker])
        self.ax.figure.canvas.draw_idle()

    def change_color(self, row):
        """

        Parameters
        ----------
        row :


        Returns
        -------

        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_widges[row].setText(color.name())
            line = self.ax.lines[row]
            line.set_color(color.name())
            name = self.ax.lines[row].get_label()
            self.livePlot.current_lines[name].set_color(color.name())
            self.ax.figure.canvas.draw_idle()

    def set_log(self):
        """ """
        x = self.checkBox_log_x.isChecked()
        x_scale = "log" if x else "linear"
        self.checkBox_use_abs_x.setEnabled(x)
        y = self.checkBox_log_y.isChecked()
        y_scale = "log" if y else "linear"
        self.checkBox_use_abs_y.setEnabled(y)
        y2 = self.checkBox_log_y2.isChecked()
        y2_scale = "log" if y2 else "linear"
        self.checkBox_use_abs_y2.setEnabled(y2)
        self.ax.set_xscale(x_scale)
        self.ax.set_yscale(y_scale)
        if self.ax2:
            self.ax2.set_yscale(y2_scale)
        self.livePlot.use_abs = {
            "x": self.checkBox_use_abs_x.isChecked() and x,
            "y": self.checkBox_use_abs_y.isChecked() and y,
            "y2": self.checkBox_use_abs_y2.isChecked() and y2,
        }
        self.livePlot.update_plot()


class MultiLivePlot(LivePlot, QObject):
    """ """

    new_data = Signal()
    setup_done = Signal()

    def __init__(
        self,
        ys=(),
        x=None,
        *,
        legend_keys=None,
        xlim=None,
        ylim=None,
        ax=None,
        epoch="run",
        xlabel="",
        ylabel="",
        evaluator=None,
        title="",
        stream_name="primary",
        do_plot=True,
        fitPlots=None,
        multi_stream=False,
        y_axes=None,
        ax2=None,
        ylabel2="",
        **kwargs,
    ):
        LivePlot.__init__(
            self,
            y=ys[0],
            x=x,
            legend_keys=legend_keys,
            xlim=xlim,
            ylim=ylim,
            ax=ax,
            epoch=epoch,
            **kwargs,
        )
        QObject.__init__(self)
        self.use_abs = {"x": False, "y": False, "y2": False}
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()
        self.eva = evaluator
        self.stream_name = stream_name
        self.desc = []
        self.do_plot = do_plot
        self.multi_stream = multi_stream
        self.fitPlots = fitPlots or []
        self.y_axes = y_axes or {}
        self.ax2 = ax2
        for fit in self.fitPlots:
            fit.parent_plot = self
        if isinstance(ys, str):
            ys = [ys]

        def setup():
            """ """
            # Run this code in start() so that it runs on the correct thread.
            nonlocal ys, x, legend_keys, xlim, ylim, ax, epoch, kwargs, xlabel, ylabel, title
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
                self.x = "seq_num"
            self.ys = get_obj_fields(ys)
            # a = ylabel or ys[0]
            # print(a)
            self.ax.set_ylabel(ylabel or ys[0])
            self.ax.set_xlabel(xlabel or x or "sequence #")
            if title:
                self.ax.set_title(title)
            if xlim is not None:
                self.ax.set_xlim(*xlim)
            if ylim is not None:
                self.ax.set_ylim(*ylim)
            self.ax.margins(0.1)
            self.kwargs = kwargs
            self.lines = []
            self.legend = None
            # self.legend_title = " :: ".join([name for name in self.legend_keys])
            self._epoch_offset = None  # used if x == 'time'
            self._epoch = epoch

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ylabel2 = ylabel2
        self.__setup = setup
        self._epoch_offset = 0
        self.x_data = []
        self.y_data = {}
        self.maxlen = np.inf
        self.y_names = ys
        self.ys = get_obj_fields(ys)
        for y in ys:
            self.y_data[y] = []
        self.current_lines = {}
        self.descs_fit_readying = {}
        self.legend = None
        self.line_number = 0

    def change_maxlen(self, maxlen):
        """

        Parameters
        ----------
        maxlen :


        Returns
        -------

        """
        self.maxlen = maxlen
        if maxlen < np.inf:
            self.x_data = deque(self.x_data, maxlen=maxlen)
            for y in self.y_data:
                self.y_data[y] = deque(self.y_data[y], maxlen=maxlen)
        else:
            self.x_data = list(self.x_data)
            for y in self.y_data:
                self.y_data[y] = list(self.y_data[y])

    def start(self, doc):
        """

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        self.__setup()
        # The doc is not used; we just use the signal that a new run began.
        # self._epoch_offset = doc['time']  # used if self.x == 'time'
        # self.x_data = []
        # self.y_data = {}
        # for y in self.ys:
        #     self.y_data[y] = []
        # label = " :: ".join(
        # [str(doc.get(name, name)) for name in self.legend_keys])
        kwargs = ChainMap({"ls": "None", "marker": "x"})
        self.current_lines = {}
        for i, y in enumerate(self.ys):
            try:
                if y in self.y_axes and self.y_axes[y] == 2:
                    (self.current_lines[y],) = self.ax2.plot(
                        [], [], label=self.legend_keys[i], color=stdCols[i], **kwargs
                    )
                    self.ax.plot(
                        [], [], label=self.legend_keys[i], color=stdCols[i], **kwargs
                    )
                else:
                    (self.current_lines[y],) = self.ax.plot(
                        [], [], label=self.legend_keys[i], color=stdCols[i], **kwargs
                    )
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
        for fit in self.fitPlots:
            fit.start(doc)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        if self.ax2:
            self.ax2.set_ylabel(self.ylabel2)
        self.setup_done.emit()

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
        elif doc["name"].startswith(f"{self.stream_name}_fits_readying_"):
            for fit in self.fitPlots:
                if (
                    doc["name"]
                    == f"{self.stream_name}_fits_readying_{fit.livefit.name}"
                ):
                    self.descs_fit_readying[doc["uid"]] = fit
        elif self.multi_stream and doc["name"].startswith(self.stream_name):
            self.desc.append(doc["uid"])

    def clear_plot(self):
        """ """
        self.x_data.clear()
        for y in self.y_data:
            self.y_data[y].clear()

    def event(self, doc):
        """Unpack data from the event and call self.update_plot().

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        # This outer try/except block is needed because multiple event
        # streams will be emitted by the RunEngine and not all event
        # streams will have the keys we want.
        # This inner try/except block handles seq_num and time, which could
        # be keys in the data or accessing the standard entries in every
        # event.
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

        new_y = {}
        for y in self.ys:
            try:
                new_y[y] = doc["data"][y]
            except KeyError:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_y[y] = self.eva.eval(y)

        # Special-case 'time' to plot against against experiment epoch, not
        # UNIX epoch.
        if self.x == "time" and self._epoch == "run":
            new_x -= self._epoch_offset

        self.update_caches(new_x, new_y)
        for fit in self.fitPlots:
            fit.event(doc)
        self.update_plot()
        # super().event(doc)

    def update_caches(self, x, ys):
        """

        Parameters
        ----------
        x :

        ys :


        Returns
        -------

        """
        for y in ys:
            self.y_data[y].append(ys[y])
        self.x_data.append(x)

    def update_plot(self):
        """ """
        for y, line in self.current_lines.items():
            xdat = np.abs(self.x_data) if self.use_abs["x"] else self.x_data
            ydat = np.abs(self.y_data[y]) if self.use_abs["y"] else self.y_data[y]
            line.set_data(xdat, ydat)
        # Rescale and redraw.
        try:
            self.ax.relim(visible_only=True)
            self.ax.autoscale_view(tight=True)
            if self.ax2:
                self.ax2.relim(visible_only=True)
                self.ax2.autoscale_view(tight=True)
            self.ax.figure.canvas.draw_idle()
            self.new_data.emit(None)
        except:
            pass

    def stop(self, doc):
        """

        Parameters
        ----------
        doc :


        Returns
        -------

        """
        if not self.x_data:
            print(
                "MultiLivePlot did not get any data that corresponds to the "
                "x axis. {}".format(self.x)
            )
        for y in self.y_data:
            if not self.y_data[y]:
                print(
                    "MultiLivePlot did not get any data that corresponds to the "
                    "y axis. {}".format(y)
                )
            if len(self.y_data[y]) != len(self.x_data):
                print(
                    "MultiLivePlot has a different number of elements for x ({}) and"
                    "y ({}, {})".format(len(self.x_data), len(self.y_data), y)
                )
        for fit in self.fitPlots:
            fit.stop(doc)


class PlotWidget_NoBluesky(QWidget):
    """ """

    def __init__(
        self,
        xlabel="",
        ylabel="",
        parent=None,
        title="",
        ylabel2="",
        y_axes=None,
        labels=(),
        first_hidden=None,
        show_plot=True,
        maxlen=np.inf,
    ):
        app = QCoreApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        super().__init__(parent=parent)
        canvas = MPLwidget()
        self.ax = canvas.axes
        self.plot = MultiPlot_NoBluesky(
            self.ax, xlabel, ylabel, ylabel2, y_axes, labels, first_hidden, show_plot
        )
        self.toolbar = NavigationToolbar2QT(canvas, self)

        self.pushButton_show_options = QPushButton("Show Options")
        self.pushButton_show_options.clicked.connect(self.show_options)
        self.pushButton_autoscale = QPushButton("Autoscale")
        self.pushButton_autoscale.clicked.connect(self.autoscale)
        self.pushButton_clear = QPushButton("Clear Plot")
        self.pushButton_clear.clicked.connect(self.clear_plot)
        self.plot_options = Plot_Options(self, self.ax, self.plot)
        label_n_data = QLabel("# data points:")
        self.lineEdit_n_data = QLineEdit(str(maxlen))
        self.lineEdit_n_data.returnPressed.connect(self.change_maxlen)
        self.change_maxlen()

        self.setWindowTitle(title or f"{xlabel} vs. {ylabel}")
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "camels_icon.png")))

        layout = QGridLayout()
        layout.addWidget(canvas, 0, 1, 1, 6)
        layout.addWidget(self.toolbar, 1, 4)
        layout.addWidget(self.pushButton_show_options, 1, 1)
        layout.addWidget(self.pushButton_autoscale, 1, 2)
        layout.addWidget(self.pushButton_clear, 1, 3)
        layout.addWidget(label_n_data, 1, 5)
        layout.addWidget(self.lineEdit_n_data, 1, 6)
        layout.addWidget(self.plot_options, 0, 0, 2, 1)
        self.setLayout(layout)

        self.plot_options.hide()
        self.options_open = False
        self.show()

    def change_maxlen(self):
        """ """
        text = self.lineEdit_n_data.text()
        if not text:
            maxlen = np.inf
        else:
            try:
                maxlen = int(text)
            except:
                return
        self.plot.change_maxlen(maxlen)

    def clear_plot(self):
        """Clear the plot by removing the data from the plot and clearing all
        fit plots.

        Parameters
        ----------

        Returns
        -------

        """
        self.plot.clear_plot()

    def autoscale(self):
        """ """
        self.ax.autoscale()
        self.plot.ax2.autoscale()
        self.ax.figure.canvas.draw_idle()

    def show_options(self):
        """ """
        if self.options_open:
            self.pushButton_show_options.setText("Show Options")
            self.options_open = False
            self.plot_options.hide()
        else:
            self.pushButton_show_options.setText("Hide Options")
            self.options_open = True
            self.plot_options.show()
        self.adjustSize()


class MultiPlot_NoBluesky(QObject):
    """ """

    new_data = Signal()
    setup_done = Signal()

    def __init__(
        self,
        ax,
        xlabel="",
        ylabel="",
        ylabel2="",
        y_axes=None,
        labels=(),
        first_hidden=None,
        show_plot=True,
    ):
        super().__init__()
        self.ax = ax
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax2 = self.ax.twinx()
        self.ax2.set_ylabel(ylabel2)
        self.labels = labels
        self.maxlen = np.inf
        self.xdata = []
        self.ydata = {}
        self.current_lines = {}
        self.y_axes = y_axes or {}
        self.first_hidden = first_hidden or []
        self.show_plot = show_plot
        self.use_abs = {"x": False, "y": False, "y2": False}

    def add_data(self, x, ys, add=True):
        """

        Parameters
        ----------
        x :

        ys :

        add :
             (Default value = True)

        Returns
        -------

        """
        if not self.current_lines:
            if len(self.labels) != len(ys):
                self.labels = list(ys.keys())
            for i, y in enumerate(ys):
                try:
                    if y in self.y_axes and self.y_axes[y] == 2:
                        (self.current_lines[y],) = self.ax2.plot(
                            [],
                            [],
                            linestyle="" if y in self.first_hidden else "-",
                            label=self.labels[i],
                            color=stdCols[i],
                        )
                        self.ax.plot(
                            [],
                            [],
                            linestyle="" if y in self.first_hidden else "-",
                            label=self.labels[i],
                            color=stdCols[i],
                        )
                    else:
                        (self.current_lines[y],) = self.ax.plot(
                            [],
                            [],
                            linestyle="" if y in self.first_hidden else "-",
                            label=self.labels[i],
                            color=stdCols[i],
                        )
                    if self.maxlen < np.inf:
                        self.ydata[y] = deque(maxlen=self.maxlen)
                    else:
                        self.ydata[y] = []
                except Exception as e:
                    print(e)
            self.setup_done.emit()
        if add:
            self.xdata.append(x)
            for y in ys:
                if y in self.ydata:
                    self.ydata[y].append(ys[y])
        else:
            self.xdata = [x]
            self.ydata.clear()
            for y in ys:
                self.ydata[y] = [ys[y]]
        if self.show_plot:
            self.update_plot()

    def change_maxlen(self, maxlen):
        """

        Parameters
        ----------
        maxlen :


        Returns
        -------

        """
        self.maxlen = maxlen
        if maxlen < np.inf:
            self.xdata = deque(self.xdata, maxlen=maxlen)
            for y in self.ydata:
                self.ydata[y] = deque(self.ydata[y], maxlen=maxlen)
        else:
            self.xdata = list(self.xdata)
            for y in self.ydata:
                self.ydata[y] = list(self.ydata[y])

    def update_plot(self):
        """ """
        for y, line in self.current_lines.items():
            xdat = np.abs(self.xdata) if self.use_abs["x"] else self.xdata
            ydat = np.abs(self.ydata[y]) if self.use_abs["y"] else self.ydata[y]
            line.set_data(xdat, ydat)
        # Rescale and redraw.
        self.ax.relim(visible_only=True)
        self.ax.autoscale_view(tight=True)
        self.ax.legend()
        self.ax.figure.canvas.draw_idle()
        self.new_data.emit()

    def clear_plot(self):
        """ """
        self.xdata.clear()
        for y in self.ydata:
            self.ydata[y].clear()


# if __name__ == '__main__':
#     from bluesky import RunEngine
#     from bluesky.plans import scan
#     from ophyd.sim import motor, det
#
#     motor.delay = 0.1
#
#     def plan():
#         for i in range(4, 5):
#             yield from scan([det], motor, -5, 5, 3**i)
#
#     RE = RunEngine()
#     app = QApplication(sys.argv)
#     # myapp = PlotWidget(run_engine=RE, x_name='motor', y_names=['det'], title='test', xlabel='aaaa', ylabel='bbbb')
#     myapp = PlotWidget('motor', ['det', 'det**2', 'sin(motor)'])
#     myapp.show()
#     RE.subscribe(myapp.livePlot)
#     RE(plan())
#     sys.exit(app.exec())
