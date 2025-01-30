from plotly import graph_objs as go
from plotly.subplots import make_subplots
from bluesky.callbacks import CallbackBase
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
import sys
import os
import threading
from multiprocessing import Process, Event, Manager
import json
from nomad_camels.utility.fit_variable_renaming import replace_name

sys.path.append(os.path.dirname(__file__).split("nomad_camels")[0])
import numpy as np
from PySide6.QtCore import QThread
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

import requests
from flask import request as flask_request


default_colors = [
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


def run_dash_app(
    web_port,
    wait_for_dash_app_event,
    x_name,
    y_names,
    y_axes,
    xlabel,
    ylabel,
    ylabel2,
    title,
    logX,
    logY,
    logY2,
    maxlen,
    fits,
):
    fit_model_dict = {}
    data = {x_name: []}
    for y_name in y_names:
        data[y_name] = []
    dash_app = Dash("Browser Plots")
    # Define the app layout
    dash_app.layout = html.Div(
        [
            dcc.Graph(id="scatter-plot"),
            dcc.Interval(
                id="graph-update",
                interval=500,  # Update every 0.2 second
                n_intervals=0,
            ),
        ]
    )

    # Add custom endpoint to get the fit results.
    @dash_app.server.route("/fit_result", methods=["POST"])
    def fit_result():
        """
        Endpoint that receives the fit results
        from the query string, for example:
        """
        nonlocal data, x_name, y_names
        # Retrieve parameters from the query string
        try:
            json_payload = flask_request.json
            fit_result = json_payload["best_fit"]  # Access the "best_fit" key
            name = json_payload["name"]  # Access the "name" key
            fit_params = json_payload["fit_params"]  # Access the "fit_params" key
            y_axis_name = json_payload["y_axis_name"]

            # Add the fit result to the data dictionary
            data[f"fit_{name}"] = {
                "fit_result": fit_result,
                "fit_params": fit_params,
                "y_axis_name": y_axis_name,
            }
            return "Data successfully updated", 200
        except ValueError:
            return f"Invalid data value: {fit_result}", 400

    # Add a custom endpoint to receive data from CAMELS
    @dash_app.server.route("/add_data", methods=["GET"])
    def add_data():
        """
        Endpoint that receives x, y
        from the query string, for example:
        GET /add_data?x=1.23&y=4.56
        """
        nonlocal data, x_name, y_names
        # Retrieve parameters from the query string
        x_value = flask_request.args.get("x")  # returns None if not present
        y_value = flask_request.args.get("y")  # optional
        # Validate that x, y exist
        if x_value is None or y_value is None:
            return "Missing required x or y parameter", 400
        try:
            data[x_name].append(float(x_value))
            for y_name in y_names:
                data[y_name].append(float(json.loads(y_value)[y_name]))
            return "Data successfully updated", 200
        except ValueError:
            return f"Invalid data value: {x_value}, {y_value}", 400

    # Update the scatter plot dynamically
    @dash_app.callback(
        Output("scatter-plot", "figure"),
        Input("graph-update", "n_intervals"),
    )
    def update_scatter_plot(_):
        """ """
        nonlocal data, title, xlabel, ylabel, ylabel2, logX, logY, logY2, maxlen, y_axes, fits, fit_model_dict
        # Create the scatter plot
        # If there is only the index in in the y_axes dict, plot all y_values on the same axis

        for fit in fits:
            if fit["use_custom_func"]:
                model = lmfit.models.ExpressionModel(fit["custom_func"])
                label = "custom"
            else:
                model = lmfit.models.lmfit_models[fit["predef_func"]]()
                label = fit["predef_func"]
            model_name = f"{label}_{fit['y']}_v_{fit['x']}"
            fit_model_dict[model_name] = model

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i, y_name in enumerate(y_names):
            scatter = go.Scatter(
                x=data[x_name],
                y=data[y_name],
                mode="markers",
                marker=dict(size=10, color=i, opacity=0.8),
                name=y_name,
            )
            secondary_y = False if y_axes[y_name] == 1 else True
            fig.add_trace(scatter, secondary_y=secondary_y)

            # Add the fit result trace
            for key in list(data.keys()):
                if key.startswith("fit_"):
                    if data[key]["y_axis_name"] == y_name:
                        fit_name = key[4:]
                        for fit_model_name, fit in fit_model_dict.items():
                            if replace_name(fit_model_name) in fit_name:
                                fit_data = data[key]
                                x_data = np.linspace(
                                    min(data[x_name]),
                                    max(data[x_name]),
                                    len(data[x_name]) * 2,
                                )
                                params = lmfit.Parameters()
                                for param_name, param_value in fit_data[
                                    "fit_params"
                                ].items():
                                    params.add(
                                        param_name, value=param_value
                                    )  # Ensure correct conversion
                                fit_y_points = fit.eval(params=params, x=x_data)
                                fit_result_trace = go.Scatter(
                                    x=x_data,
                                    y=fit_y_points,
                                    mode="lines",  # Lines instead of markers for the fit result
                                    line=dict(
                                        color="red", dash="dash"
                                    ),  # Dashed line for the fit
                                    name=f"fit_{y_name}",
                                )
                                fig.add_trace(fit_result_trace, secondary_y=secondary_y)

        layout = go.Layout(
            title=title,
            xaxis={
                "title": xlabel,
                "type": "log" if logX else "linear",
            },
            yaxis={
                "title": ylabel,
                "type": "log" if logY else "linear",
            },
            # Configure a secondary y-axis on the right if needed
            yaxis2=dict(
                title=ylabel2,
                type="log" if logY2 else "linear",
                overlaying="y",
                side="right",
            ),
            margin={"l": 40, "r": 20, "t": 40, "b": 30},
            uirevision=True,
        )

        # Return the figure dictionary
        return {
            "data": fig.data,
            "layout": layout,
        }

    wait_for_dash_app_event.set()
    dash_app.run(host="127.0.0.1", port=web_port, debug=False, use_reloader=False)


class PlotlyLiveCallback(CallbackBase):
    """
    A Bluesky callback that caches x- and y-values whenever an event is emitted.
    We'll later read these values in the Dash app to update the figure.
    Only takes a single y-value for now!
    """

    def __init__(
        self,
        x_name,
        y_names,
        evaluator,
        web_port,
        fits=None,
        **kwargs,
    ):
        CallbackBase.__init__(self)
        self.fits = fits
        self.x_name = x_name
        self.y_axes: dict = kwargs.get("y_axes")
        self.y_names = y_names or self.y_axes.keys()
        # Get plot labels
        self.xlabel = kwargs.get("xlabel", self.x_name or "sequence #")
        self.ylabel = kwargs.get("ylabel", self.y_names[0] or "value")
        self.ylabel2 = kwargs.get("ylabel2")
        self.title = kwargs.get("title", f"{self.xlabel} vs. {self.ylabel}")
        self.logX = kwargs.get("logX", False)
        self.logY = kwargs.get("logY", False)
        self.logY2 = kwargs.get("logY2", False)
        self.maxlen = kwargs.get("maxlen", "inf")

        self.eva = evaluator
        # self.dash_app = dash_app
        self.web_port = web_port
        self.stream_name = kwargs.get("stream_name")
        self.multi_stream = kwargs.get("multi_stream")

        self.desc = []
        self.ignore_fit_docs = []
        self.setup_is_done = False
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()

    def start(self, doc):
        wait_for_dash_app_event = Event()
        self.setup()
        self.dash_process = Process(
            target=run_dash_app,
            kwargs={
                "x_name": self.x_name,
                "y_names": self.y_names,
                "y_axes": self.y_axes,
                "xlabel": self.xlabel,
                "ylabel": self.ylabel,
                "ylabel2": self.ylabel2,
                "title": self.title,
                "logX": self.logX,
                "logY": self.logY,
                "logY2": self.logY2,
                "maxlen": self.maxlen,
                "web_port": self.web_port,
                "wait_for_dash_app_event": wait_for_dash_app_event,
                "fits": self.fits,
            },
        )
        self.dash_process.start()
        wait_for_dash_app_event.wait()

    def event(self, doc):
        """Called every time the RunEngine emits an event document."""
        if doc["descriptor"] not in self.desc:
            return
        elif doc["uid"] in self.ignore_fit_docs:
            return
        try:
            new_x = doc["data"][self.x_name]
        except KeyError:
            if self.x_name in ("time", "seq_num"):
                new_x = doc[self.x_name]
            else:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_x = self.eva.eval(self.x_name, do_not_reraise=True)
        if self.x_name == "time" and self._epoch == "run":
            new_x -= self._epoch_offset

        new_y = {}
        for y_name in self.y_names:
            try:
                new_y[y_name] = doc["data"][y_name]
            except KeyError:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_y[y_name] = self.eva.eval(y_name, do_not_reraise=True)
        try:
            response = requests.get(
                f"http://127.0.0.1:{self.web_port}/add_data",
                params={"x": new_x, "y": json.dumps(new_y)},
            )
            if response.status_code == 200:
                pass
            else:
                print(f"Failed to add data point: {response.text}")
        except requests.ConnectionError:
            print("Cannot connect to Dash server. Is it running?")

    def stop(self, doc):
        import time
        if hasattr(self, "dash_process") and self.dash_process.is_alive():
            time.sleep(1)
            self.dash_process.terminate()
            self.dash_process.join()
            self.dash_process = None
            print("Terminated the dash app process.")

    def clear_data(self):
        """A helper to clear the data between runs if desired."""
        self.x_data = []
        self.y_data = []

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
            self.ignore_fit_docs.append(doc["uid"])
        elif self.multi_stream and doc["name"].startswith(self.stream_name):
            self.desc.append(doc["uid"])

    def setup(self):
        with self.__setup_lock:
            if self.__setup_event.is_set():
                return
            self.__setup_event.set()
        self.setup_is_done = True


def run_dash_app_2d(
    web_port,
    wait_for_dash_app_event,
    x_name,
    y_name,
    z_name,
    xlabel,
    ylabel,
    title,
    maxlen,
):
    import plotly.express as px
    import pandas as pd

    data = {x_name: [], y_name: [], z_name: []}
    dash_app = Dash("Browser Plots")
    # Define the app layout
    dash_app.layout = html.Div(
        [
            dcc.Graph(id="scatter-plot"),
            dcc.Interval(
                id="graph-update",
                interval=5000,  # Update every 0.2 second
                n_intervals=0,
            ),
        ]
    )

    # Add a custom endpoint to receive data from CAMELS
    @dash_app.server.route("/add_data_2d", methods=["GET"])
    def add_data_2d():
        """
        Endpoint that receives x, y and z data
        from the query string, for example:
        """
        nonlocal data, x_name, y_name, z_name
        # Retrieve parameters from the query string
        x_value = flask_request.args.get("x")  # returns None if not present
        y_value = flask_request.args.get("y")
        z_value = flask_request.args.get("z")  # optional
        # Validate that x, y exist
        if x_value is None or y_value is None:
            return "Missing required x or y parameter", 400
        try:
            data[x_name].append(float(x_value))
            data[y_name].append(float(y_value))
            data[z_name].append(float(z_value))
            return "Data successfully updated", 200
        except ValueError:
            return f"Invalid data value: {x_value}, {y_value}, {z_value}", 400

    # Update the scatter plot dynamically
    @dash_app.callback(
        Output("scatter-plot", "figure"),
        Input("graph-update", "n_intervals"),
    )
    def update_scatter_plot(_):
        """ """
        nonlocal data, title, xlabel, ylabel, maxlen
        # Create the scatter plot
        # If there is only the index in in the y_axes dict, plot all y_values on the same axis
        # Create the scatter plot
        # Create a DataFrame from the lists
        data_pd = pd.DataFrame(
            {"x": data[x_name], "y": data[y_name], "z": data[z_name]}
        )
        fig = px.scatter(
            data_pd,
            x="x",
            y="y",
            color="z",
            color_continuous_scale="Viridis",
            title=title,
            labels={x_name: xlabel, y_name: ylabel, z_name: z_name},
        )

        # Return the figure
        return fig

    wait_for_dash_app_event.set()
    dash_app.run(host="127.0.0.1", port=web_port, debug=False, use_reloader=False)


class PlotlyLiveCallback_2d(CallbackBase):
    """
    A Bluesky callback that caches x-, y- and z values whenever an event is emitted.
    We'll later read these values in the Dash app to update the figure.
    Only takes a single y-value for now!
    These are the plot options:
    plot_info = dict(x_name="ElapsedTime", y_names=['opcInst_n1', 'opcInst_v2'], ylabel="opcInst_n1", xlabel="ElapsedTime", title="", stream_name=stream, namespace=namespace, fits=fits, multi_stream=True, y_axes={'opcInst_n1': 1, 'opcInst_v2': 2}, ylabel2="opcInst_v2", logX=False, logY=False, logY2=False, maxlen="inf", top_left_x="0", top_left_y="0", plot_width="", plot_height="")
    """

    def __init__(
        self,
        x_name,
        y_name,
        z_name,
        evaluator,
        web_port,
        **kwargs,
    ):
        CallbackBase.__init__(self)
        self.x_name = x_name
        self.y_name = y_name
        self.z_name = z_name
        # Get plot labels
        self.xlabel = kwargs.get("xlabel", self.x_name or "x value")
        self.ylabel = kwargs.get("ylabel", self.y_name or "y value")
        self.zlabel = kwargs.get("zlabel", self.z_name or "z value")
        self.title = kwargs.get("title", f"{self.xlabel} vs. {self.ylabel}")
        self.maxlen = kwargs.get("maxlen", "inf")

        self.eva = evaluator
        # self.dash_app = dash_app
        self.web_port = web_port
        self.stream_name = kwargs.get("stream_name")
        self.multi_stream = kwargs.get("multi_stream")

        self.desc = []
        self.ignore_fit_docs = []
        self.setup_is_done = False
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()

    def start(self, doc):
        wait_for_dash_app_event = Event()
        self.setup()
        self.dash_process = Process(
            target=run_dash_app_2d,
            kwargs={
                "x_name": self.x_name,
                "y_name": self.y_name,
                "z_name": self.z_name,
                "xlabel": self.xlabel,
                "ylabel": self.ylabel,
                "title": self.title,
                "maxlen": self.maxlen,
                "web_port": self.web_port,
                "wait_for_dash_app_event": wait_for_dash_app_event,
            },
        )
        self.dash_process.start()
        wait_for_dash_app_event.wait()

    def event(self, doc):
        """Called every time the RunEngine emits an event document."""
        if doc["descriptor"] not in self.desc:
            return
        elif doc["uid"] in self.ignore_fit_docs:
            return
        try:
            x = doc["data"][self.x_name]
        except KeyError:
            if self.x in ("time", "seq_num"):
                x = doc[self.x_name]
            else:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                x = self.eva.eval(self.x, do_not_reraise=True)
        try:
            y = doc["data"][self.y_name]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            y = self.eva.eval(self.y_name, do_not_reraise=True)
        try:
            z = doc["data"][self.z_name]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            z = self.eva.eval(self.z_name, do_not_reraise=True)
        try:
            response = requests.get(
                f"http://127.0.0.1:{self.web_port}/add_data_2d",
                params={"x": x, "y": y, "z": z},
            )
            if response.status_code == 200:
                pass
            else:
                print(f"Failed to add data point: {response.text}")
        except requests.ConnectionError:
            print("Cannot connect to Dash server. Is it running?")

    def stop(self, doc):
        if hasattr(self, "dash_process") and self.dash_process.is_alive():
            self.dash_process.terminate()
            self.dash_process.join()
            self.dash_process = None
            print("Terminated the dash app process.")

    def clear_data(self):
        """A helper to clear the data between runs if desired."""
        self.x_data = []
        self.y_data = []

    def descriptor(self, doc):
        """
        This method is called when a new descriptor document is received. If the descriptor is relevant, (compared with `self.stream_name`), the uid of the descriptor is added to the list of relevant descriptors. If the descriptor is a fit descriptor, the fit stream is added to the list of fits.

        Parameters
        ----------
        doc : dict
            The descriptor document
        """
        if doc["name"] == self.stream_name:
            self.desc = doc["uid"]

    def setup(self):
        with self.__setup_lock:
            if self.__setup_event.is_set():
                return
            self.__setup_event.set()
        self.setup_is_done = True
