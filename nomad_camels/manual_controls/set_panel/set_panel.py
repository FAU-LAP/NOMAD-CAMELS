from PySide6.QtWidgets import QCheckBox, QLabel, QWidget, QGridLayout, QLineEdit, QApplication, QTabWidget, QPushButton, QScrollArea, QFrame, QRadioButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont

from nomad_camels.main_classes.manual_control import Manual_Control, Manual_Control_Config
from nomad_camels.ui_widgets.channels_check_table import Channels_Check_Table
from nomad_camels.utility import device_handling



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


        for n, (group, group_data) in enumerate(groups.items()):
            group_widget = QFrame()
            layout = QGridLayout()
            group_widget.setLayout(layout)
            layout.setContentsMargins(0, 0, 0, 0)

            label = QLabel(group)
            layout.addWidget(label, 0, 0)
            if self.horizontal:
                for i, (button, set_vals) in enumerate(group_data.items()):
                    radio_button = QRadioButton(button)
                    radio_button.clicked.connect(self.button_pushed)
                    layout.addWidget(radio_button, 0, 1+i)
                    self.buttons.append(radio_button)
                    self.set_vals.append(set_vals)
                self.layout().addWidget(group_widget, n, 0)
            else:
                for i, (button, set_vals) in enumerate(group_data.items()):
                    radio_button = QRadioButton(button)
                    radio_button.clicked.connect(self.button_pushed)
                    layout.addWidget(radio_button, 1+i, 0)
                    self.buttons.append(radio_button)
                    self.set_vals.append(set_vals)
                self.layout().addWidget(group_widget, 0, n)
            for data in group_data.values():
                channels += data['channel']
        channels = list(set(channels))
        self.device_list, _ = device_handling.start_devices_from_channel_list(channels)
        self.channels = device_handling.get_channels_from_string_list(channels, True)
        self.adjustSize()

    def button_pushed(self):
        for i, button in enumerate(self.buttons):
            if button.isChecked():
                for j, channel in enumerate(self.set_vals[i]['channel']):
                    value = self.set_vals[i]['value'][j]
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
                    self.channels[channel].put(value)






class Set_Panel_Config(Manual_Control_Config):
    """ """
    def __init__(self, parent=None, control_data=None):
        super().__init__(parent=parent, control_data=control_data,
                         title='Set Panel Config',
                         control_type='Set_Panel')
        font = QFont()
        font.setBold(True)

        control_data = control_data or {}
        label_button_groups = QLabel('Button Groups')
        label_button_groups.setStyleSheet('font-size: 9pt')
        label_button_groups.setFont(font)
        self.checkBox_groups_horizontal = QCheckBox('arrange groups horizontally')
        self.pushButton_add_group = QPushButton('add button group')
        self.pushButton_add_group.clicked.connect(self.add_button_group)

        self.tabs = []
        self.tab_widget = QTabWidget()
        if 'button_groups' in control_data:
            for name, group in control_data['button_groups'].items():
                self.add_button_group(name, group)
        if not self.tabs:
            self.add_button_group()


        layout = self.layout()
        layout.addWidget(label_button_groups, 2, 0)
        layout.addWidget(self.checkBox_groups_horizontal, 2, 1)
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
        super().accept()


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