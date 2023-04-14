from PySide6.QtWidgets import QTextEdit
from nomad_camels.utility import variables_handling

import io

import sys


class Error_Writer(io.StringIO):
    def __init__(self, textEdit, use_old_stderr=False):
        super().__init__()
        self.textEdit = textEdit
        self.old_stderr = sys.stderr
        self.use_old_stderr = use_old_stderr

    def write(self, *args, **kwargs):
        text = args[0]
        if self.use_old_stderr:
            self.old_stderr.write(text)
        self.textEdit.setTextColor(variables_handling.get_color('strong_red'))
        self.textEdit.append(text)



class Text_Writer(io.StringIO):
    def __init__(self, textEdit, use_old_stdout=False):
        super().__init__()
        self.textEdit = textEdit
        self.old_stdout = sys.stdout
        self.use_old_stdout = use_old_stdout

    def write(self, *args, **kwargs):
        text = args[0]
        if self.use_old_stdout:
            self.old_stdout.write(text)
        if text == '\n':
            return
        self.textEdit.setTextColor(variables_handling.get_color('black'))
        self.textEdit.append(text)


class Console_TextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        use_old = not sys.executable.endswith('pythonw.exe')
        self.text_writer = Text_Writer(self, use_old)
        self.error_writer = Error_Writer(self, use_old)

