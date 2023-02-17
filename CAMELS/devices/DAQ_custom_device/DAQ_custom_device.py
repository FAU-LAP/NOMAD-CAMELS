import copy

from PyQt5.QtWidgets import QCheckBox, QLineEdit, QComboBox, QLabel, QFrame,\
    QTabWidget, QGridLayout, QWidget

from main_classes import device_class

from DAQ_custom_device.DAQ_custom_device_ophyd import Custom_DAQ_Device


class subclass(device_class.Device):
    def __init__(self, **kwargs):
        files = []
        req = []
        super().__init__(name='DAQ_custom_device', virtual=False, tags=['DAQ'], directory='DAQ_custom_device', ophyd_device=Custom_DAQ_Device, requirements=req, files=files, ophyd_class_name='Custom_DAQ_Device',
                         **kwargs)

    def get_finalize_steps(self):
        s = '\t\tfrom bluesky_handling import daq_signal\n'
        s += '\t\tdaq_signal.close_tasks()\n'
        return s

    def get_settings(self):
        return {'component_setups': self.settings}

    def get_channels(self):
        channels = copy.deepcopy(super().get_channels())
        keeps = []
        for keep_key in self.settings.keys():
            for key in self.channels:
                if key.endswith(keep_key):
                    keeps.append(key)
        for r in self.channels:
            if r not in keeps:
                channels.pop(r)
        return channels


class subclass_config(device_class.Device_Config):
    def __init__(self, parent=None, data='', settings_dict=None,
                 config_dict=None, ioc_dict=None, additional_info=None):
        super().__init__(parent, 'Custom DAQ device', data, settings_dict,
                         config_dict, ioc_dict, additional_info)
        self.layout().removeWidget(self.comboBox_connection_type)
        self.comboBox_connection_type.deleteLater()
        self.layout().removeWidget(self.label_connection)
        self.label_connection.deleteLater()
        self.layout().removeWidget(self.checkBox_use_local_ioc)
        self.checkBox_use_local_ioc.deleteLater()
        self.layout().removeWidget(self.lineEdit_ioc_name)
        self.lineEdit_ioc_name.deleteLater()
        self.layout().removeWidget(self.label_ioc_name)
        self.label_ioc_name.deleteLater()

        self.tabwidge = QTabWidget()
        self.input_widge = Channel_Widget(settings=settings_dict)
        self.output_widge = Channel_Widget(is_input=False, settings=settings_dict)

        self.tabwidge.addTab(self.input_widge, 'Input')
        self.tabwidge.addTab(self.output_widge, 'Output')
        self.layout().addWidget(self.tabwidge, 20, 0, 1, 5)

    def get_ioc_settings(self):
        return {}

    def get_settings(self):
        sets = self.input_widge.get_settings()
        sets.update(self.output_widge.get_settings())
        return sets





class Channel_Widget(QWidget):

    def __init__(self, parent=None, is_input=True, settings=None):
        super().__init__(parent)
        self.settings = settings or {}
        self.is_input = is_input
        layout = QGridLayout()
        self.setLayout(layout)
        terminal_configs = ['default', 'bal_diff', 'nrse', 'pseudodifferential',
                            'rse']

        self.comboboxes = []
        self.checkboxes_use = []
        self.checkboxes_digital = []
        self.lineedits_name = []
        self.lineedits_minv = []
        self.lineedits_maxv = []
        self.labels_minv = []
        self.labels_maxv = []
        self.labels_name = []
        self.labels_combobox = []
        self.change_use()
        for i in range(1, 9):
            if is_input:
                usebox = QCheckBox(f'Use input channel {i}')
            else:
                usebox = QCheckBox(f'Use output channel {i}')
            usebox.clicked.connect(self.change_use)
            self.checkboxes_use.append(usebox)
            digbox = QCheckBox('is digital')
            digbox.clicked.connect(self.change_use)
            self.checkboxes_digital.append(digbox)
            maxline = QLineEdit()
            self.lineedits_maxv.append(maxline)
            minline = QLineEdit()
            self.lineedits_minv.append(minline)
            nameline = QLineEdit()
            self.lineedits_name.append(nameline)
            label_maxv = QLabel('max (V)')
            self.labels_maxv.append(label_maxv)
            label_minv = QLabel('min (V)')
            self.labels_minv.append(label_minv)
            label_name = QLabel('line name')
            self.labels_name.append(label_name)

            shifter = 3 if i > 4 else 0
            shifter_down = 6*((i - 1) % 4)
            self.layout().addWidget(usebox, shifter_down, shifter)
            self.layout().addWidget(digbox, shifter_down, 1+shifter)
            self.layout().addWidget(label_name, 1+shifter_down, shifter)
            self.layout().addWidget(nameline, 1+shifter_down, 1+shifter)
            self.layout().addWidget(label_minv, 2+shifter_down, shifter)
            self.layout().addWidget(minline, 2+shifter_down, 1+shifter)
            self.layout().addWidget(label_maxv, 3+shifter_down, shifter)
            self.layout().addWidget(maxline, 3+shifter_down, 1+shifter)
            if is_input:
                combobox = QComboBox()
                combobox.addItems(terminal_configs)
                self.comboboxes.append(combobox)
                label_combo = QLabel('terminal config')
                self.labels_combobox.append(label_combo)
                self.layout().addWidget(label_combo, 4+shifter_down, shifter)
                self.layout().addWidget(combobox, 4+shifter_down, 1+shifter)
            if i % 4:
                line = QFrame(self)
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                self.layout().addWidget(line, 5+shifter_down, shifter, 1, 2)

            if is_input and f'in{i}' in self.settings:
                sets = self.settings[f'in{i}']
                usebox.setChecked(True)
                digbox.setChecked(sets['digital'])
                combobox.setCurrentText('terminal_config')
                minline.setText(str(sets['minV']))
                maxline.setText(str(sets['maxV']))
                nameline.setText(sets['line_name'])
            elif not is_input and f'out{i}' in self.settings:
                sets = self.settings[f'out{i}']
                usebox.setChecked(True)
                digbox.setChecked(sets['digital'])
                minline.setText(str(sets['minV']))
                maxline.setText(str(sets['maxV']))
                nameline.setText(sets['line_name'])
        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout().addWidget(line, 0, 2, 4*6, 1)
        self.change_use()


    def change_use(self):
        for i, box in enumerate(self.checkboxes_use):
            use = box.isChecked()
            digi = self.checkboxes_digital[i].isChecked()
            self.checkboxes_digital[i].setHidden(not use)
            self.lineedits_name[i].setHidden(not use)
            self.lineedits_minv[i].setHidden(not use or digi)
            self.lineedits_maxv[i].setHidden(not use or digi)
            self.labels_maxv[i].setHidden(not use or digi)
            self.labels_minv[i].setHidden(not use or digi)
            self.labels_name[i].setHidden(not use)
            if self.is_input:
                self.comboboxes[i].setHidden(not use or digi)
                self.labels_combobox[i].setHidden(not use or digi)


    def get_settings(self):
        settings = {}
        for i, box in enumerate(self.checkboxes_use):
            if not box.isChecked():
                continue
            sets = {}
            sets['digital'] = self.checkboxes_digital[i].isChecked()
            sets['line_name'] = self.lineedits_name[i].text()
            text = self.lineedits_minv[i].text()
            sets['minV'] = float(text) if text else 0
            text = self.lineedits_maxv[i].text()
            sets['maxV'] = float(text) if text else 0
            if self.is_input:
                sets['terminal_config'] = self.comboboxes[i].currentText()
                name = f'in{i+1}'
            else:
                sets['terminal_config'] = 'default'
                name = f'out{i+1}'
            settings[name] = sets
        return settings


