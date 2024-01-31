from PySide6.QtWidgets import QComboBox, QWidget

class ELN_Context:
    def __init__(self, ui):
        self.comboBox_user_type = ui.comboBox_user_type
        self.user_widget = ui.user_widget
        self.sample_widget = ui.sample_widget
        self.session_upload_widget = ui.session_upload_widget
        self.comboBox_user_type = ui.comboBox_user_type
        self.run_done_file_signal = ui.run_done_file_signal
        self.extension_user = ui.extension_user
        self.extension_sample = ui.extension_sample
