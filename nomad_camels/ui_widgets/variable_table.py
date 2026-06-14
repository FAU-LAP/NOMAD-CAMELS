from PySide6.QtWidgets import QTableView, QWidget, QVBoxLayout, QPushButton, QComboBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPainter, QColor, QIcon
from PySide6.QtCore import Qt, Signal
from nomad_camels.utility import variables_handling
from nomad_camels.utility.ontology_helper import get_physical_quantities

from importlib import resources
from nomad_camels import graphics


class VariableTable(QTableView):
    """ """

    def __init__(self, parent=None, protocol=None, editable_names=True, variables=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Name", "Value", "Semantics", "Data-Type"])
        self.model.itemChanged.connect(self.check_variable)
        self.editable_names = editable_names
        self.protocol = protocol
        self.variables = variables
        if protocol:
            self.set_protocol(protocol)
        elif variables:
            for var in sorted(variables):
                self.append_variable(var, str(variables[var]), unique=False)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.model.rowCount() == 0:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(128, 128, 128))  # Gray color

            # Set font to be larger and bold
            font = self.font()
            font.setPointSize(font.pointSize() + 2)  # Make font larger
            font.setBold(True)
            painter.setFont(font)

            rect = self.viewport().rect()
            painter.drawText(rect, Qt.AlignCenter, "Define your variables here.")

    def set_protocol(self, protocol):
        """ """
        self.protocol = protocol
        for var in sorted(self.protocol.variables):
            self.append_variable(var, str(self.protocol.variables[var]), unique=False)

    def append_variable(self, name="name", value="value", unique=True):
        """ """
        if unique:
            name = self.get_unique_name(name)
        name_item = QStandardItem(name)
        value_item = QStandardItem(value)
        semantic_item = QStandardItem("")
        type_item = QStandardItem(variables_handling.check_data_type(value))
        name_item.setEditable(self.editable_names)
        semantic_item.setEditable(False)
        type_item.setEditable(False)
        self.model.appendRow([name_item, value_item, semantic_item, type_item])
        row = self.model.rowCount() - 1
        combo = self.make_semantics_combo(name)
        self.setIndexWidget(self.model.index(row, 2), combo)

    def check_variable(self):
        """ """
        ind = self.selectedIndexes()
        if ind:
            ind = ind[0]
        else:
            return
        item = self.model.itemFromIndex(ind)
        if ind.column() == 0:
            variables_handling.check_variable_name(item.text(), parent=self)
        if ind.column() == 0 and item.text() in self.protocol.variables:
            new_name = self.get_unique_name(item.text())
            item.setText(new_name)
            raise Exception("Variable names must be unique!")
        if ind.column() == 1:
            d_type = variables_handling.check_data_type(item.text())
            self.model.item(ind.row(), 3).setText(d_type)
        self.update_variables()

    def update_variables(self):
        """Update protocol variables and variable semantic annotations."""
        variables = {}
        variable_semantics = {}
        variable_semantic_iris = {}
        for row in range(self.model.rowCount()):
            name_item = self.model.item(row, 0)
            value_item = self.model.item(row, 1)
            if name_item is None or value_item is None:
                continue
            name = name_item.text()
            value = variables_handling.get_data(value_item.text())
            variables[name] = value
            combo = self.indexWidget(self.model.index(row, 2))
            if combo is not None and combo.currentIndex() >= 0:
                label = combo.currentText()
                iri = combo.currentData() or ""
                if label:
                    variable_semantics[name] = label
                    variable_semantic_iris[name] = iri
        if self.editable_names:
            self.protocol.variables = variables
            self.protocol.variable_semantics = variable_semantics
            self.protocol.variable_semantic_iris = variable_semantic_iris
            variables_handling.protocol_variables = self.protocol.variables
        else:
            return variables

    def get_unique_name(self, name="name"):
        """ """
        i = 1
        while name in self.protocol.variables:
            if "_" not in name:
                name += f"_{i}"
            else:
                name = f'{name.split("_")[0]}_{i}'
            i += 1
        return name
    
    def get_semantic_options(self):
        """Return physical quantity options for the selected experiment.
        Returns a list of (label, iri) tuples.
        If no experiment is selected, an empty list is returned.
        """
        if self.protocol is None:
            return []
        experiment_class = getattr(
            self.protocol,
            "experiment_ontology_class",
            "",
        )
        if not experiment_class:
            return []
        return get_physical_quantities(class_name=experiment_class) or []
    
    def make_semantics_combo(self, variable_name):
        """Create the semantics dropdown for one variable row."""
        combo = QComboBox(self)
        combo.setStyleSheet(
            """
            QComboBox {
                background-color: white;
                color: black;
            }
            QComboBox:disabled {
                background-color: white;
                color: gray;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #d6eaff;
                selection-color: black;
            }
            """
        )
        options = self.get_semantic_options()
        for label, iri in options:
            combo.addItem(label, iri)
        semantic_iri = ""
        if self.protocol is not None:
            semantic_iri = getattr(
                self.protocol,
                "variable_semantic_iris",
                {},
            ).get(variable_name, "")
        selected_index = -1
        if semantic_iri:
            for index, (_label, iri) in enumerate(options):
                if iri == semantic_iri:
                    selected_index = index
                    break
        combo.setCurrentIndex(selected_index)
        combo.setEnabled(bool(options))
        combo.currentTextChanged.connect(self.update_variables)
        return combo
    
    def refresh_semantic_options(self):
        """Refresh all semantics dropdowns after the selected experiment changed."""
        for row in range(self.model.rowCount()):
            name_item = self.model.item(row, 0)
            if name_item is None:
                continue
            variable_name = name_item.text()
            new_combo = self.make_semantics_combo(variable_name)
            self.setIndexWidget(self.model.index(row, 2), new_combo)
        self.update_variables()

    def clear(self):
        """ """
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Name", "Value", "Semantics", "Data-Type"])
        self.model.itemChanged.connect(self.check_variable)
        self.update_variables()


class VariableBox(QWidget):
    new_values_signal = Signal(dict)
    closing = Signal()

    def __init__(
        self, parent=None, protocol=None, editable_names=True, variables=None, name=""
    ):
        super().__init__(parent)
        name = name or (protocol.name if protocol else "protocol")
        self.setWindowTitle(f"Live variable control - {name} - NOMAD CAMELS")
        self.setWindowIcon(QIcon(str(resources.files(graphics) / "CAMELS_Icon.png")))
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.table = VariableTable(
            protocol=protocol,
            editable_names=editable_names,
            parent=self,
            variables=variables,
        )
        self.layout.addWidget(self.table)
        self.button = QPushButton("update values")
        self.button.clicked.connect(self.update_values)
        self.layout.addWidget(self.button)
        # Disable the close button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

    def update_values(self):
        variables = self.table.update_variables()
        self.new_values_signal.emit(variables)
        return variables

    def closeEvent(self, event):
        # Emit the closing signal
        self.closing.emit()
        # Accept the event to close the window
        event.accept()
