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

        self.python_packages_versions = (
            step_info["python_packages_versions"]
            if "python_packages_versions" in step_info
            else []
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
        if self.use_existing_env:
            protocol_string += f'{tabs}subprocess.run([r"{os.path.abspath(self.python_exe_path)}", r"{os.path.abspath(self.file_path)}"], cwd=r"{os.path.abspath(os.path.dirname(self.file_path))}")\n'

        if self.use_specific_packages:
            protocol_string += f'{tabs}helper_functions.create_venv_run_file_delete_venv({self.python_packages_versions}, r"{os.path.abspath(self.file_path)}")\n'

        if self.use_camels_python:
            import sys
            protocol_string += f'{tabs}subprocess.run([r"{os.path.abspath(sys.executable)}", r"{os.path.abspath(self.file_path)}"], cwd=r"{os.path.abspath(os.path.dirname(self.file_path))}")\n'
        return protocol_string


class Execute_Python_File_Config(Loop_Step_Config):
    """The configuration settings for the Execute_Python_File loop step."""

    def __init__(
        self,
        loop_step: Execute_Python_File,
        parent=None,
    ):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step

        # Labels and path buttons setup
        self.label_python_file_path = QLabel("Python File Path")
        self.label_python_exe_path = QLabel("Python Executable Path")
        self.path_button_edit_python_file = Path_Button_Edit()
        self.path_button_edit_python_exe = Path_Button_Edit()
        self.python_packages_versions_label = QLabel("Python Packages and Versions")

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

        # Initial paths setup
        self.path_button_edit_python_file.set_path(self.loop_step.file_path)
        self.path_button_edit_python_exe.set_path(self.loop_step.python_exe_path)
        self.path_button_edit_python_file.path_changed.connect(self.update_file_path)
        self.path_button_edit_python_exe.path_changed.connect(self.update_exe_path)

        # AddRemoveTable widget setup
        self.add_remove_table_packages = AddRemoveTable(
            headerLabels=["Python Package", "Version"]
        )
        # Save changes of the table to the loop step
        self.add_remove_table_packages.table_model.itemChanged.connect(
            self.update_python_packages
        )
        self.add_remove_table_packages.change_table_data(
            self.loop_step.python_packages_versions
        )

        # Layout setup
        layout = self.layout()

        layout.addWidget(self.label_python_file_path, 1, 0)
        layout.addWidget(self.path_button_edit_python_file, 1, 1)
        layout.addWidget(self.label_python_exe_path, 3, 0)
        layout.addWidget(self.path_button_edit_python_exe, 3, 1)
        layout.addWidget(self.python_packages_versions_label, 4, 0, 1, 2)
        layout.addWidget(self.add_remove_table_packages, 5, 0, 1, 2)

        # Horizontal line setup
        h_line = QFrame()
        h_line.setFrameShape(QFrame.HLine)
        h_line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(h_line, 6, 0, 1, 2)

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

        # Layout for radio buttons
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.radio_existing_env)
        radio_layout.addWidget(self.radio_specific_packages)
        radio_layout.addWidget(self.radio_camels_python)

        # Create a widget to hold radio buttons and add it to the main layout
        radio_widget = QWidget()
        radio_widget.setLayout(radio_layout)
        layout.addWidget(radio_widget, 2, 0, 1, 2)

        # Connect radio button signals
        self.radio_existing_env.toggled.connect(self.toggle_add_remove_table)
        self.radio_specific_packages.toggled.connect(self.toggle_python_exe_path)

    def update_exe_path(self, path):
        self.loop_step.python_exe_path = path

    def update_file_path(self, path):
        self.loop_step.file_path = path

    def update_python_packages(self):
        self.loop_step.python_packages_versions = (
            self.add_remove_table_packages.update_table_data()
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
