from PyQt5.QtWidgets import QCheckBox, QComboBox, QLabel, QWidget, QGridLayout, QStyle, QLineEdit

from CAMELS.main_classes.manual_control import Manual_Control, Manual_Control_Config
from CAMELS.utility import variables_handling

from .ui_stage_control import Ui_Form


class Stage_Control(Manual_Control, Ui_Form):
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if 'name' in control_data:
            name = control_data['name']
        else:
            name = 'Stage Control'
        super().__init__(parent=parent, title=name)
        self.setupUi(self)
        self.setWindowTitle(f'CAMELS - {name}')
        self.control_data = control_data

        self.pushButton_up.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        self.pushButton_down.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.pushButton_left.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton_right.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.pushButton_zUp.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        self.pushButton_zDown.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.pushButton_position.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.pushButton_stop.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))

        self.read_frequ = control_data['read_frequ'] if 'read_frequ' in control_data else 0.5
        self.stepSize_X = control_data['stepSize_X'] if 'stepSize_X' in control_data else 0
        self.stepSize_Y = control_data['stepSize_Y'] if 'stepSize_Y' in control_data else 0
        self.stepSize_Z = control_data['stepSize_Z'] if 'stepSize_Z' in control_data else 0
        self.manual_X = control_data['manual_X'] if 'manual_X' in control_data else 0
        self.manual_Y = control_data['manual_Y'] if 'manual_Y' in control_data else 0
        self.manual_Z = control_data['manual_Z'] if 'manual_Z' in control_data else 0
        self.go_to_X = control_data['go_to_X'] if 'go_to_X' in control_data else 0
        self.go_to_Y = control_data['go_to_Y'] if 'go_to_Y' in control_data else 0
        self.go_to_Z = control_data['go_to_Z'] if 'go_to_Z' in control_data else 0
        self.find_ref_X = control_data['find_ref_X'] if 'find_ref_X' in control_data else True
        self.find_ref_Y = control_data['find_ref_Y'] if 'find_ref_Y' in control_data else True
        self.find_ref_Z = control_data['find_ref_Z'] if 'find_ref_Z' in control_data else True
        self.manual_active = control_data['manual_active'] if 'manual_active' in control_data else False

        self.lineEdit_read_frequ.setText(str(self.read_frequ))
        self.lineEdit_stepX.setText(str(self.stepSize_X))
        self.lineEdit_stepY.setText(str(self.stepSize_Y))
        self.lineEdit_stepZ.setText(str(self.stepSize_Z))
        self.lineEdit_manualX.setText(str(self.manual_X))
        self.lineEdit_manualY.setText(str(self.manual_Y))
        self.lineEdit_manualZ.setText(str(self.manual_Z))
        self.lineEdit_goX.setText(str(self.go_to_X))
        self.lineEdit_goY.setText(str(self.go_to_Y))
        self.lineEdit_goZ.setText(str(self.go_to_Z))
        self.checkBox_refX.setChecked(self.find_ref_X)
        self.checkBox_refY.setChecked(self.find_ref_Y)
        self.checkBox_refZ.setChecked(self.find_ref_Z)
        self.checkBox_manualActive.setChecked(self.manual_active)

    def closeEvent(self, a0) -> None:
        self.control_data['read_frequ'] = self.read_frequ
        self.control_data['stepSize_X'] = self.stepSize_X
        self.control_data['stepSize_Y'] = self.stepSize_Y
        self.control_data['stepSize_Z'] = self.stepSize_Z
        self.control_data['manual_X'] = self.manual_X
        self.control_data['manual_Y'] = self.manual_Y
        self.control_data['manual_Z'] = self.manual_Z
        self.control_data['go_to_X'] = self.go_to_X
        self.control_data['go_to_Y'] = self.go_to_Y
        self.control_data['go_to_Z'] = self.go_to_Z
        self.control_data['find_ref_X'] = self.find_ref_X
        self.control_data['find_ref_Y'] = self.find_ref_Y
        self.control_data['find_ref_Z'] = self.find_ref_Z
        self.control_data['manual_active'] = self.manual_active
        return super().closeEvent(a0)




class Stage_Control_Config(Manual_Control_Config):
    def __init__(self, parent=None, control_data=None):
        super().__init__(parent=parent, control_data=control_data,
                         title='Stage Control Config',
                         control_type='Stage_Control')
        control_data = control_data or {}
        self.axis_checkboxes = []
        self.channels_combos = []
        self.read_checkboxes = []
        self.read_combos = []
        self.ref_combos = []
        self.ref_vals = []
        outputs = variables_handling.get_output_channels()
        channels = list(variables_handling.channels.keys())
        help_widge = QWidget()
        layout = QGridLayout()
        help_widge.setLayout(layout)
        for i, ax in enumerate(['x', 'y', 'z']):
            label = QLabel(ax)
            layout.addWidget(label, 2+i, 0)

            axis_box = QCheckBox(f'use axis {ax}')
            if 'use_axis' in control_data and control_data['use_axis']:
                axis_box.setChecked(control_data['use_axis'][i])
            self.axis_checkboxes.append(axis_box)
            layout.addWidget(axis_box, 2+i, 1)

            channel_combo = QComboBox()
            channel_combo.addItems(outputs)
            if 'axis_channel' in control_data and control_data['axis_channel'][i] in outputs:
                channel_combo.setCurrentText(control_data['axis_channel'][i])
            self.channels_combos.append(channel_combo)
            layout.addWidget(channel_combo, 2+i, 2)

            read_box = QCheckBox(f'readback axis {ax}')
            self.read_checkboxes.append(read_box)
            if 'read_axis' in control_data and control_data['read_axis']:
                read_box.setChecked(control_data['read_axis'][i])
            layout.addWidget(read_box, 2+i, 3)

            read_combo = QComboBox()
            read_combo.addItems(channels)
            if 'read_channel' in control_data and control_data['read_channel'][i] in channels:
                read_combo.setCurrentText(control_data['read_channel'][i])
            self.read_combos.append(read_combo)
            layout.addWidget(read_combo, 2+i, 4)

            label = QLabel(f'reference function {ax}:')
            layout.addWidget(label, 10+i, 0)


            ref_combo = QComboBox()
            ref_combo.addItems(outputs + ['None'])
            if 'axis_ref' in control_data and control_data['axis_ref'][i] in outputs:
                ref_combo.setCurrentText(control_data['axis_ref'][i])
            else:
                ref_combo.setCurrentText('None')
            self.ref_combos.append(ref_combo)
            layout.addWidget(ref_combo, 10+i, 1)

            ref_val = QLineEdit()
            if 'ref_vals' in control_data and control_data['ref_vals']:
                ref_val.setText(control_data['ref_vals'][i])
            self.ref_vals.append(ref_val)
            layout.addWidget(ref_val, 10+i, 2)

            axis_box.clicked.connect(self.change_usage)
            read_box.clicked.connect(self.change_usage)
        self.layout().addWidget(help_widge, 1, 0, 1, 2)
        self.change_usage()

    def change_usage(self):
        for i, box in enumerate(self.axis_checkboxes):
            able = box.isChecked()
            readback = self.read_checkboxes[i].isChecked()
            self.channels_combos[i].setEnabled(able)
            self.read_checkboxes[i].setEnabled(able)
            self.read_combos[i].setEnabled(able and readback)
            self.ref_combos[i].setEnabled(able)
            self.ref_vals[i].setEnabled(able)

    def accept(self):
        self.control_data['use_axis'] = []
        self.control_data['axis_channel'] = []
        self.control_data['read_axis'] = []
        self.control_data['read_channel'] = []
        self.control_data['axis_ref'] = []
        self.control_data['ref_vals'] = []
        for i in range(3):
            self.control_data['use_axis'].append(self.axis_checkboxes[i].isChecked())
            self.control_data['axis_channel'].append(self.channels_combos[i].currentText())
            self.control_data['read_axis'].append(self.read_checkboxes[i].isChecked())
            self.control_data['read_channel'].append(self.read_combos[i].currentText())
            self.control_data['ref_vals'].append(self.read_checkboxes[i].text())
            self.control_data['axis_ref'].append(self.read_combos[i].currentText())
        super().accept()

