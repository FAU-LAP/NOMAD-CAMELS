import copy
import numpy as np
import re

from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QCheckBox,
    QLineEdit,
    QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeyEvent

from lmfit import models

from nomad_camels.gui.plot_definer import Ui_Plot_Definer
from nomad_camels.gui.plot_definer_2d import Ui_Plot_Definer_2D
from nomad_camels.gui.fit_definer import Ui_Fit_Definer

from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.utility import variables_handling
from nomad_camels.utility.fit_variable_renaming import replace_name


plot_types = ["X-Y plot", "Value-List", "2D plot"]


class Plot_Info:
    """ """

    def __init__(
        self,
        plt_type="X-Y plot",
        x_axis="",
        y_axes=None,
        title="",
        xlabel="",
        ylabel="",
        ylabel2="",
        do_plot=True,
        zlabel="",
        same_fit=False,
        fits=None,
        all_fit=None,
        z_axis="",
        logX=False,
        logY=False,
        logY2=False,
        top_left_x="",
        top_left_y="",
        plot_width="",
        plot_height="",
        checkbox_manual_plot_position = False,
        checkbox_show_in_browser = False,
    ):
        self.plt_type = plt_type
        self.x_axis = x_axis
        self.y_axes = y_axes or {"formula": [], "axis": []}
        self.z_axis = z_axis
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ylabel2 = ylabel2
        self.logX = logX
        self.logY = logY
        self.logY2 = logY2
        self.zlabel = zlabel
        self.do_plot = do_plot
        self.same_fit = same_fit
        self.fits = fits or []
        self.plot_all_available = True
        self.all_fit = all_fit or Fit_Info()
        self.name = ""
        self.maxlen = np.inf
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.plot_width = plot_width
        self.plot_height = plot_width
        self.checkbox_manual_plot_position = checkbox_manual_plot_position
        self.checkbox_show_in_browser = checkbox_show_in_browser
        self.browser_port = None
        self.update_name()

    def update_name(self):
        """ """
        if self.title:
            self.name = self.title
        elif self.plt_type == "X-Y plot":
            if self.xlabel and self.ylabel:
                self.name = f"{self.ylabel} vs. {self.xlabel}"
            elif self.x_axis and self.y_axes["formula"]:
                self.name = f"{self.y_axes['formula'][0]} vs. {self.x_axis}"
            elif self.y_axes["formula"]:
                self.name = self.y_axes["formula"][0]
            else:
                self.name = self.x_axis
        elif self.plt_type == "Value-List":
            self.name = "Current Values"
        elif self.plt_type == "2D plot":
            if self.zlabel and self.xlabel and self.ylabel:
                self.name = f"{self.zlabel} vs. ({self.xlabel}; {self.ylabel})"
            elif self.zlabel:
                self.name = f"{self.zlabel} 2D"
            if self.z_axis and self.x_axis and self.y_axes["formula"]:
                self.name = (
                    f"{self.z_axis} vs. ({self.x_axis}; {self.y_axes['formula'][0]})"
                )
            elif self.z_axis:
                self.name = f"{self.z_axis} 2D"

    def get_fit_vars(self, stream=""):
        """

        Parameters
        ----------
        stream :
             (Default value = '')

        Returns
        -------

        """
        variables = {}
        if self.same_fit:
            if self.all_fit.do_fit:
                self.all_fit.x = self.x_axis
                for y in self.y_axes["formula"]:
                    fit = copy.deepcopy(self.all_fit)
                    fit.y = y
                    variables.update(fit.get_variables(stream))
        else:
            for fit in self.fits:
                if fit.do_fit:
                    variables.update(fit.get_variables(stream))
        return variables


class Fit_Info:
    """ """

    def __init__(
        self,
        do_fit=False,
        predef_func="",
        custom_func="",
        use_custom_func=False,
        guess_params=True,
        initial_params=None,
        y="",
        x="",
        additional_data=None,
        display_values=False,
    ):
        self.do_fit = do_fit
        self.predef_func = predef_func
        self.custom_func = custom_func
        self.use_custom_func = use_custom_func
        self.guess_params = guess_params
        self.name = ""
        self.display_values = display_values
        self.initial_params = initial_params or {
            "name": [],
            "initial value": [],
            "lower bound": [],
            "upper bound": [],
        }
        self.additional_data = additional_data or []
        self.y = y or ""
        self.x = x or ""

    def get_name(self, stream=""):
        """

        Parameters
        ----------
        stream :
             (Default value = '')

        Returns
        -------

        """
        if self.use_custom_func:
            label = "custom"
        else:
            label = self.predef_func
        self.name = f"{label}_{self.y}_v_{self.x}_{stream}".replace(" ", "_")
        return self.name

    def get_variables(self, stream=""):
        """

        Parameters
        ----------
        stream :
             (Default value = '')

        Returns
        -------

        """
        variables = {}
        name = self.get_name(stream)
        for var in self.initial_params["name"]:
            var_name = f"{name}_{var}"
            var_name = replace_name(var_name)
            variables[var_name] = 1
        return variables


class Plot_Definer(QDialog):
    """ """

    def __init__(self, parent=None, plot_data=None):
        self.plot_data = plot_data or []
        super().__init__(parent)
        self.setWindowTitle("Define plot - NOMAD CAMELS")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        cols = ["plot-type", "name"]
        comboBoxes = {"plot-type": plot_types}
        tableData = {"plot-type": [], "name": []}
        for plt in self.plot_data:
            tableData["plot-type"].append(plt.plt_type)
            tableData["name"].append(plt.name)
        self.plot_table = AddRemoveTable(
            headerLabels=cols,
            title="Plots",
            editables=[],
            comboBoxes=comboBoxes,
            tableData=tableData,
            askdelete=True,
        )
        self.plot_table.table.clicked.connect(self.change_plot_def)
        self.plot_table.added.connect(self.plot_added)
        self.plot_table.removed.connect(self.plot_removed)
        self.plot_def = QLabel("Select a plot!")
        self.dialog_buttons = QDialogButtonBox()
        self.dialog_buttons.setOrientation(Qt.Horizontal)
        self.dialog_buttons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        layout = QGridLayout()
        layout.addWidget(self.plot_table, 0, 0)
        layout.addWidget(self.plot_def, 0, 1)
        layout.addWidget(self.dialog_buttons, 1, 0, 1, 2)
        self.setLayout(layout)

    def accept(self) -> None:
        """ """
        if not isinstance(self.plot_def, QLabel):
            self.plot_def.get_data()
        super().accept()

    def reject(self):
        """ """
        discard_dialog = QMessageBox.question(
            self,
            "Discard Changes?",
            f"All changes to the defined plots / fits will be lost!",
            QMessageBox.Yes | QMessageBox.No,
        )
        if discard_dialog != QMessageBox.Yes:
            return
        super().reject()

    def change_plot_def(self, a0):
        """

        Parameters
        ----------
        a0 :


        Returns
        -------

        """
        if not isinstance(self.plot_def, QLabel):
            self.plot_def.get_data()
        plot_dat = self.plot_data[a0.row()]
        ind = self.plot_table.table_model.index(a0.row(), 0)
        plot_dat.plt_type = self.plot_table.table.indexWidget(ind).currentText()
        tableData = {"plot-type": [], "name": []}
        for plt in self.plot_data:
            tableData["plot-type"].append(plt.plt_type)
            tableData["name"].append(plt.name)
        self.plot_table.change_table_data(tableData)
        if plot_dat.plt_type == "X-Y plot":
            plot_def = Single_Plot_Definer_XY(plot_dat, self)
        elif plot_dat.plt_type == "Value-List":
            plot_def = Single_Plot_Definer_List(plot_dat, self)
        elif plot_dat.plt_type == "2D plot":
            plot_def = Single_Plot_Definer_2D(plot_dat, self)
        else:
            plot_def = QLabel("Not implemented yet!")
        self.layout().replaceWidget(self.plot_def, plot_def)
        self.plot_def.deleteLater()
        self.plot_def = plot_def
        flag = self.plot_table.table.selectionModel().SelectionFlag.Select
        self.plot_table.table.selectionModel().select(a0, flag)

    def plot_added(self, n):
        """

        Parameters
        ----------
        n :


        Returns
        -------

        """
        if n >= len(self.plot_data):
            self.plot_data.append(Plot_Info())

    def plot_removed(self, n):
        """

        Parameters
        ----------
        n :


        Returns
        -------

        """
        self.plot_data.pop(n)


class Single_Plot_Definer(QWidget):
    """ """

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(parent)
        self.plot_data = plot_data

    def get_data(self):
        """ """
        return self.plot_data

    def add_y(self, n):
        """

        Parameters
        ----------
        n :


        Returns
        -------

        """
        if n >= len(self.plot_data.fits):
            self.plot_data.fits.append(Fit_Info())

    def remove_y(self, n):
        """

        Parameters
        ----------
        n :


        Returns
        -------

        """
        self.plot_data.fits.pop(n)


class Single_Plot_Definer_List(Single_Plot_Definer):
    """Class to define a list of plots with position and size attributes and other parameters"""

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(plot_data, parent)
        self.plot_data = plot_data

        # CheckBox for plotting all available channels
        self.checkBox_plot_all = QCheckBox("Plot all available channels")
        self.checkBox_plot_all.setChecked(plot_data.plot_all_available)

        # Table for formula data
        self.table = AddRemoveTable(
            title="Values",
            headerLabels=[],
            tableData=plot_data.y_axes["formula"],
            checkstrings=[0],
        )
        self.table.added.connect(self.add_y)
        self.table.removed.connect(self.remove_y)

        # Layout for the widget
        self.layout: QGridLayout = QGridLayout()

        # Add the checkBox and table to the layout
        self.layout.addWidget(self.checkBox_plot_all, 0, 0, 1, 4)
        self.layout.addWidget(self.table, 1, 0, 1, 4)

        self.line = QFrame(self)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line, 3, 0, 1, 4)

        # Line Edit and Label for top_left_x
        self.label_top_left_x = QLabel("Top Left X:", self)
        self.lineEdit_top_left_x = QLineEdit(self)
        self.layout.addWidget(self.label_top_left_x, 11, 0)
        self.layout.addWidget(self.lineEdit_top_left_x, 11, 1)

        # Line Edit and Label for top_left_y
        self.label_top_left_y = QLabel("Top Left Y:", self)
        self.lineEdit_top_left_y = QLineEdit(self)
        self.layout.addWidget(self.label_top_left_y, 12, 0)
        self.layout.addWidget(self.lineEdit_top_left_y, 12, 1)

        # Line Edit and Label for plot_width
        self.label_plot_width = QLabel("Plot Width:", self)
        self.lineEdit_plot_width = QLineEdit(self)
        self.layout.addWidget(self.label_plot_width, 11, 2, 1, 1)
        self.layout.addWidget(self.lineEdit_plot_width, 11, 3, 1, 1)

        # Line Edit and Label for plot_height
        self.label_plot_height = QLabel("Plot Height:", self)
        self.lineEdit_plot_height = QLineEdit(self)
        self.layout.addWidget(self.label_plot_height, 12, 2, 1, 1)
        self.layout.addWidget(self.lineEdit_plot_height, 12, 3, 1, 1)

        # Set the layout of the widget
        self.setLayout(self.layout)
        self.load_data()

        # Update the plot data name after layout setup
        self.plot_data.update_name()

    def get_data(self):
        """ """
        self.plot_data.plot_all_available = self.checkBox_plot_all.isChecked()
        self.plot_data.y_axes["formula"] = self.table.update_table_data()
        self.plot_data.y_axes["axis"] = [1] * len(self.plot_data.y_axes["formula"])
        # If the string is empty set empty string
        if self.lineEdit_top_left_x.text():
            try:
                self.plot_data.top_left_x = max(int(self.lineEdit_top_left_x.text()), 0)
            except ValueError:
                self.plot_data.top_left_x = ""
            
        else:
            self.plot_data.top_left_x = ""

        if self.lineEdit_top_left_y.text():
            try:
                self.plot_data.top_left_y = max(int(self.lineEdit_top_left_y.text()), 0)
            except ValueError:
                self.plot_data.top_left_y = ""
        else:
            self.plot_data.top_left_y = ""

        if self.lineEdit_plot_width.text():
            try:
                self.plot_data.plot_width = max(int(self.lineEdit_plot_width.text()), 430)
            except ValueError:
                self.plot_data.plot_width = ""
            
        else:
            self.plot_data.plot_width = ""

        if self.lineEdit_plot_height.text():
            try:
                self.plot_data.plot_height = max(int(self.lineEdit_plot_height.text()), 126)
            except ValueError:
                self.plot_data.plot_height = ""
            
        else:
            self.plot_data.plot_height = ""

        # Check to see if only x or y is set and raise error
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set")
        # Check to see if only height or width is set and raise error
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set")
        
        self.plot_data.update_name()
        return super().get_data()

    def load_data(self):
        """ """
        # If plot_data has the top_left_x attribute set it as text
        if hasattr(self.plot_data, "top_left_x"):
            self.lineEdit_top_left_x.setText(str(self.plot_data.top_left_x))
        if hasattr(self.plot_data, "top_left_y"):
            self.lineEdit_top_left_y.setText(str(self.plot_data.top_left_y))
        if hasattr(self.plot_data, "plot_width"):
            self.lineEdit_plot_width.setText(str(self.plot_data.plot_width))
        if hasattr(self.plot_data, "plot_height"):
            self.lineEdit_plot_height.setText(str(self.plot_data.plot_height))


class Single_Plot_Definer_2D(Ui_Plot_Definer_2D, Single_Plot_Definer):
    """ """

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(plot_data, parent)
        self.setupUi(self)
        self.lineEdit_x_axis.setText(self.plot_data.x_axis)
        if not self.plot_data.y_axes["formula"]:
            self.plot_data.y_axes["formula"].append("")
            self.plot_data.y_axes["axis"].append(1)
        self.lineEdit_y_axis.setText(self.plot_data.y_axes["formula"][0])
        self.lineEdit_z_axis.setText(self.plot_data.z_axis)
        self.lineEdit_xlabel.setText(self.plot_data.xlabel)
        self.lineEdit_ylabel.setText(self.plot_data.ylabel)
        self.lineEdit_zlabel.setText(self.plot_data.zlabel)
        self.lineEdit_title.setText(self.plot_data.title)
        self.lineEdit_n_data_points.setText(str(self.plot_data.maxlen))
        self.load_data()
        self.plot_data.update_name()
        # Connect on set event of the checkbox to hide the manual position elements
        self.checkBox_manual_plot_position_2d.stateChanged.connect(self.hide_show_manual_position)
        # Connect on set event of the checkbox to hide the show in plot elements
        self.checkBox_show_in_browser.stateChanged.connect(self.hide_show_show_in_browser)

    def get_data(self):
        """ """
        self.plot_data.xlabel = self.lineEdit_xlabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.xlabel):
            raise ValueError(
                "x-label contains special characters.\nYou cannot use ' \" or `."
            )
        self.plot_data.ylabel = self.lineEdit_ylabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.ylabel):
            raise ValueError(
                "y-label contains special characters.\nYou cannot use ' \" or `."
            )
        self.plot_data.zlabel = self.lineEdit_zlabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.zlabel):
            raise ValueError(
                "z-label contains special characters.\nYou cannot use ' \" or `."
            )
        self.plot_data.x_axis = self.lineEdit_x_axis.text()
        self.plot_data.y_axes["formula"][0] = self.lineEdit_y_axis.text()
        self.plot_data.z_axis = self.lineEdit_z_axis.text()
        self.plot_data.title = self.lineEdit_title.text()
        self.plot_data.maxlen = self.lineEdit_n_data_points.text() or "inf"
        # If the string is empty set empty string
        if self.lineEdit_top_left_x.text():
            try:
                self.plot_data.top_left_x = max(int(self.lineEdit_top_left_x.text()), 0)
            except ValueError:
                self.plot_data.top_left_x = ""
            
        else:
            self.plot_data.top_left_x = ""

        if self.lineEdit_top_left_y.text():
            try:
                self.plot_data.top_left_y = max(int(self.lineEdit_top_left_y.text()), 0)
            except ValueError:
                self.plot_data.top_left_y = ""
        else:
            self.plot_data.top_left_y = ""

        if self.lineEdit_plot_width.text():
            try:
                self.plot_data.plot_width = max(int(self.lineEdit_plot_width.text()), 430)
            except ValueError:
                self.plot_data.plot_width = ""
            
        else:
            self.plot_data.plot_width = ""

        if self.lineEdit_plot_height.text():
            try:
                self.plot_data.plot_height = max(int(self.lineEdit_plot_height.text()), 126)
            except ValueError:
                self.plot_data.plot_height = ""
            
        else:
            self.plot_data.plot_height = ""

        self.plot_data.checkbox_manual_plot_position = self.checkBox_manual_plot_position_2d.isChecked()
        self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
        self.plot_data.browser_port = self.spinBox_port.value()

        # Check to see if only x or y is set and raise error
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set")
        # Check to see if only height or width is set and raise error
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set")
        
        self.plot_data.update_name()
        return super().get_data()

    def hide_show_manual_position(self):
        if self.checkBox_manual_plot_position_2d.isChecked():
            self.label_top_left_x.setHidden(False)
            self.lineEdit_top_left_x.setHidden(False)
            self.label_top_left_y.setHidden(False)
            self.lineEdit_top_left_y.setHidden(False)
            self.label_plot_width.setHidden(False)
            self.lineEdit_plot_width.setHidden(False)
            self.label_plot_height.setHidden(False)
            self.lineEdit_plot_height.setHidden(False)
        else:
            self.label_top_left_x.setHidden(True)
            self.lineEdit_top_left_x.setHidden(True)
            self.label_top_left_y.setHidden(True)
            self.lineEdit_top_left_y.setHidden(True)
            self.label_plot_width.setHidden(True)
            self.lineEdit_plot_width.setHidden(True)
            self.label_plot_height.setHidden(True)
            self.lineEdit_plot_height.setHidden(True)

    def hide_show_show_in_browser(self):
        if self.checkBox_show_in_browser.isChecked():
            self.label_port.setHidden(False)
            self.spinBox_port.setHidden(False)
        else:
            self.label_port.setHidden(True)
            self.spinBox_port.setHidden(True)
    
    
    def load_data(self):
        """ """
        if hasattr(self.plot_data, "top_left_x"):
            self.lineEdit_top_left_x.setText(str(self.plot_data.top_left_x))
        if hasattr(self.plot_data, "top_left_y"):
            self.lineEdit_top_left_y.setText(str(self.plot_data.top_left_y))
        if hasattr(self.plot_data, "plot_width"):
            self.lineEdit_plot_width.setText(str(self.plot_data.plot_width))
        if hasattr(self.plot_data, "plot_height"):
            self.lineEdit_plot_height.setText(str(self.plot_data.plot_height))
        if hasattr(self.plot_data, "checkbox_manual_plot_position"):
            self.checkBox_manual_plot_position_2d.setChecked(
                self.plot_data.checkbox_manual_plot_position
            )
        else:
            self.checkBox_manual_plot_position_2d.setChecked(False)
        if hasattr(self.plot_data, "checkbox_show_in_browser"):
            self.checkBox_show_in_browser.setChecked(
                self.plot_data.checkbox_show_in_browser
            )
        else:
            self.checkBox_show_in_browser.setChecked(False)

        if hasattr(self.plot_data, "browser_port") and self.plot_data.browser_port:
            try:
                port = int(self.plot_data.browser_port)
            except ValueError:
                port = 8050
            self.spinBox_port.setValue(port)
        else:
            self.spinBox_port.setValue(8050)
        self.hide_show_manual_position()
        self.hide_show_show_in_browser()


class Single_Plot_Definer_XY(Ui_Plot_Definer, Single_Plot_Definer):
    """ """

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(plot_data, parent)
        self.fit_definer = None
        self.setupUi(self)

        cols = ["formula", "axis"]
        comboBoxes = {"axis": ["left", "right"]}
        self.y_table = AddRemoveTable(
            headerLabels=cols,
            title="y-axes",
            comboBoxes=comboBoxes,
            tableData=plot_data.y_axes,
            checkstrings=[0],
        )
        self.y_table.added.connect(self.add_y)
        self.y_table.removed.connect(self.remove_y)
        self.y_table.table.clicked.connect(self.fit_change)
        self.checkBox_same_fit.clicked.connect(self.fit_change)
        self.layout().replaceWidget(self.y_axes, self.y_table)

        # self.checkBox_plot.clicked.connect(self.plot_change)
        self.load_data()
        # self.plot_change()
        self.fit_change()

        # Connect on set event of the checkbox to hide the manual position elements
        self.checkBox_manual_plot_position.stateChanged.connect(self.hide_show_manual_position)
        # Connect on set event of the checkbox to hide the show in browser elements
        self.checkBox_show_in_browser.stateChanged.connect(self.hide_show_show_in_browser)


    # def plot_change(self):
    #     """ """
    #     self.plotting_group.setEnabled(self.checkBox_plot.isChecked())

    def load_data(self):
        """ """
        self.lineEdit_x_axis.setText(self.plot_data.x_axis)
        self.lineEdit_title.setText(self.plot_data.title)
        self.lineEdit_xlabel.setText(self.plot_data.xlabel)
        self.lineEdit_ylabel.setText(self.plot_data.ylabel)
        self.lineEdit_ylabel2.setText(self.plot_data.ylabel2)
        # self.checkBox_plot.setChecked(self.plot_data.do_plot)
        self.lineEdit_nPoints.setText(str(self.plot_data.maxlen))
        self.checkBox_same_fit.setChecked(self.plot_data.same_fit)
        self.checkBox_xlog.setChecked(self.plot_data.logX)
        self.checkBox_ylog.setChecked(self.plot_data.logY)
        self.checkBox_ylog2.setChecked(self.plot_data.logY2)
        # If plot_data has the top_left_x attribute set it as text
        if hasattr(self.plot_data, "top_left_x"):
            self.lineEdit_top_left_x.setText(str(self.plot_data.top_left_x))
        if hasattr(self.plot_data, "top_left_y"):
            self.lineEdit_top_left_y.setText(str(self.plot_data.top_left_y))
        if hasattr(self.plot_data, "plot_width"):
            self.lineEdit_plot_width.setText(str(self.plot_data.plot_width))
        if hasattr(self.plot_data, "plot_height"):
            self.lineEdit_plot_height.setText(str(self.plot_data.plot_height))
        if hasattr(self.plot_data, "checkbox_manual_plot_position"):
            self.checkBox_manual_plot_position.setChecked(
                self.plot_data.checkbox_manual_plot_position
            )
        else:
            self.checkBox_manual_plot_position.setChecked(False)
        if hasattr(self.plot_data, "checkbox_show_in_browser"):
            self.checkBox_show_in_browser.setChecked(
                self.plot_data.checkbox_show_in_browser
            )
        else:
            self.checkBox_show_in_browser.setChecked(False)

        if hasattr(self.plot_data, "browser_port") and self.plot_data.browser_port:
            try:
                port = int(self.plot_data.browser_port)
            except ValueError:
                port = 8050
            self.spinBox_port.setValue(port)
        else:
            self.spinBox_port.setValue(8050)
        self.hide_show_manual_position()
        self.hide_show_show_in_browser()
        self.plot_data.update_name()

    def get_data(self):
        """ """
        self.plot_data.y_axes = self.y_table.update_table_data()
        self.plot_data.x_axis = self.lineEdit_x_axis.text()
        self.plot_data.title = self.lineEdit_title.text()
        if re.search(r"[\\'\"`]", self.plot_data.title):
            raise ValueError(
                "Title contains special characters.\nYou cannot use ' \" or `."
            )
        self.plot_data.xlabel = self.lineEdit_xlabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.xlabel):
            raise ValueError(
                "x-label contains special characters.\nYou cannot use ' \" or `."
            )
        self.plot_data.ylabel = self.lineEdit_ylabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.ylabel):
            raise ValueError(
                "y-label contains special characters.\nYou cannot use ' \" or `."
            )
        self.plot_data.ylabel2 = self.lineEdit_ylabel2.text()
        if re.search(r"[\\'\"`]", self.plot_data.zlabel):
            raise ValueError(
                "z-label contains special characters.\nYou cannot use ' \" or `."
            )
        # self.plot_data.do_plot = self.checkBox_plot.isChecked()
        try:
            self.plot_data.maxlen = int(self.lineEdit_nPoints.text())
        except ValueError:
            self.plot_data.maxlen = np.inf
        self.plot_data.same_fit = self.checkBox_same_fit.isChecked()
        self.plot_data.logX = self.checkBox_xlog.isChecked()
        self.plot_data.logY = self.checkBox_ylog.isChecked()
        self.plot_data.logY2 = self.checkBox_ylog2.isChecked()
        # If the string is empty set empty string
        if self.lineEdit_top_left_x.text():
            try:
                self.plot_data.top_left_x = max(int(self.lineEdit_top_left_x.text()), 0)
            except ValueError:
                self.plot_data.top_left_x = ""
            
        else:
            self.plot_data.top_left_x = ""

        if self.lineEdit_top_left_y.text():
            try:
                self.plot_data.top_left_y = max(int(self.lineEdit_top_left_y.text()), 0)
            except ValueError:
                self.plot_data.top_left_y = ""
        else:
            self.plot_data.top_left_y = ""

        if self.lineEdit_plot_width.text():
            try:
                self.plot_data.plot_width = max(int(self.lineEdit_plot_width.text()), 430)
            except ValueError:
                self.plot_data.plot_width = ""
            
        else:
            self.plot_data.plot_width = ""

        if self.lineEdit_plot_height.text():
            try:
                self.plot_data.plot_height = max(int(self.lineEdit_plot_height.text()), 126)
            except ValueError:
                self.plot_data.plot_height = ""
            
        else:
            self.plot_data.plot_height = ""

        # Check to see if only x or y is set and raise error
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set")
        # Check to see if only height or width is set and raise error
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set")

        # Get the checkBox_manual_plot_position value
        self.plot_data.checkbox_manual_plot_position = self.checkBox_manual_plot_position.isChecked()
        self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
        self.plot_data.browser_port = self.spinBox_port.value()


        
        if not isinstance(self.fit_definer, QLabel):
            self.fit_definer.get_data()
        self.plot_data.update_name()
        if self.plot_data.all_fit:
            self.plot_data.all_fit.x = self.plot_data.x_axis
        for i, fit in enumerate(self.plot_data.fits):
            fit.y = self.plot_data.y_axes["formula"][i]
            fit.x = self.plot_data.x_axis
        return super().get_data()

    def hide_show_manual_position(self):
        if self.checkBox_manual_plot_position.isChecked():
            self.label_top_left_x.setHidden(False)
            self.lineEdit_top_left_x.setHidden(False)
            self.label_top_left_y.setHidden(False)
            self.lineEdit_top_left_y.setHidden(False)
            self.label_plot_width.setHidden(False)
            self.lineEdit_plot_width.setHidden(False)
            self.label_plot_height.setHidden(False)
            self.lineEdit_plot_height.setHidden(False)
        else:
            self.label_top_left_x.setHidden(True)
            self.lineEdit_top_left_x.setHidden(True)
            self.label_top_left_y.setHidden(True)
            self.lineEdit_top_left_y.setHidden(True)
            self.label_plot_width.setHidden(True)
            self.lineEdit_plot_width.setHidden(True)
            self.label_plot_height.setHidden(True)
            self.lineEdit_plot_height.setHidden(True)

    def hide_show_show_in_browser(self):
        if self.checkBox_show_in_browser.isChecked():
            self.label_port.setHidden(False)
            self.spinBox_port.setHidden(False)
        else:
            self.label_port.setHidden(True)
            self.spinBox_port.setHidden(True)

    
    def fit_change(self):
        """ """
        if not isinstance(self.fit_definer, QLabel):
            self.fit_definer.get_data()
        if self.checkBox_same_fit.isChecked():
            fit_dat = self.plot_data.all_fit
            fit_to = "all y-axes"
        else:
            ind = self.y_table.table.selectedIndexes()
            if ind:
                n = ind[0].row()
                fit_to = self.y_table.table_model.item(n, 0).text()
                fit_dat = self.plot_data.fits[n]
            else:
                fit_dat = None
                fit_to = None
        if fit_dat is None:
            fit_definer = QLabel("No y-axis selected")
        else:
            fit_definer = Fit_Definer(fit_dat, self, fit_to)
        self.layout().replaceWidget(self.fit_definer, fit_definer)
        self.fit_definer.deleteLater()
        self.fit_definer = fit_definer


class Fit_Definer(Ui_Fit_Definer, QWidget):
    """ """

    def __init__(self, fit_info: Fit_Info, parent=None, fit_to=""):
        super().__init__(parent)
        self.setupUi(self)
        self.fit_info = fit_info
        self.label.setText(f"Fit to: {fit_to}")
        self.comboBox_predef_func.addItems(sorted(models_names.keys()))
        cols = ["name", "initial value", "lower bound", "upper bound"]
        self.start_params = AddRemoveTable(
            headerLabels=cols,
            title="Fit Parameters",
            editables=[1, 2, 3],
            tableData=fit_info.initial_params,
        )
        self.add_data = AddRemoveTable(
            headerLabels=[], title="Additional Data", tableData=fit_info.additional_data
        )
        self.start_params.addButton.setHidden(True)
        self.start_params.removeButton.setHidden(True)
        self.load_data()

        self.checkBox_fit.clicked.connect(self.change_func)
        self.radioButton_custom_func.clicked.connect(self.change_func)
        self.radioButton_predef_func.clicked.connect(self.change_func)
        self.checkBox_guess.clicked.connect(self.change_func)
        self.comboBox_predef_func.currentTextChanged.connect(self.change_func)
        self.lineEdit_custom_func.textChanged.connect(self.change_func)
        self.change_func()
        self.layout().addWidget(self.start_params, 10, 0, 1, 2)
        self.layout().addWidget(self.add_data, 0, 3, 11, 2)

    def change_func(self):
        """ """
        fit = self.checkBox_fit.isChecked()
        custom = self.radioButton_custom_func.isChecked()
        guess = self.checkBox_guess.isChecked()
        self.radioButton_custom_func.setEnabled(fit)
        self.radioButton_predef_func.setEnabled(fit)
        self.checkBox_guess.setEnabled(fit)
        self.comboBox_predef_func.setEnabled(fit and not custom)
        self.lineEdit_custom_func.setEnabled(fit and custom)
        # self.start_params.setEnabled(fit and not guess)
        self.start_params.enableds = [0, 2, 3]
        self.start_params.editables = [2, 3]
        self.start_params.addButton.setHidden(not custom)
        self.start_params.removeButton.setHidden(not custom)
        if custom:
            self.start_params.editables += [0]
        if not guess:
            self.start_params.editables += [1]
            self.start_params.enableds += [1]
        par_vals = self.start_params.update_table_data()
        self.start_params.change_table_data(par_vals)

        func = self.comboBox_predef_func.currentText()
        if func != self.fit_info.predef_func:
            if custom:
                try:
                    mod = models.ExpressionModel(self.lineEdit_custom_func.text())
                except (ValueError, SyntaxError):
                    self.lineEdit_custom_func.setStyleSheet(
                        f"background-color: rgb{variables_handling.get_color('red', True)}"
                    )
                    return
                self.lineEdit_custom_func.setStyleSheet(
                    f"background-color: rgb{variables_handling.get_color('green', True)}"
                )
            else:
                mod = models_names[func]()
            params = mod.param_names
            par_vals = {
                "name": [],
                "initial value": [],
                "lower bound": [],
                "upper bound": [],
            }
            for param in params:
                par_vals["name"].append(param)
                par_vals["initial value"].append(1)
                par_vals["lower bound"].append("")
                par_vals["upper bound"].append("")
            self.start_params.change_table_data(par_vals)
            self.fit_info.predef_func = func
        if fit and not custom and func == "Linear" and par_vals["name"] == []:
            mod = models_names[func]()
            params = mod.param_names
            par_vals = {
                "name": [],
                "initial value": [],
                "lower bound": [],
                "upper bound": [],
            }
            for param in params:
                par_vals["name"].append(param)
                par_vals["initial value"].append(1)
                par_vals["lower bound"].append("")
                par_vals["upper bound"].append("")
            self.start_params.change_table_data(par_vals)

    def load_data(self):
        """ """
        self.checkBox_fit.setChecked(self.fit_info.do_fit)
        self.comboBox_predef_func.setCurrentText(self.fit_info.predef_func)
        self.lineEdit_custom_func.setText(self.fit_info.custom_func)
        self.radioButton_custom_func.setChecked(self.fit_info.use_custom_func)
        self.checkBox_guess.setChecked(self.fit_info.guess_params)
        self.checkBox_display_values.setChecked(self.fit_info.display_values)

    def get_data(self):
        """ """
        self.fit_info.initial_params = self.start_params.update_table_data()
        rems = []
        for i, param in enumerate(self.fit_info.initial_params["name"]):
            if not param:
                rems.append(i)
        for i in rems[::-1]:
            for key in self.fit_info.initial_params:
                self.fit_info.initial_params[key].pop(i)
        self.fit_info.additional_data = self.add_data.update_table_data()
        self.fit_info.do_fit = self.checkBox_fit.isChecked()
        self.fit_info.predef_func = self.comboBox_predef_func.currentText()
        self.fit_info.custom_func = self.lineEdit_custom_func.text()
        self.fit_info.use_custom_func = self.radioButton_custom_func.isChecked()
        self.fit_info.guess_params = self.checkBox_guess.isChecked()
        self.fit_info.display_values = self.checkBox_display_values.isChecked()


def add_fit(tableData, fit):
    """

    Parameters
    ----------
    tableData :

    fit :


    Returns
    -------

    """
    custom = fit.use_custom_func
    if custom:
        tableData["fit"].append(fit.custom_func)
    else:
        tableData["fit"].append(fit.predef_func)


def make_table_data(plot_data):
    """

    Parameters
    ----------
    plot_data :


    Returns
    -------

    """
    tableData = {"plot-type": [], "name": [], "fit": []}
    for plt in plot_data:
        tableData["plot-type"].append(plt.plt_type)
        tableData["name"].append(plt.name)
        if plt.all_fit and plt.all_fit.do_fit and plt.same_fit:
            add_fit(tableData, plt.all_fit)
        elif plt.fits:
            added = False
            for fit in plt.fits:
                if not fit.do_fit:
                    continue
                add_fit(tableData, fit)
                added = True
                break
            if not added:
                tableData["fit"].append("None")
        else:
            tableData["fit"].append("None")
    return tableData


class Plot_Button_Overview(QWidget):
    """ """

    def __init__(self, parent, plot_data=None):
        self.plot_data = plot_data
        super().__init__(parent)
        tableData = make_table_data(plot_data)
        cols = ["plot-type", "name", "fit"]
        self.plot_table = AddRemoveTable(
            headerLabels=cols,
            title="plot-overview",
            editables=[],
            tableData=tableData,
            askdelete=True,
            horizontal=False,
        )
        self.plot_table.addButton.setHidden(True)
        self.plot_table.removeButton.setHidden(True)
        self.plot_button = QPushButton("Configure: Plots/Fits")
        font = QFont()
        font.setBold(True)
        self.plot_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; /* green */
                border: none; /* Remove border for a cleaner look */
                color: white; /* Text color */
                padding: 3px; /* Adjust padding as needed */
                padding-bottom: 3px;
                border-radius: 6px; /* Rounded corners with a radius of 10px */
                font-size: 13px;
                font-weight: bold;
                text-align: center;
                margin: 2px 2px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Slightly lighter green on hover */
            }
            QPushButton:pressed {
                background-color: #2f6331; /* Slightly darker green when pressed */
            }
            """
        )
        self.plot_button.setFont(font)
        self.plot_button.clicked.connect(self.define_plots)

        layout = QGridLayout()
        layout.addWidget(self.plot_button, 0, 0)
        layout.addWidget(self.plot_table, 1, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def define_plots(self):
        """ """
        plot_definer = Plot_Definer(self, self.plot_data)
        if plot_definer.exec():
            self.plot_data = plot_definer.plot_data
            tableData = make_table_data(self.plot_data)
            self.plot_table.change_table_data(tableData)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """Overwrites the keyPressEvent of the QDialog so that it does
        not close when pressing Enter/Return.

        Parameters
        ----------
        a0: QKeyEvent :


        Returns
        -------

        """
        if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            return
        super().keyPressEvent(a0)


models_names = dict(models.lmfit_models)
models_names.pop("Expression")
