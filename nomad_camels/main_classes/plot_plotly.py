import sys
import os
import threading
import json
import requests
import numpy as np
import lmfit

# For running the Dash app in a separate process.
from multiprocessing import Process, Event

# Flask request is used to receive query parameters or JSON from POST/GET in the Dash server.
from flask import request as flask_request

# Import necessary Plotly components for creating and manipulating plots.
from plotly import graph_objs as go

# Subplots allow multiple traces with secondary y-axes, etc.
from plotly.subplots import make_subplots

# Core components for building Dash layout and interactive elements.
from dash import dcc, html, Dash

# For reactive callbacks in Dash (linking outputs to inputs).
from dash.dependencies import Input, Output

# Extend Python's module search path for the current file location.
sys.path.append(os.path.dirname(__file__).split("nomad_camels")[0])

# For substituting variable names in the fit model.
from nomad_camels.utility.fit_variable_renaming import replace_name

from bluesky.callbacks.core import CallbackBase

# A predefined set of colors used for the plotly traces.
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
    """
    This function creates and runs a Dash application in a separate process.
    It defines a Plotly figure that updates automatically with incoming data.

    Parameters
    ----------
    web_port : int
        The TCP port on which the Dash server will listen for requests.
    wait_for_dash_app_event : multiprocessing.Event
        An event used to signal that the Dash app is fully started and ready.
    x_name : str
        The key under which x-values will be stored in the data dictionary.
    y_names : list of str
        A list of keys under which y-values will be stored in the data dictionary.
    y_axes : dict
        A dictionary that maps each y-name to the axis it should be associated with
        (1 for the left/primary y-axis and 2 for the right/secondary y-axis).
    xlabel : str
        Label for the x-axis in the generated Plotly figure.
    ylabel : str
        Label for the primary y-axis in the generated Plotly figure.
    ylabel2 : str
        Label for the secondary y-axis (on the right) in the generated Plotly figure.
    title : str
        The main title of the Plotly figure.
    logX : bool
        If True, the x-axis is displayed on a logarithmic scale.
    logY : bool
        If True, the primary y-axis is displayed on a logarithmic scale.
    logY2 : bool
        If True, the secondary y-axis is displayed on a logarithmic scale.
    maxlen : str or int
        Maximum number of data points to keep in the lists (if needed). "inf" for unlimited.
    fits : list of dict
        A list of fit definitions, where each dict describes a predefined lmfit model
        or a custom expression model, along with associated x and y variables.

    Notes
    -----
    - The Dash server uses custom endpoints ("/fit_result" and "/add_data") to receive data.
    - The Plotly figure updates periodically via a Dash Interval component. This ensures
      the graph is automatically refreshed with incoming data points and fit curves.
    - The server runs in debug=False mode and does not use a reloader to avoid issues
      in subprocess execution.
    """

    # Dictionary to store different fit models by their name for repeated usage.
    fit_model_dict = {}

    # Data dictionary stores x values under x_name and each y under its own key.
    data = {x_name: []}
    for y_name in y_names:
        data[y_name] = []

    # Create a new Dash instance with the name "Browser Plots".
    dash_app = Dash("Browser Plots")

    # Define the layout of the Dash application, including the Graph and an Interval component.
    dash_app.layout = html.Div(
        [
            dcc.Graph(id="scatter-plot"),
            dcc.Interval(
                id="graph-update",
                interval=500,  # Interval for periodic update checks (ms).
                n_intervals=0,
            ),
        ]
    )

    # Add a status endpoint to signal that the app is up.
    @dash_app.server.route("/status", methods=["GET"])
    def status():
        return "OK", 200

    @dash_app.server.route("/fit_result", methods=["POST"])
    def fit_result():
        """
        Endpoint that receives fit results (fit function + parameters) via POST request.
        The payload is expected to have:
          - best_fit: the list of fit y-values
          - name: the fit name
          - fit_params: the dictionary of fit parameters
          - y_axis_name: the name of the y-data to which this fit belongs
        Data is stored in `data[f"fit_{name}"]`.
        """
        nonlocal data, x_name, y_names
        try:
            json_payload = flask_request.json
            fit_result = json_payload["best_fit"]
            name = json_payload["name"]
            fit_params = json_payload["fit_params"]
            y_axis_name = json_payload["y_axis_name"]

            # Store the fit information in the `data` dictionary under key "fit_<name>".
            data[f"fit_{name}"] = {
                "fit_result": fit_result,
                "fit_params": fit_params,
                "y_axis_name": y_axis_name,
            }
            return "Data successfully updated", 200
        except ValueError:
            # The error here might happen if the JSON is malformed or data is missing.
            return f"Invalid data value: {fit_result}", 400

    # @dash_app.server.route("/shutdown", methods=["GET"])
    # def shutdown():
    #     func = flask_request.environ.get("werkzeug.server.shutdown")
    #     if func is None:
    #         raise RuntimeError("Not running with the Werkzeug Server")
    #     func()
    #     return "Server shutting down..."

    @dash_app.server.route("/add_data", methods=["GET"])
    def add_data():
        """
        Endpoint that receives new data points (x, y) via GET request.
        The y-values are expected to be a JSON string that includes
        all required y_names mapped to their numeric values.
        """
        nonlocal data, x_name, y_names
        # Retrieve the x and y query parameters.
        x_value = flask_request.args.get("x")
        y_value = flask_request.args.get("y")
        if x_value is None or y_value is None:
            return "Missing required x or y parameter", 400
        try:
            # Convert string values to float and append them to the data dictionary.
            data[x_name].append(float(x_value))
            for y_name in y_names:
                data[y_name].append(float(json.loads(y_value)[y_name]))
            return "Data successfully updated", 200
        except ValueError:
            # This indicates that the conversion to float failed.
            return f"Invalid data value: {x_value}, {y_value}", 400

    @dash_app.callback(
        Output("scatter-plot", "figure"),
        Input("graph-update", "n_intervals"),
    )
    def update_scatter_plot(_):
        """
        Dash callback to update the scatter plot at each interval.
        It creates or updates the figure with x vs. multiple y data
        and (if present) the corresponding fit curves.
        """
        nonlocal data, title, xlabel, ylabel, ylabel2, logX, logY, logY2, maxlen, y_axes, fits, fit_model_dict

        # Build an lmfit model dictionary for each fit definition found in fits.
        for fit in fits:
            if fit["use_custom_func"]:
                model = lmfit.models.ExpressionModel(fit["custom_func"])
                label = "custom"
            else:
                # For a predefined function, create a model instance by name from lmfit.
                model = lmfit.models.lmfit_models[fit["predef_func"]]()
                label = fit["predef_func"]
            model_name = f"{label}_{fit['y']}_v_{fit['x']}"
            fit_model_dict[model_name] = model

        # Create a figure with secondary y-axis possibility.
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add a scatter trace for each y_name in y_names.
        for i, y_name in enumerate(y_names):
            scatter = go.Scatter(
                x=data[x_name],
                y=data[y_name],
                mode="markers",
                marker=dict(size=10, color=i, opacity=0.8),
                name=y_name,
            )
            # Decide whether trace belongs to the primary y-axis or secondary y-axis.
            secondary_y = False if y_axes[y_name] == 1 else True
            fig.add_trace(scatter, secondary_y=secondary_y)

            # Look for any fit data that matches this y_name.
            for key in list(data.keys()):
                # Fit keys always start with 'fit_' in this logic.
                if key.startswith("fit_"):
                    # If the 'fit_' data is for the correct y-axis, proceed.
                    if data[key]["y_axis_name"] == y_name:
                        fit_name = key[4:]  # Remove 'fit_' prefix.
                        for fit_model_name, fit in fit_model_dict.items():
                            # Check for matching fit name (with variable renaming considered).
                            if replace_name(fit_model_name) in fit_name:
                                fit_data = data[key]
                                # Create a denser x array for smooth fit curves.
                                x_data = np.linspace(
                                    min(data[x_name]),
                                    max(data[x_name]),
                                    len(data[x_name]) * 2,
                                )
                                # Rebuild lmfit.Parameters from the stored dictionary.
                                params = lmfit.Parameters()
                                for param_name, param_value in fit_data[
                                    "fit_params"
                                ].items():
                                    params.add(param_name, value=param_value)
                                # Evaluate the model at the new x_data points.
                                fit_y_points = fit.eval(params=params, x=x_data)
                                # Create a scatter trace for the fit result, drawn as a dashed line.
                                fit_result_trace = go.Scatter(
                                    x=x_data,
                                    y=fit_y_points,
                                    mode="lines",
                                    line=dict(color="red", dash="dash"),
                                    name=f"fit_{y_name}",
                                )
                                fig.add_trace(fit_result_trace, secondary_y=secondary_y)

        # Construct the layout, including axis labels and log/linear scale decisions.
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
            yaxis2=dict(
                title=ylabel2,
                type="log" if logY2 else "linear",
                overlaying="y",
                side="right",
            ),
            margin={"l": 40, "r": 20, "t": 40, "b": 30},
            uirevision=True,  # Prevents re-layout on updates.
        )

        # Return the figure for Dash to render.
        return {
            "data": fig.data,
            "layout": layout,
        }

    # Signal to the main process that the Dash server is up.
    wait_for_dash_app_event.set()

    # Run the Dash server (blocking call).
    dash_app.run(host="127.0.0.1", port=web_port, debug=False, use_reloader=False)


class PlotlyLiveCallback(CallbackBase):
    """
    A Bluesky callback that caches x- and y-values whenever an event is emitted.
    We'll later read these values in the Dash app to update the figure.

    It spawns a new Dash application in a separate process using run_dash_app.
    The data is sent to this Dash app via REST endpoints.
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
        """
        Initialize the PlotlyLiveCallback.

        Parameters
        ----------
        x_name : str
            The name of the x-data.
        y_names : list of str
            The list of y-data names.
        evaluator : Evaluator
            An object to dynamically evaluate expressions if raw data is not present.
        web_port : int
            The port on which the Dash server will run.
        fits : list
            A list of dictionaries describing fit functions.
        kwargs : dict
            Additional parameters such as y_axes, xlabel, ylabel, log scales, etc.
        """
        CallbackBase.__init__(self)
        self.fits = fits
        self.x_name = x_name
        self.y_axes: dict = kwargs.get("y_axes")
        self.y_names = y_names or self.y_axes.keys()

        # Axis labels and plot meta-info.
        self.xlabel = kwargs.get("xlabel", self.x_name or "sequence #")
        self.ylabel = kwargs.get("ylabel", self.y_names[0] or "value")
        self.ylabel2 = kwargs.get("ylabel2")
        self.title = kwargs.get("title", f"{self.xlabel} vs. {self.ylabel}")

        # Log scale flags for x, y, y2.
        self.logX = kwargs.get("logX", False)
        self.logY = kwargs.get("logY", False)
        self.logY2 = kwargs.get("logY2", False)

        # For limiting the length of stored data. "inf" means no limit by default.
        self.maxlen = kwargs.get("maxlen", "inf")

        # Holds an Evaluator instance if needed for derived data or delayed evaluation.
        self.eva = evaluator
        self.web_port = web_port

        # The name of the desired data stream in Bluesky, and if multi_stream usage is required.
        self.stream_name = kwargs.get("stream_name")
        self.multi_stream = kwargs.get("multi_stream")

        # Will hold descriptors once recognized.
        self.desc = []
        # UIDs of docs that should be ignored for fit or other reasons.
        self.ignore_fit_docs = []

        # Flags and synchronization objects for controlling setup.
        self.setup_is_done = False
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()

    def start(self, doc):
        """
        Called at the beginning of a Bluesky run (when the 'start' document is emitted).
        Creates and starts the Dash server process, ensuring the app is set up.
        """
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
        # Wait until the Dash server signals that it is ready.
        wait_for_dash_app_event.wait()

    def event(self, doc):
        """
        Called whenever a new event document is emitted from the RunEngine.
        Uses the `stream_name` to filter relevant data.
        Once an event is validated, it extracts x and y values
        and sends them to the Dash server via GET request.
        """
        if doc["descriptor"] not in self.desc:
            return
        elif doc["uid"] in self.ignore_fit_docs:
            return

        # Check to see if doc["data"] contains keys matching any on the self.ys strings or self.x. This means that plots are only tried to be updated if the data is present.
        if not (any(key in s for key in doc["data"] for s in self.y_names)):
            return
        # Try to retrieve x value from doc["data"], or fallback to evaluator if missing.
        try:
            new_x = doc["data"][self.x_name]
        except KeyError:
            # If x_name is time or seq_num, we can find it in doc directly or compute it.
            if self.x_name in ("time", "seq_num"):
                new_x = doc[self.x_name]
            else:
                # Evaluate x using the evaluator if possible.
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_x = self.eva.eval(self.x_name, do_not_reraise=True)

        # Prepare a dictionary of y values from the doc or evaluate them.
        new_y = {}
        for y_name in self.y_names:
            try:
                new_y[y_name] = doc["data"][y_name]
            except KeyError:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                new_y[y_name] = self.eva.eval(y_name, do_not_reraise=True)

        # Send the new data to the Dash app via HTTP request.
        try:
            response = requests.get(
                f"http://127.0.0.1:{self.web_port}/add_data",
                params={"x": new_x, "y": json.dumps(new_y)},
                timeout=1,
            )
            if response.status_code == 200:
                pass  # Data updated successfully.
            else:
                print(f"Failed to add data point: {response.text}")
        except requests.ConnectionError:
            print("Cannot connect to Dash server. Is it running?")

    def stop(self, doc):
        """
        Called when the Bluesky run ends (at 'stop' document).
        Terminates the Dash process if it is still alive.
        """
        import time

        if hasattr(self, "dash_process") and self.dash_process.is_alive():
            # Give a short pause before terminating.
            time.sleep(1)
            self.dash_process.terminate()
            self.dash_process.join()
            self.dash_process = None
            print("Terminated the web plot app process.")

    def clear_data(self):
        """
        Helper method to clear data if needed between runs.
        This is not actively used in the current approach
        but can be useful for certain workflows.
        """
        self.x_data = []
        self.y_data = []

    def descriptor(self, doc):
        """
        Called when a new descriptor is emitted.
        Checks if the descriptor matches the configured stream_name.
        If so, its uid is recorded to be recognized in future event() calls.

        If multi_stream is True, it checks descriptors that start with the given stream_name.
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
        """
        Internal method that ensures setup is executed once.
        Sets the setup_is_done flag and triggers the setup event.
        """
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
    """
    Runs a Dash application in a separate process for visualizing 2D data (x, y) with a color dimension z.

    Parameters
    ----------
    web_port : int
        The TCP port on which the Dash server will listen for requests.
    wait_for_dash_app_event : multiprocessing.Event
        An event used to signal to the calling process that the Dash app is fully started and ready.
    x_name : str
        The key under which x-values will be stored in the data dictionary.
    y_name : str
        The key under which y-values will be stored in the data dictionary.
    z_name : str
        The key under which z-values (color dimension) will be stored in the data dictionary.
    xlabel : str
        Label for the x-axis in the Plotly figure.
    ylabel : str
        Label for the y-axis in the Plotly figure.
    title : str
        The main title of the Plotly figure.
    maxlen : str or int
        Maximum number of data points to keep (if relevant). "inf" indicates no limit.

    Notes
    -----
    - The application includes a custom endpoint ("/add_data_2d") to receive x, y, and z values.
      These values are appended to a shared data dictionary.
    - A Dash callback periodically redraws the scatter plot using `plotly.express.scatter`,
      with `z` mapped to the color dimension.
    - The server runs in debug=False mode and does not use a reloader to avoid issues
      with subprocess execution.
    """
    # Store x, y, z data in a dictionary of lists.
    data = {x_name: [], y_name: [], z_name: []}
    # Create the Dash app.
    dash_app = Dash("Browser Plots")

    # Define the layout with a Graph and an Interval for periodic updates.
    dash_app.layout = html.Div(
        [
            dcc.Graph(id="scatter-plot"),
            dcc.Interval(
                id="graph-update",
                interval=500,  # Check every 0.5 second for new data.
                n_intervals=0,
            ),
        ]
    )

    @dash_app.server.route("/status", methods=["GET"])
    def status():
        return "OK", 200

    # @dash_app.server.route("/shutdown", methods=["GET"])
    # def shutdown():
    #     func = flask_request.environ.get("werkzeug.server.shutdown")
    #     if func is None:
    #         raise RuntimeError("Not running with the Werkzeug Server")
    #     func()
    #     return "Server shutting down..."

    @dash_app.server.route("/add_data_2d", methods=["GET"])
    def add_data_2d():
        """
        Endpoint that receives x, y, and z data as query parameters.
        Attempts to convert them to floats and append to the data dictionary.
        """
        nonlocal data, x_name, y_name, z_name
        x_value = flask_request.args.get("x")
        y_value = flask_request.args.get("y")
        z_value = flask_request.args.get("z")
        if x_value is None or y_value is None:
            return "Missing required x or y parameter", 400
        try:
            data[x_name].append(float(x_value))
            data[y_name].append(float(y_value))
            data[z_name].append(float(z_value))
            return "Data successfully updated", 200
        except ValueError:
            return f"Invalid data value: {x_value}, {y_value}, {z_value}", 400

    @dash_app.callback(
        Output("scatter-plot", "figure"),
        Input("graph-update", "n_intervals"),
    )
    def update_scatter_plot(_):
        """
        Periodic callback that regenerates the figure based on the data dictionary.
        """
        nonlocal data, title, xlabel, ylabel, maxlen

        if xlabel == "":
            xlabel = x_name
        if ylabel == "":
            ylabel = y_name
        fig = go.Figure(
            data=go.Scatter(
                x=data[x_name],
                y=data[y_name],
                mode="markers",
                marker=dict(
                    color=data[z_name],  # Use z values for color
                    colorscale="Viridis",  # Specify the colorscale
                    colorbar=dict(title=z_name),  # Optionally add a colorbar
                    showscale=True,
                ),
            )
        )
        # Update layout to include axis labels and title
        fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
        return fig

    # Signal that the Dash server has started.
    wait_for_dash_app_event.set()
    dash_app.run(host="127.0.0.1", port=web_port, debug=False, use_reloader=False)


class PlotlyLiveCallback_2d(CallbackBase):
    """
    A Bluesky callback that automatically collects and plots 2D data (x, y) with an associated
    color dimension z in a separate Dash application. During a Bluesky run, each event document
    triggers an update that sends the latest x, y, and z data to a Dash endpoint, rendering a
    scatter plot where z is visualized as a color scale.

    This class is particularly useful for real-time visualizations of 2D data where one
    axis depends on x and y, and an additional parameter (z) is encoded as color. It manages
    the lifecycle of a subprocess running Dash (start, stop) and ensures that relevant data
    are gathered and transmitted appropriately.

    Parameters
    ----------
    x_name : str
        The key under which x-values are located in the event documents' "data" fields or
        can be evaluated using the `evaluator`.
    y_name : str
        The key under which y-values are located in the event documents' "data" fields or
        can be evaluated using the `evaluator`.
    z_name : str
        The key under which z-values are located, representing the color dimension in the
        plotly scatter plot.
    evaluator : Evaluator
        An instance of an evaluation helper, used to compute derived x, y, or z values
        if they are not directly available in the event data.
    web_port : int
        The TCP port on which the Dash server will listen for requests.

    Other Parameters
    ----------------
    xlabel : str, optional
        Label for the x-axis in the plot. Defaults to `x_name` if not provided.
    ylabel : str, optional
        Label for the y-axis in the plot. Defaults to `y_name` if not provided.
    zlabel : str, optional
        Label for the color dimension in the plot. Defaults to `z_name` if not provided.
    title : str, optional
        Main title of the plot. Defaults to a combination of `xlabel` and `ylabel`.
    maxlen : str or int, optional
        Maximum number of data points retained. Can be "inf" for unlimited storage.
        Defaults to "inf".
    stream_name : str, optional
        The specific Bluesky stream name this callback should monitor. When a new descriptor
        document's name matches `stream_name`, its events will be recognized for plotting.
        If not provided, no stream filtering is performed.
    multi_stream : bool, optional
        Indicates if multiple streams are used. This can adjust how the descriptor checks
        are performed. Defaults to False.

    Notes
    -----
    - The `start` method spawns the Dash server in a separate process, using
      `run_dash_app_2d`. That server provides a REST endpoint (`"/add_data_2d"`) to receive
      x, y, z values.
    - The `event` method inspects each Bluesky event document to extract or evaluate x, y, and
      z, then sends them to the Dash server if the descriptor matches.
    - The `stop` method terminates the Dash server subprocess upon the completion of a Bluesky run.
    - The `clear_data` method can be used to reset any accumulated data between runs.
    - The `descriptor` method ensures that only events from relevant descriptors (matching
      `stream_name`) are processed.
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
        """
        Initialize the 2D Plotly live callback with x, y, z data definitions.
        """
        CallbackBase.__init__(self)
        self.x_name = x_name
        self.y_name = y_name
        self.z_name = z_name

        # Axis labels, with fallback to the variable names themselves.
        self.xlabel = kwargs.get("xlabel", self.x_name or "x value")
        self.ylabel = kwargs.get("ylabel", self.y_name or "y value")
        self.zlabel = kwargs.get("zlabel", self.z_name or "z value")
        self.title = kwargs.get("title", f"{self.xlabel} vs. {self.ylabel}")

        # Limit on data size if needed.
        self.maxlen = kwargs.get("maxlen", "inf")

        # For evaluating expressions if data is missing.
        self.eva = evaluator

        # The port used by the Dash server.
        self.web_port = web_port

        # The relevant Bluesky stream name, and a flag if multiple streams are used.
        self.stream_name = kwargs.get("stream_name")
        self.multi_stream = kwargs.get("multi_stream")

        # Track descriptors and items to ignore.
        self.desc = []
        self.ignore_fit_docs = []

        # Setup control.
        self.setup_is_done = False
        self.__setup_lock = threading.Lock()
        self.__setup_event = threading.Event()

    def start(self, doc):
        """
        Called at run start, spawns the Dash app for 2D data visualization.
        """
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
        """
        Called whenever an event document is emitted.
        This callback extracts x, y, z from the doc or from an evaluator
        if the direct data is not available, then sends it via HTTP to the Dash server.
        """
        if doc["descriptor"] not in self.desc:
            return
        elif doc["uid"] in self.ignore_fit_docs:
            return

        # Attempt to retrieve x from the event data, or evaluate it.
        try:
            x = doc["data"][self.x_name]
        except KeyError:
            if self.x in ("time", "seq_num"):
                x = doc[self.x_name]
            else:
                if not self.eva.is_to_date(doc["time"]):
                    self.eva.event(doc)
                x = self.eva.eval(self.x, do_not_reraise=True)

        # Attempt to retrieve y.
        try:
            y = doc["data"][self.y_name]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            y = self.eva.eval(self.y_name, do_not_reraise=True)

        # Attempt to retrieve z.
        try:
            z = doc["data"][self.z_name]
        except KeyError:
            if not self.eva.is_to_date(doc["time"]):
                self.eva.event(doc)
            z = self.eva.eval(self.z_name, do_not_reraise=True)

        # Send the new x, y, z to the Dash endpoint via GET.
        try:
            response = requests.get(
                f"http://127.0.0.1:{self.web_port}/add_data_2d",
                params={"x": x, "y": y, "z": z},
                timeout=1,
            )
            if response.status_code == 200:
                pass  # Data updated successfully.
            else:
                print(f"Failed to add data point: {response.text}")
        except requests.ConnectionError:
            print("Cannot connect to Dash server. Is it running?")

    def stop(self, doc):
        """
        Called when the Bluesky run ends.
        Terminates the Dash process if it is still alive.
        """
        if hasattr(self, "dash_process") and self.dash_process.is_alive():
            self.dash_process.terminate()
            self.dash_process.join()
            self.dash_process = None
            print("Terminated the web plot app process.")

    def clear_data(self):
        """
        Helper to clear data between runs if needed.
        """
        self.x_data = []
        self.y_data = []

    def descriptor(self, doc):
        """
        Handles descriptor documents.
        If it matches the stream_name, we mark its uid for recognized events.
        """
        if doc["name"] == self.stream_name:
            self.desc = doc["uid"]

    def setup(self):
        """
        Ensures the setup is done once, sets the flag and event.
        """
        with self.__setup_lock:
            if self.__setup_event.is_set():
                return
            self.__setup_event.set()
        self.setup_is_done = True
