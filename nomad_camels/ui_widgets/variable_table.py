from PySide6.QtWidgets import QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from nomad_camels.utility import variables_handling


class VariableTable(QTableView):
    """ """

    def __init__(self, parent=None, protocol=None, editable_names=True):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Name", "Value", "Data-Type"])
        self.model.itemChanged.connect(self.check_variable)
        self.editable_names = editable_names
        self.protocol = protocol
        if protocol:
            self.set_protocol(protocol)

    def set_protocol(self, protocol):
        """ """
        self.protocol = protocol
        for var in sorted(self.protocol.variables):
            self.append_variable(var, str(self.protocol.variables[var]))

    def append_variable(self, name="name", value="value"):
        """ """
        name = self.get_unique_name(name)
        name_item = QStandardItem(name)
        value_item = QStandardItem(value)
        type_item = QStandardItem(variables_handling.check_data_type(value))
        name_item.setEditable(self.editable_names)
        type_item.setEditable(False)
        self.model.appendRow([name_item, value_item, type_item])

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
            self.model.item(ind.row(), 2).setText(d_type)
        self.update_variables()

    def update_variables(self):
        """ """
        self.protocol.variables = {}
        for i in range(self.model.rowCount()):
            name = self.model.item(i, 0).text()
            value = variables_handling.get_data(self.model.item(i, 1).text())
            self.protocol.variables.update({name: value})
        variables_handling.protocol_variables = self.protocol.variables

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
