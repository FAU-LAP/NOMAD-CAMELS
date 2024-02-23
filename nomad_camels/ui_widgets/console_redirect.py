from PySide6.QtWidgets import QTextEdit, QWidget
from PySide6.QtCore import Signal
from nomad_camels.utility import variables_handling

import io

import sys


class Error_Writer(io.StringIO):
    """ """

    def __init__(self, text_signal_handler, use_old_stderr=False):
        super().__init__()
        self.text_signal_handler = text_signal_handler
        self.old_stderr = sys.stderr
        self.use_old_stderr = use_old_stderr

    def write(self, *args, **kwargs):
        """

        Parameters
        ----------
        *args :

        **kwargs :


        Returns
        -------

        """
        text = args[0]
        if self.use_old_stderr:
            self.old_stderr.write(text)
        self.text_signal_handler.write_error_signal.emit(text)


class Text_Writer(io.StringIO):
    """ """

    def __init__(self, text_signal_handler, use_old_stdout=False):
        super().__init__()
        self.text_signal_handler = text_signal_handler
        self.old_stdout = sys.stdout
        self.use_old_stdout = use_old_stdout

    def write(self, *args, **kwargs):
        """

        Parameters
        ----------
        *args :

        **kwargs :


        Returns
        -------

        """
        text = args[0]
        if self.use_old_stdout:
            self.old_stdout.write(text)
        if text == "\n":
            return
        self.text_signal_handler.write_output_signal.emit(text)


class TextSignalHanlder(QWidget):
    write_error_signal = Signal(str)
    write_output_signal = Signal(str)


class Console_TextEdit(QTextEdit):
    """ """

    def __init__(self, parent):
        super().__init__(parent)
        use_old = not sys.executable.endswith("pythonw.exe")
        self.text_handler = TextSignalHanlder()
        self.text_handler.write_output_signal.connect(self.write_output)
        self.text_handler.write_error_signal.connect(self.write_error)
        self.text_writer = Text_Writer(self.text_handler, use_old)
        self.error_writer = Error_Writer(self.text_handler, use_old)

    def write_error(self, text):
        self.setTextColor(variables_handling.get_color("strong_red"))
        self.append(text)

    def write_output(self, text):
        self.setTextColor(variables_handling.get_color("black"))
        self.append(text)
