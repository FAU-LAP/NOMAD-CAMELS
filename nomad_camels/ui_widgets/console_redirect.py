from PySide6.QtWidgets import QTextEdit, QWidget
from PySide6.QtCore import Signal
from PySide6.QtGui import QTextCursor
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

    def __init__(self, parent, max_lines=10000):
        super().__init__(parent)
        use_old = not sys.executable.endswith("pythonw.exe")
        self.text_handler = TextSignalHanlder()
        self.text_handler.write_output_signal.connect(self.write_output)
        self.text_handler.write_error_signal.connect(self.write_error)
        self.text_writer = Text_Writer(self.text_handler, use_old)
        self.error_writer = Error_Writer(self.text_handler, use_old)
        self.max_lines = max_lines

    def write_error(self, text):
        self.setTextColor(variables_handling.get_color("strong_red"))
        self.append(text)

    def write_output(self, text):
        self.setTextColor(variables_handling.get_color("black"))
        self.append(text)

    def append(self, text):
        """Ensure the number of lines does not exceed `self.max_lines`."""
        super().append(text)
        document = self.document()
        line_count = document.blockCount()

        # Remove excess lines from the beginning
        if line_count > self.max_lines:
            cursor = QTextCursor(document)
            cursor.movePosition(
                QTextCursor.Start
            )  # Move cursor to the start of the document
            for _ in range(line_count - self.max_lines):
                cursor.select(QTextCursor.BlockUnderCursor)  # Select the first block
                cursor.removeSelectedText()  # Remove the selected text
                cursor.deleteChar()  # Remove the newline character
