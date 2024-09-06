from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QTextEdit,
)
from PySide6.QtCore import Qt, Signal
from nomad_camels.main_classes.loop_step import Loop_Step, Loop_Step_Config
import os
import json
import requests


class API_Call(Loop_Step):
    """
    A loop step that makes an API call.
    You can perform a CAMELS API call with more sophisticated control and better handling.
    Or you can perform an arbitrary API call.
    You always need to specify the host (ip address) and the port of the web server supplying the API.
    """

    def __init__(self, name="", parent_step=None, step_info=None, **kwargs):
        super().__init__(name, parent_step, step_info, **kwargs)
        self.step_type = "API Call"
        self.selected_camels_function_index = None
        if step_info is None:
            step_info = {}

        # Extract information from the step_info dictionary
        self.camels_function_parameters = step_info.get(
            "camels_function_parameters", None
        )
        # Get the host address
        self.host = step_info["host"] if "host" in step_info else ""
        # Get the port
        self.port = step_info["port"] if "port" in step_info else ""
        self.api_url = step_info["api_url"] if "api_url" in step_info else ""
        self.generic_api_method = (
            step_info["generic_api_method"]
            if "generic_api_method" in step_info
            else "GET"
        )
        self.api_type = step_info["api_type"] if "api_type" in step_info else "CAMELS"
        self.message_body = (
            step_info["message_body"] if "message_body" in step_info else ""
        )
        self.authentication_type = (
            step_info["authentication_type"]
            if "authentication_type" in step_info
            else ""
        )
        self.authentication_string = (
            step_info["authentication_string"]
            if "authentication_string" in step_info
            else ""
        )
        self.selected_camels_function_index = step_info.get(
            "selected_camels_function_index", 0
        )
        if self.selected_camels_function_index == 'None':
            self.selected_camels_function_index = None
        self.camels_function_parameters = step_info.get(
            "camels_function_parameters", None
        )
        self.protocol_step_name = step_info.get("name", None)

    def get_protocol_string(self, n_tabs=1):
        """
        This function executes the API call and returns the results.
        """
        tabs = "\t" * n_tabs
        protocol_string = super().get_protocol_string(n_tabs)
        if self.api_type == "CAMELS":
            protocol_string += f"{tabs}message_body = helper_functions.evaluate_message_body({self.message_body}, eva)\n"
            protocol_string += (
                f"{tabs}api_result = helper_functions.execute_camels_api_call("
            )
            protocol_string += f"host='{self.host}', port={self.port}, api_type='{self.api_type}', message_body=message_body, authentication_type='{self.authentication_type}', authentication_string='{self.authentication_string}', selected_camels_function_index={self.selected_camels_function_index}, camels_function_parameters={self.camels_function_parameters}"
            protocol_string += ")\n"
            protocol_string += f"{tabs}helper_functions.save_API_response_to_variable(api_result, namespace, protocol_step_name='{self.protocol_step_name}')\n"
        elif self.api_type == "Generic":
            protocol_string += (
                f"{tabs}api_result = helper_functions.execute_generic_api_call("
            )
            protocol_string += f"host='{self.host}', port={self.port}, api_type='{self.api_type}', api_url='{self.api_url}', http_method='{self.generic_api_method}', message_body={self.message_body}, authentication_type='{self.authentication_type}', authentication_string='{self.authentication_string}'"
            protocol_string += ")\n"
            protocol_string += f"{tabs}helper_functions.save_API_response_to_variable(api_result, namespace, protocol_step_name='{self.protocol_step_name}')\n"

        return protocol_string


class API_Call_Config(Loop_Step_Config):
    """
    A class to configure the API Call loop step.
    """

    def __init__(
        self,
        loop_step: API_Call,
        parent=None,
    ):
        super().__init__(parent, loop_step)
        self.loop_step = loop_step
        self.api_functions_list = {}

        # Label setup
        self.label_host = QLabel("Host:")
        self.label_port = QLabel("Port:")
        self.label_api_type = QLabel("API Type:")
        self.label_message_body = QLabel("Message Body:")
        self.label_authentication_type = QLabel("Authentication Type:")
        self.label_authentication_string = QLabel("Authentication:")
        self.label_camels_api_functions = QLabel("CAMELS API Functions:")
        self.label_api_url = QLabel("API URL:")
        self.label_generic_api_method = QLabel("HTTP Method:")

        # Create combobox for API type
        self.combobox_camels_api_functions = None
        self.combobox_api_type = QComboBox()
        self.combobox_api_type.addItem("CAMELS")
        self.combobox_api_type.addItem("Generic")
        self.combobox_api_type.currentIndexChanged.connect(self.api_type_changed)

        # Create combobox for HTTP method
        self.combobox_generic_api_method = QComboBox()
        self.combobox_generic_api_method.addItem("GET")
        self.combobox_generic_api_method.addItem("POST")
        self.combobox_generic_api_method.addItem("DELETE")
        self.combobox_generic_api_method.addItem("PATCH")
        self.combobox_generic_api_method.addItem("PUT")
        self.combobox_generic_api_method.currentIndexChanged.connect(
            self.update_generic_api_method
        )

        # Line edit for API URL
        self.line_edit_api_url = QLineEdit()
        self.line_edit_api_url.setText(self.loop_step.api_url)
        self.line_edit_api_url.textChanged.connect(self.update_api_url)

        # Line edit host
        self.line_edit_host = QLineEdit()
        self.line_edit_host.setText(self.loop_step.host)
        self.line_edit_host.textChanged.connect(self.update_host)
        # Line edit port
        self.line_edit_port = QLineEdit()
        self.line_edit_port.setText(self.loop_step.port)
        self.line_edit_port.textChanged.connect(self.update_port)
        # Text edit post body
        self.text_edit_message_body = QTextEdit()
        self.text_edit_message_body.setText(self.loop_step.message_body)
        self.text_edit_message_body.textChanged.connect(self.update_message_body)

        # Combobox for authentication type
        self.combobox_authentication_type = QComboBox()
        self.combobox_authentication_type.addItem("None")
        self.combobox_authentication_type.addItem("HTTP Basic")
        self.combobox_authentication_type.addItem("Bearer Token")
        self.combobox_authentication_type.setCurrentText(
            self.loop_step.authentication_type
        )
        self.combobox_authentication_type.currentIndexChanged.connect(
            self.authentication_type_changed
        )
        # Add tooltips to the combobox items
        self.combobox_authentication_type.setItemData(
            0, "No authentication required", Qt.ToolTipRole
        )
        self.combobox_authentication_type.setItemData(
            1, "Use format: username:password", Qt.ToolTipRole
        )
        self.combobox_authentication_type.setItemData(
            2, "Use format: Token", Qt.ToolTipRole
        )
        # Line edit authentication string
        self.line_edit_authentication_string = QLineEdit()
        self.line_edit_authentication_string.textChanged.connect(
            self.update_authentication_string
        )
        self.line_edit_authentication_string.setToolTip(
            "For HTTP Basic Authentication, use the format: username:password.\nFor Bearer Token Authentication, use the format: Token."
        )
        self.line_edit_authentication_string.setText(
            self.loop_step.authentication_string
        )

        # Combobox for CAMELS API functions
        self.CAMELS_functions_layout = QGridLayout()
        self.combobox_camels_api_functions = Combobox_CAMELS_functions()
        # Update the available CAMELS API functions when clicking on the combobox
        self.combobox_camels_api_functions.popupAboutToBeShown.connect(
            self.extract_all_api_functionality_from_json
        )
        self.combobox_camels_api_functions.currentIndexChanged.connect(
            self.update_camels_function_parameters
        )
        # Load the latest CAMELS function selection from the last time the protocol was closed
        if self.loop_step.selected_camels_function_index is not None:
            self.load_camels_function_on_bootup(
                self.loop_step.selected_camels_function_index
            )

        # Layout setup
        layout = self.layout()
        # Set host
        layout.addWidget(self.label_host, 1, 0)
        layout.addWidget(self.line_edit_host, 1, 1)
        # Set port
        layout.addWidget(self.label_port, 2, 0)
        layout.addWidget(self.line_edit_port, 2, 1)
        # Set API type
        layout.addWidget(self.label_api_type, 3, 0)
        layout.addWidget(self.combobox_api_type, 3, 1)
        # Set CAMELS API functions
        layout.addWidget(self.label_camels_api_functions, 4, 0)
        layout.addWidget(self.combobox_camels_api_functions, 4, 1)
        # Set Generic API URL
        layout.addWidget(self.label_api_url, 5, 0)
        layout.addWidget(self.line_edit_api_url, 5, 1)
        # Set genereic API HTTP method
        layout.addWidget(self.label_generic_api_method, 6, 0)
        layout.addWidget(self.combobox_generic_api_method, 6, 1)
        # Set CAMELS parameter layout
        camels_function_parameter_widget = QWidget()
        camels_function_parameter_widget.setLayout(self.CAMELS_functions_layout)
        layout.addWidget(camels_function_parameter_widget, 7, 0, 1, 2)

        # Set post body
        layout.addWidget(self.label_message_body, 12, 0)
        layout.addWidget(self.text_edit_message_body, 12, 1)

        # Set authentication type
        layout.addWidget(self.label_authentication_type, 20, 0)
        layout.addWidget(self.combobox_authentication_type, 20, 1)
        self.combobox_authentication_type.setToolTip(
            "For HTTP Basic Authentication, use the format 'username:password'.\nFor Bearer Token Authentication, use the format: Token."
        )
        # Set authentication string
        layout.addWidget(self.label_authentication_string, 21, 0)
        layout.addWidget(self.line_edit_authentication_string, 21, 1)

        # Set the saved API type to the combobox
        self.combobox_api_type.setCurrentText(self.loop_step.api_type)
        self.combobox_api_type.currentIndexChanged.emit(
            self.combobox_api_type.currentIndex()
        )
        # Set the saved HTTP method to the combobox
        self.combobox_generic_api_method.setCurrentIndex(
            self.combobox_generic_api_method.findText(self.loop_step.generic_api_method)
        )

    def update_api_url(self):
        """
        Update the API URL.
        """
        self.loop_step.api_url = self.line_edit_api_url.text()

    def update_host(self):
        """
        Update the host address.
        """
        self.loop_step.host = self.line_edit_host.text()

    def update_port(self):
        """
        Update the port.
        """
        self.loop_step.port = self.line_edit_port.text()

    def update_message_body(self):
        """
        Update the post body. Keeps the formatting."""
        self.loop_step.message_body = self.text_edit_message_body.toPlainText()

    def update_authentication_string(self):
        """
        Update the authentication string.
        """
        self.loop_step.authentication_string = (
            self.line_edit_authentication_string.text()
        )

    def update_generic_api_method(self):
        """ """
        self.loop_step.generic_api_method = (
            self.combobox_generic_api_method.currentText()
        )
        if self.loop_step.generic_api_method in {"GET", "DELETE"}:
            self.label_message_body.setVisible(False)
            self.text_edit_message_body.setVisible(False)
        elif self.loop_step.generic_api_method in {"POST", "PATCH", "PUT"}:
            self.label_message_body.setVisible(True)
            self.text_edit_message_body.setVisible(True)

    def api_type_changed(self):
        """ """
        self.loop_step.api_type = self.combobox_api_type.currentText()
        if self.loop_step.api_type == "CAMELS":
            self.label_camels_api_functions.setVisible(True)
            self.combobox_camels_api_functions.setVisible(True)
            self.label_api_url.setVisible(False)
            self.line_edit_api_url.setVisible(False)
            self.label_generic_api_method.setVisible(False)
            self.combobox_generic_api_method.setVisible(False)

            # Set authentication type and hide it
            self.combobox_authentication_type.setCurrentText("Bearer Token")
            self.label_authentication_type.setVisible(False)
            self.combobox_authentication_type.setVisible(False)

            if self.loop_step.host and self.loop_step.port:
                self.extract_all_api_functionality_from_json()
            if self.loop_step.selected_camels_function_index is not None:
                self.load_camels_function_on_bootup(
                    self.loop_step.selected_camels_function_index
                )

        elif self.loop_step.api_type == "Generic":
            self.label_authentication_type.setVisible(True)
            self.combobox_authentication_type.setVisible(True)
            self.label_api_url.setVisible(True)
            self.line_edit_api_url.setVisible(True)
            self.label_generic_api_method.setVisible(True)
            self.combobox_generic_api_method.setVisible(True)
            # emit signal of the combobox to update the method
            self.combobox_generic_api_method.setCurrentIndex(
                self.combobox_generic_api_method.findText(self.loop_step.generic_api_method)
            )
            self.combobox_camels_api_functions.setVisible(False)
            self.label_camels_api_functions.setVisible(False)
            if self.combobox_camels_api_functions is not None:
                # Temporarily disconnect the signal
                self.combobox_camels_api_functions.currentIndexChanged.disconnect(
                    self.update_camels_function_parameters
                )
                # Clear the combobox
                self.combobox_camels_api_functions.clear()
                # Reconnect the signal
                self.combobox_camels_api_functions.currentIndexChanged.connect(
                    self.update_camels_function_parameters
                )

                # Hide camels function parameters
                for i in reversed(range(self.CAMELS_functions_layout.count())):
                    self.CAMELS_functions_layout.itemAt(i).widget().setParent(None)

    def authentication_type_changed(self):
        """ """
        self.loop_step.authentication_type = (
            self.combobox_authentication_type.currentText()
        )

    def extract_all_api_functionality_from_json(self):
        """ """
        # Make the API call to get the OpenAPI schema
        host = self.loop_step.host
        port = self.loop_step.port
        try:
            json_response = requests.get(f"http://{host}:{port}/openapi.json")
        except requests.exceptions.ConnectionError as e:
            print(
                "Could not connect to the server.\nMake sure the server is running and that the host and port are correct."
            )
            self.combobox_camels_api_functions.clear()
            self.combobox_camels_api_functions.addItem(
                "Could not connect to the server."
            )
            return
        # Parse the JSON response
        openapi_schema = json.loads(json_response.text)
        paths = openapi_schema.get("paths", {})
        # Extract the function names and descriptions
        api_functions = []
        for path, methods in paths.items():
            for method, details in methods.items():
                summary = details.get("summary", "No summary available")
                operation_id = details.get("operationId", "Unnamed function")
                description = details.get("description", "No description available")
                parameters = details.get("parameters", [])
                api_functions.append(
                    {
                        "summary": summary,
                        "method": method.upper(),
                        "path": path,
                        "operation_id": operation_id,
                        "description": description,
                        "parameters": parameters,
                    }
                )
        self.api_functions_list = api_functions
        # Update the combobox with the API functions
        # Temporarily disconnect the signal
        self.combobox_camels_api_functions.currentIndexChanged.disconnect(
            self.update_camels_function_parameters
        )
        # Clear the combobox
        self.combobox_camels_api_functions.clear()
        for func in api_functions:
            self.combobox_camels_api_functions.addItem(func["summary"])
            index = self.combobox_camels_api_functions.count() - 1
            self.combobox_camels_api_functions.setItemData(
                index, func["description"], Qt.ToolTipRole
            )
        # Reconnect the signal
        self.combobox_camels_api_functions.currentIndexChanged.connect(
            self.update_camels_function_parameters
        )
        if self.loop_step.selected_camels_function_index is not None:
            self.combobox_camels_api_functions.setCurrentIndex(
                int(self.loop_step.selected_camels_function_index)
            )
            selected_function = self.api_functions_list[
                self.loop_step.selected_camels_function_index
            ]
            if selected_function["parameters"]:
                # clear the layout
                for i in reversed(range(self.CAMELS_functions_layout.count())):
                    self.CAMELS_functions_layout.itemAt(i).widget().setParent(None)
                self.CAMELS_functions_layout.addWidget(QLabel("Parameters:"), 0, 0)
                self.CAMELS_functions_layout.addWidget(QLabel("Value:"), 0, 1)
                self.camels_function_parameters = {}
                for i, parameter in enumerate(selected_function["parameters"]):
                    self.CAMELS_functions_layout.addWidget(
                        QLabel(parameter["name"]), i + 1, 0
                    )
                    line_edit_parameter = QLineEdit()
                    self.CAMELS_functions_layout.addWidget(
                        line_edit_parameter, i + 1, 1
                    )
                    # match the parameter name with the value
                    if self.loop_step.camels_function_parameters is not None and self.loop_step.camels_function_parameters != 'None':
                        for (
                            parameter_name,
                            value,
                        ) in self.loop_step.camels_function_parameters.items():
                            if parameter_name == parameter["name"]:
                                line_edit_parameter.setText(value)
                    line_edit_parameter.textChanged.connect(
                        lambda text, param_name=parameter[
                            "name"
                        ]: self.update_parameter_value(param_name, text)
                    )

    def update_camels_function_parameters(self, index=None):
        """ """
        selected_index = self.combobox_camels_api_functions.currentIndex()
        if index is not None:
            selected_index = index
        if len(self.api_functions_list) == 0:
            return
        selected_function = self.api_functions_list[selected_index]
        if selected_function["method"] == "GET":
            self.label_message_body.setVisible(False)
            self.text_edit_message_body.setVisible(False)
        elif selected_function["method"] == "POST":
            self.label_message_body.setVisible(True)
            self.text_edit_message_body.setVisible(True)
        if selected_function["parameters"]:
            # clear the layout
            for i in reversed(range(self.CAMELS_functions_layout.count())):
                self.CAMELS_functions_layout.itemAt(i).widget().setParent(None)
            self.CAMELS_functions_layout.addWidget(QLabel("Parameters:"), 0, 0)
            self.CAMELS_functions_layout.addWidget(QLabel("Value:"), 0, 1)
            self.camels_function_parameters = {}
            for i, parameter in enumerate(selected_function["parameters"]):
                self.CAMELS_functions_layout.addWidget(
                    QLabel(parameter["name"]), i + 1, 0
                )
                line_edit_parameter = QLineEdit()
                self.CAMELS_functions_layout.addWidget(line_edit_parameter, i + 1, 1)
                line_edit_parameter.textChanged.connect(
                    lambda text, param_name=parameter[
                        "name"
                    ]: self.update_parameter_value(param_name, text)
                )
        else:
            # clear the layout
            for i in reversed(range(self.CAMELS_functions_layout.count())):
                self.CAMELS_functions_layout.itemAt(i).widget().setParent(None)
        self.loop_step.selected_camels_function_index = (
            self.combobox_camels_api_functions.currentIndex()
        )

    def load_camels_function_on_bootup(self, index):
        """ """
        self.extract_all_api_functionality_from_json()
        self.combobox_camels_api_functions.setCurrentIndex(index)
        try:
            self.update_camels_function_parameters(index)
        except KeyError as e:
            print(
                "Could not load the CAMELS function. Check your connection to the server."
            )
        if self.loop_step.camels_function_parameters is not None or self.loop_step.camels_function_parameters != 'None':
            for (
                parameter_name,
                value,
            ) in self.loop_step.camels_function_parameters.items():
                for i in range(self.CAMELS_functions_layout.count()):
                    if (
                        self.CAMELS_functions_layout.itemAt(i).widget().text()
                        == parameter_name
                    ):
                        self.CAMELS_functions_layout.itemAt(i + 1).widget().setText(
                            value
                        )

    def update_parameter_value(self, parameter_name, value):
        """ """
        self.camels_function_parameters[parameter_name] = value
        self.loop_step.camels_function_parameters = self.camels_function_parameters


class Combobox_CAMELS_functions(QComboBox):
    popupAboutToBeShown = Signal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super().showPopup()
