import copy
import re

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


plot_types = ["X-Y plot", "Value-List", "2D plot"]

# Dictionary of lmfit models, excluding "Expression"
models_names = dict(models.lmfit_models)
models_names.pop("Expression", None)


class Plot_Info:
    """
    Holds all relevant metadata about a single plot configuration, 
    including axes labels, plot type, fit information, and display 
    options such as position, size, and logging.

    Attributes:
        plt_type (str): The type of plot (e.g., "X-Y plot", "Value-List", "2D plot").
        x_axis (str): Variable name or expression for the x-axis.
        y_axes (dict): Contains lists for 'formula' and 'axis' specifying 
            y-axis expressions and whether they go on the left or right axis.
        z_axis (str): Variable name or expression for the z-axis (if applicable).
        title (str): The plot title.
        xlabel (str): The x-axis label.
        ylabel (str): The y-axis label (for the left axis in XY plots).
        ylabel2 (str): The label for the right y-axis in XY plots (if used).
        zlabel (str): The z-axis label in 2D plots.
        do_plot (bool): Whether or not to actually show the plot.
        same_fit (bool): Whether to use the same fit parameters for all y-axes.
        fits (list of Fit_Info): Fit_Info objects for each y-axis.
        all_fit (Fit_Info): A single Fit_Info object if same_fit is used.
        plot_all_available (bool): For Value-List plots, plot all available channels.
        maxlen (int or float): Maximum number of data points to display (default: infinity).
        top_left_x (str/int): The x-coordinate for the plot if placed manually.
        top_left_y (str/int): The y-coordinate for the plot if placed manually.
        plot_width (str/int): The width of the plot (if manually placed).
        plot_height (str/int): The height of the plot (if manually placed).
        checkbox_manual_plot_position (bool): Whether the user opted for manual plotting position.
        checkbox_show_in_browser (bool): Whether the user wants to render the plot in a browser (for interactive dashboards).
        browser_port (int): The port to be used for a browser-based plot.

        name (str): A short name auto-generated from other properties (e.g., "y vs x").
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
        self.plot_all_available = True  # used mainly in Value-List
        self.all_fit = all_fit or Fit_Info()
        self.name = ""
        self.maxlen = np.inf
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.checkbox_manual_plot_position = checkbox_manual_plot_position
        self.checkbox_show_in_browser = checkbox_show_in_browser
        self.browser_port = browser_port

        self.update_name()

    def update_name(self):
        """
        Update the plot's `name` attribute to a short descriptive string 
        based on the current plot type, axis labels, and titles.
        """
        if self.title:
            self.name = self.title
        elif self.plt_type == "X-Y plot":
            # Prefer user-provided labels; otherwise derive from expressions
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
            # For 2D plots, check for user-provided or derived labels
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
            stream (str): An identifier or suffix for the variable names 
                          (e.g., the name of the data stream).

        Returns:
            dict: A dictionary mapping variable names to an initial value (1).
        """
        variables = {}
        if self.same_fit:
            if self.all_fit.do_fit:
                self.all_fit.x = self.x_axis
                for y in self.y_axes["formula"]:
                    fit_copy = copy.deepcopy(self.all_fit)
                    fit_copy.y = y
                    variables.update(fit_copy.get_variables(stream))
        else:
            for fit in self.fits:
                if fit.do_fit:
                    variables.update(fit.get_variables(stream))
        return variables


class Fit_Info:
    """
    Stores all relevant fit settings, including which function to fit 
    (custom or predefined), parameters, and bounds.

    Attributes:
        do_fit (bool): Whether to perform the fit.
        predef_func (str): Name of a predefined lmfit model (e.g., "Gaussian", "Linear").
        custom_func (str): A custom expression to fit if use_custom_func is True.
        use_custom_func (bool): Whether to use a custom function or a predefined one.
        guess_params (bool): Whether to guess parameter values automatically.
        initial_params (dict): Parameter names, initial values, and bounds.
        display_values (bool): Whether to display fit values on the final plot.
        y (str): The expression or channel name for the y-axis.
        x (str): The expression or channel name for the x-axis.
        additional_data (list): Additional data used in the fit (if any).
        name (str): A generated name for the fit.
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
            stream (str): An identifier or suffix (e.g., data stream name).

        Returns:
            str: Generated fit name (e.g., "Gaussian_channelY_v_channelX_stream").
        """
        if self.use_custom_func:
            label = "custom"
        else:
            label = self.predef_func

        self.name = f"{label}_{self.y}_v_{self.x}_{stream}".replace(" ", "_")
        return self.name

    def get_variables(self, stream=""):
        """
        Build a dictionary of parameter names required by this fit 
        (with underscore-separated prefixes).

        Parameters:
            stream (str): An identifier or suffix for parameter names.

        Returns:
            dict: A mapping {param_name: 1} for each parameter in initial_params.
        """
        variables = {}
        fit_name = self.get_name(stream)
        for var in self.initial_params["name"]:
            var_name = f"{fit_name}_{var}"
            # Replace special characters to keep naming consistent
            var_name = replace_name(var_name)
            variables[var_name] = 1
        return variables


class Plot_Definer(QDialog):
    """
    A dialog for defining or editing multiple Plot_Info objects. 

    Displays an Add/Remove table of existing plots and, for the selected
    plot, a child widget for configuring plot-specific options (e.g.,
    X-Y plot specifics, 2D plot specifics, Value-List specifics).
    """

    def __init__(self, parent=None, plot_data=None):
        super().__init__(parent)
        self.plot_data = plot_data or []

        self.setWindowTitle("Define plot - NOMAD CAMELS")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        # The table of plots (each row is a plot)
        columns = ["plot-type", "name"]
        combo_boxes = {"plot-type": plot_types}
        table_data = {"plot-type": [], "name": []}

        # Populate initial table data
        for plt_info in self.plot_data:
            table_data["plot-type"].append(plt_info.plt_type)
            table_data["name"].append(plt_info.name)

        # Create the AddRemoveTable for the list of plots
        self.plot_table = AddRemoveTable(
            headerLabels=columns,
            title="Plots",
            editables=[],
            comboBoxes=combo_boxes,
            tableData=table_data,
            askdelete=True,
        )
        self.plot_table.table.clicked.connect(self.change_plot_def)
        self.plot_table.added.connect(self.plot_added)
        self.plot_table.removed.connect(self.plot_removed)

        # Placeholder widget; replaced when user selects a plot
        self.plot_def = QLabel("Select a plot!")

        # Buttons for "OK" and "Cancel"
        self.dialog_buttons = QDialogButtonBox()
        self.dialog_buttons.setOrientation(Qt.Horizontal)
        self.dialog_buttons.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)

        # Arrange everything in a grid layout
        layout = QGridLayout()
        layout.addWidget(self.plot_table, 0, 0)
        layout.addWidget(self.plot_def, 0, 1)
        layout.addWidget(self.dialog_buttons, 1, 0, 1, 2)
        self.setLayout(layout)

    def accept(self) -> None:
        """
        Overridden accept method to ensure that the last selected 
        plot configuration is saved before closing.
        """
        if not isinstance(self.plot_def, QLabel):
            self.plot_def.get_data()
        super().accept()

    def reject(self):
        """
        Confirm with the user before discarding changes.
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
        Called when the user selects a plot in the table. Replaces 
        the right-hand widget with the correct sub-definer 
        (XY, Value-List, or 2D).

        Parameters:
            index (QModelIndex): The index of the selected row in the table.
        """
        # First save any changes in the currently shown widget
        if not isinstance(self.plot_def, QLabel):
            self.plot_def.get_data()

        # Get the corresponding Plot_Info object
        plot_dat = self.plot_data[index.row()]

        # Update the type in the table data (in case user changed it via combo box)
        type_index = self.plot_table.table_model.index(index.row(), 0)
        plot_dat.plt_type = self.plot_table.table.indexWidget(type_index).currentText()

        # Re-populate the table with updated data
        table_data = {"plot-type": [], "name": []}
        for plt_info in self.plot_data:
            table_data["plot-type"].append(plt_info.plt_type)
            table_data["name"].append(plt_info.name)
        self.plot_table.change_table_data(table_data)

        # Choose the right child widget based on the plot type
        if plot_dat.plt_type == "X-Y plot":
            plot_def = Single_Plot_Definer_XY(plot_dat, self)
        elif plot_dat.plt_type == "Value-List":
            plot_def = Single_Plot_Definer_List(plot_dat, self)
        elif plot_dat.plt_type == "2D plot":
            plot_def = Single_Plot_Definer_2D(plot_dat, self)
        else:
            plot_def = QLabel("Not implemented yet!")

        # Replace the old widget
        self.layout().replaceWidget(self.plot_def, plot_def)
        self.plot_def.deleteLater()
        self.plot_def = plot_def

        # Keep the new row selected
        selection_flag = self.plot_table.table.selectionModel().SelectionFlag.Select
        self.plot_table.table.selectionModel().select(index, selection_flag)

    def plot_added(self, n):
        """
        Called when a new plot row is added in the table.

        Parameters:
            n (int): The index of the newly added row.
        """
        if n >= len(self.plot_data):
            self.plot_data.append(Plot_Info())

    def plot_removed(self, n):
        """
        Called when a plot row is removed from the table.

        Parameters:
            n (int): The index of the removed row.
        """
        self.plot_data.pop(n)


class Single_Plot_Definer(QWidget):
    """
    Base class for a single plot definer widget. Extended by 
    Single_Plot_Definer_XY, Single_Plot_Definer_List, and Single_Plot_Definer_2D.
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(parent)
        self.plot_data = plot_data

    def get_data(self):
        """
        Returns the `Plot_Info` object. Child classes should override 
        this to do additional updates.
        """
        return self.plot_data

    def add_y(self, n):
        """
        Called when a new row (y-axis or formula) is added in the table 
        that displays plot data (like y_axes or fits).

        Parameters:
            n (int): The row index just added.
        """
        if n >= len(self.plot_data.fits):
            self.plot_data.fits.append(Fit_Info())

    def remove_y(self, n):
        """
        Called when a row (y-axis or formula) is removed from the table.

        Parameters:
            n (int): The row index just removed.
        """
        self.plot_data.fits.pop(n)


class Single_Plot_Definer_List(Single_Plot_Definer):
    """
    Widget to configure a "Value-List" type plot. Displays a list of 
    channels/expressions to plot as well as optional position/size overrides.
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(plot_data, parent)

        # Checkbox for plotting all available channels
        self.checkBox_plot_all = QCheckBox("Plot all available channels")
        self.checkBox_plot_all.setChecked(plot_data.plot_all_available)

        # Table to list custom expressions (i.e., if not plotting all)
        self.table = AddRemoveTable(
            title="Values",
            headerLabels=[],
            tableData=plot_data.y_axes["formula"],
            checkstrings=[0],
        )
        self.table.added.connect(self.add_y)
        self.table.removed.connect(self.remove_y)

        # Layout
        layout = QGridLayout()

        # Add widgets
        layout.addWidget(self.checkBox_plot_all, 0, 0, 1, 4)
        layout.addWidget(self.table, 1, 0, 1, 4)

        # Separator line
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line, 3, 0, 1, 4)

        # Manual positioning/size (optional)
        label_top_left_x = QLabel("Top Left X:", self)
        self.lineEdit_top_left_x = QLineEdit(self)
        label_top_left_y = QLabel("Top Left Y:", self)
        self.lineEdit_top_left_y = QLineEdit(self)
        label_plot_width = QLabel("Plot Width:", self)
        self.lineEdit_plot_width = QLineEdit(self)
        label_plot_height = QLabel("Plot Height:", self)
        self.lineEdit_plot_height = QLineEdit(self)

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
        Populate the line edits with existing data from the Plot_Info object.
        """
        # If any of these attributes are set, convert to string
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
        Validate and retrieve all data for the Value-List plot from the UI elements.

        Returns:
            Plot_Info: The updated plot configuration.
        """
        self.plot_data.plot_all_available = self.checkBox_plot_all.isChecked()
        self.plot_data.y_axes["formula"] = self.table.update_table_data()
        self.plot_data.y_axes["axis"] = [1] * len(self.plot_data.y_axes["formula"])

        # Parse and store manual position/size if provided
        # top_left_x
        if self.lineEdit_top_left_x.text():
            try:
                self.plot_data.top_left_x = max(int(self.lineEdit_top_left_x.text()), 0)
            except ValueError:
                self.plot_data.top_left_x = ""
        else:
            self.plot_data.top_left_x = ""

        # top_left_y
        if self.lineEdit_top_left_y.text():
            try:
                self.plot_data.top_left_y = max(int(self.lineEdit_top_left_y.text()), 0)
            except ValueError:
                self.plot_data.top_left_y = ""
        else:
            self.plot_data.top_left_y = ""

        # plot_width
        if self.lineEdit_plot_width.text():
            try:
                self.plot_data.plot_width = max(int(self.lineEdit_plot_width.text()), 430)
            except ValueError:
                self.plot_data.plot_width = ""
        else:
            self.plot_data.plot_width = ""

        # plot_height
        if self.lineEdit_plot_height.text():
            try:
                self.plot_data.plot_height = max(int(self.lineEdit_plot_height.text()), 126)
            except ValueError:
                self.plot_data.plot_height = ""
        else:
            self.plot_data.plot_height = ""

        # Check for partial definitions of position or size
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set, but x position is.")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set, but y position is.")
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set, but width is.")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set, but height is.")

        self.plot_data.update_name()
        return super().get_data()


class Single_Plot_Definer_2D(Ui_Plot_Definer_2D, Single_Plot_Definer):
    """
    Widget to configure a "2D plot". This is driven by the Qt Designer 
    form `plot_definer_2d.ui` compiled into `Ui_Plot_Definer_2D`.
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(plot_data, parent)
        self.setupUi(self)

        # Pre-fill UI elements
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

        # Connect checkboxes that show/hide manual positioning and browser port
        self.checkBox_manual_plot_position_2d.stateChanged.connect(self.hide_show_manual_position)
        self.checkBox_show_in_browser.stateChanged.connect(self.hide_show_show_in_browser)
        self.checkBox_show_in_browser.clicked.connect(self.hide_show_show_in_browser)

    def load_data(self):
        """
        Populate manual position, size, and browser rendering UI 
        with the existing Plot_Info data.
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

        if hasattr(self.plot_data, "browser_port") and self.plot_data.browser_port:
            try:
                port_val = int(self.plot_data.browser_port)
            except ValueError:
                port_val = 8050
            self.spinBox_port.setValue(port_val)
        else:
            self.spinBox_port.setValue(8050)

        # Ensure the UI matches the current checkbox states
        self.hide_show_manual_position()
        self.hide_show_show_in_browser()

    def get_data(self):
        """
        Validate and retrieve all data from the UI elements for a 2D plot.

        Returns:
            Plot_Info: The updated plot configuration.
        """
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

        # Parse and store manual position/size if provided
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

        # Check for partial definitions of position or size
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set, but x position is.")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set, but y position is.")
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set, but width is.")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set, but height is.")

        # Save checkbox states
        self.plot_data.checkbox_manual_plot_position = (
            self.checkBox_manual_plot_position_2d.isChecked()
        )
        self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
        self.plot_data.browser_port = self.spinBox_port.value()

        self.plot_data.update_name()
        return super().get_data()

    def hide_show_manual_position(self):
        """
        Show or hide manual positioning fields (top-left x/y, plot width/height) 
        based on the checkbox_manual_plot_position checkbox state.
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
        Show or hide the browser port selection based on 
        the checkbox_show_in_browser state. 
        Executed when the state is changed or if the checkbox is clicked.
        """
        is_checked = self.checkBox_show_in_browser.isChecked()
        self.label_port.setHidden(not is_checked)
        self.spinBox_port.setHidden(not is_checked)
        if is_checked:
            check_if_plotly_modules_are_available(self)

    
                    


class Single_Plot_Definer_XY(Ui_Plot_Definer, Single_Plot_Definer):
    """
    Widget to configure a classic "X-Y plot". This is driven by the 
    Qt Designer form `plot_definer.ui` compiled into `Ui_Plot_Definer`.
    """

    def __init__(self, plot_data: Plot_Info, parent=None):
        super().__init__(plot_data, parent)
        self.fit_definer = None
        self.setupUi(self)

        # Set up a table for y-axes
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

        # "Use the same fit for all y-axes" checkbox
        self.checkBox_same_fit.clicked.connect(self.fit_change)

        # Replace placeholder with y_table
        self.layout().replaceWidget(self.y_axes, self.y_table)

        # Populate initial values
        self.load_data()
        self.fit_change()

        # Connect checkboxes that show/hide manual positioning and browser port
        self.checkBox_manual_plot_position.stateChanged.connect(self.hide_show_manual_position)
        self.checkBox_show_in_browser.stateChanged.connect(self.hide_show_show_in_browser)
        self.checkBox_show_in_browser.clicked.connect(self.hide_show_show_in_browser)

    def load_data(self):
        """
        Populate all fields from the Plot_Info object.
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

        # Manual position/size fields
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

        # Browser port
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
        Validate and retrieve all data for an X-Y plot from the UI elements.

        Returns:
            Plot_Info: The updated plot configuration.
        """
        # Update the y-axes info
        self.plot_data.y_axes = self.y_table.update_table_data()
        self.plot_data.x_axis = self.lineEdit_x_axis.text()
        self.plot_data.title = self.lineEdit_title.text()

        # Validate strings for special characters
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

        # Parse max data points
        try:
            self.plot_data.maxlen = int(self.lineEdit_nPoints.text())
        except ValueError:
            self.plot_data.maxlen = np.inf

        self.plot_data.same_fit = self.checkBox_same_fit.isChecked()
        self.plot_data.logX = self.checkBox_xlog.isChecked()
        self.plot_data.logY = self.checkBox_ylog.isChecked()
        self.plot_data.logY2 = self.checkBox_ylog2.isChecked()

        # Manual position/size
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

        # Check for partial definitions of position or size
        if self.lineEdit_top_left_x.text() and not self.lineEdit_top_left_y.text():
            raise ValueError("Plot y position is not set, but x position is.")
        if self.lineEdit_top_left_y.text() and not self.lineEdit_top_left_x.text():
            raise ValueError("Plot x position is not set, but y position is.")
        if self.lineEdit_plot_width.text() and not self.lineEdit_plot_height.text():
            raise ValueError("Plot height is not set, but width is.")
        if self.lineEdit_plot_height.text() and not self.lineEdit_plot_width.text():
            raise ValueError("Plot width is not set, but height is.")

        self.plot_data.checkbox_manual_plot_position = self.checkBox_manual_plot_position.isChecked()
        self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()
        self.plot_data.browser_port = self.spinBox_port.value()

        # Retrieve any changes in the embedded fit definer
        if not isinstance(self.fit_definer, QLabel):
            self.fit_definer.get_data()

        self.plot_data.update_name()

        # Update the fit x/y references
        if self.plot_data.all_fit:
            self.plot_data.all_fit.x = self.plot_data.x_axis
        for i, fit in enumerate(self.plot_data.fits):
            # Each fit should correspond to a y-axis
            fit.y = self.plot_data.y_axes["formula"][i]
            fit.x = self.plot_data.x_axis

        return super().get_data()

    def hide_show_manual_position(self):
        """
        Show or hide manual positioning fields (top-left x/y, plot width/height) 
        based on the checkbox_manual_plot_position state.
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
        Show or hide the browser port spinbox based on 
        the checkbox_show_in_browser state.
        """
        is_checked = self.checkBox_show_in_browser.isChecked()
        self.label_port.setHidden(not is_checked)
        self.spinBox_port.setHidden(not is_checked)
        if is_checked:
            check_if_plotly_modules_are_available(self)

    def fit_change(self):
        """
        Switch the fit-defining widget to either a single, shared 
        Fit_Definer (if same_fit is checked) or a Fit_Definer for the 
        currently selected y-axis row in the table.
        """
        # Save current fit settings if the old widget is active
        if not isinstance(self.fit_definer, QLabel):
            self.fit_definer.get_data()

        if self.checkBox_same_fit.isChecked():
            fit_dat = self.plot_data.all_fit
            fit_to = "all y-axes"
        else:
            # If not using the same fit, get the row selected in y_table
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

        self.layout().replaceWidget(self.fit_definer, fit_definer)
        self.fit_definer.deleteLater()
        self.fit_definer = fit_definer


class Fit_Definer(Ui_Fit_Definer, QWidget):
    """
    Widget for configuring a Fit_Info object (choosing a predefined or 
    custom function, setting initial parameters, bounds, etc.). 
    Driven by the Qt Designer form `fit_definer.ui`.
    """

    def __init__(self, fit_info: Fit_Info, parent=None, fit_to=""):
        super().__init__(parent)
        self.setupUi(self)
        self.fit_info = fit_info

        # Show which y-axis or data is being fit
        self.label.setText(f"Fit to: {fit_to}")

        # Populate the combo box with known models
        self.comboBox_predef_func.addItems(sorted(models_names.keys()))

        # Table for initial fit parameters
        cols = ["name", "initial value", "lower bound", "upper bound"]
        self.start_params = AddRemoveTable(
            headerLabels=cols,
            title="Fit Parameters",
            editables=[1, 2, 3],
            tableData=fit_info.initial_params,
        )
        # Table for additional data
        self.add_data = AddRemoveTable(
            headerLabels=[],
            title="Additional Data",
            tableData=fit_info.additional_data,
        )

        # We hide the add/remove parameter buttons unless user 
        # picks a custom function that might have arbitrary params
        self.start_params.addButton.setHidden(True)
        self.start_params.removeButton.setHidden(True)

        # Load the Fit_Info object into the UI
        self.load_data()

        # Connect signals to re-check the user choices
        self.checkBox_fit.clicked.connect(self.change_func)
        self.radioButton_custom_func.clicked.connect(self.change_func)
        self.radioButton_predef_func.clicked.connect(self.change_func)
        self.checkBox_guess.clicked.connect(self.change_func)
        self.comboBox_predef_func.currentTextChanged.connect(self.change_func)
        self.lineEdit_custom_func.textChanged.connect(self.change_func)

        # Lay out the parameter and additional-data tables
        self.layout().addWidget(self.start_params, 10, 0, 1, 2)
        self.layout().addWidget(self.add_data, 0, 3, 11, 2)

        # Initial invocation to ensure UI is set
        self.change_func()

    def load_data(self):
        """
        Load the Fit_Info object into the UI elements.
        """
        self.checkBox_fit.setChecked(self.fit_info.do_fit)
        self.comboBox_predef_func.setCurrentText(self.fit_info.predef_func)
        self.lineEdit_custom_func.setText(self.fit_info.custom_func)
        self.radioButton_custom_func.setChecked(self.fit_info.use_custom_func)
        self.checkBox_guess.setChecked(self.fit_info.guess_params)
        self.checkBox_display_values.setChecked(self.fit_info.display_values)

    def change_func(self):
        """
        Enable or disable various fields depending on the user's choice 
        of "fit", "custom function", and "guess parameters."
        """
        fit_enabled = self.checkBox_fit.isChecked()
        custom_func_enabled = self.radioButton_custom_func.isChecked()
        guess_enabled = self.checkBox_guess.isChecked()

        # Enable/disable radio buttons and input fields
        self.radioButton_custom_func.setEnabled(fit_enabled)
        self.radioButton_predef_func.setEnabled(fit_enabled)
        self.checkBox_guess.setEnabled(fit_enabled)
        self.comboBox_predef_func.setEnabled(fit_enabled and not custom_func_enabled)
        self.lineEdit_custom_func.setEnabled(fit_enabled and custom_func_enabled)

        # By default, we disable manual param editing if guess is used
        self.start_params.enableds = [0, 2, 3]
        self.start_params.editables = [2, 3]
        self.start_params.addButton.setHidden(not custom_func_enabled)
        self.start_params.removeButton.setHidden(not custom_func_enabled)

        # If using custom func and not guessing, we can also edit initial values
        if custom_func_enabled:
            self.start_params.editables.append(0)
        if not guess_enabled:
            self.start_params.editables.append(1)
            self.start_params.enableds.append(1)

        # Refresh the table with updated editable columns
        current_params = self.start_params.update_table_data()
        self.start_params.change_table_data(current_params)

        # If the user switched the predefined function, reset the parameter list
        func_name = self.comboBox_predef_func.currentText()
        if func_name != self.fit_info.predef_func:
            if custom_func_enabled:
                # For custom expressions, try to parse it (this might fail if invalid syntax)
                try:
                    expression_model = models.ExpressionModel(self.lineEdit_custom_func.text())
                    params = expression_model.param_names
                    self.lineEdit_custom_func.setStyleSheet(
                        f"background-color: rgb{variables_handling.get_color('green', True)}"
                    )
                except (ValueError, SyntaxError):
                    self.lineEdit_custom_func.setStyleSheet(
                        f"background-color: rgb{variables_handling.get_color('red', True)}"
                    )
                    return
            else:
                # If using a predefined model, instantiate and read its param_names
                predefined_model = models_names[func_name]()
                params = predefined_model.param_names

            # Rebuild param list
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
            self.start_params.change_table_data(new_param_table)
            self.fit_info.predef_func = func_name

        # Special case: If user just selected "Linear" (or any) and 
        # the table is empty, ensure we populate default param set
        if fit_enabled and not custom_func_enabled and func_name == "Linear":
            current_params = self.start_params.update_table_data()
            if not current_params["name"]:
                linear_model = models_names[func_name]()
                params = linear_model.param_names
                param_table = {
                    "name": [],
                    "initial value": [],
                    "lower bound": [],
                    "upper bound": [],
                }
                for param_name in params:
                    param_table["name"].append(param_name)
                    param_table["initial value"].append(1)
                    param_table["lower bound"].append("")
                    param_table["upper bound"].append("")
                self.start_params.change_table_data(param_table)

    def get_data(self):
        """
        Store the final user configuration into the Fit_Info object 
        (parameters, function choice, etc.).
        """
        self.fit_info.initial_params = self.start_params.update_table_data()

        # Remove any rows that have an empty parameter 'name'
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
    Helper function to insert the appropriate fit function name 
    (custom expression or predefined name) into table_data["fit"].

    Parameters:
        table_data (dict): The dictionary used by an AddRemoveTable object 
                           with keys like "plot-type", "name", and "fit".
        fit (Fit_Info): The fit data to be appended to the "fit" column.
    """
    if fit.use_custom_func:
        table_data["fit"].append(fit.custom_func)
    else:
        table_data["fit"].append(fit.predef_func)


def make_table_data(plot_data):
    """
    Build a table-data dictionary for a quick overview of the plots and 
    their fits, used by Plot_Button_Overview.

    Parameters:
        plot_data (list of Plot_Info): List of Plot_Info objects.

    Returns:
        dict: A dict with keys ["plot-type", "name", "fit"], each a list 
              to show in the overview table.
    """
    table_data = {"plot-type": [], "name": [], "fit": []}
    for plt_info in plot_data:
        table_data["plot-type"].append(plt_info.plt_type)
        table_data["name"].append(plt_info.name)
        if plt_info.all_fit and plt_info.all_fit.do_fit and plt_info.same_fit:
            add_fit(table_data, plt_info.all_fit)
        elif plt_info.fits:
            # If multiple fits exist, show the first one that is active
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
    A small overview widget that shows an AddRemoveTable (read-only) 
    summarizing the plot types, plot names, and the associated fit. 
    Also provides a single button to open the Plot_Definer dialog 
    for editing those plots.
    """

    def __init__(self, parent, plot_data=None):
        super().__init__(parent)
        self.plot_data = plot_data or []

        # Build initial table data
        table_data = make_table_data(self.plot_data)
        columns = ["plot-type", "name", "fit"]

        # Create overview table (read-only, no add/remove)
        self.plot_table = AddRemoveTable(
            headerLabels=columns,
            title="plot-overview",
            editables=[],
            tableData=table_data,
            askdelete=True,
            horizontal=False,
        )
        # Hide add/remove buttons since this is only an overview
        self.plot_table.addButton.setHidden(True)
        self.plot_table.removeButton.setHidden(True)

        # Configure button to open Plot_Definer
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

        # Layout
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
            # Update local plot data with possible changes
            self.plot_data = plot_definer.plot_data
            # Rebuild table data to reflect new changes
            table_data = make_table_data(self.plot_data)
            self.plot_table.change_table_data(table_data)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Overridden to ignore the Enter/Return key, preventing the 
        dialog from closing prematurely when embedded in a context 
        that might intercept these keys.

        Parameters:
            event (QKeyEvent): The key press event.
        """
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            return
        super().keyPressEvent(event)

def is_module_available(module_name):
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False
    
def check_if_plotly_modules_are_available(self):
    # Function to check if a module is available.
    # List the required modules.
    required_modules = ['flask', 'dash', 'plotly']

    # Determine which modules are missing.
    missing_modules = [mod for mod in required_modules if not is_module_available(mod)]

    if missing_modules:
        # Create the message to warn the user.
        msg = (
            f"The following modules are required: {', '.join(missing_modules)}.\n\n"
            "These modules are fairly large and may take several minutes to install. You only need to do this once.\n"
            "Do you want to install them now?"
        )

        # Show a question message box.
        reply_update_modules = QMessageBox.question(
            None,
            "Install Required Modules",
            msg,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply_update_modules == QMessageBox.Yes:
            try:
                import sys
                import subprocess
                # Build the pip install command.
                try:
                    command = [sys.executable, "-m", "pip", "install", "nomad-camels[plotly]"]
                    missing_modules = [mod for mod in required_modules if not is_module_available(mod)]
                    if missing_modules:
                        raise Exception("Failed to install nomad-camels[plotly]")

                except Exception as e:
                    print(e)
                    command = [sys.executable, "-m", "pip", "install"] + missing_modules
                # Optionally, you might show another popup or a console message indicating progress.
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
            # Exit the application (or you could try to continue, if that makes sense in your context).
        else:
            QMessageBox.warning(
                None,
                "Modules Missing",
                "You can not display the plots in the browser without the required modules."
            )
            self.checkBox_show_in_browser.setChecked(False)
            self.plot_data.checkbox_show_in_browser = self.checkBox_show_in_browser.isChecked()