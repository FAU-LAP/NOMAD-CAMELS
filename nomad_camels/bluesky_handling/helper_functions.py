"""Functions to be used in protocols.

The functions in this module may be used inside a protocol. It is much
simpler to use these than writing them as a string into the protocol-file.
"""

import numpy as np
from bluesky import plan_stubs as bps

from ophyd import SignalRO, Device

from PySide6.QtWidgets import (
    QMessageBox,
    QWidget,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table

from suitcase.nomad_camels_hdf5 import Serializer, export

import inspect
import os
import sys
import glob


def get_newest_file(directory):
    """
    Return the newest file in the given directory.

    Parameters
    ----------
    directory : str
        The directory where the newest file should be found.

    Returns
    -------
    newest_file : str
        The path to the newest file in the directory.
    """
    # If the given directory is a file, take the directory of the file
    if os.path.isfile(directory):
        directory = os.path.dirname(directory)
    # List all files in the directory
    files = glob.glob(os.path.join(directory, "*"))
    # Find the newest file
    newest_file = max(files, key=os.path.getmtime)
    return newest_file


def export_function(
    runs,
    save_path,
    do_export,
    new_file_each=True,
    export_csv=False,
    export_json=False,
    plot_data=None,
):
    """
    Export the given runs to the given path.

    Parameters
    ----------
    runs : list[databroker.core.BlueskyRun]
        The runs to be exported.
    save_path : str
        The path where the files should be saved.
    do_export : bool
        Whether the runs should be exported.
    new_file_each : bool, optional
        (Default value = True)
        Whether a new file should be created for each run. If True, the files are
        padded with the start-time of the run. Ignored if `do_export` is False.
    export_csv : bool, optional
        (Default value = False)
        Whether the data should be exported to a csv file.
    export_json : bool, optional
        (Default value = False)
        Whether the metadata should be exported to a json file.
    plot_data : dict, optional
        (Default value = None)
        The data to be plotted.

    """
    if os.path.splitext(save_path)[1] == ".nxs":
        fname = os.path.basename(save_path)
        path = os.path.dirname(save_path)
    if do_export:
        if not isinstance(runs, list):
            runs = [runs]
        for run in runs:
            docs = run.documents(fill="yes")
            export(docs, path, fname, new_file_each, plot_data=plot_data)
    if export_csv or export_json:
        from nomad_camels.utility.databroker_export import export_h5_to_csv_json

        file = get_newest_file(path)
        export_h5_to_csv_json(file, export_data=export_csv, export_metadata=export_json)


def saving_function(name, start_doc, path, new_file_each=True, plot_data=None):
    """
    Create a Serializer and return it.

    The serializer is from the suitcase.nomad_camels_hdf5 module and used to save
    the data during a run.

    Parameters
    ----------
    name : str
        The name of the file.
    start_doc : dict
        The start document of the run.
    path : str
        The path where the file should be saved.
    new_file_each : bool, optional
        (Default value = True)
        Whether a new file should be created for each run. If True, the files are
        padded with the start-time of the run.
    plot_data : dict, optional
        (Default value = None)
        The data to be plotted.

    Returns
    -------
    serializers : list
        The serializers to be used.
    resources : list
        The resources to be used. In this case, an empty list.
    """
    fname = start_doc["uid"]
    if os.path.splitext(path)[1] == ".nxs":
        fname = os.path.basename(path)
        path = os.path.dirname(path)
    return [
        Serializer(path, fname, new_file_each=new_file_each, plot_data=plot_data)
    ], []


def trigger_multi(devices, grp=None):
    """
    Trigger multiple devices.

    Parameters
    ----------
    devices : list[ophyd.Device]
        List of the devices that should be triggered.

    grp : string (or any hashable object), optional
        identifier used by 'wait'; None by default
    """
    for obj in devices:
        if hasattr(obj, "trigger"):
            yield from bps.trigger(obj, group=grp)


def read_wo_trigger(devices, grp=None, stream="primary"):
    """
    Used if not reading by trigger_and_read, but splitting both. This function only reads, without triggering.

    Parameters
    ----------
    devices : list[ophyd.Device]
        List of the devices that should be read.
    grp : string (or any hashable object), optional
        identifier used by 'wait'; None by default
    stream : string, optional
        event stream name, a convenient human-friendly identifier; default
        name is 'primary'

    Returns
    -------
    ret : dict
        The readings of the devices.
    """
    if grp is not None:
        yield from bps.wait(grp)
    yield from bps.create(stream)
    ret = {}  # collect and return readings to give plan access to them
    for obj in devices:
        reading = yield from bps.read(obj)
        if reading is not None:
            ret.update(reading)
    yield from bps.save()
    return ret


def simplify_configs_dict(configs):
    """
    Returns a simplified version of the given dictionary `configs` by returning confs[key] = configs[key]['value'].

    Parameters
    ----------
    configs : dict
        The dictionary to be simplified.


    Returns
    -------
    confs : dict
        The simplified dictionary.
    """
    confs = {}
    for key, value in configs.items():
        if "value" in value:
            val = value["value"]
        else:
            val = value
        if isinstance(val, Device):
            confs[key] = val.name
        else:
            confs[key] = val
    return confs


def get_fit_results(fits, namespace, yielding=False, stream="primary"):
    """
    Updates and reads all the fits that correspond to the given stream and
    resets the fits in the end.

    Parameters
    ----------
    fits : dict
        Dictionary of all the fits to take into account.
    namespace : dict
        Namespace dictionary where to write the fit results.
    yielding : bool, optional
         (Default value = False)
         If True, the fits will be triggered and updated.
    stream : str, optional
         (Default value = 'primary')
         The stream on which the regarded fits should run. Only the fits which
         have `stream_name` equal to `stream` will be used.
    """
    for name, fit in fits.items():
        if yielding and fit.stream_name == stream:
            yield from bps.trigger_and_read(
                [fit.read_ready], name=f"{stream}_fits_readying_{name}"
            )
            yield from fit.update_fit()
            # yield from bps.trigger_and_read(fit.ophyd_fit.used_comps,
            #                                 name=f'{stream}_fits_{name}')
        if not fit.result:
            continue
        for param in fit.params:
            if param in fit.result.best_values:
                namespace[f"{name}_{param}"] = fit.result.best_values[param]
        namespace[f"{name}_covar"] = fit.result.covar
        fit._reset()


def clear_plots(plots, stream="primary"):
    """
    Clears all given plots if they correspond to the given stream.

    Parameters
    ----------
    plots : list
        List of the plots to be cleared.
    stream : str
         (Default value = 'primary')
         The stream to which the plots that should be cleared correspond.
    """
    for plot in plots:
        if plot.stream_name == stream or plot.stream_name.startswith(f"{stream}_fits_"):
            plot.clear_plot()


def gradient_descent(
    max_iterations,
    threshold,
    w_init,
    func_text,
    evaluator,
    set_channel,
    read_channels,
    min_step,
    max_step,
    min_val,
    max_val,
    stream_name="gradient_descent",
    learning_rate=0.05,
    momentum=0.8,
    max_step_for_diff=None,
):
    """
    Helper function for the gradient descent protocol-step.
    It follows a simple gradient descent algorithm to find an optimum.

    Parameters
    ----------
    max_iterations : int
        The maximum number of iterations until the algorithm should stop if it
        did not arrive at the threshold yet.
    threshold : float
        If the difference between two measurements is smaller than this
        threshold, the algorithm recognizes the value as the optimum and stops.
    w_init : float
        The initial set-value from where the algorithm should start.
    func_text : str
        This string is evaluated by the given evaluator to give the target
        function.
    evaluator : Evaluator
        Used to evaluate the read values.
    set_channel : ophyd.Signal
        The channel which is used for the optimization.
    read_channels : list
        A list of all the channels which are read for the optimization.
    min_step : float
        The minimum step size.
    max_step : float
        The maximum step size.
    min_val : float
        The minimum value that should be given to the `set_channel`.
    max_val : float
        The maximum value that should be given to the `set_channel`.
    stream_name : str
         (Default value = 'gradient_descent')
         The bluesky stream in which everything should run.
    learning_rate : float
         (Default value = 0.05)
         A weight for the learning of the gradient descent.
         The next shift `delta_w` is calculated as:
         delta_w = -learning_rate * <current_gradient> + momentum * <last_delta_w>
    momentum : float
         (Default value = 0.8)
         A momentum to keep up the last direction.
         The next shift `delta_w` is calculated as:
         delta_w = -learning_rate * <current_gradient> + momentum * <last_delta_w>
    max_step_for_diff : float, None
        If none, max_step_for_diff = 10 * min_step
        Only if the last step was smaller than `max_step_for_diff`, the
        algorithm breaks if the threshold is reached.

    Returns
    -------
    w_history :
        The history of values of set_channel
    f_history :
        The history of evaluated values

    """
    if set_channel not in read_channels:
        read_channels += [set_channel]

    def obj_func(set_val):
        """
        Set the value and then read the channels for each iteration of the algorithm.

        Parameters
        ----------
        set_val : float
            Value to be set on the set_channel
        """
        yield from bps.checkpoint()
        yield from bps.abs_set(set_channel, set_val, group="A")
        yield from bps.wait("A")
        yield from bps.trigger_and_read(read_channels, name=stream_name)
        # yield from bps.sleep(1)

    if max_step_for_diff is None:
        max_step_for_diff = 10 * min_step

    w = w_init
    w_history = [w]
    yield from obj_func(w)
    f_history = [evaluator.eval(func_text)]
    if w - min_val > max_val - w:
        w -= max_step_for_diff
        delta_w = -max_step_for_diff
    else:
        w += max_step_for_diff
        delta_w = max_step_for_diff
    i = 0
    diff = np.inf

    while i < max_iterations and (
        diff > threshold or np.abs(delta_w) > max_step_for_diff
    ):
        yield from obj_func(w)
        f = evaluator.eval(func_text)
        grad = (f - f_history[-1]) / (w - w_history[-1])
        delta_w = -learning_rate * grad + momentum * delta_w
        w_history.append(w)
        f_history.append(f)
        if np.abs(delta_w) > max_step:
            delta_w = np.sign(delta_w) * max_step
        elif np.abs(delta_w) < min_step:
            delta_w = np.sign(delta_w) * min_step
        w += delta_w
        if w < min_val:
            w = min_val
        elif w > max_val:
            w = max_val
        if w == w_history[-1]:
            if w - min_val > max_val - w:
                w -= max_step_for_diff
                delta_w -= max_step_for_diff
            else:
                w += max_step_for_diff
                delta_w = max_step_for_diff
        # store the history of w and f

        # update iteration number and diff between successive values
        # of objective function
        i += 1
        diff = np.abs(f_history[-1] - f_history[-2])

    sort_w = [i for j, i in sorted(zip(f_history, w_history))]
    sort_f = sorted(f_history)
    while True:
        fs = []
        for i in range(2):
            yield from obj_func(sort_w[0])
            fs.append(evaluator.eval(func_text))
        if fs[0] and fs[1] < sort_f[0] + 0.1 * (sort_f[-1] - sort_f[0]):
            break
        elif len(sort_f) < 0.5 * len(f_history):
            yield from obj_func(w_init)
            break
        else:
            sort_f.pop(0)
            sort_w.pop(0)
    return w_history, f_history


def get_range(
    evaluator,
    start,
    stop,
    points: int,
    min_val=np.nan,
    max_val=np.nan,
    loop_type="start - stop",
    sweep_mode="linear",
    endpoint=True,
    distance=np.nan,
    use_distance=False,
):
    """
    Helper function for steps like sweeps and the for loop.

    Using the evaluator, it creates the range of iterations given the other
    values.

    Parameters
    ----------
    evaluator : Evaluator
        Used to evaluate the given expressions (`start`, `stop`, `points`,
        `min_val`, `max_val`).
    start : float, str
        The starting position for the sweep / loop.
    stop : float, str
        The end position for the sweep / loop.
    points : int, str
        The number of points in the range. If using `min_val` / `max_val`,
        `points` is the distance between those two.
    min_val : float, str
         (Default value = np.nan)
         Minimum value of the loop / sweep. Useful for hysteresis-sweeps.
    max_val : float, str
         (Default value = np.nan)
         Minimum value of the loop / sweep. Useful for hysteresis-sweeps.
    loop_type : str
         (Default value = 'start - stop')
         Possible values: 'start - stop', ignoring `min_val` and `max_val`
         'start - min - max - stop' going to minimum first, then maximum
         'start - max - min - stop', or anything not-specified.
    sweep_mode : str
         (Default value = 'linear')
         The type how the distance between the points is calculated.
         If 'linear', they are equidistant, if 'logarithmic', the points between
         log(start) and log(stop) are equidistant, if 'exponential', between
         exp(start) and exp(stop), otherwise they are equidistant between
         1/start and 1/stop.
    endpoint : bool
         (Default value = True)
         Whether to include the endpoint into the range.
    distance : float, str
        (Default value = np.nan)
        The distance between the points.
    use_distance : bool
        (Default value = False)
        If True, the distance is used to calculate the range.

    Returns
    -------
        An array of the calculated range.
    """
    start = float(evaluator.eval(str(start)))
    stop = float(evaluator.eval(str(stop)))
    points = int(evaluator.eval(str(points)))
    min_val = evaluator.eval(str(min_val))
    max_val = evaluator.eval(str(max_val))
    try:
        distance = evaluator.eval(str(distance))
    except ValueError:
        distance = np.nan
    if loop_type == "start - stop":
        return get_inner_range(
            start,
            stop,
            points,
            sweep_mode,
            endpoint,
            use_distance=use_distance,
            distance=distance,
        )
    if (
        min_val > max_val
        or not (min_val <= start <= max_val)
        or not (min_val <= stop <= max_val)
    ):
        raise ValueError("Start and Stop must be between min and max!")
    full_dist = np.abs(max_val - min_val)
    if loop_type == "start - min - max - stop":
        full_dist += np.abs(start - min_val) + np.abs(stop - max_val)
        p1 = round(points * np.abs(start - min_val) / full_dist)
        p3 = round(points * np.abs(stop - max_val) / full_dist)
        p2 = points - p1 - p3
        vals1 = get_inner_range(
            start, min_val, p1, sweep_mode, endpoint, use_distance, distance
        )
        vals2 = get_inner_range(
            min_val, max_val, p2, sweep_mode, endpoint, use_distance, distance
        )
        vals3 = get_inner_range(
            max_val, stop, p3, sweep_mode, endpoint, use_distance, distance
        )
    else:
        full_dist += np.abs(start - max_val) + np.abs(stop - min_val)
        p1 = round(points * np.abs(start - max_val) / full_dist)
        p3 = round(points * np.abs(stop - min_val) / full_dist)
        p2 = points - p1 - p3
        vals1 = get_inner_range(
            start, max_val, p1, sweep_mode, endpoint, use_distance, distance
        )
        vals2 = get_inner_range(
            max_val, min_val, p2, sweep_mode, endpoint, use_distance, distance
        )
        vals3 = get_inner_range(
            min_val, stop, p3, sweep_mode, endpoint, use_distance, distance
        )
    return np.concatenate([vals1, vals2, vals3])


def get_inner_range(
    start, stop, points, sweep_mode, endpoint, use_distance=False, distance=np.nan
):
    """
    Used for `get_range`, to make the split up ranges if doing a hysteresis
    sweep.

    Parameters
    ----------
    start : float, str
        The starting position for the sweep / loop.
    stop : float, str
        The end position for the sweep / loop.
    points : float, str
        The number of points in the range. If using `min_val` / `max_val`,
        `points` is the distance between those two.
    sweep_mode : str
         (Default value = 'linear')
         The type how the distance between the points is calculated.
         If 'linear', they are equidistant, if 'logarithmic', the points between
         log(start) and log(stop) are equidistant, if 'exponential', between
         exp(start) and exp(stop), otherwise they are equidistant between
         1/start and 1/stop.
    endpoint : bool
         (Default value = True)
         Whether to include the endpoint into the range.

    Returns
    -------
        An array of the calculated range.
    """
    if sweep_mode == "linear":
        if use_distance:
            if start < stop:
                vals = np.arange(start, stop, distance)
            else:
                vals = np.arange(start, stop, -distance)
            if endpoint:
                vals = np.append(vals, stop)
            return vals
        return np.linspace(start, stop, points, endpoint=endpoint)
    elif sweep_mode == "logarithmic":
        start = np.log(start)
        stop = np.log(stop)
        return np.exp(np.linspace(start, stop, points, endpoint=endpoint))
    elif sweep_mode == "exponential":
        start = np.exp(start)
        stop = np.exp(stop)
        return np.log(np.linspace(start, stop, points, endpoint=endpoint))
    return 1 / np.linspace(1 / start, 1 / stop, points, endpoint=endpoint)


class Prompt_Box(QMessageBox):
    """
    A subclass of QMessageBox that is used in the prompt-step.
    The protocol is paused until `self.done_flag` is True.

    Parameters
    ----------
    icon : str
        If 'Error', the `QMessagebox.Critical` icon is displayed, if 'Warning',
        then `QMessagebox.Warning` is used, otherwise `QMessagebox.Information`.
    text : str
        The text to be displayed by the prompt.
    title : str
        The window-title of the prompt.
    """

    def __init__(self, icon="", text="", title="", parent=None):
        super().__init__(parent=parent)
        if icon == "Error":
            self.setIcon(QMessageBox.Critical)
        elif icon == "Warning":
            self.setIcon(QMessageBox.Warning)
        else:
            self.setIcon(QMessageBox.Information)
        self.setText(text)
        self.setWindowTitle(title)
        self.helper = BoxHelper()
        self.helper.executor.connect(self.start_execution)
        self.buttonClicked.connect(self.set_done)
        self.done_flag = False

    def set_done(self):
        """Sets `self.done_flag` to True."""
        self.done_flag = True

    def start_execution(self):
        """Sets `self.done_flag` to False and starts `self.exec()`."""
        self.done_flag = False
        self.exec()


class BoxHelper(QWidget):
    """Helper-class to start the execution of Prompts and other boxes from
    within the protocol."""

    executor = Signal()


class Value_Box(QDialog):
    """
    Dialog to set variables or channels at runtime of a protocol.

    Parameters
    ----------
    text : str
        A text to be displayed with the box.
    title : str
        The window title of the box.
    variables : list, default: None
        The variables that should be set by the user. A QLineEdit will be
        provided for each of the variables.
    channels : list, default: None
        The channels that should be set by the user. A QLineEdit will be
        provided for each of the channels.
    free_variables : bool, default: False
        Whether the user is allowed to freely set any variables.
    free_channels : bool, default: False
        Whether the user is allowed to freely set any channels.
    devs : dict, default: None
        Dictionary of the available devices. Only needed, if `free_channels` is
        True, to provide the available channels.
    """

    def __init__(
        self,
        text="",
        title="",
        variables=None,
        channels=None,
        free_variables=False,
        free_channels=False,
        parent=None,
        devs=None,
    ):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        text_label = QLabel(text)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        layout = QGridLayout()

        self.helper = BoxHelper()
        self.helper.executor.connect(self.start_execution)
        self.done_flag = False

        channels_label = QLabel("Channels")
        font = QFont()
        font.setBold(True)
        channels_label.setStyleSheet("font-size: 9pt")
        channels_label.setFont(font)
        layout.addWidget(channels_label, 1, 0, 1, 2)
        variables_label = QLabel("Variables")
        font = QFont()
        font.setBold(True)
        variables_label.setStyleSheet("font-size: 9pt")
        variables_label.setFont(font)
        layout.addWidget(variables_label, 1, 2, 1, 2)

        channels = channels or []
        n_channels = len(channels)
        self.channel_boxes = []
        self.channels = channels
        for i, channel in enumerate(channels):
            channel_label = QLabel(f"{channel}:")
            channel_box = QLineEdit()
            self.channel_boxes.append(channel_box)
            layout.addWidget(channel_label, 2 + i, 0)
            layout.addWidget(channel_box, 2 + i, 1)

        variables = variables or []
        n_variables = len(variables)
        self.variable_boxes = []
        self.variables = variables
        for i, variable in enumerate(variables):
            variable_label = QLabel(f"{variable}:")
            variable_box = QLineEdit()
            self.variable_boxes.append(variable_box)
            layout.addWidget(variable_label, 2 + i, 2)
            layout.addWidget(variable_box, 2 + i, 3)

        devs = devs or {}
        self.channel_devs = {}
        for dev, val in devs.items():
            self.channel_devs.update(get_channels(val))
        self.channel_table = None
        self.variable_table = None
        if free_channels:
            self.channel_table = Channels_Check_Table(
                self,
                ["set", "channel", "value"],
                True,
                channels=list(self.channel_devs.keys()),
            )
            layout.addWidget(self.channel_table, 2 + n_channels + n_variables, 0, 1, 2)
        if free_variables:
            header = ["variable", "value"]
            self.variable_table = AddRemoveTable(headerLabels=header)
            layout.addWidget(self.variable_table, 2 + n_channels + n_variables, 2, 1, 2)

        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.setLayout(layout)
        layout.addWidget(text_label, 0, 0, 1, 4)
        layout.addWidget(self.buttonBox, 10 + n_channels + n_variables, 0, 1, 4)
        self.setWindowTitle(title)
        # self.table.sizechange.connect(self.adjustSize)
        self.adjustSize()
        self.was_accepted = False
        self.set_variables = {}
        self.set_channels = {}

    def start_execution(self):
        """Sets `self.done_flag` to False and starts `self.exec()`."""
        self.done_flag = False
        self.exec()

    def accept(self) -> None:
        """
        Reads all the values to be set to channels / variables and saves them in
        `self.set_channels` and `self.set_variables` respectively, then sets
        `self.done_flag` to True, allowing the protocol to go on and accepts the dialog.
        """
        self.set_variables = {}
        self.set_channels = {}
        for i, v_box in enumerate(self.variable_boxes):
            val = v_box.text()
            if val:
                self.set_variables[self.variables[i]] = val
        for i, c_box in enumerate(self.channel_boxes):
            val = c_box.text()
            if val:
                self.set_channels[self.channels[i]] = val
        if self.variable_table:
            var_table_data = self.variable_table.update_table_data()
            for i, var in enumerate(var_table_data["variable"]):
                if var in self.set_variables:
                    box = Prompt_Box(
                        "Critical",
                        f"Cannot set two values to variable {var}!",
                        "identical variable names",
                    )
                    box.exec()
                    return
                self.set_variables[var] = var_table_data["value"][i]
        if self.channel_table:
            channel_table_data = self.channel_table.get_info()
            for i, channel in enumerate(channel_table_data["channel"]):
                if channel in self.set_channels:
                    box = Prompt_Box(
                        "Critical",
                        f"Cannot set two values to channel {channel}!",
                        "identical channel names",
                    )
                    box.exec()
                    return
                self.set_channels[channel] = channel_table_data["value"][i]
        self.was_accepted = True
        self.done_flag = True
        return super().accept()

    def reject(self) -> None:
        """
        Sets `self.done_flag` to True, allowing the protocol to go on before
        rejecting the dialog.
        """
        self.done_flag = True
        return super().reject()


def get_channels(dev):
    """
    Goes through the components of the given ophyd device and returns all that
    are not read-only and not config.

    Parameters
    ----------
    dev : ophyd.Device
        The device that is checked for output channels.

    Returns
    -------
    channels : dict
        The keys are the channels in CAMELS-style. The values are
        [dev.name, <name_of_the_component>].
    """
    channels = {}
    for comp in dev.walk_components():
        if issubclass(comp.item.cls, SignalRO):
            continue
        name = comp.item.attr
        if name not in dev.configuration_attrs:
            channels[f"{dev.name}_{name}"] = [dev.name, name]
    return channels


def get_opyd_and_py_file_contents(classname, md, device_name):
    """
    Reads the content of the .py and _opyd.py driver files of the given instrument and adds
    them to the metadata dictionary. If the files are not found, it adds a corresponding message
    to the dictionary.

    Parameters
    ----------
    classname : class or function
        The class or function whose associated files' contents are to be read.
    md : dict
        The metadata dictionary where the content of the files should be added.
    device_name : str
        The name of the device associated with the classname.

    Returns
    -------
    md : dict
        The updated metadata dictionary with the content of the files added or with a message
        indicating that the file was not found.

    Raises
    ------
    FileNotFoundError
        If the .py or _opyd.py files associated with the classname are not found.
    """
    if inspect.isfunction(classname):
        try:
            with open(classname.__code__.co_filename, "r") as file:
                md["devices"][device_name][
                    f"python_file_{os.path.splitext(os.path.basename(classname.__code__.co_filename))[0]}"
                ] = file.read()
        except FileNotFoundError:
            md["devices"][device_name][
                os.path.splitext(os.path.basename(classname.__code__.co_filename))[0]
            ] = "._ophyd file not found"
        try:
            with open(
                classname.__code__.co_filename.replace("_ophyd.py", ".py"), "r"
            ) as file:
                md["devices"][device_name][
                    f"python_file_{os.path.splitext(os.path.basename(classname.__code__.co_filename))[0]}".replace(
                        "_ophyd", ""
                    )
                ] = file.read()
        except FileNotFoundError:
            md["devices"][device_name][
                os.path.splitext(os.path.basename(classname.__code__.co_filename))[
                    0
                ].replace("_ophyd", "")
            ] = ".py file not found"

    elif inspect.isclass(classname):
        try:
            with open(sys.modules[classname.__module__].__file__, "r") as file:
                md["devices"][device_name][
                    f"python_file_{os.path.splitext(os.path.basename(sys.modules[classname.__module__].__file__))[0]}"
                ] = file.read()
        except FileNotFoundError:
            md["devices"][device_name][
                os.path.splitext(
                    os.path.basename(sys.modules[classname.__module__].__file__)
                )[0]
            ] = "._ophyd file not found"
        try:
            with open(
                sys.modules[classname.__module__].__file__.replace("_ophyd.py", ".py"),
                "r",
            ) as file:
                md["devices"][device_name][
                    f"python_file_{os.path.splitext(os.path.basename(sys.modules[classname.__module__].__file__))[0]}".replace(
                        "_ophyd", ""
                    )
                ] = file.read()
        except FileNotFoundError:
            md["devices"][device_name][
                os.path.splitext(
                    os.path.basename(sys.modules[classname.__module__].__file__)
                )[0].replace("_ophyd", "")
            ] = ".py file not found"
    return md


def create_venv_run_file_delete_venv(packages, script_to_run):
    """
    Create a virtual environment, install the specified packages
    in it, run the specified Python script, and then delete the virtual environment.
    """
    import venv
    import subprocess
    import tempfile
    import shutil

    # Step 1: Create the virtual environment in a temp folder using tempfile
    try:
        temp_folder = tempfile.mkdtemp()
    except Exception as e:
        raise Exception(f"Error creating temporary folder: {e}")
    try:
        venv.create(temp_folder, with_pip=True)
    except Exception as e:
        raise Exception(f"Error creating virtual environment: {e}")

    # Path to the virtual environment's Python interpreter
    python_executable = (
        os.path.join(temp_folder, "bin", "python")
        if os.name != "nt"
        else os.path.join(temp_folder, "Scripts", "python.exe")
    )

    # Step 2: Install the specified packages
    for package, version in zip(packages["Python Package"], packages["Version"]):
        if not version:
            try:
                subprocess.run(
                    [python_executable, "-m", "pip", "install", f"{package}"]
                )
            except Exception as e:
                raise Exception(f"Error installing package {package}: {e}")
        else:
            try:
                subprocess.run(
                    [python_executable, "-m", "pip", "install", f"{package}=={version}"]
                )
            except Exception as e:
                raise Exception(f"Error installing package {package}=={version}: {e}")

    # Step 3: Run the specified Python script
    try:
        result_python_file = subprocess.run(
            [python_executable, script_to_run], cwd=os.path.dirname(script_to_run)
        )
    except Exception as e:
        raise Exception(f"Error running script {script_to_run}: {e}")

    # Step 4: Delete the virtual environment
    try:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
    except Exception as e:
        raise Exception(f"Error deleting temporary folder: {e}")
    return result_python_file


def evaluate_python_file_output(stdout, namespace):
    """Evaluates the stdout of a Python file execution and writes the returned key value pairs to the namespace, so CAMELS can access their values"""
    import json
    import re

    if stdout:
        json_pattern = re.compile(
            r"\{(?:[^{}]*|\{.*?\})*\}"
        )  # Extract the dictionary from the stdout, can handle one level of nested dictionaries

        # Search for JSON in the stdout
        match = json_pattern.search(stdout)

        if match:
            json_str = match.group()

            # Load the JSON string into a Python dictionary
            data = json.loads(json_str)
        else:
            raise ValueError("No valid dictionary found in the output")
        variables_dict = {}
        if isinstance(data, list):  # Step 1: Check if the stdout is a dictionary
            for item in data:  # Step 2: Loop through the list
                key, value = map(
                    str.strip, item.split("=", 1)
                )  # Step 3: Split each string
                variables_dict[key] = value

            for key, value in variables_dict.items():
                namespace[key] = value

        if isinstance(data, dict):
            for key, value in data.items():
                namespace[key] = value


class Value_Setter(QWidget):
    """A widget to set a value and a wait-time for a waiting bar."""

    set_signal = Signal(float)
    hide_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_time = 0
        self.end_time = 0
        self.timer = 0
        self.wait_time = 0

    def set_wait_time(self, wait_time):
        """Set the wait time for the waiting bar."""
        import datetime as dt

        self.wait_time = dt.timedelta(seconds=wait_time).total_seconds()

    def update_timer(self):
        """Update the timer of the waiting bar."""
        import datetime as dt

        self.timer = (dt.datetime.now() - self.start_time).total_seconds()
        self.set_signal.emit(self.timer / self.wait_time * 100)


class Waiting_Bar(QWidget):
    """A widget to show a waiting bar.

    Used in the wait step with a progress bar or also to wait for a condition and
    display the list plot of the condition.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    title : str
        The title of the waiting bar.
    skipable : bool
        (Default value = True)
        Whether the waiting bar can be skipped and shows a skip button.
    with_timer : bool
        (Default value = False)
        Whether the waiting bar has a timer.
    display_bar : bool
        (Default value = True)
        Whether the waiting bar should be displayed.
    plot : QWidget, optional
        A plot to be displayed together with the waiting bar.
    """

    def __init__(
        self,
        parent=None,
        title="",
        skipable=True,
        with_timer=False,
        display_bar=True,
        plot=None,
    ):
        super().__init__(parent=parent)
        layout = QGridLayout()
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar, 0, 0)
        self.progressBar.setHidden(not display_bar)

        self.skip = False
        if skipable:
            self.skipButton = QPushButton("SKIP")
            layout.addWidget(self.skipButton, 0, 1)
            self.skipButton.clicked.connect(self.skipping)
        self.setLayout(layout)
        self.setWindowTitle(title or "CAMELS progress bar")
        self.adjustSize()
        self.helper = BoxHelper()
        self.helper.executor.connect(self.start_execution)
        self.setter = Value_Setter()
        self.setter.set_signal.connect(self.setValue)
        self.setter.hide_signal.connect(self.hide)
        self.with_timer = with_timer
        if plot is not None:
            self.plot = plot
            layout.addWidget(self.plot, 1, 0, 1, 2)
        self.adjustSize()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def setValue(self, value):
        """Set the value of the progress bar."""
        self.progressBar.setValue(value)

    def skipping(self):
        """Set the skip flag to True and hide the waiting bar."""
        self.skip = True
        self.hide()

    def start_execution(self):
        """Sets `self.done_flag` to False and starts `self.exec()`."""
        self.skip = False
        self.setHidden(False)
        if self.with_timer:
            import datetime as dt

            self.setter.start_time = dt.datetime.now()

        self.show()
