import numpy as np
from bluesky import plan_stubs as bps

from ophyd import SignalRO

from PyQt5.QtWidgets import QMessageBox, QWidget, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

from CAMELS.utility.add_remove_table import AddRemoveTable
from CAMELS.utility.channels_check_table import Channels_Check_Table


def trigger_multi(devices, grp=None):
    for obj in devices:
        if hasattr(obj, 'trigger'):
            yield from bps.trigger(obj, group=grp)

def read_wo_trigger(devices, grp=None, stream='primary'):
    if grp is not None:
        yield from bps.wait(grp)
    yield from bps.create(stream)
    ret = {}  # collect and return readings to give plan access to them
    for obj in devices:
        reading = (yield from bps.read(obj))
        if reading is not None:
            ret.update(reading)
    yield from bps.save()
    return ret

def simplify_configs_dict(configs):
    confs = {}
    for key, value in configs.items():
        if 'value' in value:
            confs[key] = value['value']
        else:
            confs[key] = value
    return confs

def get_fit_results(fits, namespace, yielding=False, stream='primary'):
    for name, fit in fits.items():
        if yielding and fit.stream_name == stream:
            yield from bps.trigger_and_read([fit.read_ready],
                                            name=f'{stream}_fits_readying_{name}')
            yield from fit.update_fit()
            # yield from bps.trigger_and_read(fit.ophyd_fit.used_comps,
            #                                 name=f'{stream}_fits_{name}')
        if not fit.result:
            continue
        for param in fit.params:
            if param in fit.result.best_values:
                namespace[f'{name}_{param}'] = fit.result.best_values[param]
        namespace[f'{name}_covar'] = fit.result.covar
        fit._reset()

def clear_plots(plots, stream='primary'):
    for plot in plots:
        if plot.stream_name == stream or plot.stream_name.startswith(f'{stream}_fits_'):
            plot.clear_plot()


def gradient_descent(max_iterations, threshold, w_init, func_text, evaluator,
                     set_channel, read_channels, min_step, max_step, min_val,
                     max_val, stream_name='gradient_descent', learning_rate=0.05,
                     momentum=0.8, max_step_for_diff=None):

    def obj_func(set_val):
        yield from bps.checkpoint()
        yield from bps.abs_set(set_channel, set_val, group='A')
        yield from bps.wait('A')
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

    while i < max_iterations and (diff > threshold or np.abs(delta_w) > max_step_for_diff):
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
        diff = np.abs(f_history[-1]-f_history[-2])

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
    return w_history,f_history


class Prompt_Box(QMessageBox):
    def __init__(self, icon='', text='', title='', parent=None):
        super().__init__(parent=parent)
        if icon == 'Error':
            self.setIcon(QMessageBox.Critical)
        elif icon == 'Warning':
            self.setIcon(QMessageBox.Warning)
        else:
            self.setIcon(QMessageBox.Information)
        self.setText(text)
        self.setWindowTitle(title)
        self.helper = BoxHelper()
        self.helper.executor.connect(self.start_execution)
        self.buttonClicked.connect(self.set_done)
        self.done = False

    def set_done(self):
        self.done = True

    def start_execution(self):
        self.done = False
        self.exec()

class BoxHelper(QWidget):
    executor = pyqtSignal()


class Value_Box(QDialog):
    def __init__(self, text='', title='', variables=None, channels=None,
                 free_variables=False, free_channels=False, parent=None,
                 devs=None):
        super().__init__(parent)
        text_label = QLabel(text)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        layout = QGridLayout()

        self.helper = BoxHelper()
        self.helper.executor.connect(self.start_execution)
        self.done = False

        channels_label = QLabel('Channels')
        font = QFont()
        font.setBold(True)
        channels_label.setStyleSheet('font-size: 9pt')
        channels_label.setFont(font)
        layout.addWidget(channels_label, 1, 0, 1, 2)
        variables_label = QLabel('Variables')
        font = QFont()
        font.setBold(True)
        variables_label.setStyleSheet('font-size: 9pt')
        variables_label.setFont(font)
        layout.addWidget(variables_label, 1, 2, 1, 2)

        channels = channels or []
        n_channels = len(channels)
        self.channel_boxes = []
        self.channels = channels
        for i, channel in enumerate(channels):
            channel_label = QLabel(f'{channel}:')
            channel_box = QLineEdit()
            self.channel_boxes.append(channel_box)
            layout.addWidget(channel_label, 2+i, 0)
            layout.addWidget(channel_box, 2+i, 1)

        variables = variables or []
        n_variables = len(variables)
        self.variable_boxes = []
        self.variables = variables
        for i, variable in enumerate(variables):
            variable_label = QLabel(f'{variable}:')
            variable_box = QLineEdit()
            self.variable_boxes.append(variable_box)
            layout.addWidget(variable_label, 2+i, 2)
            layout.addWidget(variable_box, 2+i, 3)

        devs = devs or {}
        self.channel_devs = {}
        for dev, val in devs.items():
            self.channel_devs.update(get_channels(val))
        self.channel_table = None
        if free_channels:
            self.channel_table = Channels_Check_Table(self, ['set', 'channel', 'value'], True, channels=list(self.channel_devs.keys()))
            layout.addWidget(self.channel_table, 2+n_channels+n_variables, 0, 1, 2)
        if free_variables:
            header = ['variable', 'value']
            self.variable_table = AddRemoveTable(headerLabels=header)
            layout.addWidget(self.variable_table, 2+n_channels+n_variables, 2, 1, 2)

        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)

        self.setLayout(layout)
        layout.addWidget(text_label, 0, 0, 1, 4)
        layout.addWidget(self.buttonBox, 10+n_channels+n_variables, 0, 1, 4)
        self.setWindowTitle(title)
        # self.table.sizechange.connect(self.adjustSize)
        self.adjustSize()
        self.was_accepted = False
        self.set_variables = {}
        self.set_channels = {}

    def start_execution(self):
        self.done = False
        self.exec()

    def accept(self) -> None:
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
        var_table_data = self.variable_table.update_table_data()
        for i, var in enumerate(var_table_data['variable']):
            if var in self.set_variables:
                box = Prompt_Box('Critical',
                                 f'Cannot set two values to variable {var}!',
                                 'identical variable names')
                return box.exec()
            self.set_variables[var] = var_table_data['value'][i]
        channel_table_data = self.channel_table.get_info()
        for i, channel in enumerate(channel_table_data['channel']):
            if channel in self.set_channels:
                box = Prompt_Box('Critical',
                                 f'Cannot set two values to channel {channel}!',
                                 'identical channel names')
                return box.exec()
            self.set_channels[channel] = channel_table_data['value'][i]
        self.was_accepted = True
        self.done = True
        return super().accept()

    def reject(self) -> None:
        self.done = True
        return super().reject()

def get_channels(dev):
    """returns the components of an ophyd-device that are not listed in
    the configuration"""
    channels = {}
    for comp in dev.walk_components():
        if issubclass(comp.item.cls, SignalRO):
            continue
        name = comp.item.attr
        if name not in dev.configuration_attrs:
            channels[f'{dev.name}_{name}'] = [dev.name, name]
    return channels
