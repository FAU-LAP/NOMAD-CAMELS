from PyQt5.QtWidgets import QTextEdit
from utility import variables_handling

import io

class Error_Writer(io.StringIO):
    def __init__(self, textEdit):
        super().__init__()
        self.textEdit = textEdit

    def write(self, *args, **kwargs):
        text = args[0]
        self.textEdit.setTextColor(variables_handling.get_color('strong_red'))
        self.textEdit.append(text)



class Text_Writer(io.StringIO):
    def __init__(self, textEdit):
        super().__init__()
        self.textEdit = textEdit

    def write(self, *args, **kwargs):
        text = args[0]
        if text == '\n':
            return
        self.textEdit.setTextColor(variables_handling.get_color('black'))
        self.textEdit.append(text)


class Console_TextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.text_writer = Text_Writer(self)
        self.error_writer = Error_Writer(self)

