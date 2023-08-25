from PySide6.QtWidgets import QCheckBox, QLabel, QWidget, QGridLayout, QLineEdit, QApplication, QTabWidget, QPushButton, QScrollArea, QFrame, QRadioButton, QButtonGroup, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal, QThread
from PySide6.QtGui import QFont

from nomad_camels.main_classes.manual_control import Manual_Control, Manual_Control_Config
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.utility import device_handling, variables_handling

import time

bold_font = QFont()
bold_font.setBold(True)


class Set_Panel(Manual_Control):
    """This class provides convenience to set given values quickly at the push
    of a button. Further, it provides a utility-instrument using the buttons as
    channels to easily use the functionality in protocols."""
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if 'name' in control_data:
            name = control_data['name']
        else:
            name = 'Step Panel'
        super().__init__(parent=parent, title=name)
        self.horizontal = control_data['horizontal'] if 'horizontal' in control_data else False
        self.setLayout(QGridLayout())
        groups = control_data['button_groups'] if 'button_groups' in control_data else {}

        channels = []
        self.buttons = []
        self.set_vals = []
        self.button_groups = []


        for n, (group, group_data) in enumerate(groups.items()):
            self.buttons.append([])
            self.set_vals.append([])
            button_group = QButtonGroup()
            self.button_groups.append(button_group)
            group_widget = QFrame()
            layout = QGridLayout()
            group_widget.setLayout(layout)
            layout.setContentsMargins(0, 0, 0, 0)

            label = QLabel(group)
            label.setFont(bold_font)
            layout.addWidget(label, 0, 0)
            if self.horizontal:
                spacer = QSpacerItem(0, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
                for i, (button, set_vals) in enumerate(group_data.items()):
                    radio_button = QRadioButton(button)
                    radio_button.clicked.connect(self.button_pushed)
                    layout.addWidget(radio_button, 0, 1+i)
                    self.buttons[n].append(radio_button)
                    self.set_vals[n].append(set_vals)
                    button_group.addButton(radio_button)
                layout.addItem(spacer, 0, len(group_data)+1)
                self.layout().addWidget(group_widget, n, 0)
            else:
                spacer = QSpacerItem(1, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
                for i, (button, set_vals) in enumerate(group_data.items()):
                    radio_button = QRadioButton(button)
                    radio_button.clicked.connect(self.button_pushed)
                    layout.addWidget(radio_button, 1+i, 0)
                    self.buttons[n].append(radio_button)
                    self.set_vals[n].append(set_vals)
                    button_group.addButton(radio_button)
                layout.addItem(spacer, len(group_data)+1, 0)
                self.layout().addWidget(group_widget, 0, n)
            for data in group_data.values():
                channels += data['channel']
        channels = list(set(channels))
        self.device_list, _ = device_handling.start_devices_from_channel_list(channels)
        self.channels = device_handling.get_channels_from_string_list(channels, True)
        self.adjustSize()

        t = control_data['readback_time'] if 'readback_time' in control_data else 5
        self.read_thread = Readback_Thread(self, self.channels, t)
        if 'readback' in control_data and control_data['readback']:
            self.read_thread.data_sig.connect(self.check_readback)
            self.read_thread.start()

    def button_pushed(self):
        for n, group in enumerate(self.buttons):
            for i, button in enumerate(group):
                if button.isChecked():
                    for j, channel in enumerate(self.set_vals[n][i]['channel']):
                        value = self.set_vals[n][i]['value'][j]
                        value = conv_value(value)
                        self.channels[channel].put(value)

    def check_readback(self, vals):
        for n, group in enumerate(self.buttons):
            self.button_groups[n].setExclusive(False)
            for i, button in enumerate(group):
                is_same = True
                for j, channel in enumerate(self.set_vals[n][i]['channel']):
                    set_value = self.set_vals[n][i]['value'][j]
                    set_value = conv_value(set_value)
                    is_value = conv_value(str(vals[channel]))
                    if set_value != is_value:
                        is_same = False
                        break
                button.setChecked(is_same)
            self.button_groups[n].setExclusive(True)

    def close(self) -> bool:
        self.read_thread.still_running = False
        return super().close()

    def closeEvent(self, a0) -> None:
        self.read_thread.still_running = False
        return super().closeEvent(a0)



def conv_value(value):
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            try:
                value = bool(value)
            except ValueError:
                pass
    return value


class Readback_Thread(QThread):
    data_sig = Signal(dict)

    def __init__(self, parent=None, channels=None, read_time=5):
        super().__init__(parent=parent)
        self.channels = channels or []
        self.read_time = read_time
        self.still_running = True

    def run(self):
        self.do_reading()
        accum = 0
        while self.still_running:
            if self.read_time > 5:
                if self.read_time - accum > 5:
                    time.sleep(5)
                    accum += 5
                    continue
                else:
                    time.sleep(self.read_time - accum)
                    accum = 0
            else:
                time.sleep(self.read_time)
            self.do_reading()

    def do_reading(self):
        vals = {}
        for name, channel in self.channels.items():
            vals[name] = channel.get()
        self.data_sig.emit(vals)




class Set_Panel_Config(Manual_Control_Config):
    """ """
    def __init__(self, parent=None, control_data=None):
        super().__init__(parent=parent, control_data=control_data,
                         title='Set Panel Config',
                         control_type='Set_Panel')
        control_data = control_data or {}
        label_button_groups = QLabel('Button Groups')
        label_button_groups.setStyleSheet('font-size: 9pt')
        label_button_groups.setFont(bold_font)
        self.checkbox_readback = QCheckBox('readback loop in s:')
        if 'readback' in control_data:
            self.checkbox_readback.setChecked(control_data['readback'])
        self.lineEdit_readback = QLineEdit('5')
        if 'readback_time' in control_data:
            self.lineEdit_readback.setText(str(control_data['readback_time']))
        self.checkBox_as_instr = QCheckBox('provide set panel as instrument')
        if 'provide_instr' in control_data:
            self.checkBox_as_instr.setChecked(control_data['provide_instr'])
        self.checkBox_groups_horizontal = QCheckBox('arrange groups horizontally')
        if 'horizontal' in control_data:
            self.checkBox_groups_horizontal.setChecked(control_data['horizontal'])
        self.pushButton_add_group = QPushButton('add button group')
        self.pushButton_add_group.clicked.connect(self.add_button_group)

        self.tabs = []
        self.tab_widget = QTabWidget()
        if 'button_groups' in control_data:
            for name, group in control_data['button_groups'].items():
                self.add_button_group(name, group)
        if not self.tabs:
            self.add_button_group()
        self.change_tab_name()


        layout = self.layout()
        layout.addWidget(self.checkBox_as_instr, 1, 0, 1, 2)
        layout.addWidget(self.checkbox_readback, 2, 0)
        layout.addWidget(self.lineEdit_readback, 2, 1)
        layout.addWidget(label_button_groups, 3, 0)
        layout.addWidget(self.checkBox_groups_horizontal, 3, 1)
        layout.addWidget(self.pushButton_add_group, 4, 0, 1, 2)
        layout.addWidget(self.tab_widget, 6, 0, 1, 2)

    def remove_button_group(self):
        """ """
        ind = self.tab_widget.currentIndex()
        self.tab_widget.removeTab(ind)
        self.tabs.pop(ind)

    def add_button_group(self, name='', group_data=None):
        """

        Parameters
        ----------


        Returns
        -------

        """
        tab = Button_Group_Tab(name, group_data, self)
        tab.signal_name_change.connect(self.change_tab_name)
        tab.signal_remove.connect(self.remove_button_group)
        tab.signal_move_left.connect(lambda: self.move_tab(-1))
        tab.signal_move_right.connect(lambda: self.move_tab(1))
        self.tabs.append(tab)
        self.tab_widget.addTab(tab, '')

    def change_tab_name(self):
        """ """
        for i, tab in enumerate(self.tabs):
            name = tab.lineEdit_group_name.text()
            self.tab_widget.setTabText(i, name)

    def move_tab(self, direction=1):
        """

        Parameters
        ----------
        direction :
             (Default value = 1)

        Returns
        -------

        """
        ind = self.tab_widget.currentIndex()
        self.tab_widget.tabBar().moveTab(ind, ind + direction)
        self.tabs[ind + direction], self.tabs[ind] = self.tabs[ind], self.tabs[ind + direction]

    def accept(self):
        self.control_data['horizontal'] = self.checkBox_groups_horizontal.isChecked()
        if 'button_groups' not in self.control_data:
            self.control_data['button_groups'] = {}
        button_groups = self.control_data['button_groups']
        button_groups.clear()
        for group in self.tabs:
            button_groups.update(group.get_data())
        self.control_data['provide_instr'] = self.checkBox_as_instr.isChecked()
        self.control_data['readback'] = self.checkbox_readback.isChecked()
        self.control_data['readback_time'] = float(self.lineEdit_readback.text())
        if self.checkBox_as_instr.isChecked():
            self.provide_instrument()
        else:
            self.remove_instrument()
        super().accept()

    def provide_instrument(self):
        groups = self.control_data['button_groups']
        set_vals = []
        channels = []
        group_names = []
        for n, (group, group_data) in enumerate(groups.items()):
            set_vals.append([])
            group_names.append(group)
            for i, (button, vals) in enumerate(group_data.items()):
                set_vals[n].append(vals)
            for data in group_data.values():
                channels += data['channel']
        channels = list(set(channels))
        non_str_channels = {}
        str_channels = {}
        for channel in channels:
            str_channels[channel] = channel
            non_str_channels[channel] = variables_handling.channels[channel].get_bluesky_name()
        settings = {'set_vals': set_vals,
                    'group_names': group_names,
                    'channel_names': channels,
                    '!non_string!_channels': non_str_channels}
        from .nomad_camels_driver_set_panel_device.set_panel_device import subclass
        dev = subclass(**settings)
        dev.settings = settings
        name = f'{self.lineEdit_name.text()}_manual_control'
        dev.custom_name = name
        dev.get_channels()
        variables_handling.devices[name] = dev
        variables_handling.channels.update(dev.get_channels())


    def remove_instrument(self):
        name = f'{self.lineEdit_name.text()}_manual_control'
        if name in variables_handling.devices:
            dev = variables_handling.devices[name]
            for chan in dev.get_channels():
                variables_handling.channels.pop(chan)
            variables_handling.devices.pop(name)


class Button_Group_Tab(QWidget):
    signal_remove = Signal()
    signal_move_left = Signal()
    signal_move_right = Signal()
    signal_name_change = Signal(str)

    def __init__(self, name='', group_data=None, parent=None):
        super().__init__(parent)
        group_data = group_data or {}
        label_group_name = QLabel('Group Name:')
        self.lineEdit_group_name = QLineEdit(name)
        self.lineEdit_group_name.textChanged.connect(self.signal_name_change.emit)

        self.moveLeftButton = QPushButton('Move left')
        self.moveRightButton = QPushButton('Move right')
        self.removeButton = QPushButton('Remove')

        self.moveRightButton.clicked.connect(self.signal_move_right.emit)
        self.moveLeftButton.clicked.connect(self.signal_move_left.emit)
        self.removeButton.clicked.connect(self.signal_remove.emit)

        self.add_button_button = QPushButton('Add Button')
        self.add_button_button.clicked.connect(self.add_button)
        self.button_widge = QWidget()
        self.button_widge.setLayout(QGridLayout())
        button_area = QScrollArea()
        button_area.setWidget(self.button_widge)
        button_area.setWidgetResizable(True)

        self.buttons = {'labels': [], 'texts': [], 'tables': [], 'removers': [],
                        'lines': []}

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.moveLeftButton, 2, 0)
        layout.addWidget(self.moveRightButton, 2, 1)
        layout.addWidget(self.removeButton, 2, 2)
        layout.addWidget(label_group_name, 4, 0)
        layout.addWidget(self.lineEdit_group_name, 4, 1, 1, 2)
        layout.addWidget(self.add_button_button, 6, 0, 1, 3)
        layout.addWidget(button_area, 10, 0, 1, 3)

        for name, data in group_data.items():
            self.add_button(name, data)



    def add_button(self, name='', data=None):
        n = len(self.buttons['labels'])
        label = QLabel('text:')
        lineEdit = QLineEdit(name)
        button = QPushButton('remove button')
        button.clicked.connect(lambda state=None, x=n: self.remove_button(x))
        table = Channels_Check_Table(self, ['set', 'channel', 'value'],
                                     only_output=True, info_dict=data,
                                     checkstrings=[2])
        line = QFrame()
        line.setFrameShadow(QFrame.Raised)
        line.setLineWidth(5)
        line.setFrameShape(QFrame.HLine)
        self.button_widge.layout().addWidget(label, n*3, 0)
        self.button_widge.layout().addWidget(lineEdit, n*3, 1)
        self.button_widge.layout().addWidget(button, n*3, 2)
        self.button_widge.layout().addWidget(table, 1+n*3, 0, 1, 3)
        self.button_widge.layout().addWidget(line, 2+n*3, 0, 1, 3)
        self.buttons['labels'].append(label)
        self.buttons['texts'].append(lineEdit)
        self.buttons['tables'].append(table)
        self.buttons['removers'].append(button)
        self.buttons['lines'].append(line)

    def remove_button(self, n):
        print(n)
        for i, label in enumerate(self.buttons['labels']):
            if i < n:
                continue
            lineEdit = self.buttons['texts'][i]
            button = self.buttons['removers'][i]
            table = self.buttons['tables'][i]
            line = self.buttons['lines'][i]
            button.clicked.disconnect()
            if i > n:
                self.button_widge.layout().removeWidget(label)
                self.button_widge.layout().removeWidget(lineEdit)
                self.button_widge.layout().removeWidget(button)
                self.button_widge.layout().removeWidget(table)
                self.button_widge.layout().removeWidget(line)
                self.button_widge.layout().addWidget(label, (i-1)*3, 0)
                self.button_widge.layout().addWidget(lineEdit, (i-1)*3, 1)
                self.button_widge.layout().addWidget(button, (i-1)*3, 2)
                self.button_widge.layout().addWidget(table, 1+(i-1)*3, 0, 1, 3)
                self.button_widge.layout().addWidget(line, 2+(i-1)*3, 0, 1, 3)
                button.clicked.connect(lambda state=None, x=i-1: self.remove_button(x))
            else:
                self.button_widge.layout().removeWidget(label)
                self.button_widge.layout().removeWidget(lineEdit)
                self.button_widge.layout().removeWidget(button)
                self.button_widge.layout().removeWidget(table)
                self.button_widge.layout().removeWidget(line)
        for v in self.buttons.values():
            widget = v.pop(n)
            widget.deleteLater()

    def get_data(self):
        button_data = {}
        for i, line in enumerate(self.buttons['texts']):
            name = line.text()
            if not name or name in button_data:
                raise Exception(f'Buttons must be named and two buttons should not be named the same!\n{name}')
            button_data[name] = self.buttons['tables'][i].get_info()
        name = self.lineEdit_group_name.text()
        if not name:
            raise Exception('Button groups must be named!')
        return {name: button_data}





if __name__ == '__main__':
    app = QApplication()
    panel = Set_Panel_Config()
    panel.show()
    import sys
    sys.exit(app.exec())