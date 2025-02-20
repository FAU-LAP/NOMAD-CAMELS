"""
This module provides GUI dialogs and widgets for defining plot configurations
and fit settings for NOMAD CAMELS. It uses PySide6 for the GUI and lmfit for
fitting functions. The code defines several classes to store metadata (Plot_Info,
Fit_Info) and multiple widgets for configuring different plot types (X-Y, Value-List,
2D) as well as fit definitions.
"""

import copy
import re
import subprocess
import sys

import numpy as np

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
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

# List of available plot types
plot_types = ["X-Y plot", "Value-List", "2D plot"]

# Get a dictionary of available lmfit models and remove the "Expression" model if present.
models_names = dict(models.lmfit_models)
models_names.pop("Expression", None)


def parse_int_field(text, min_value, fallback=""):
    """
    Parse an integer from the provided text while enforcing a minimum value.
    
    Parameters:
        text (str): The string to parse.
        min_value (int): The minimum allowed value.
        fallback (str): The value to return if parsing fails.
        
    Returns:
        int or str: The parsed integer (if successful) or the fallback.
    """
    if text:
        try:
            return max(int(text), min_value)
        except ValueError:
            return fallback
    return fallback


class Plot_Info:
    """
    Holds all relevant metadata about a single plot configuration.
    
    This includes information such as the type of plot, axis definitions,
    fit settings, manual positioning options, and display options.

    Attributes:
        plt_type (str): The type of plot (e.g., "X-Y plot", "Value-List", "2D plot").
        x_axis (str): Expression or variable for the x-axis.
        y_axes (dict): Contains lists for 'formula' (expressions) and 'axis' (left/right assignment).
        z_axis (str): Expression or variable for the z-axis (used in 2D plots).
        title (str): Plot title.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the left y-axis (in XY plots).
        ylabel2 (str): Label for the right y-axis (if used).
        zlabel (str): Label for the z-axis (in 2D plots).
        logX (bool): Whether to use logarithmic scaling for the x-axis.
        logY (bool): Whether to use logarithmic scaling for the y-axis.
        logY2 (bool): Whether to use logarithmic scaling for the second y-axis.
        do_plot (bool): Whether the plot should be rendered.
        same_fit (bool): If True, the same fit settings apply to all y-axes.
        fits (list of Fit_Info): Fit configuration for each y-axis.
        all_fit (Fit_Info): Single fit configuration if same_fit is True.
        plot_all_available (bool): For Value-List plots, plot all available channels.
        maxlen (int or float): Maximum number of data points to display (default: infinity).
        top_left_x (str/int): Manual x-coordinate for plot placement.
        top_left_y (str/int): Manual y-coordinate for plot placement.
        plot_width (str/int): Manual width for the plot.
        plot_height (str/int): Manual height for the plot.
        checkbox_manual_plot_position (bool): Flag indicating if manual positioning is enabled.
        checkbox_show_in_browser (bool): Flag for showing the plot in a browser.
        browser_port (int): Port number for the browser-based plot.
        name (str): A short name auto-generated from the plot properties.
    """

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
        checkbox_manual_plot_position=False,
        checkbox_show_in_browser=False,
        browser_port=8050,
    ):
        # Initialize plot type and axis definitions
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
        # For Value-List plots, default to plotting all available channels.
        self.plot_all_available = True  
        self.all_fit = all_fit or Fit_Info()
        self.name = ""
        self.maxlen = np.inf
        # Manual positioning and sizing parameters
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.checkbox_manual_plot_position = checkbox_manual_plot_position
        self.checkbox_show_in_browser = checkbox_show_in_browser
        self.browser_port = browser_port

        # Generate a human-readable name based on available data.
        self.update_name()

    def update_name(self):
        """
        Update the plot's `name` attribute to a short descriptive string 
        based on the current plot configuration.
        """
        if self.title:
            # Use title if provided.
            self.name = self.title
        elif self.plt_type == "X-Y plot":
            # Use provided axis labels or expressions to generate a name.
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
            # Try to generate a descriptive name for 2D plots.
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
        Collect all fit variable names needed for this plot.
        
        Parameters:
            stream (str): An identifier or suffix to append to variable names.
            
        Returns:
            dict: A dictionary mapping variable names to an initial value (1).
        """
        variables = {}
        if self.same_fit:
            # Use a single fit for all y-axes.
            if self.all_fit.do_fit:
                self.all_fit.x = self.x_axis
                for y in self.y_axes["formula"]:
                    fit_copy = copy.deepcopy(self.all_fit)
                    fit_copy.y = y
                    variables.update(fit_copy.get_variables(stream))
        else:
            # Iterate over individual fit configurations.
            for fit in self.fits:
                if fit.do_fit:
                    variables.update(fit.get_variables(stream))
        return variables


class Fit_Info:
    """
    Stores all relevant settings for performing a curve fit.
    
    Attributes:
        do_fit (bool): Flag indicating if a fit should be performed.
        predef_func (str): Name of a predefined lmfit model.
        custom_func (str): Custom function expression (if using a custom fit).
        use_custom_func (bool): Flag to choose between custom and predefined fit.
        guess_params (bool): Flag to enable automatic parameter guessing.
        initial_params (dict): Dictionary with keys "name", "initial value",
                               "lower bound", "upper bound" for parameters.
        y (str): Expression or variable representing the dependent data.
        x (str): Expression or variable representing the independent data.
        additional_data (list): Extra data used for the fit (if any).
        display_values (bool): Whether to display the fit parameter values on the plot.
        name (str): Auto-generated name for the fit.
    """

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

        # Initialize initial_params with default empty lists if not provided.
        self.initial_params = initial_params or {
            "name": [],
            "initial value": [],
            "lower bound": [],
            "upper bound": [],
        }
        self.additional_data = additional_data or []
        self.y = y
        self.x = x

    def get_name(self, stream=""):
        """
        Generate a unique name for this fit.
        
        Parameters:
            stream (str): An identifier (e.g., a data stream name) to append.
            
        Returns:
            str: A generated fit name (e.g., "Gaussian_channelY_v_channelX_stream").
        """
        # Choose label based on whether a custom function is used.
        label = "custom" if self.use_custom_func else self.predef_func
        self.name = f"{label}_{self.y}_v_{self.x}_{stream}".replace(" ", "_")
        return self.name

    def get_variables(self, stream=""):
        """
        Build a dictionary of parameter variable names for this fit.
        
        Each parameter name is prefixed by the unique fit name.
        
        Parameters:
            stream (str): An identifier to append to parameter names.
            
        Returns:
            dict: A mapping {param_name: 1} for each parameter in initial_params.
        """
        variables = {}
        fit_name = self.get_name(stream)
        # Iterate over all parameter names to build variable names.
        for var in self.initial_params["name"]:
            var_name = f"{fit_name}_{var}"
            # Clean the variable name by replacing special characters.
            var_name = replace_name(var_name)
            variables[var_name] = 1
        return variables


class Plot_Definer(QDialog):
    """
    Dialog for defining or editing multiple Plot_Info objects.
    
    It displays a table (AddRemoveTable) with existing plots and a child widget
    on the right for configuring details of the selected plot.
    """

    def __init__(self, parent=None, plot_data=None):
        """
        Initialize the Plot_Definer dialog.
        
        Parameters:
            parent (QWidget, optional): The parent widget.
            plot_data (list of Plot_Info, optional): Initial plot configurations.
        """
        super().__init__(parent)
        self.plot_data = plot_data or []

        self.setWindowTitle("Define plot - NOMAD CAMELS")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        # Define columns and combo-box options for the plot table.
        columns = ["plot-type", "name"]
        combo_boxes = {"plot-type": plot_types}
        table_data = {"plot-type": [], "name": []}

        # Populate the table data from the current Plot_Info objects.
        for plt_info in self.plot_data:
            table_data["plot-type"].append(plt_info.plt_type)
            table_data["name"].append(plt_info.name)

        # Create the AddRemoveTable widget for the plots list.
        self.plot_table = AddRemoveTable(
            headerLabels=columns,
            title="Plots",
            editables=[],
            comboBoxes=combo_boxes,
            tableData=table_data,
            askdelete=True,
        )
        # Connect signals for table interactions.
        self.plot_table.table.clicked.connect(self.change_plot_def)
        self.plot_table.added.connect(self.plot_added)
        self.plot_table.removed.connect(self.plot_removed)

        # Placeholder widget; replaced when a plot is selected.
        self.plot_def = QLabel("Select a plot!")

        # Create OK/Cancel dialog buttons.
        self.dialog_buttons = QDialogButtonBox()
        self.dialog_buttons.setOrientation(Qt.Horizontal)
        self.dialog_buttons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)

        # Arrange all widgets in a grid layout.
        layout = QGridLayout()
        layout.addWidget(self.plot_table, 0, 0)
        layout.addWidget(self.plot_def, 0, 1)
        layout.addWidget(self.dialog_buttons, 1, 0, 1, 2)
        self.setLayout(layout)

    def accept(self) -> None:
        """
        Overridden accept method to ensure that the current plot configuration
        is saved before closing the dialog.
        """
        # If the current plot definition widget is not just a placeholder, update data.
        if not isinstance(self.plot_def, QLabel):
            self.plot_def.get_data()
        super().accept()

    def reject(self):
        """
        Overridden reject method that asks for confirmation before discarding changes.
        """
        discard_dialog = QMessageBox.question(
            self,
            "Discard Changes?",
            "All changes to the defined plots/fits will be lost!",
            QMessageBox.Yes | QMessageBox.No,
        )
        if discard_dialog != QMessageBox.Yes:
            return
        super().reject()

    def change_plot_def(self, index):
        """
        Called when the user selects a plot in the table.
        
        Replaces the right-hand widget with the appropriate sub-definer
        based on the selected plot type.
        
        Parameters:
            index (QModelIndex): Index of the selected row.
        """
        # Save current changes from the active plot definition widget.
        if not isinstance(self.plot_def, QLabel):
            self.plot_def.get_data()

        # Get the Plot_Info object corresponding to the selected row.
        plot_dat = self.plot_data[index.row()]

        # Update the plot type based on the current selection in the combo box.
        type_index = self.plot_table.table_model.index(index.row(), 0)
        plot_dat.plt_type = self.plot_table.table.indexWidget(type_index).currentText()

        # Refresh the table data to reflect any updates.
        table_data = {"plot-type": [], "name": []}
        for plt_info in self.plot_data:
            table_data["plot-type"].append(plt_info.plt_type)
            table_data["name"].append(plt_info.name)
        self.plot_table.change_table_data(table_data)

        # Create the appropriate sub-widget based on the plot type.
        if plot_dat.plt_type == "X-Y plot":
            plot_def = Single_Plot_Definer_XY(plot_dat, self)
        elif plot_dat.plt_type == "Value-List":
            plot_def = Single_Plot_Definer_List(plot_dat, self)
        elif plot_dat.plt_type == "2D plot":
            plot_def = Single_Plot_Definer_2D(plot_dat, self)
        else:
            plot_def = QLabel("Not implemented yet!")

        # Replace the old plot definition widget with the new one.
        self.layout().replaceWidget(self.plot_def, plot_def)
        self.plot_def.deleteLater()
        self.plot_def = plot_def

        # Keep the new row selected.
        selection_flag = self.plot_table.table.selectionModel().SelectionFlag.Select
        self.plot_table.table.selectionModel().select(index, selection_flag)

    def plot_added(self, n):
        """
        Slot called when a new plot row is added.
        
        Parameters:
            n (int): The index of the newly added row.
        """
        if n >= len(self.plot_data):
            self.plot_data.append(Plot_Info())

    def plot_removed(self, n):
        """
        Slot called when a plot row is removed.
        
        Parameters:
            n (int): The index of the removed row.
        """
        self.plot_data.pop(n)


class Single_Plot_Definer(QWidget):
    """
    Base class for a widget that defines a single plot.
    
    Extended by subclasses for specific plot types (e.g., X-Y, Value-List, 2D).
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        """
        Initialize with a Plot_Info instance.
        
        Parameters:
            plot_data (Plot_Info): The plot configuration to be edited.
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(parent)
        self.plot_data = plot_data

    def get_data(self):
        """
        Retrieve the current plot configuration.
        
        Child classes should override this method to update additional data.
        
        Returns:
            Plot_Info: The current plot configuration.
        """
        return self.plot_data

    def add_y(self, n):
        """
        Called when a new y-axis (or formula) row is added.
        
        Parameters:
            n (int): The index of the newly added row.
        """
        if n >= len(self.plot_data.fits):
            self.plot_data.fits.append(Fit_Info())

    def remove_y(self, n):
        """
        Called when a y-axis (or formula) row is removed.
        
        Parameters:
            n (int): The index of the removed row.
        """
        self.plot_data.fits.pop(n)


class Single_Plot_Definer_List(Single_Plot_Definer):
    """
    Widget to configure a "Value-List" plot.
    
    This widget displays a checkbox to plot all available channels, a table for
    custom expressions, and fields for manual positioning and sizing.
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        """
        Initialize the Value-List definer widget.
        
        Parameters:
            plot_data (Plot_Info): The plot configuration to be edited.
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(plot_data, parent)

        # Checkbox to determine if all channels should be plotted.
        self.checkBox_plot_all = QCheckBox("Plot all available channels")
        self.checkBox_plot_all.setChecked(plot_data.plot_all_available)

        # Table to list custom expressions (if not plotting all channels).
        self.table = AddRemoveTable(
            title="Values",
            headerLabels=[],
            tableData=plot_data.y_axes["formula"],
            checkstrings=[0],
        )
        self.table.added.connect(self.add_y)
        self.table.removed.connect(self.remove_y)

        # Create the layout and add widgets.
        layout = QGridLayout()
        layout.addWidget(self.checkBox_plot_all, 0, 0, 1, 4)
        layout.addWidget(self.table, 1, 0, 1, 4)

        # Separator line for visual separation.
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line, 3, 0, 1, 4)

        # Labels and line edits for manual positioning and size.
        label_top_left_x = QLabel("Top Left X:", self)
        self.lineEdit_top_left_x = QLineEdit(self)
        label_top_left_y = QLabel("Top Left Y:", self)
        self.lineEdit_top_left_y = QLineEdit(self)
        label_plot_width = QLabel("Plot Width:", self)
        self.lineEdit_plot_width = QLineEdit(self)
        label_plot_height = QLabel("Plot Height:", self)
        self.lineEdit_plot_height = QLineEdit(self)

        # Place the manual positioning widgets in the grid.
        layout.addWidget(label_top_left_x, 11, 0)
        layout.addWidget(self.lineEdit_top_left_x, 11, 1)
        layout.addWidget(label_plot_width, 11, 2)
        layout.addWidget(self.lineEdit_plot_width, 11, 3)

        layout.addWidget(label_top_left_y, 12, 0)
        layout.addWidget(self.lineEdit_top_left_y, 12, 1)
        layout.addWidget(label_plot_height, 12, 2)
        layout.addWidget(self.lineEdit_plot_height, 12, 3)

        self.setLayout(layout)
        self.load_data()
        self.plot_data.update_name()

    def load_data(self):
        """
        Load existing manual positioning and sizing data into the line edits.
        """
        # Populate each line edit with the corresponding Plot_Info attribute.
        if hasattr(self.plot_data, "top_left_x"):
            self.lineEdit_top_left_x.setText(str(self.plot_data.top_left_x))
        if hasattr(self.plot_data, "top_left_y"):
            self.lineEdit_top_left_y.setText(str(self.plot_data.top_left_y))
        if hasattr(self.plot_data, "plot_width"):
            self.lineEdit_plot_width.setText(str(self.plot_data.plot_width))
        if hasattr(self.plot_data, "plot_height"):
            self.lineEdit_plot_height.setText(str(self.plot_data.plot_height))

    def get_data(self):
        """
        Validate and retrieve data from the UI elements for the Value-List plot.
        
        Returns:
            Plot_Info: The updated plot configuration.
        
        Raises:
            ValueError: If manual position/size is partially defined.
        """
        # Update plot_data with the state of the "plot all" checkbox.
        self.plot_data.plot_all_available = self.checkBox_plot_all.isChecked()
        self.plot_data.y_axes["formula"] = self.table.update_table_data()
        # Set the y-axis assignment to 1 (default for Value-List plots).
        self.plot_data.y_axes["axis"] = [1] * len(self.plot_data.y_axes["formula"])

        # Parse and store manual position/size using the helper function.
        self.plot_data.top_left_x = parse_int_field(self.lineEdit_top_left_x.text(), 0)
        self.plot_data.top_left_y = parse_int_field(self.lineEdit_top_left_y.text(), 0)
        self.plot_data.plot_width = parse_int_field(self.lineEdit_plot_width.text(), 430)
        self.plot_data.plot_height = parse_int_field(self.lineEdit_plot_height.text(), 126)

        # Check for partial definitions of manual positioning or sizing.
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set, but x position is.")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set, but y position is.")
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set, but width is.")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set, but height is.")

        # Update the plot name based on the latest data.
        self.plot_data.update_name()
        return super().get_data()


class Single_Plot_Definer_2D(Ui_Plot_Definer_2D, Single_Plot_Definer):
    """
    Widget to configure a "2D plot".
    
    This widget is based on the Qt Designer form compiled into Ui_Plot_Definer_2D.
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        """
        Initialize the 2D plot definer.
        
        Parameters:
            plot_data (Plot_Info): The plot configuration to be edited.
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(plot_data, parent)
        self.setupUi(self)

        # Pre-fill UI elements with existing Plot_Info data.
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

        # Connect checkboxes for manual positioning and browser port display.
        self.checkBox_manual_plot_position_2d.stateChanged.connect(self.hide_show_manual_position)
        self.checkBox_show_in_browser.stateChanged.connect(self.hide_show_show_in_browser)
        self.checkBox_show_in_browser.clicked.connect(self.hide_show_show_in_browser)

    def load_data(self):
        """
        Load manual positioning, sizing, and browser rendering options from Plot_Info.
        """
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
            self.checkBox_show_in_browser.setChecked(self.plot_data.checkbox_show_in_browser)
        else:
            self.checkBox_show_in_browser.setChecked(False)

        # Set the browser port; fallback to 8050 if not valid.
        if hasattr(self.plot_data, "browser_port") and self.plot_data.browser_port:
            try:
                port_val = int(self.plot_data.browser_port)
            except ValueError:
                port_val = 8050
            self.spinBox_port.setValue(port_val)
        else:
            self.spinBox_port.setValue(8050)

        # Adjust visibility of manual position and browser port fields.
        self.hide_show_manual_position()
        self.hide_show_show_in_browser()

    def get_data(self):
        """
        Validate and retrieve data from the UI for the 2D plot.
        
        Returns:
            Plot_Info: The updated plot configuration.
            
        Raises:
            ValueError: If any axis label contains invalid characters or if manual
                        positioning/sizing is partially defined.
        """
        # Validate and update axis labels and title.
        self.plot_data.xlabel = self.lineEdit_xlabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.xlabel):
            raise ValueError("x-label contains invalid characters (' \" `).")

        self.plot_data.ylabel = self.lineEdit_ylabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.ylabel):
            raise ValueError("y-label contains invalid characters (' \" `).")

        self.plot_data.zlabel = self.lineEdit_zlabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.zlabel):
            raise ValueError("z-label contains invalid characters (' \" `).")

        self.plot_data.x_axis = self.lineEdit_x_axis.text()
        self.plot_data.y_axes["formula"][0] = self.lineEdit_y_axis.text()
        self.plot_data.z_axis = self.lineEdit_z_axis.text()
        self.plot_data.title = self.lineEdit_title.text()
        max_len_str = self.lineEdit_n_data_points.text()
        self.plot_data.maxlen = max_len_str if max_len_str else "inf"

        # Parse manual positioning and sizing using the helper function.
        self.plot_data.top_left_x = parse_int_field(self.lineEdit_top_left_x.text(), 0)
        self.plot_data.top_left_y = parse_int_field(self.lineEdit_top_left_y.text(), 0)
        self.plot_data.plot_width = parse_int_field(self.lineEdit_plot_width.text(), 430)
        self.plot_data.plot_height = parse_int_field(self.lineEdit_plot_height.text(), 126)

        # Validate that position/size fields are either fully specified or left empty.
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set, but x position is.")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set, but y position is.")
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set, but width is.")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set, but height is.")

        # Save checkbox states and browser port.
        self.plot_data.checkbox_manual_plot_position = (
            self.checkBox_manual_plot_position_2d.isChecked()
        )
        self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
        self.plot_data.browser_port = self.spinBox_port.value()

        self.plot_data.update_name()
        return super().get_data()

    def hide_show_manual_position(self):
        """
        Toggle visibility of manual positioning fields based on the checkbox state.
        """
        is_checked = self.checkBox_manual_plot_position_2d.isChecked()
        self.label_top_left_x.setHidden(not is_checked)
        self.lineEdit_top_left_x.setHidden(not is_checked)
        self.label_top_left_y.setHidden(not is_checked)
        self.lineEdit_top_left_y.setHidden(not is_checked)
        self.label_plot_width.setHidden(not is_checked)
        self.lineEdit_plot_width.setHidden(not is_checked)
        self.label_plot_height.setHidden(not is_checked)
        self.lineEdit_plot_height.setHidden(not is_checked)

    def hide_show_show_in_browser(self):
        """
        Toggle visibility of the browser port selection based on the checkbox state.
        """
        is_checked = self.checkBox_show_in_browser.isChecked()
        self.label_port.setHidden(not is_checked)
        self.spinBox_port.setHidden(not is_checked)
        if is_checked:
            check_if_plotly_modules_are_available(self)


class Single_Plot_Definer_XY(Ui_Plot_Definer, Single_Plot_Definer):
    """
    Widget to configure a classic "X-Y plot".
    
    This widget is based on the Qt Designer form compiled into Ui_Plot_Definer.
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        """
        Initialize the X-Y plot definer widget.
        
        Parameters:
            plot_data (Plot_Info): The plot configuration to be edited.
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(plot_data, parent)
        self.fit_definer = None
        self.setupUi(self)

        # Create a table for y-axis definitions (formula and axis side).
        cols = ["formula", "axis"]
        combo_boxes = {"axis": ["left", "right"]}
        self.y_table = AddRemoveTable(
            headerLabels=cols,
            title="y-axes",
            comboBoxes=combo_boxes,
            tableData=plot_data.y_axes,
            checkstrings=[0],
        )
        self.y_table.added.connect(self.add_y)
        self.y_table.removed.connect(self.remove_y)
        self.y_table.table.clicked.connect(self.fit_change)

        # Checkbox to indicate if the same fit should be used for all y-axes.
        self.checkBox_same_fit.clicked.connect(self.fit_change)

        # Replace the placeholder y_axes widget with the custom table.
        self.layout().replaceWidget(self.y_axes, self.y_table)

        # Load initial data into the UI elements.
        self.load_data()
        self.fit_change()

        # Connect checkboxes for manual positioning and browser port display.
        self.checkBox_manual_plot_position.stateChanged.connect(self.hide_show_manual_position)
        self.checkBox_show_in_browser.stateChanged.connect(self.hide_show_show_in_browser)
        self.checkBox_show_in_browser.clicked.connect(self.hide_show_show_in_browser)

    def load_data(self):
        """
        Populate UI fields with data from the Plot_Info object.
        """
        self.lineEdit_x_axis.setText(self.plot_data.x_axis)
        self.lineEdit_title.setText(self.plot_data.title)
        self.lineEdit_xlabel.setText(self.plot_data.xlabel)
        self.lineEdit_ylabel.setText(self.plot_data.ylabel)
        self.lineEdit_ylabel2.setText(self.plot_data.ylabel2)
        self.lineEdit_nPoints.setText(str(self.plot_data.maxlen))
        self.checkBox_same_fit.setChecked(self.plot_data.same_fit)
        self.checkBox_xlog.setChecked(self.plot_data.logX)
        self.checkBox_ylog.setChecked(self.plot_data.logY)
        self.checkBox_ylog2.setChecked(self.plot_data.logY2)

        # Populate manual positioning and sizing fields.
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

        # Set browser port with fallback to 8050.
        if hasattr(self.plot_data, "browser_port") and self.plot_data.browser_port:
            try:
                port_val = int(self.plot_data.browser_port)
            except ValueError:
                port_val = 8050
            self.spinBox_port.setValue(port_val)
        else:
            self.spinBox_port.setValue(8050)

        self.hide_show_manual_position()
        self.hide_show_show_in_browser()
        self.plot_data.update_name()

    def get_data(self):
        """
        Validate and retrieve data from the UI for the X-Y plot.
        
        Returns:
            Plot_Info: The updated plot configuration.
        
        Raises:
            ValueError: If any label contains invalid characters or if manual
                        position/size is partially defined.
        """
        # Update the y-axis definitions from the table.
        self.plot_data.y_axes = self.y_table.update_table_data()
        self.plot_data.x_axis = self.lineEdit_x_axis.text()
        self.plot_data.title = self.lineEdit_title.text()

        # Validate title and axis labels for invalid characters.
        if re.search(r"[\\'\"`]", self.plot_data.title):
            raise ValueError("Title contains invalid characters (' \" `).")
        self.plot_data.xlabel = self.lineEdit_xlabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.xlabel):
            raise ValueError("x-label contains invalid characters (' \" `).")
        self.plot_data.ylabel = self.lineEdit_ylabel.text()
        if re.search(r"[\\'\"`]", self.plot_data.ylabel):
            raise ValueError("y-label contains invalid characters (' \" `).")
        self.plot_data.ylabel2 = self.lineEdit_ylabel2.text()
        if re.search(r"[\\'\"`]", self.plot_data.ylabel2):
            raise ValueError("Second y-label contains invalid characters (' \" `).")

        # Parse maximum data points; use infinity if invalid.
        try:
            self.plot_data.maxlen = int(self.lineEdit_nPoints.text())
        except ValueError:
            self.plot_data.maxlen = np.inf

        self.plot_data.same_fit = self.checkBox_same_fit.isChecked()
        self.plot_data.logX = self.checkBox_xlog.isChecked()
        self.plot_data.logY = self.checkBox_ylog.isChecked()
        self.plot_data.logY2 = self.checkBox_ylog2.isChecked()

        # Parse manual positioning and sizing using the helper function.
        self.plot_data.top_left_x = parse_int_field(self.lineEdit_top_left_x.text(), 0)
        self.plot_data.top_left_y = parse_int_field(self.lineEdit_top_left_y.text(), 0)
        self.plot_data.plot_width = parse_int_field(self.lineEdit_plot_width.text(), 430)
        self.plot_data.plot_height = parse_int_field(self.lineEdit_plot_height.text(), 126)

        # Validate that either both or none of the manual position/size fields are provided.
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set, but x position is.")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set, but y position is.")
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set, but width is.")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set, but height is.")

        # Save checkbox states and browser port.
        self.plot_data.checkbox_manual_plot_position = self.checkBox_manual_plot_position.isChecked()
        self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
        self.plot_data.browser_port = self.spinBox_port.value()

        # Retrieve any changes from the embedded fit definer widget.
        if not isinstance(self.fit_definer, QLabel):
            self.fit_definer.get_data()

        self.plot_data.update_name()

        # Update the fit references for each y-axis.
        if self.plot_data.all_fit:
            self.plot_data.all_fit.x = self.plot_data.x_axis
        for i, fit in enumerate(self.plot_data.fits):
            # Each fit corresponds to the respective y-axis formula.
            fit.y = self.plot_data.y_axes["formula"][i]
            fit.x = self.plot_data.x_axis

        return super().get_data()

    def hide_show_manual_position(self):
        """
        Toggle visibility of manual positioning fields based on the checkbox state.
        """
        is_checked = self.checkBox_manual_plot_position.isChecked()
        self.label_top_left_x.setHidden(not is_checked)
        self.lineEdit_top_left_x.setHidden(not is_checked)
        self.label_top_left_y.setHidden(not is_checked)
        self.lineEdit_top_left_y.setHidden(not is_checked)
        self.label_plot_width.setHidden(not is_checked)
        self.lineEdit_plot_width.setHidden(not is_checked)
        self.label_plot_height.setHidden(not is_checked)
        self.lineEdit_plot_height.setHidden(not is_checked)

    def hide_show_show_in_browser(self):
        """
        Toggle visibility of the browser port spinbox based on the checkbox state.
        """
        is_checked = self.checkBox_show_in_browser.isChecked()
        self.label_port.setHidden(not is_checked)
        self.spinBox_port.setHidden(not is_checked)
        if is_checked:
            check_if_plotly_modules_are_available(self)

    def fit_change(self):
        """
        Switch the fit-defining widget based on the user's selection.
        
        Uses a single shared Fit_Definer if "same fit" is checked, or an individual
        Fit_Definer for the selected y-axis row otherwise.
        """
        # Save current fit settings if the old widget is active.
        if not isinstance(self.fit_definer, QLabel):
            self.fit_definer.get_data()

        if self.checkBox_same_fit.isChecked():
            fit_dat = self.plot_data.all_fit
            fit_to = "all y-axes"
        else:
            # Get the currently selected y-axis row from the table.
            selection_indexes = self.y_table.table.selectedIndexes()
            if selection_indexes:
                row_idx = selection_indexes[0].row()
                fit_to = self.y_table.table_model.item(row_idx, 0).text()
                fit_dat = self.plot_data.fits[row_idx]
            else:
                fit_dat = None
                fit_to = None

        if fit_dat is None:
            fit_definer = QLabel("No y-axis selected")
        else:
            fit_definer = Fit_Definer(fit_dat, self, fit_to)

        # Replace the current fit definer widget.
        self.layout().replaceWidget(self.fit_definer, fit_definer)
        self.fit_definer.deleteLater()
        self.fit_definer = fit_definer


class Fit_Definer(Ui_Fit_Definer, QWidget):
    """
    Widget for configuring a Fit_Info object.
    
    Users can choose between a predefined or custom function, set initial parameters,
    and adjust bounds. This widget is based on the Qt Designer form compiled into
    Ui_Fit_Definer.
    """

    def __init__(self, fit_info: Fit_Info, parent=None, fit_to=""):
        """
        Initialize the Fit_Definer widget.
        
        Parameters:
            fit_info (Fit_Info): The fit configuration to be edited.
            parent (QWidget, optional): The parent widget.
            fit_to (str): A label indicating which y-axis or data is being fitted.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.fit_info = fit_info

        # Display the target of the fit.
        self.label.setText(f"Fit to: {fit_to}")

        # Populate the combo box with available predefined models.
        self.comboBox_predef_func.addItems(sorted(models_names.keys()))

        # Create a table for initial fit parameters.
        cols = ["name", "initial value", "lower bound", "upper bound"]
        self.start_params = AddRemoveTable(
            headerLabels=cols,
            title="Fit Parameters",
            editables=[1, 2, 3],
            tableData=fit_info.initial_params,
        )
        # Create a table for additional data.
        self.add_data = AddRemoveTable(
            headerLabels=[],
            title="Additional Data",
            tableData=fit_info.additional_data,
        )

        # Hide add/remove buttons for parameters unless a custom function is used.
        self.start_params.addButton.setHidden(True)
        self.start_params.removeButton.setHidden(True)

        # Load existing Fit_Info data into the UI.
        self.load_data()

        # Connect UI elements to update the interface dynamically.
        self.checkBox_fit.clicked.connect(self.change_func)
        self.radioButton_custom_func.clicked.connect(self.change_func)
        self.radioButton_predef_func.clicked.connect(self.change_func)
        self.checkBox_guess.clicked.connect(self.change_func)
        self.comboBox_predef_func.currentTextChanged.connect(self.change_func)
        self.lineEdit_custom_func.textChanged.connect(self.change_func)

        # Add the parameter and additional-data tables to the layout.
        self.layout().addWidget(self.start_params, 10, 0, 1, 2)
        self.layout().addWidget(self.add_data, 0, 3, 11, 2)

        # Initial call to configure the UI based on current settings.
        self.change_func()

    def load_data(self):
        """
        Load the Fit_Info configuration into the UI elements.
        """
        self.checkBox_fit.setChecked(self.fit_info.do_fit)
        self.comboBox_predef_func.setCurrentText(self.fit_info.predef_func)
        self.lineEdit_custom_func.setText(self.fit_info.custom_func)
        self.radioButton_custom_func.setChecked(self.fit_info.use_custom_func)
        self.checkBox_guess.setChecked(self.fit_info.guess_params)
        self.checkBox_display_values.setChecked(self.fit_info.display_values)

    def _build_param_table(self, params):
        """
        Build a new parameter table given a list of parameter names.
        
        Parameters:
            params (list): List of parameter names.
        
        Returns:
            dict: A dictionary with keys "name", "initial value", "lower bound", "upper bound".
        """
        new_param_table = {
            "name": [],
            "initial value": [],
            "lower bound": [],
            "upper bound": [],
        }
        for param_name in params:
            new_param_table["name"].append(param_name)
            new_param_table["initial value"].append(1)
            new_param_table["lower bound"].append("")
            new_param_table["upper bound"].append("")
        return new_param_table

    def change_func(self):
        """
        Enable or disable various fields depending on the user's fit selections.
        
        This method dynamically updates the UI elements based on whether the fit is
        enabled, if a custom function is chosen, and whether parameter guessing is enabled.
        """
        fit_enabled = self.checkBox_fit.isChecked()
        custom_func_enabled = self.radioButton_custom_func.isChecked()
        guess_enabled = self.checkBox_guess.isChecked()

        # Enable or disable controls based on the fit selection.
        self.radioButton_custom_func.setEnabled(fit_enabled)
        self.radioButton_predef_func.setEnabled(fit_enabled)
        self.checkBox_guess.setEnabled(fit_enabled)
        self.comboBox_predef_func.setEnabled(fit_enabled and not custom_func_enabled)
        self.lineEdit_custom_func.setEnabled(fit_enabled and custom_func_enabled)

        # Set default editable columns in the parameters table.
        self.start_params.enableds = [0, 2, 3]
        self.start_params.editables = [2, 3]
        self.start_params.addButton.setHidden(not custom_func_enabled)
        self.start_params.removeButton.setHidden(not custom_func_enabled)

        # If using a custom function, allow editing of parameter names if not guessing.
        if custom_func_enabled:
            self.start_params.editables.append(0)
        if not guess_enabled:
            self.start_params.editables.append(1)
            self.start_params.enableds.append(1)

        # Refresh the table with the updated editable columns.
        current_params = self.start_params.update_table_data()
        self.start_params.change_table_data(current_params)

        # If the predefined function has changed, reset the parameter list.
        func_name = self.comboBox_predef_func.currentText()
        if func_name != self.fit_info.predef_func:
            if custom_func_enabled:
                # For custom functions, try parsing the expression.
                try:
                    expression_model = models.ExpressionModel(self.lineEdit_custom_func.text())
                    params = expression_model.param_names
                    # Set the background color to green on success.
                    self.lineEdit_custom_func.setStyleSheet(
                        f"background-color: rgb{variables_handling.get_color('green', True)}"
                    )
                except (ValueError, SyntaxError):
                    # Set the background color to red on failure.
                    self.lineEdit_custom_func.setStyleSheet(
                        f"background-color: rgb{variables_handling.get_color('red', True)}"
                    )
                    return
            else:
                # For predefined models, instantiate the model to get parameter names.
                predefined_model = models_names[func_name]()
                params = predefined_model.param_names

            # Rebuild the parameter table using the helper method.
            new_param_table = self._build_param_table(params)
            self.start_params.change_table_data(new_param_table)
            self.fit_info.predef_func = func_name

        # Special case: if the "Linear" model is selected and the table is empty, populate defaults.
        if fit_enabled and not custom_func_enabled and func_name == "Linear":
            current_params = self.start_params.update_table_data()
            if not current_params["name"]:
                linear_model = models_names[func_name]()
                params = linear_model.param_names
                param_table = self._build_param_table(params)
                self.start_params.change_table_data(param_table)

    def get_data(self):
        """
        Store the current UI configuration into the Fit_Info object.
        """
        self.fit_info.initial_params = self.start_params.update_table_data()

        # Remove any rows with an empty parameter name.
        rows_to_delete = []
        for i, param_name in enumerate(self.fit_info.initial_params["name"]):
            if not param_name:
                rows_to_delete.append(i)
        for i in reversed(rows_to_delete):
            for key in self.fit_info.initial_params:
                self.fit_info.initial_params[key].pop(i)

        self.fit_info.additional_data = self.add_data.update_table_data()
        self.fit_info.do_fit = self.checkBox_fit.isChecked()
        self.fit_info.predef_func = self.comboBox_predef_func.currentText()
        self.fit_info.custom_func = self.lineEdit_custom_func.text()
        self.fit_info.use_custom_func = self.radioButton_custom_func.isChecked()
        self.fit_info.guess_params = self.checkBox_guess.isChecked()
        self.fit_info.display_values = self.checkBox_display_values.isChecked()


def add_fit(table_data, fit):
    """
    Helper function to add the appropriate fit function name into the table data.
    
    Parameters:
        table_data (dict): Dictionary used by an AddRemoveTable (keys include "fit").
        fit (Fit_Info): The fit data object.
    """
    if fit.use_custom_func:
        table_data["fit"].append(fit.custom_func)
    else:
        table_data["fit"].append(fit.predef_func)


def make_table_data(plot_data):
    """
    Build a summary table data dictionary for an overview of plots and their fits.
    
    Parameters:
        plot_data (list of Plot_Info): List of plot configurations.
        
    Returns:
        dict: A dictionary with keys "plot-type", "name", and "fit" for the overview table.
    """
    table_data = {"plot-type": [], "name": [], "fit": []}
    for plt_info in plot_data:
        table_data["plot-type"].append(plt_info.plt_type)
        table_data["name"].append(plt_info.name)
        if plt_info.all_fit and plt_info.all_fit.do_fit and plt_info.same_fit:
            add_fit(table_data, plt_info.all_fit)
        elif plt_info.fits:
            # If multiple fits exist, use the first active one.
            added_fit = False
            for one_fit in plt_info.fits:
                if one_fit.do_fit:
                    add_fit(table_data, one_fit)
                    added_fit = True
                    break
            if not added_fit:
                table_data["fit"].append("None")
        else:
            table_data["fit"].append("None")
    return table_data


class Plot_Button_Overview(QWidget):
    """
    Overview widget displaying a read-only table summarizing plot configurations
    and associated fits, along with a button to open the Plot_Definer dialog.
    """

    def __init__(self, parent, plot_data=None):
        """
        Initialize the overview widget.
        
        Parameters:
            parent (QWidget): The parent widget.
            plot_data (list of Plot_Info, optional): List of plot configurations.
        """
        super().__init__(parent)
        self.plot_data = plot_data or []

        # Build initial table data.
        table_data = make_table_data(self.plot_data)
        columns = ["plot-type", "name", "fit"]

        # Create the overview table (read-only, without add/remove functionality).
        self.plot_table = AddRemoveTable(
            headerLabels=columns,
            title="plot-overview",
            editables=[],
            tableData=table_data,
            askdelete=True,
            horizontal=False,
        )
        # Hide add/remove buttons for the overview table.
        self.plot_table.addButton.setHidden(True)
        self.plot_table.removeButton.setHidden(True)

        # Configure the button to open the Plot_Definer dialog.
        self.plot_button = QPushButton("Configure: Plots/Fits")
        font = QFont()
        font.setBold(True)
        self.plot_button.setFont(font)
        self.plot_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50; /* green */
                border: none;
                color: white;
                padding: 3px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                text-align: center;
                margin: 2px 2px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #2f6331;
            }
            """
        )
        self.plot_button.clicked.connect(self.define_plots)

        # Arrange the button and table in a grid layout.
        layout = QGridLayout()
        layout.addWidget(self.plot_button, 0, 0)
        layout.addWidget(self.plot_table, 1, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def define_plots(self):
        """
        Open the Plot_Definer dialog to edit the plot and fit configurations.
        """
        plot_definer = Plot_Definer(self, self.plot_data)
        if plot_definer.exec():
            # Update the local plot data with changes from the dialog.
            self.plot_data = plot_definer.plot_data
            # Rebuild the overview table to reflect new changes.
            table_data = make_table_data(self.plot_data)
            self.plot_table.change_table_data(table_data)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Overridden to ignore the Enter/Return key to prevent premature dialog closure.
        
        Parameters:
            event (QKeyEvent): The key press event.
        """
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            return
        super().keyPressEvent(event)


def is_module_available(module_name):
    """
    Check if a module is available for import.
    
    Parameters:
        module_name (str): The name of the module.
        
    Returns:
        bool: True if the module can be imported, False otherwise.
    """
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False
    

def check_if_plotly_modules_are_available(self):
    """
    Check for the availability of required modules for browser-based plotting.
    
    If any required modules are missing, prompt the user to install them.
    
    Parameters:
        self: The calling widget instance (used to update UI elements based on the outcome).
    """
    # List of required modules.
    required_modules = ['flask', 'dash', 'plotly']

    # Identify any missing modules.
    missing_modules = [mod for mod in required_modules if not is_module_available(mod)]

    if missing_modules:
        # Construct a message listing missing modules.
        msg = (
            f"The following modules are required: {', '.join(missing_modules)}.\n\n"
            "These modules are fairly large and may take several minutes to install. You only need to do this once.\n"
            "Do you want to install them now?"
        )

        # Ask the user if they wish to install the missing modules.
        reply_update_modules = QMessageBox.question(
            None,
            "Install Required Modules",
            msg,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply_update_modules == QMessageBox.Yes:
            try:
                # First attempt to install nomad-camels[dash] which should cover dependencies.
                try:
                    command = [sys.executable, "-m", "pip", "install", "nomad-camels[dash]"]
                    subprocess.check_call(command)
                    missing_modules = [mod for mod in required_modules if not is_module_available(mod)]
                    if missing_modules:
                        raise Exception("Failed to install nomad-camels[dash]")
                except Exception as e:
                    print(e)
                    # If that fails, install the missing modules individually.
                    command = [sys.executable, "-m", "pip", "install"] + missing_modules
                # Run the pip install command.
                subprocess.check_call(command)
                QMessageBox.information(
                    None,
                    "Installation Complete",
                    "The required modules have been installed.\nYou can now view your plots from a web browser."
                )
            except Exception as e:
                QMessageBox.critical(
                    None,
                    "Installation Failed",
                    f"An error occurred during installation:\n{str(e)}"
                )
                self.checkBox_show_in_browser.setChecked(False)
                self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
        else:
            QMessageBox.warning(
                None,
                "Modules Missing",
                "You cannot display the plots in the browser without the required modules."
            )
            self.checkBox_show_in_browser.setChecked(False)
            self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
