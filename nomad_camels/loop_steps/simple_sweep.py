from PySide6.QtWidgets import QComboBox, QLabel, QCheckBox
from PySide6.QtGui import QFont

from nomad_camels.main_classes.loop_step import Loop_Step_Config
from nomad_camels.utility import variables_handling
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.utility.load_save_helper_functions import load_plots
from nomad_camels.bluesky_handling import builder_helper_functions
from nomad_camels.frontpanels.plot_definer import Plot_Button_Overview

from nomad_camels.loop_steps.for_while_loops import For_Loop_Step_Config_Sub, For_Loop_Step

class Simple_Sweep(For_Loop_Step):
    """ """
    def __init__(self, name='', children=None, parent_step=None, step_info=None,
                 **kwargs):
        super().__init__(name, children, parent_step, step_info, **kwargs)
        step_info = step_info or {}
        self.step_type = 'Simple Sweep'
        self.has_children = False
        self.sweep_channel = step_info['sweep_channel'] if 'sweep_channel' in step_info else ''
        self.data_output = step_info['data_output'] if 'data_output' in step_info else 'sub-stream'
        self.plots = load_plots([], step_info['plots']) if 'plots' in step_info else []
        self.read_channels = step_info['read_channels'] if 'read_channels' in step_info else []
        self.use_own_plots = step_info['use_own_plots'] if 'use_own_plots' in step_info else False
        self.calc_minmax = step_info['calc_minmax'] if 'calc_minmax' in step_info else False
        self.calc_mean = step_info['calc_mean'] if 'calc_mean' in step_info else False
        self.calc_stddev = step_info['calc_stddev'] if 'calc_stddev' in step_info else False
        self.use_custom_fit = step_info['use_custom_fit'] if 'use_custom_fit' in step_info else False
        self.calc_fit = step_info['calc_fit'] if 'calc_fit' in step_info else False
        self.predef_fit = step_info['predef_fit'] if 'predef_fit' in step_info else 'Linear'
        self.custom_fit = step_info['custom_fit'] if 'custom_fit' in step_info else ''
        self.fit_params = step_info['fit_params'] if 'fit_params' in step_info else {}
        self.guess_fit_params = step_info['guess_fit_params'] if 'guess_fit_params' in step_info else True

    def update_used_devices(self):
        """ """
        self.used_devices = []
        set_device = variables_handling.channels[self.sweep_channel].device
        self.used_devices.append(set_device)
        for channel in self.read_channels:
            if channel in variables_handling.channels:
                device = variables_handling.channels[channel].device
                if device not in self.used_devices:
                    self.used_devices.append(device)

    def update_variables(self):
        """ """
        variables = {}
        stream = f'{self.name}'
        for plot in self.plots:
            variables.update(plot.get_fit_vars(stream))
        variables_handling.loop_step_variables.update(variables)
        super().update_variables()



    def get_outer_string(self):
        """ """
        if self.use_own_plots:
            return builder_helper_functions.plot_creator(self.plots,
                                                         f'create_plots_{self.name}')[0]
        return ''

    def get_add_main_string(self):
        """ """
        stream = f'"{self.name}"'
        if self.data_output == 'main stream':
            stream = '"primary"'
        add_main_string = ''
        if self.use_own_plots:
            add_main_string += builder_helper_functions.get_plot_add_string(self.name, stream)
        return add_main_string

    def get_protocol_string(self, n_tabs=1):
        """The loop is enumerating over the selected points.

        Parameters
        ----------
        n_tabs :
             (Default value = 1)

        Returns
        -------

        """
        tabs = '\t'*n_tabs
        # if self.loop_type in ['start - stop', 'start - min - max - stop',
        #                       'start - max - min - stop']:
        #     enumerator = get_space_string(self.start_val, self.stop_val,
        #                                   self.n_points, self.min_val,
        #                                   self.max_val, self.loop_type,
        #                                   self.sweep_mode,
        #                                   self.include_end_points)
        # elif self.loop_type == 'Value-List':
        #     enumerator = self.val_list
        # else:
        #     enumerator = f'np.loadtxt("{self.file_path}")'

        stream = f'"{self.name}"'
        if self.data_output == 'main stream':
            stream = 'stream_name'

        protocol_string = f'{tabs}channels = ['
        for i, channel in enumerate(self.read_channels):
            if channel not in variables_handling.channels:
                raise Exception(f'Trying to read channel {channel} in {self.full_name}, but it does not exist!')
            if i > 0:
                protocol_string += ', '
            name = variables_handling.channels[channel].name
            if '.' in name:
                dev, chan = name.split('.')
                protocol_string += f'devs["{dev}"].{chan}'
            else:
                protocol_string += f'devs["{name}"]'
        protocol_string += ']\n'
        protocol_string += f'{tabs}helper_functions.clear_plots(plots, {stream})'
        protocol_string += super().get_protocol_string(n_tabs)
        name = variables_handling.channels[self.sweep_channel].name
        if '.' in name:
            dev, chan = name.split('.')
            setter = f'devs["{dev}"].{chan}'
        else:
            setter = f'devs["{name}"]'

        # protocol_string += f'{tabs}for {self.name.replace(" ", "_")}_Count, {self.name.replace(" ", "_")}_Value in enumerate({enumerator}):\n'
        # protocol_string += f'{tabs}\tnamespace.update({{"{self.name.replace(" ", "_")}_Count": {self.name.replace(" ", "_")}_Count, "{self.name.replace(" ", "_")}_Value": {self.name.replace(" ", "_")}_Value}})\n'
        protocol_string += f'{tabs}\tyield from bps.abs_set({setter}, {self.name.replace(" ", "_")}_Value, group="A")\n'
        protocol_string += f'{tabs}\tyield from bps.wait("A")\n'
        protocol_string += f'{tabs}\tyield from bps.trigger_and_read(channels, name={stream})\n'
        protocol_string += f'{tabs}yield from helper_functions.get_fit_results(all_fits, namespace, True, {stream})\n'
        self.update_time_weight()
        return protocol_string

    def get_protocol_short_string(self, n_tabs=0):
        """

        Parameters
        ----------
        n_tabs :
             (Default value = 0)

        Returns
        -------

        """
        short_string = super().get_protocol_short_string(n_tabs)
        tabs = '\t' * n_tabs
        short_string += f'{tabs}Sweep: {self.sweep_channel}, Read: {self.read_channels}\n'
        return short_string



class Simple_Sweep_Config(Loop_Step_Config):
    """ """
    def __init__(self, loop_step:Simple_Sweep, parent=None):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step
        label_sweep_channel = QLabel('Sweep Channel:')
        out_box = []
        in_box = []
        for channel in variables_handling.channels:
            in_box.append(channel)
            if variables_handling.channels[channel].output:
                out_box.append(channel)
        self.comboBox_sweep_channel = QComboBox()
        self.comboBox_sweep_channel.addItems(out_box)
        if loop_step.sweep_channel in out_box:
            self.comboBox_sweep_channel.setCurrentText(loop_step.sweep_channel)

        label_data = QLabel('Data Output:')
        self.comboBox_data_output = QComboBox()
        output_types = ['sub-stream', 'main stream', 'own file']
        self.comboBox_data_output.addItems(output_types)
        self.comboBox_data_output.setCurrentText(loop_step.data_output)

        self.sweep_widget = For_Loop_Step_Config_Sub(parent=self,
                                                   loop_step=loop_step)

        # self.read_table = AddRemoveTable(title='Read Channels', headerLabels=[],
        #                                  tableData=loop_step.read_channels,
        #                                  comboBoxes=in_box)
        labels = ['read', 'channel']
        info_dict = {'channel': self.loop_step.read_channels}
        self.read_table = Channels_Check_Table(self, labels, info_dict=info_dict,
                                               title='Read-Channels')

        self.checkBox_use_own_plots = QCheckBox('Use own Plots')
        self.checkBox_use_own_plots.setChecked(loop_step.use_own_plots)

        self.plot_widge = Plot_Button_Overview(self, self.loop_step.plots)

        label_proc = QLabel('Data processing')
        font = QFont()
        font.setBold(True)
        label_proc.setStyleSheet('font-size: 9pt')
        label_proc.setFont(font)
        self.checkBox_minmax = QCheckBox('Calculate min/max')
        self.checkBox_minmax.setChecked(loop_step.calc_minmax)
        self.checkBox_mean = QCheckBox('Calculate mean')
        self.checkBox_mean.setChecked(loop_step.calc_mean)
        self.checkBox_stddev = QCheckBox('Calculate standard deviation')
        self.checkBox_stddev.setChecked(loop_step.calc_stddev)
        # self.checkBox_fit = QCheckBox('Calculate fit')
        # self.checkBox_fit.setChecked(loop_step.calc_fit)
        # self.checkBox_fit.clicked.connect(self.change_fitting)
        # self.checkBox_guess_fit = QCheckBox('Guess initial params')
        # self.checkBox_guess_fit.setChecked(loop_step.guess_fit_params)
        # self.checkBox_guess_fit.clicked.connect(self.change_fitting)
        # self.radioButton_predev = QRadioButton('Predefined function')
        # self.radioButton_own = QRadioButton('Own function')
        # self.radioButton_predev.setChecked(True)
        # self.radioButton_own.setChecked(loop_step.use_custom_fit)
        # self.radioButton_predev.clicked.connect(self.change_fitting)
        # self.radioButton_own.clicked.connect(self.change_fitting)
        #
        # self.comboBox_fit = QComboBox()
        # self.comboBox_fit.addItems(sorted(models_names.keys()))
        # if loop_step.predef_fit in models_names.keys():
        #     self.comboBox_fit.setCurrentText(loop_step.predef_fit)
        # else:
        #     self.comboBox_fit.setCurrentText('Linear')
        # self.lineEdit_fit_func = QLineEdit()
        # self.lineEdit_fit_func.setText(loop_step.custom_fit)
        # self.comboBox_fit.currentTextChanged.connect(self.change_fitting)
        # self.lineEdit_fit_func.textChanged.connect(self.change_fitting)
        #
        # cols = ['name', 'initial value']
        # self.start_params = AddRemoveTable(headerLabels=cols,
        #                                   title='Fit Parameters',
        #                                   editables=[1],
        #                                   tableData=loop_step.fit_params)
        # self.start_params.addButton.setHidden(True)
        # self.start_params.removeButton.setHidden(True)
        # self.change_fitting()

        self.layout().addWidget(label_sweep_channel, 1, 0)
        self.layout().addWidget(self.comboBox_sweep_channel, 1, 1, 1, 4)
        self.layout().addWidget(label_data, 2, 0)
        self.layout().addWidget(self.comboBox_data_output, 2, 1, 1, 4)
        self.layout().addWidget(self.sweep_widget, 5, 0, 1, 5)
        self.layout().addWidget(self.read_table, 6, 0, 1, 5)

        self.layout().addWidget(self.plot_widge, 8, 0, 1, 5)
        self.layout().addWidget(self.checkBox_use_own_plots, 7, 0, 1, 5)
        # self.layout().addWidget(self.plot_table, 7, 2, 1, 3)
        self.checkBox_use_own_plots.clicked.connect(self.use_plot_change)

        self.layout().addWidget(label_proc, 10, 0, 1, 5)
        self.layout().addWidget(self.checkBox_minmax, 11, 0, 1, 2)
        self.layout().addWidget(self.checkBox_mean, 11, 2, 1, 3)
        self.layout().addWidget(self.checkBox_stddev, 13, 0, 1, 2)
        # self.layout().addWidget(self.checkBox_fit, 20, 0, 1, 2)
        # self.layout().addWidget(self.checkBox_guess_fit, 20, 2, 1, 3)
        # self.layout().addWidget(self.radioButton_predev, 21, 0, 1, 2)
        # self.layout().addWidget(self.radioButton_own, 21, 2, 1, 3)
        # self.layout().addWidget(self.comboBox_fit, 22, 0, 1, 2)
        # self.layout().addWidget(self.lineEdit_fit_func, 22, 2, 1, 3)
        # self.layout().addWidget(self.start_params, 23, 0, 1, 5)


        self.use_plot_change()

    # def setup_plots(self):
    #     """Called when any preferences are changed. Makes the dictionary
    #      of preferences and calls save_preferences from the
    #      load_save_functions module."""
    #     plot_dialog = Plot_Definer(self)
    #     plot_dialog.exec()
    #     print(plot_dialog.data)
        # if settings_dialog.exec():
        #     self.preferences = settings_dialog.get_settings()
        #     number_formatting.preferences = self.preferences
        #     self.toggle_dark_mode()
        #     load_save_functions.save_preferences(self.preferences)
        #     variables_handling.device_driver_path = self.preferences['device_driver_path']
        #     variables_handling.meas_files_path = self.preferences['meas_files_path']
        # prefs = {'autosave': self.actionAutosave_on_closing.isChecked(),
        #          'dark_mode': self.actionDark_Mode.isChecked()}
        # load_save_functions.save_preferences(prefs)

    def use_plot_change(self):
        """ """
        use_plots = self.checkBox_use_own_plots.isChecked()
        self.plot_widge.setEnabled(use_plots)




    def update_step_config(self):
        """ """
        super().update_step_config()
        self.loop_step.use_own_plots = self.checkBox_use_own_plots.isChecked()
        self.loop_step.plots = self.plot_widge.plot_data
        # self.loop_step.plots = self.plot_table.update_table_data()
        self.loop_step.read_channels = self.read_table.get_info()['channel']
        self.loop_step.data_output = self.comboBox_data_output.currentText()
        self.loop_step.sweep_channel = self.comboBox_sweep_channel.currentText()
        self.loop_step.calc_minmax = self.checkBox_minmax.isChecked()
        self.loop_step.calc_mean = self.checkBox_mean.isChecked()
        self.loop_step.calc_stddev = self.checkBox_stddev.isChecked()
        # self.loop_step.calc_fit = self.checkBox_fit.isChecked()
        # self.loop_step.use_custom_fit = self.radioButton_own.isChecked()
        # self.loop_step.predef_fit = self.comboBox_fit.currentText()
        # self.loop_step.custom_fit = self.lineEdit_fit_func.text()


