import time

from CAMELS.main_classes.add_on import AddOn
from PID_python.PID_python_config_sub import subclass_config_sub
from PID_python.PID_python_ophyd import PID_Controller

from PyQt5.QtWidgets import QCheckBox, QLineEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import pyqtSignal, QThread

from utility import variables_handling, device_handling


class PID_manual_control(AddOn):
    def __init__(self, device=None, ophyd_device=None, device_list=None):
        super().__init__(title='PID-controller: manual control', device=device,
                         ophyd_device=ophyd_device, device_list=device_list)

        self.settings_widge = subclass_config_sub(settings_dict=self.device.settings, config_dict=self.device.config, parent=self)
        self.settings_widge.input_label.setHidden(True)
        self.settings_widge.comboBox_input.setHidden(True)
        self.settings_widge.output_label.setHidden(True)
        self.settings_widge.comboBox_output.setHidden(True)

        label_state = QLabel('current state:')
        self.on_off_box = QCheckBox('Off')
        label_set = QLabel('Setpoint:')
        self.lineEdit_setpoint = QLineEdit(str(self.ophyd_device.setpoint.get()))
        self.lineEdit_setpoint_show = QLineEdit(str(self.ophyd_device.setpoint.get()))
        self.lineEdit_setpoint_show.setEnabled(False)
        label_pidval = QLabel('Actual value:')
        self.lineEdit_pid_val = QLineEdit(str(self.ophyd_device.current_value.get()))
        self.lineEdit_pid_val.setEnabled(False)
        label_output = QLabel('Output:')
        self.lineEdit_output = QLineEdit(str(self.ophyd_device.output_value.get()))
        self.lineEdit_output.setEnabled(False)

        label_update = QLabel('Update speed:')
        self.lineEdit_update = QLineEdit(str(self.ophyd_device.dt.get()))

        self.pushButton_plot = QPushButton('Show Plot')
        self.pushButton_settings = QPushButton('Show Settings')
        self.pushButton_update_settings = QPushButton('Update Settings')

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layout().addWidget(label_state, 0, 0)
        self.layout().addWidget(self.on_off_box, 1, 0, 2, 1)
        self.layout().addWidget(label_set, 0, 1)
        self.layout().addWidget(self.lineEdit_setpoint, 1, 1)
        self.layout().addWidget(self.lineEdit_setpoint_show, 2, 1)
        self.layout().addWidget(label_pidval, 0, 2)
        self.layout().addWidget(self.lineEdit_pid_val, 1, 2, 2, 1)
        self.layout().addWidget(label_output, 0, 3)
        self.layout().addWidget(self.lineEdit_output, 1, 3, 2, 1)
        self.layout().addWidget(label_update, 0, 4)
        self.layout().addWidget(self.lineEdit_update, 1, 4, 2, 1)
        self.layout().addWidget(self.pushButton_plot, 3, 0, 1, 2)
        self.layout().addWidget(self.pushButton_settings, 3, 2, 1, 3)

        self.layout().addWidget(line, 5, 0, 1, 5)

        self.layout().addWidget(self.settings_widge, 10, 0, 1, 5)
        self.layout().addWidget(self.pushButton_update_settings, 11, 3, 1, 2)
        self.layout().addItem(spacer, 20, 0)

        self.settings_widge.setHidden(True)

        self.on_off_box.clicked.connect(self.change_state)
        self.pushButton_settings.clicked.connect(self.show_settings)
        self.pushButton_update_settings.clicked.connect(self.update_settings)
        self.lineEdit_update.returnPressed.connect(self.change_update_time)
        self.lineEdit_setpoint.returnPressed.connect(self.change_setpoint)
        self.pushButton_plot.clicked.connect(self.change_show_plot)
        self.change_show_plot()
        self.change_show_plot()

        self.update_thread = PID_update_thread(self, self.ophyd_device)
        self.update_thread.data_sig.connect(self.data_update)
        self.update_thread.start()

        self.sub_devices = []
        for dev in device_list:
            if dev in device_handling.running_devices:
                self.sub_devices.append(device_handling.running_devices[dev])



    def change_show_plot(self):
        showing = self.ophyd_device.plot.plot.show_plot
        self.ophyd_device.change_show_plot(not showing)
        if showing:
            self.pushButton_plot.setText('show plot')
        else:
            self.pushButton_plot.setText('hide plot')

    def update_settings(self):
        settings = self.settings_widge.get_settings()
        config = self.settings_widge.get_config()
        self.run_thread.update_config_settings(config, settings)

    def data_update(self, setp, pid_val, output, on):
        self.lineEdit_setpoint_show.setText(f'{setp:.3e}')
        self.lineEdit_pid_val.setText(f'{pid_val:.3e}')
        self.lineEdit_output.setText(f'{output:.3e}')
        self.change_on_state(on)

    def change_setpoint(self):
        setp = float(self.lineEdit_setpoint.text())
        self.ophyd_device.setpoint.put(setp)
        # self.run_thread.device.pid_val.put(setp)

    def change_update_time(self):
        self.ophyd_device.dt.put(float(self.lineEdit_update.text()))
        # self.run_thread.update_time = float(self.lineEdit_update.text())

    def change_on_state(self, on):
        self.on_off_box.setChecked(on)
        col = variables_handling.get_color('green' if on else 'red', True)
        self.on_off_box.setText('On' if on else 'Off')
        self.on_off_box.setStyleSheet(f"color: rgb{col}")

    def change_state(self):
        on = self.on_off_box.isChecked()
        if on:
            for dev in self.sub_devices:
                if hasattr(dev, 'turn_on_output') and callable(dev.turn_on_output):
                    dev.turn_on_output()
        col = variables_handling.get_color('green' if on else 'red', True)
        self.on_off_box.setText('On' if on else 'Off')
        self.on_off_box.setStyleSheet(f"color: rgb{col}")
        self.ophyd_device.pid_on.put(on)


    def show_settings(self):
        hidden = self.settings_widge.isHidden()
        self.settings_widge.setHidden(not hidden)
        if hidden:
            self.pushButton_settings.setText('Hide Settings')
        else:
            self.pushButton_settings.setText('Show Settings')

    def close(self) -> bool:
        self.update_thread.still_running = False
        return super().close()

    def closeEvent(self, a0) -> None:
        self.update_thread.still_running = False
        return super().closeEvent(a0)


class PID_update_thread(QThread):
    data_sig = pyqtSignal(float, float, float, bool)

    def __init__(self, parent=None, device=None):
        super().__init__(parent=parent)
        self.device = device
        self.update_time = device.dt.get()
        self.stopping = False
        self.starttime = 0
        self.still_running = True

    def run(self):
        self.starttime = time.time()
        self.do_reading()
        while self.still_running:
            if self.update_time < 0:
                time.sleep(5)
                continue
            time.sleep(self.update_time)
            self.do_reading()

    def do_reading(self):
        setp = self.device.setpoint.get()
        pid_val = self.device.current_value.get()
        output = self.device.output_value.get()
        on = self.device.pid_on.get()
        self.data_sig.emit(setp, pid_val, output, on)

# class PID_thread(Manual_Device_Thread):
#     data_sig = pyqtSignal(float, float, float, bool, float, list)
#
#     def __init__(self, device, update_time):
#         super().__init__(device=device, ophyd_class=PID_Controller)
#         self.update_time = update_time
#         self.stopping = False
#         self.starttime = 0
#
#     def run(self) -> None:
#         self.starttime = time.time()
#         self.do_reading()
#         while True:
#             if self.update_time < 0:
#                 time.sleep(5)
#                 continue
#             time.sleep(self.update_time)
#             self.do_reading()
#
#     def do_reading(self):
#         setp = self.device.pid_val.get()
#         pid_val = self.device.pid_cval.get()
#         output = self.device.pid_oval.get()
#         on = self.device.pid_fbon.get()
#         pval = self.device.pid_pval.get()
#         ival = self.device.pid_ival.get()
#         dval = self.device.pid_dval.get()
#         self.data_sig.emit(setp, pid_val, output, on,
#                            time.time() - self.starttime, [pval, ival, dval])

