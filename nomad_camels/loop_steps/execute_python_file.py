from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
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
        self.file_path = step_info["file_path"] if "file_path" in step_info else ""
        self.python_exe_path = (
            step_info["python_exe_path"] if "python_exe_path" in step_info else ""
        )

    def get_protocol_string(self, n_tabs=1):
        """
        This function runs the python file with the python exe using the subprocess module.
        The the cwd of the subprocess is changed to the python files location.
        """
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        # use subprocess to run the python file
        protocol_string += f'{tabs}subprocess.run([r"{os.path.abspath(self.python_exe_path)}", r"{os.path.abspath(self.file_path)}"], cwd=r"{os.path.abspath(os.path.dirname(self.file_path))}")\n'
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
        label_python_file_path = QLabel("Python File Path")
        label_python_exe_path = QLabel("Python Executable Path")
        self.path_button_edit_python_file = Path_Button_Edit()
        self.path_button_edit_python_exe = Path_Button_Edit()

        # Adding tooltips to the labels
        label_python_file_path.setToolTip(
            "Specify the path to the Python file to be executed."
        )
        label_python_exe_path.setToolTip(
            "Specify the path to the Python executable (python.exe)."
        )
        # Adding tooltips to the patheditbuttons
        self.path_button_edit_python_file.setToolTip(
            "Specify the path to the Python file to be executed."
        )
        self.path_button_edit_python_exe.setToolTip(
            "Specify the path to the Python executable (python.exe)."
        )

        self.path_button_edit_python_file.set_path(self.loop_step.file_path)
        self.path_button_edit_python_exe.set_path(self.loop_step.python_exe_path)
        self.path_button_edit_python_file.path_changed.connect(self.update_file_path)
        self.path_button_edit_python_exe.path_changed.connect(self.update_exe_path)

        self.layout().addWidget(label_python_file_path, 1, 0)
        self.layout().addWidget(self.path_button_edit_python_file, 1, 1)
        self.layout().addWidget(label_python_exe_path, 2, 0)
        self.layout().addWidget(self.path_button_edit_python_exe, 2, 1)

    def update_exe_path(self, path):
        self.loop_step.python_exe_path = path

    def update_file_path(self, path):
        self.loop_step.file_path = path
