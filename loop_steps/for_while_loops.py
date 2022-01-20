import numpy as np
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

from main_classes.loop_step import Loop_Step_Container, Loop_Step_Config
from utility.number_formatting import format_number
from utility import variables_handling

from gui.for_loop import Ui_for_loop_config

class For_Loop_Step(Loop_Step_Container):
    def __init__(self, name='', children=None, parent_step=None, step_info=None):
        super().__init__(name, children, parent_step)
        self.step_type = 'For Loop'
        if step_info is None:
            step_info = {}
        self.loop_type = step_info['loop_type'] if 'loop_type' in step_info else 'start - stop'
        self.start_val = step_info['start_val'] if 'start_val' in step_info else np.nan
        self.stop_val = step_info['stop_val'] if 'stop_val' in step_info else np.nan
        self.min_val = step_info['min_val'] if 'min_val' in step_info else np.nan
        self.max_val = step_info['max_val'] if 'max_val' in step_info else np.nan
        self.n_points = step_info['n_points'] if 'n_points' in step_info else np.nan
        self.sweep_mode = step_info['sweep_mode'] if 'sweep_mode' in step_info else 'linear'
        self.point_array = step_info['point_array'] if 'point_array' in step_info else []
        self.val_list = step_info['val_list'] if 'val_list' in step_info else []
        self.file_path = step_info['file_path'] if 'file_path' in step_info else ''
        self.include_end_points = step_info['include_end_points'] if 'include_end_points' in step_info else True
        # self.update_variables()

    def update_variables(self):
        variables = {f'{self.name.replace(" ", "_")}_Count': 0,
                     f'{self.name.replace(" ", "_")}_Value': np.nan}
        for variable in variables:
            if variable in variables_handling.loop_step_variables:
                raise Exception('Variable already defined!')
            variables_handling.loop_step_variables.update({variable: variables[variable]})
        super().update_variables()

    def get_protocol_string(self, n_tabs=1):
        tabs = '\t'*n_tabs
        protocol_string = f'{tabs}for {self.name.replace(" ", "_")}_Count, {self.name.replace(" ", "_")}_Value in enumerate({list(self.point_array)}):\n'
        protocol_string += f'{tabs}\tprint("starting loop_step {self.full_name}")\n'
        protocol_string += self.get_children_strings(n_tabs+1)
        self.update_time_weight()
        return protocol_string

    def update_time_weight(self):
        super().update_time_weight()
        self.time_weight *= len(self.point_array)

class For_Loop_Step_Config(Loop_Step_Config):
    def __init__(self, loop_step:For_Loop_Step, parent=None):
        super().__init__(parent, loop_step)
        self.sub_widget = For_Loop_Step_Config_Sub(parent=self, loop_step=loop_step)
        self.layout().addWidget(self.sub_widget, 1, 0)

    def update_step_config(self):
        super().update_step_config()

class For_Loop_Step_Config_Sub(QWidget, Ui_for_loop_config):
    def __init__(self, loop_step:For_Loop_Step, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loop_step = loop_step
        self.load_data()
        self.loop_type_change()
        self.build_preview_array()

        self.comboBox_loop_type.currentTextChanged.connect(self.loop_type_change)
        self.lineEdit_start.textChanged.connect(self.change_n_points)
        self.lineEdit_stop.textChanged.connect(self.change_n_points)
        self.lineEdit_min.textChanged.connect(self.change_n_points)
        self.lineEdit_max.textChanged.connect(self.change_n_points)
        self.lineEdit_point_distance.textChanged.connect(self.change_point_dist)
        self.lineEdit_n_points.textChanged.connect(self.change_n_points)
        self.checkBox_include_endpoints.clicked.connect(self.change_n_points)
        self.comboBox_sweep_mode.currentTextChanged.connect(self.change_sweep_mode)
        self.pushButton_del_point.clicked.connect(self.del_point)
        self.pushButton_add_point.clicked.connect(self.add_point)

        self.tableWidget_points.cellChanged.connect(self.value_list_changed)
        self.path_line_button.path_changed.connect(self.build_preview_array)

        self.building = False

    def load_data(self):
        self.comboBox_loop_type.setCurrentText(self.loop_step.loop_type)
        if not np.isnan(self.loop_step.start_val):
            self.lineEdit_start.setText(str(self.loop_step.start_val))
        if not np.isnan(self.loop_step.stop_val):
            self.lineEdit_stop.setText(str(self.loop_step.stop_val))
        if not np.isnan(self.loop_step.min_val):
            self.lineEdit_min.setText(str(self.loop_step.min_val))
        if not np.isnan(self.loop_step.max_val):
            self.lineEdit_max.setText(str(self.loop_step.max_val))
        if not np.isnan(self.loop_step.n_points):
            self.lineEdit_n_points.setText(str(self.loop_step.n_points))
        self.comboBox_sweep_mode.setCurrentText(self.loop_step.sweep_mode)
        self.checkBox_include_endpoints.setChecked(self.loop_step.include_end_points)
        self.path_line_button.set_path(self.loop_step.file_path)


    def loop_type_change(self):
        combo_text = self.comboBox_loop_type.currentText()
        if self.comboBox_loop_type.currentText() == 'start - stop':
            self.path_line_button.setEnabled(False)
            self.sweep_widget.setEnabled(True)
            self.lineEdit_max.setEnabled(False)
            self.lineEdit_min.setEnabled(False)
            self.pushButton_add_point.setEnabled(False)
            self.pushButton_del_point.setEnabled(False)
            self.label_min.setEnabled(False)
            self.label_max.setEnabled(False)
        elif combo_text in ['start - min - max - stop', 'start - max - min - stop']:
            self.path_line_button.setEnabled(False)
            self.sweep_widget.setEnabled(True)
            self.lineEdit_max.setEnabled(True)
            self.lineEdit_min.setEnabled(True)
            self.pushButton_add_point.setEnabled(False)
            self.pushButton_del_point.setEnabled(False)
            self.label_min.setEnabled(True)
            self.label_max.setEnabled(True)
        elif combo_text == 'Value-List':
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
        if self.building:
            return
        try:
            start = float(self.lineEdit_start.text())
            stop = float(self.lineEdit_stop.text())
            distance = float(self.lineEdit_point_distance.text())
            points = int((stop - start) / distance)
        except (ValueError, ZeroDivisionError):
            return
        if self.checkBox_include_endpoints.isChecked():
            points += 1
        self.building = True
        self.lineEdit_n_points.setText(str(points))
        self.building = False
        self.build_preview_array()

    def change_n_points(self):
        if self.building:
            return
        try:
            start = float(self.lineEdit_start.text())
            stop = float(self.lineEdit_stop.text())
            points = int(self.lineEdit_n_points.text())
            self.loop_step.n_points = points
        except ValueError:
            return
        if self.comboBox_sweep_mode.currentText() == 'linear':
            vals = np.linspace(start, stop, points, endpoint=self.checkBox_include_endpoints.isChecked())
            distance = vals[1] - vals[0] if len(vals) > 1 else np.nan
        else:
            distance = np.nan
        self.building = True
        self.lineEdit_point_distance.setText(format_number(distance))
        self.building = False
        self.build_preview_array()
        self.loop_step.include_end_points = self.checkBox_include_endpoints.isChecked()

    def change_sweep_mode(self):
        if self.comboBox_sweep_mode.currentText() == 'linear':
            self.lineEdit_point_distance.setEnabled(True)
        else:
            self.lineEdit_point_distance.setEnabled(False)
        self.build_preview_array()
        self.loop_step.sweep_mode = self.comboBox_sweep_mode.currentText()

    def build_preview_array(self):
        self.tableWidget_points.clear()
        self.tableWidget_points.setRowCount(0)
        if self.comboBox_loop_type.currentText() in ['start - stop', 'start - min - max - stop', 'start - max - min - stop']:
            try:
                start = float(self.lineEdit_start.text())
                self.loop_step.start_val = start
            except ValueError:
                start = np.nan
            try:
                stop = float(self.lineEdit_stop.text())
                self.loop_step.stop_val = stop
            except ValueError:
                stop = np.nan
            try:
                points = int(self.lineEdit_n_points.text())
                self.loop_step.n_points = points
            except ValueError:
                points = 0
            if self.comboBox_loop_type.currentText() == 'start - stop':
                vals = self.get_space(start, stop, points)
            else:
                try:
                    min_val = float(self.lineEdit_min.text())
                    self.loop_step.min_val = min_val
                except ValueError:
                    min_val = np.nan
                try:
                    max_val = float(self.lineEdit_max.text())
                    self.loop_step.max_val = max_val
                except ValueError:
                    max_val = np.nan
                try:
                    if self.comboBox_sweep_mode.currentText() == 'start - min - max - stop':
                        part_points1 = round(points * np.abs(start-min_val)/np.abs(max_val-min_val))
                        part_points2 = round(points * np.abs(stop-max_val)/np.abs(max_val-min_val))
                        vals1 = self.get_space(start, min_val, part_points1)
                        vals2 = self.get_space(min_val, max_val, points)
                        vals3 = self.get_space(max_val, stop, part_points2)
                    else:
                        part_points1 = round(points * np.abs(start-max_val)/np.abs(max_val-min_val))
                        part_points2 = round(points * np.abs(stop-min_val)/np.abs(max_val-min_val))
                        vals1 = self.get_space(start, max_val, part_points1)
                        vals2 = self.get_space(max_val, min_val, points)
                        vals3 = self.get_space(min_val, stop, part_points2)
                    vals = np.concatenate([vals1, vals2, vals3])
                except ValueError:
                    return [np.nan]
        elif self.comboBox_loop_type.currentText() == 'Value-List':
            vals = self.loop_step.val_list
        else:
            try:
                file = self.path_line_button.get_path()
                vals = np.loadtxt(file)
                self.loop_step.file_path = file
            except OSError:
                return
        self.tableWidget_points.setRowCount(len(vals))
        self.tableWidget_points.horizontalHeader().hide()
        self.tableWidget_points.setColumnCount(1)
        self.loop_step.point_array = vals
        for i, val in enumerate(vals):
            # TODO put value where to start scientific notation into settings
            item = QTableWidgetItem(format_number(val))
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableWidget_points.setItem(i, 0, item)
        if self.comboBox_loop_type.currentText() == 'Value-List':
            for i in range(self.tableWidget_points.rowCount()):
                item = self.tableWidget_points.item(i, 0)
                item.setFlags(item.flags() | Qt.ItemIsEditable)

    def add_point(self):
        rows = self.tableWidget_points.rowCount()
        self.tableWidget_points.setRowCount(rows+1)
        self.loop_step.val_list.append(0)
        item = QTableWidgetItem('0')
        self.tableWidget_points.setItem(rows, 0, item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)

    def del_point(self):
        indexes = self.tableWidget_points.selectedIndexes()
        for index in sorted(indexes, key=lambda x: -x.row()):
            self.tableWidget_points.removeRow(index.row())
            self.loop_step.val_list.pop(index.row())

    def value_list_changed(self, row):
        if self.comboBox_loop_type.currentText() == 'Value-List':
            try:
                self.loop_step.val_list[row] = float(self.tableWidget_points.item(row, 0).text())
            except ValueError:
                return

    def get_space(self, start, stop, points):
        try:
            if self.comboBox_sweep_mode.currentText() == 'linear':
                vals = np.linspace(start, stop, points, endpoint=self.checkBox_include_endpoints.isChecked())
            elif self.comboBox_sweep_mode.currentText() == 'logarithmic':
                start = np.log(start)
                stop = np.log(stop)
                vals = np.linspace(start, stop, points, endpoint=self.checkBox_include_endpoints.isChecked())
                vals = np.exp(vals)
            elif self.comboBox_sweep_mode.currentText() == 'exponential':
                start = np.exp(start)
                stop = np.exp(stop)
                vals = np.linspace(start, stop, points, endpoint=self.checkBox_include_endpoints.isChecked())
                vals = np.log(vals)
            else:
                start = 1/start
                stop = 1/stop
                vals = np.linspace(start, stop, points, endpoint=self.checkBox_include_endpoints.isChecked())
                vals = 1/vals
        except ValueError:
            vals = [np.nan]
        return vals
