import numpy as np
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QLabel, QGridLayout, QLineEdit
from PySide6.QtCore import Qt

from nomad_camels.main_classes.loop_step import Loop_Step_Container, Loop_Step_Config
from nomad_camels.utility.number_formatting import format_number
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.variable_tool_tip_box import Variable_Box

from nomad_camels.gui.for_loop import Ui_for_loop_config


class While_Loop_Step(Loop_Step_Container):
    """A loopstep that adds a simple While Loop with a condition, that
    may be just written as python-code.

    Attributes
    ----------
    condition : str
        The condition which is used for the loop. It should be interpretable
        python-code within the namespace of the protocol.
    expected_iterations : int, default 1
        The expected number of iterations, used for the steps time weight for
        the progress bar. Ideally rather too large than to small (otherwise the
        progress bar reaches 100% too early).
    """

    def __init__(
        self, name="", children=None, parent_step=None, step_info=None, **kwargs
    ):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        self.step_type = "While Loop"
        if step_info is None:
            step_info = {}
        self.condition = step_info["condition"] if "condition" in step_info else "!"
        self.expected_interations = (
            step_info["expected_interations"]
            if "expected_interations" in step_info
            else 1
        )

    def update_variables(self):
        """Here the Count of the while-loop is included as a variable."""
        variables = {f'{self.name.replace(" ", "_")}_Count': 0}
        for variable in variables:
            if variable in variables_handling.loop_step_variables:
                raise Exception("Variable already defined!")
        variables_handling.loop_step_variables.update(variables)
        super().update_variables()

    def get_protocol_string(self, n_tabs=1):
        """The string consists of declaring the count-variable. Then the
        while loop with the desired condition is started. After all the
        children-steps, the count-variable increased by 1."""
        self.update_time_weight()
        tabs = "\t" * n_tabs
        count_var = f'{self.name.replace(" ", "_")}_Count'
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f"{tabs}{count_var} = 0\n"
        protocol_string += f'{tabs}namespace["{count_var}"] = {count_var}\n'
        protocol_string += f'{tabs}while eva.eval("{self.condition}"):\n'
        protocol_string += f'{tabs}\tnamespace["{count_var}"] = {count_var}\n'
        protocol_string += self.get_children_strings(n_tabs + 1)
        protocol_string += f"{tabs}\t{count_var} += 1\n"
        return protocol_string

    def update_time_weight(self):
        """Multiplies the time_weight of the children with the expected
        iterations + 5"""
        super().update_time_weight()
        self.time_weight *= self.expected_interations + 5

    def get_protocol_short_string(self, n_tabs=0):
        """Adds the condition to the string"""
        tabs = "\t" * n_tabs
        short_string = f"{tabs}'{self.name}' while {self.condition}:\n"
        for child in self.children:
            short_string += child.get_protocol_short_string(n_tabs + 1)
        return short_string


class While_Loop_Step_Config(Loop_Step_Config):
    """Configuration-Widget for the while-loop step."""

    def __init__(self, loop_step: While_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = While_Loop_Step_Config_Sub(loop_step, self)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)


class While_Loop_Step_Config_Sub(QWidget):
    """Sub-config for the while-loop. It consists only of a single line
    that takes the condition for the while loop.

    Parameters
    ----------

    Returns
    -------

    """

    def __init__(self, loop_step: While_Loop_Step, parent=None):
        super().__init__(parent)
        self.loop_step = loop_step

        label = QLabel("Condition:")
        label_it = QLabel("Expected number of iterations:")
        self.lineEdit_condition = Variable_Box(self)
        self.lineEdit_condition.setText(loop_step.condition)
        self.lineEdit_expection = QLineEdit(str(loop_step.expected_interations))
        self.lineEdit_condition.textChanged.connect(self.update_condition)
        self.lineEdit_expection.textChanged.connect(self.update_condition)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.lineEdit_condition, 0, 1)
        layout.addWidget(label_it, 1, 0)
        layout.addWidget(self.lineEdit_expection, 1, 1)
        self.setLayout(layout)

    def update_condition(self):
        """Saves the condition into the loop_step."""
        self.loop_step.condition = self.lineEdit_condition.text()
        try:
            self.loop_step.expected_interations = float(self.lineEdit_expection.text())
        except:
            pass


class For_Loop_Step(Loop_Step_Container):
    """Loop_Step representing a For Loop. It offers several ways of
    defining the sweep.

    Attributes
    ----------
    loop_type : str
        can be one of the following:
        - "start - stop" the loop goes from `min_val` to `max_val`
        - "start - min - max - stop" or "start - max - min - stop" goes from start over min/max, max/min to stop
        - "Value-List" the loop uses the values inside `val_list`
        - "Text-File" the loop uses the values of a single-column text file given by `file_path`
    sweep_mode : str
        only relevant if not using "Value-List" or "Text-File" mode
        can be:
        - "linear" the loop goes over a simple linear space
        - "logarithmic" the steps increase logarithmically
        - "exponential" the steps increase exponentially
        - "1/x" the steps increase with 1/x
    start_val : float
        the first value for the loop
    stop_val : float
        the last value for the loop
    min_val : float
        the minimum value for the loop
    max_val : float
        the maximum value for the loop
    n_points : int
        the number of points the loop iterates over. If using the max
        and min-vals, the distance between those is used, thus in total
        creating more steps
    n_iterations : int
        number of runs the loop will do
    val_list : list of float
        a list of all the steps, the loop iterates over, used if
        "Value-List" is chosen
    file_path : str or path
        the path where the file for "Text-File" is lying
    include_end_points : bool
        whether to include the `stop_val` into the iteration
    """

    def __init__(
        self, name="", children=None, parent_step=None, step_info=None, **kwargs
    ):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        self.step_type = "For Loop"
        if step_info is None:
            step_info = {}
        self.loop_type = (
            step_info["loop_type"] if "loop_type" in step_info else "start - stop"
        )
        self.start_val = step_info["start_val"] if "start_val" in step_info else ""
        self.stop_val = step_info["stop_val"] if "stop_val" in step_info else ""
        self.min_val = step_info["min_val"] if "min_val" in step_info else ""
        self.max_val = step_info["max_val"] if "max_val" in step_info else ""
        self.n_points = step_info["n_points"] if "n_points" in step_info else ""
        self.sweep_mode = (
            step_info["sweep_mode"] if "sweep_mode" in step_info else "linear"
        )
        self.n_iterations = (
            step_info["n_iterations"] if "n_iterations" in step_info else 0
        )
        # self.point_array = step_info['point_array'] if 'point_array' in step_info else []
        self.val_list = step_info["val_list"] if "val_list" in step_info else []
        self.file_path = step_info["file_path"] if "file_path" in step_info else ""
        self.include_end_points = (
            step_info["include_end_points"]
            if "include_end_points" in step_info
            else True
        )
        self.use_distance = (
            step_info["use_distance"] if "use_distance" in step_info else False
        )
        self.point_distance = (
            step_info["point_distance"] if "point_distance" in step_info else ""
        )
        # self.update_variables()

    def update_variables(self):
        """Includes the value and iteration-count of the loop."""
        variables = {
            f'{self.name.replace(" ", "_")}_Count': 0,
            f'{self.name.replace(" ", "_")}_Value': 0,
        }
        for variable in variables:
            if variable in variables_handling.loop_step_variables:
                raise Exception("Variable already defined!")
        variables_handling.loop_step_variables.update(variables)
        super().update_variables()

    def get_protocol_string(self, n_tabs=1):
        """The loop is enumerating over the selected points. When using a range,
        the get_range helper function is used."""
        tabs = "\t" * n_tabs
        if self.loop_type in [
            "start - stop",
            "start - min - max - stop",
            "start - max - min - stop",
        ]:
            enumerator = f'helper_functions.get_range(eva, "{self.start_val}", "{self.stop_val}", "{self.n_points}", "{self.min_val or np.nan}", "{self.max_val or np.nan}", "{self.loop_type}", "{self.sweep_mode}", "{self.include_end_points}", "{self.point_distance}", {self.use_distance})'
            # enumerator = get_space_string(self.start_val, self.stop_val,
            #                               self.n_points, self.min_val,
            #                               self.max_val, self.loop_type,
            #                               self.sweep_mode,
            #                               self.include_end_points)
        elif self.loop_type == "Value-List":
            enumerator = self.val_list
        else:
            enumerator = f'np.loadtxt("{self.file_path}")'
        protocol_string = super().get_protocol_string(n_tabs)
        protocol_string += f'{tabs}for {self.name.replace(" ", "_")}_Count, {self.name.replace(" ", "_")}_Value in enumerate({enumerator}):\n'
        protocol_string += f'{tabs}\tnamespace.update({{"{self.name.replace(" ", "_")}_Count": {self.name.replace(" ", "_")}_Count, "{self.name.replace(" ", "_")}_Value": {self.name.replace(" ", "_")}_Value}})\n'
        protocol_string += self.get_children_strings(n_tabs + 1)
        self.update_time_weight()
        return protocol_string

    def update_time_weight(self):
        """Multiplies the children time_weight (-1 for the step itself) by the
        number of iterations and adds 1 (for the step itself)."""
        super().update_time_weight()
        self.time_weight = (self.time_weight - 1) * self.n_iterations + 1

    def get_protocol_short_string(self, n_tabs=0):
        """Shows the type of loop and the range in the short string as well"""
        tabs = "\t" * n_tabs
        if self.loop_type == "Value-List":
            vals = self.val_list
        elif self.loop_type in [
            "start - stop",
            "start - min - max - stop",
            "start - max - min - stop",
        ]:
            vals = f"(start: {self.start_val}, stop: {self.stop_val}, "
            if "max" in self.loop_type:
                vals += f"min: {self.min_val}, max: {self.max_val}, "
            vals += f"points: {self.n_points})"
        else:
            vals = self.file_path
        short_string = f"{tabs}'{self.name}' for {vals}:\n"
        for child in self.children:
            short_string += child.get_protocol_short_string(n_tabs + 1)
        return short_string


class For_Loop_Step_Config(Loop_Step_Config):
    """Configuration-Widget for the for-loop step."""

    def __init__(self, loop_step: For_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = For_Loop_Step_Config_Sub(parent=self, loop_step=loop_step)
        self.layout().addWidget(self.sub_widget, 1, 0, 1, 5)


class For_Loop_Step_Config_Sub(Ui_for_loop_config, QWidget):
    """Provides the main config for the For Loop."""

    def __init__(self, loop_step: For_Loop_Step, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loop_step = loop_step
        self.load_data()
        self.loop_type_change()
        self.build_preview_array()

        self.comboBox_loop_type.currentTextChanged.connect(self.loop_type_change)
        self.lineEdit_start.textChanged.connect(self.change_dist_n_mode)
        self.lineEdit_stop.textChanged.connect(self.change_dist_n_mode)
        self.lineEdit_min.textChanged.connect(self.change_dist_n_mode)
        self.lineEdit_max.textChanged.connect(self.change_dist_n_mode)
        self.lineEdit_point_distance.textChanged.connect(self.change_point_dist)
        self.lineEdit_n_points.textChanged.connect(self.change_n_points)
        self.checkBox_include_endpoints.clicked.connect(self.change_dist_n_mode)
        self.comboBox_sweep_mode.currentTextChanged.connect(self.change_sweep_mode)
        self.pushButton_del_point.clicked.connect(self.del_point)
        self.pushButton_add_point.clicked.connect(self.add_point)
        self.radioButton_n_points.clicked.connect(self.change_dist_n_mode)
        self.radioButton_point_distance.clicked.connect(self.change_dist_n_mode)

        self.tableWidget_points.cellChanged.connect(self.value_list_changed)
        self.path_line_button.path_changed.connect(self.build_preview_array)

        self.building = False
        self.change_dist_n_mode()

    def load_data(self):
        """Loads the data from the loop_step into the UI-widgets."""
        self.comboBox_loop_type.setCurrentText(self.loop_step.loop_type)
        self.lineEdit_start.setText(self.loop_step.start_val)
        self.lineEdit_stop.setText(self.loop_step.stop_val)
        self.lineEdit_min.setText(self.loop_step.min_val)
        self.lineEdit_max.setText(self.loop_step.max_val)
        self.lineEdit_n_points.setText(self.loop_step.n_points)
        self.lineEdit_point_distance.setText(self.loop_step.point_distance)
        self.radioButton_n_points.setChecked(not self.loop_step.use_distance)
        self.radioButton_point_distance.setChecked(self.loop_step.use_distance)
        self.comboBox_sweep_mode.setCurrentText(self.loop_step.sweep_mode)
        self.checkBox_include_endpoints.setChecked(self.loop_step.include_end_points)
        self.path_line_button.set_path(self.loop_step.file_path)

    def loop_type_change(self):
        """Enables / disables the respective elements that are used for
        the single loop-types, then builds the preview.

        Parameters
        ----------

        Returns
        -------

        """
        combo_text = self.comboBox_loop_type.currentText()
        if self.comboBox_loop_type.currentText() == "start - stop":
            self.path_line_button.setEnabled(False)
            self.sweep_widget.setEnabled(True)
            self.lineEdit_max.setEnabled(False)
            self.lineEdit_min.setEnabled(False)
            self.pushButton_add_point.setEnabled(False)
            self.pushButton_del_point.setEnabled(False)
            self.label_min.setEnabled(False)
            self.label_max.setEnabled(False)
        elif combo_text in ["start - min - max - stop", "start - max - min - stop"]:
            self.path_line_button.setEnabled(False)
            self.sweep_widget.setEnabled(True)
            self.lineEdit_max.setEnabled(True)
            self.lineEdit_min.setEnabled(True)
            self.pushButton_add_point.setEnabled(False)
            self.pushButton_del_point.setEnabled(False)
            self.label_min.setEnabled(True)
            self.label_max.setEnabled(True)
        elif combo_text == "Value-List":
            self.path_line_button.setEnabled(False)
            self.sweep_widget.setEnabled(False)
            self.pushButton_add_point.setEnabled(True)
            self.pushButton_del_point.setEnabled(True)
        else:
            self.path_line_button.setEnabled(True)
            self.sweep_widget.setEnabled(False)
            self.pushButton_add_point.setEnabled(False)
            self.pushButton_del_point.setEnabled(False)
        self.build_preview_array()
        self.loop_step.loop_type = combo_text

    def change_point_dist(self):
        """Updates the number of points when the distance between them
        is changed.

        Parameters
        ----------

        Returns
        -------

        """
        if self.radioButton_n_points.isChecked():
            return
        if self.building:
            return
        self.build_preview_array()
        points = self.loop_step.n_iterations
        self.building = True
        self.lineEdit_n_points.setText(str(points))
        self.building = False

    def change_n_points(self):
        """Updates the displayed distance between the points when their
        number is changed.

        Parameters
        ----------

        Returns
        -------

        """
        if self.radioButton_point_distance.isChecked():
            return
        if self.building:
            return
        self.build_preview_array()
        self.loop_step.include_end_points = self.checkBox_include_endpoints.isChecked()
        self.building = True
        self.lineEdit_point_distance.setText(format_number(self.distance))
        self.building = False

    def change_dist_n_mode(self):
        use_dist = self.radioButton_point_distance.isChecked()
        self.loop_step.use_distance = use_dist
        if use_dist:
            self.change_point_dist()
        else:
            self.change_n_points()
        self.lineEdit_n_points.setEnabled(not use_dist)
        self.lineEdit_point_distance.setEnabled(use_dist)

    def change_sweep_mode(self):
        """Enables / disables the point-distance widget corresponding to
        the selected sweep mode.

        Parameters
        ----------

        Returns
        -------

        """
        if self.comboBox_sweep_mode.currentText() == "linear":
            self.radioButton_point_distance.setEnabled(True)
        else:
            self.radioButton_point_distance.setEnabled(False)
            self.loop_step.use_distance = self.radioButton_point_distance.isChecked()
            self.radioButton_point_distance.setChecked(False)
            self.radioButton_n_points.setChecked(True)
        self.change_dist_n_mode()
        self.loop_step.sweep_mode = self.comboBox_sweep_mode.currentText()

    def build_preview_array(self):
        """Builds the displayed array to preview the steps, the for loop
        will make.

        Parameters
        ----------

        Returns
        -------

        """
        self.tableWidget_points.clear()
        self.tableWidget_points.setRowCount(0)
        if self.comboBox_loop_type.currentText() in [
            "start - stop",
            "start - min - max - stop",
            "start - max - min - stop",
        ]:
            try:
                start = self.lineEdit_start.text()
                self.loop_step.start_val = start
            except ValueError:
                start = np.nan
            try:
                stop = self.lineEdit_stop.text()
                self.loop_step.stop_val = stop
            except ValueError:
                stop = np.nan
            try:
                points = self.lineEdit_n_points.text()
                self.loop_step.n_points = points
            except ValueError:
                points = 0
            try:
                distance = self.lineEdit_point_distance.text()
                self.loop_step.point_distance = distance
            except ValueError:
                distance = np.nan
            use_distance = self.radioButton_point_distance.isChecked()
            self.loop_step.use_distance = use_distance
            try:
                min_val = self.lineEdit_min.text()
                self.loop_step.min_val = min_val
            except ValueError:
                min_val = np.nan
            try:
                max_val = self.lineEdit_max.text()
                self.loop_step.max_val = max_val
            except ValueError:
                max_val = np.nan
            from nomad_camels.bluesky_handling import (
                helper_functions,
                evaluation_helper,
            )

            min_val = min_val if min_val != "" else np.nan
            max_val = max_val if max_val != "" else np.nan
            start = start if start != "" else np.nan
            stop = stop if stop != "" else np.nan
            points = points if points != "" else 0
            distance = distance if distance != "" else np.nan
            namespace = {}
            namespace.update(variables_handling.protocol_variables)
            namespace.update(variables_handling.loop_step_variables)
            for channel in variables_handling.channels:
                namespace.update({channel: 1})
            try:
                vals = helper_functions.get_range(
                    evaluator=evaluation_helper.Evaluator(namespace=namespace),
                    start=start,
                    stop=stop,
                    points=points,
                    min_val=min_val,
                    max_val=max_val,
                    distance=distance,
                    loop_type=self.comboBox_loop_type.currentText(),
                    sweep_mode=self.comboBox_sweep_mode.currentText(),
                    endpoint=self.checkBox_include_endpoints.isChecked(),
                    use_distance=use_distance,
                )
            except (ValueError, ZeroDivisionError) as e:
                if e.args[0] == "Start and Stop must be between min and max!":
                    vals = "Start and Stop must be between Min and Max!".split()
                else:
                    return [np.nan]
        elif self.comboBox_loop_type.currentText() == "Value-List":
            vals = self.loop_step.val_list
        else:
            try:
                file = self.path_line_button.get_path()
                vals = np.loadtxt(file)
                self.loop_step.file_path = file
            except OSError:
                return
        self.tableWidget_points.setRowCount(len(vals) if len(vals) < 1001 else 1001)
        self.tableWidget_points.horizontalHeader().hide()
        self.tableWidget_points.setColumnCount(1)
        self.loop_step.n_iterations = len(vals)
        try:
            self.distance = vals[1] - vals[0] if len(vals) > 1 else np.nan
        except:
            self.distance = np.nan
        for i, val in enumerate(vals):
            item = QTableWidgetItem(val if isinstance(val, str) else format_number(val))
            if i == 1000:
                item = QTableWidgetItem("...")
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget_points.setItem(i, 0, item)
            if i == 1000:
                break
        if self.comboBox_loop_type.currentText() == "Value-List":
            for i in range(self.tableWidget_points.rowCount()):
                item = self.tableWidget_points.item(i, 0)
                item.setFlags(item.flags() | Qt.ItemIsEditable)

    def add_point(self):
        """Used to add a point when using the "Value-List" loop-type."""
        rows = self.tableWidget_points.rowCount()
        self.tableWidget_points.setRowCount(rows + 1)
        self.loop_step.val_list.append(0)
        item = QTableWidgetItem("0")
        self.tableWidget_points.setItem(rows, 0, item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)

    def del_point(self):
        """Used to remove a point when using the "Value-List" loop-type."""
        indexes = self.tableWidget_points.selectedIndexes()
        for index in sorted(indexes, key=lambda x: -x.row()):
            self.tableWidget_points.removeRow(index.row())
            self.loop_step.val_list.pop(index.row())

    def value_list_changed(self, row):
        """Updates the `val_list` of the loopstep when it is changed.

        Parameters
        ----------
        row :


        Returns
        -------

        """
        if self.comboBox_loop_type.currentText() == "Value-List":
            try:
                self.loop_step.val_list[row] = float(
                    self.tableWidget_points.item(row, 0).text()
                )
            except ValueError:
                return
