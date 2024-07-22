from PySide6.QtWidgets import (
    QRadioButton,
    QButtonGroup,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
)
from nomad_camels.ui_widgets.add_remove_table import AddRemoveTable
from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config
from nomad_camels.ui_widgets.path_button_edit import Path_Button_Edit
import os
from nomad_camels.utility import variables_handling


class Execute_Python_File(Loop_Step):
    """
    A loop step to execute a python file. The python.exe path as well as the python file path must be given.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "Execute Python File"
        if step_info is None:
            step_info = {}
        # Get the python file path and the python exe path from the step info
        self.file_path = step_info["file_path"] if "file_path" in step_info else ""
        self.python_exe_path = (
            step_info["python_exe_path"] if "python_exe_path" in step_info else ""
        )
        # Get the python packages and versions from the step info
        self.python_packages_versions = (
            step_info["python_packages_versions"]
            if "python_packages_versions" in step_info
            else []
        )
        # Get the radio button selected from the step info
        self.radio_button_selected = (
            step_info["radio_button_selected"]
            if "radio_button_selected" in step_info
            else None
        )

        # Get the python package and version variables and their value from the step info
        self.variables_passing = (
            step_info["variables_passing"] if "variables_passing" in step_info else {}
        )
        # Get the variables returned by the file from the step info
        self.returned_values_variables = (
            step_info["returned_values_variables"]
            if "returned_values_variables" in step_info
            else {}
        )

        self.use_existing_env = (
            step_info["use_existing_env"] if "use_existing_env" in step_info else False
        )
        self.use_specific_packages = (
            step_info["use_specific_packages"]
            if "use_specific_packages" in step_info
            else False
        )
        self.use_camels_python = (
            step_info["use_camels_python"]
            if "use_camels_python" in step_info
            else False
        )

    def get_protocol_string(self, n_tabs=1):
        """
        This function runs the python file with the python exe using the subprocess module.
        The the cwd of the subprocess is changed to the python files location.
        """
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        # use subprocess to run the python file
        if self.variables_passing:
            formatted_strings = []
            variable_names = self.variables_passing["Variable Name"]
            values = self.variables_passing["Value"]
            for i in range(len(variable_names)):
                # Format each "name = value" pair
                if values[i] == "":
                    formatted_string = (
                        f'f\'{variable_names[i]}={{eva.eval("{variable_names[i]}")}}\','
                    )
                else:
                    formatted_string = f"f'{variable_names[i]}={{{values[i]}}}',"
                # Append to the list
                formatted_strings.append(formatted_string)
            # Step 4: Join all formatted strings with a space
            variables_string = " ".join(formatted_strings)
            variables_string = variables_string[:-1]
        else:
            variables_string = ""
        if self.use_existing_env:
            protocol_string = (
                f"{tabs}result_python_file = subprocess.run(['"
                f'r"{os.path.abspath(self.python_exe_path)}", '
                f'r"{os.path.abspath(self.file_path)}", '
                f"{variables_string}], "
                f'cwd=r"{os.path.abspath(os.path.dirname(self.file_path))}", '
                f"capture_output=True, text=True)\n"
                f"{tabs}helper_functions.evaluate_python_file_output(result_python_file.stdout, namespace)\n"
            )

        if self.use_specific_packages:
            protocol_string += (
                f"{tabs}result_python_file = helper_functions.create_venv_run_file_delete_venv({self.python_packages_versions}, "
                f'r"{os.path.abspath(self.file_path)}", '
                f"{variables_string})\n"
                f"{tabs}helper_functions.evaluate_python_file_output(result_python_file.stdout, namespace)\n"
            )

        if self.use_camels_python:
            import sys

            protocol_string += (
                f"{tabs}result_python_file = subprocess.run(["
                f'r"{os.path.abspath(sys.executable)}", '
                f'r"{os.path.abspath(self.file_path)}", '
                f"{variables_string}], "
                f'cwd=r"{os.path.abspath(os.path.dirname(self.file_path))}", '
                f"capture_output=True, text=True)\n"
                f"{tabs}helper_functions.evaluate_python_file_output(result_python_file.stdout, namespace)\n"
            )
        return protocol_string

    def update_variables(self):
        """ """
        # Update the global variables to have access to the variables defined to pass to the python file
        variable_names = self.variables_passing.get("Variable Name", [])
        values = self.variables_passing.get("Value", [])
        # Create a dictionary from the lists
        new_variables = dict(zip(variable_names, values))
        # remove keys and value if the key is already in variables_handling.channels.keys()
        for key in list(new_variables.keys()):
            if key in variables_handling.channels.keys():
                new_variables.pop(key)
        variables_handling.loop_step_variables.update(new_variables)
        # Update the global variables to have access to the varaibles returned by the python file
        if "Variable Name" in self.returned_values_variables:
            for returned_values_variables in self.returned_values_variables[
                "Variable Name"
            ]:
                if returned_values_variables:
                    if (
                        returned_values_variables
                        not in variables_handling.loop_step_variables
                    ):
                        variables_handling.loop_step_variables.update(
                            {returned_values_variables: 0}
                        )


class Execute_Python_File_Config(Loop_Step_Config):
    """The configuration settings for the Execute_Python_File loop step."""

    def __init__(
        self,
        loop_step: Execute_Python_File,
        parent=None,
    ):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step

        # Labels setup
        self.label_python_file_path = QLabel("Python File Path")
        self.label_python_exe_path = QLabel("Python Executable Path")
        self.python_packages_versions_label = QLabel("Python Packages and Versions")
        self.passing_variables_label = QLabel("Variables to pass to the Python file")
        self.read_variables_label = QLabel("Values returned by the Python file.")

        # Path_Button_Edit widgets setup
        self.path_button_edit_python_file = Path_Button_Edit()
        self.path_button_edit_python_exe = Path_Button_Edit()

        # Radio buttons setup
        self.radio_existing_env = QRadioButton("Use existing python environment")
        self.radio_specific_packages = QRadioButton("Use specific packages")
        self.radio_camels_python = QRadioButton("Use CAMELS python")
        # Button group to manage exclusive selection
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.addButton(self.radio_existing_env)
        self.radio_button_group.addButton(self.radio_specific_packages)
        self.radio_button_group.addButton(self.radio_camels_python)
        self.radio_button_group.buttonToggled.connect(self.handle_radio_button_clicked)
        # Layout for radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_camels_python)
        radio_layout.addWidget(self.radio_existing_env)
        radio_layout.addWidget(self.radio_specific_packages)

        # Connect radio button signals
        self.radio_existing_env.toggled.connect(self.toggle_add_remove_table)
        self.radio_specific_packages.toggled.connect(self.toggle_python_exe_path)

        # Horizontal line setup
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)

        # AddRemoveTable widget setup for python packages and their version when selecting the python packages explicitly
        self.add_remove_table_packages = AddRemoveTable(
            headerLabels=["Python Package", "Version"]
        )

        # AddRemoveTable for passing variables to the Python file
        # If no variable is given in the table, it will take the variable values from the running script
        self.add_remove_table_variables_passing = AddRemoveTable(
            headerLabels=["Variable Name", "Value"]
        )

        # AddRemoveTable for reading from the Python file
        # Value is either the index for the returned value if the file returns multiple things or the dictionary key if the file returns a dictionary
        self.add_remove_table_returned_values_variables = (
            AddRemoveTable_Returned_Variables(headerLabels=["Variable Name"])
        )

        # Tooltips
        self.label_python_file_path.setToolTip(
            "Specify the path to the Python file to be executed."
        )
        self.label_python_exe_path.setToolTip(
            "Specify the path to the Python executable (python.exe)."
        )
        self.path_button_edit_python_file.setToolTip(
            "Specify the path to the Python file to be executed."
        )
        self.path_button_edit_python_exe.setToolTip(
            "Specify the path to the Python executable (python.exe)."
        )
        self.radio_existing_env.setToolTip(
            "Run the Python file using the existing Python environment."
        )
        self.radio_specific_packages.setToolTip(
            "Create a virtual environment with specified packages to run the Python file."
        )
        self.radio_camels_python.setToolTip(
            "Run the Python file using the Python environment CAMELS is using."
        )
        self.add_remove_table_packages.setToolTip(
            "Add or remove Python packages and their versions for the virtual environment."
        )
        self.add_remove_table_variables_passing.setToolTip(
            "Specify variables and their values to be passed to the Python file during execution."
        )
        self.add_remove_table_returned_values_variables.setToolTip(
            "The Python file must return a dictionary.\nSpecify the keys of the dictionary that are returned from the Python file after execution."
        )

        # Initial paths setup
        self.path_button_edit_python_file.set_path(self.loop_step.file_path)
        self.path_button_edit_python_exe.set_path(self.loop_step.python_exe_path)
        self.path_button_edit_python_file.path_changed.connect(self.update_file_path)
        self.path_button_edit_python_exe.path_changed.connect(self.update_exe_path)

        # Save changes of the python packages table to the loop step
        self.add_remove_table_packages.table_model.itemChanged.connect(
            self.update_python_packages
        )
        self.add_remove_table_packages.change_table_data(
            self.loop_step.python_packages_versions
        )
        self.add_remove_table_packages.table_model.rowsRemoved.connect(
            self.on_rows_removed_packages
        )
        # Save changes of the variables passing table to the loop step
        self.add_remove_table_variables_passing.table_model.itemChanged.connect(
            self.update_variables_passing
        )
        self.add_remove_table_variables_passing.change_table_data(
            self.loop_step.variables_passing
        )
        self.add_remove_table_variables_passing.table_model.rowsRemoved.connect(
            self.on_rows_removed_passing
        )
        # Save changes of the returned variables table to the loop step
        self.add_remove_table_returned_values_variables.table_model.itemChanged.connect(
            self.update_returned_value_variables
        )
        self.add_remove_table_returned_values_variables.change_table_data(
            self.loop_step.returned_values_variables
        )
        self.add_remove_table_returned_values_variables.table_model.rowsRemoved.connect(
            self.on_rows_removed_returned
        )

        # Layout setup
        layout = self.layout()

        layout.addWidget(self.label_python_file_path, 1, 0)
        layout.addWidget(self.path_button_edit_python_file, 1, 1)

        # Create a widget to hold radio buttons and add it to the main layout
        radio_widget = QWidget()
        radio_widget.setLayout(radio_layout)
        layout.addWidget(radio_widget, 2, 0, 1, 2)

        layout.addWidget(self.label_python_exe_path, 3, 0)
        layout.addWidget(self.path_button_edit_python_exe, 3, 1)
        layout.addWidget(self.python_packages_versions_label, 4, 0, 1, 2)
        layout.addWidget(self.add_remove_table_packages, 5, 0, 1, 2)
        layout.addWidget(h_line, 6, 0, 1, 2)
        layout.addWidget(self.passing_variables_label, 7, 0, 1, 2)
        layout.addWidget(self.add_remove_table_variables_passing, 8, 0, 1, 2)
        layout.addWidget(self.read_variables_label, 9, 0, 1, 2)
        layout.addWidget(self.add_remove_table_returned_values_variables, 10, 0, 1, 2)

        # Set the selected radio button from the loop step
        if self.loop_step.radio_button_selected is not None:
            if (
                self.loop_step.radio_button_selected
                == "Use existing python environment"
            ):
                self.radio_existing_env.setChecked(True)
            elif self.loop_step.radio_button_selected == "Use specific packages":
                self.radio_specific_packages.setChecked(True)
            elif self.loop_step.radio_button_selected == "Use CAMELS python":
                self.radio_camels_python.setChecked(True)
        else:
            self.radio_camels_python.setChecked(True)

    def update_exe_path(self, path):
        self.loop_step.python_exe_path = path

    def update_file_path(self, path):
        self.loop_step.file_path = path

    def update_python_packages(self):
        self.loop_step.python_packages_versions = (
            self.add_remove_table_packages.update_table_data()
        )

    def update_variables_passing(self):
        self.loop_step.variables_passing = (
            self.add_remove_table_variables_passing.update_table_data()
        )

    def update_returned_value_variables(self):

        self.loop_step.returned_values_variables = (
            self.add_remove_table_returned_values_variables.update_table_data()
        )

    def handle_radio_button_clicked(self, button):
        self.loop_step.radio_button_selected = button.text()
        if button == self.radio_existing_env:
            # Handle selection for existing environment
            self.add_remove_table_packages.setVisible(False)
            self.path_button_edit_python_exe.setVisible(True)
            self.label_python_exe_path.setVisible(True)
            self.python_packages_versions_label.setVisible(False)
            self.loop_step.use_existing_env = True
            self.loop_step.use_specific_packages = False
            self.loop_step.use_camels_python = False
        elif button == self.radio_specific_packages:
            # Handle selection for specific packages
            self.add_remove_table_packages.setVisible(True)
            self.path_button_edit_python_exe.setVisible(False)
            self.label_python_exe_path.setVisible(False)
            self.python_packages_versions_label.setVisible(True)
            self.loop_step.use_specific_packages = True
            self.loop_step.use_existing_env = False
            self.loop_step.use_camels_python = False
        elif button == self.radio_camels_python:
            # Handle selection for CAMELS python
            # Hide AddRemoveTable and Python exe path
            self.add_remove_table_packages.setVisible(False)
            self.path_button_edit_python_exe.setVisible(False)
            self.label_python_exe_path.setVisible(False)
            self.python_packages_versions_label.setVisible(False)
            self.loop_step.use_camels_python = True
            self.loop_step.use_specific_packages = False
            self.loop_step.use_existing_env = False

    def toggle_add_remove_table(self, checked):
        if checked:
            self.add_remove_table_packages.setVisible(False)

    def toggle_python_exe_path(self, checked):
        if checked:
            self.path_button_edit_python_exe.setVisible(not checked)
            self.label_python_exe_path.setVisible(not checked)

    def on_rows_removed_returned(self, parent, first, last):
        self.loop_step.returned_values_variables = (
            self.add_remove_table_returned_values_variables.update_table_data()
        )

    def on_rows_removed_passing(self, parent, first, last):
        self.loop_step.variables_passing = (
            self.add_remove_table_variables_passing.update_table_data()
        )

    def on_rows_removed_packages(self, parent, first, last):
        self.loop_step.python_packages_versions = (
            self.add_remove_table_packages.update_table_data()
        )


class AddRemoveTable_Returned_Variables(AddRemoveTable):
    """Subclasses AddRemoveTable and changes the remove method to also remove the variable from the loop step variable dict."""

    def remove(self):
        try:
            index = self.table.selectedIndexes()[0]
        except IndexError:
            raise Exception("You need to select a row first!")
        row = index.row()
        variable_name_to_be_removed = self.tableData["Variable Name"][row]
        variables_handling.loop_step_variables.pop(variable_name_to_be_removed)
        super().remove()
