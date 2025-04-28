from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget, QWidgetAction
from PySide6.QtCore import Qt
import re

# from PySide6.QtGui import QStandardItem

from nomad_camels.utility import variables_handling


# class VariableItem(QStandardItem):
#     def __init__(self, value=None):
#         super().__init__(value)
#         self.setToolTip('test')


def check_no_special_characters(string):
    """
    Check if string is free of special characters.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the string is valid (no special characters), False otherwise.
    """
    return re.search(r"[^\w\s]", str(string)) is None


class Variable_Box(QLineEdit):
    """QLineEdit that checks its contents for validity and then color-
    codes the background.

    Parameters
    ----------

    Returns
    -------

    """

    def __init__(
        self,
        parent=None,
        check_function=None,
        provide_context_menu=True,
        make_green=True,
    ):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)
        self.textChanged.connect(self.check_string)
        self.check_function = check_function
        self.provide_context_menu = provide_context_menu
        self.make_green = make_green
        self.check_string()

    def set_check_function(
        self, check_function, make_green=False, tooltip=None, provide_context_menu=False
    ):
        """Set the check function for the variable box.

        Parameters
        ----------
        check_function : callable
            The function to use for checking the validity of the input.
        make_green : bool, optional
            If True, the background will be set to green if the input is valid.
        tooltip : str, optional
            The tooltip text to display when hovering over the box.
        provide_context_menu : bool, optional
            If False, the context menu with variables and channels will be suppressed.

        Returns
        -------
        None

        """
        self.check_function = check_function
        self.make_green = make_green
        if tooltip is not None:
            self.setToolTip(tooltip)
        self.provide_context_menu = provide_context_menu
        if not provide_context_menu:
            self.setContextMenuPolicy(Qt.DefaultContextMenu)
        else:
            self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.check_string()

    def setEnabled(self, a0: bool) -> None:
        """

        Parameters
        ----------
        a0: bool :


        Returns
        -------

        """
        if a0:
            self.check_string()
        else:
            self.setStyleSheet("")
        super().setEnabled(a0)

    def check_string(self):
        """Check the string and then set the corresponding background-color."""
        check_function = (
            self.check_function
            if self.check_function
            else variables_handling.check_eval
        )
        if not self.text():
            self.setStyleSheet(
                f'background-color: rgb{variables_handling.get_color("white", True)}'
            )
        elif check_function(self.text()):
            color = "green" if self.make_green else "white"
            self.setStyleSheet(
                f"background-color: rgb{variables_handling.get_color(color, True)}"
            )
        else:
            self.setStyleSheet(
                f'background-color: rgb{variables_handling.get_color("red", True)}'
            )

    def get_value(self):
        """ """
        return variables_handling.get_eval(self.text())

    def context_menu(self, pos):
        """Generates the right-click-menu.
        There are entries for inserting (replace) and appending the
        variables, channels, functions and operators.

        Parameters
        ----------
        pos :


        Returns
        -------

        """
        if not self.provide_context_menu:
            # super().contextMenuEvent(pos)
            return
        menu = self.createStandardContextMenu()
        search_bar = QLineEdit(menu)
        search_bar.setPlaceholderText("Search...")
        # Setting up layout for the menu
        layout = QVBoxLayout()
        layout.addWidget(search_bar)
        container = QWidget()
        container.setLayout(layout)

        # Adding the container widget to the menu
        action = QWidgetAction(menu)
        action.setDefaultWidget(container)
        menu.insertAction(menu.actions()[0], action)
        # putting the returned actions somewhere is necessary, otherwise
        # there will be none inside the single menus
        (self.channel_menu, self.variable_menu, self.function_menu), _ = (
            variables_handling.get_menus(self.insert_variable)
        )
        first_act = menu.actions()[1]
        menu.insertMenu(first_act, self.channel_menu)
        menu.insertMenu(first_act, self.variable_menu)
        menu.insertMenu(first_act, self.function_menu)
        # menu.insertMenu(first_act, operator_menu)
        menu.insertSeparator(first_act)
        (
            self.channel_menu2,
            self.variable_menu2,
            self.operator_menu2,
            self.function_menu2,
        ), __ = variables_handling.get_menus(self.append_variable, "Append")
        menu.insertMenu(first_act, self.channel_menu2)
        menu.insertMenu(first_act, self.variable_menu2)
        menu.insertMenu(first_act, self.function_menu2)
        menu.insertMenu(first_act, self.operator_menu2)
        menu.insertSeparator(first_act)

        search_bar.textChanged.connect(self.filter_actions)

        menu.exec_(self.mapToGlobal(pos))

    def filter_actions(self, query):
        for menu in [
            self.channel_menu,
            self.variable_menu,
            self.function_menu,
            self.channel_menu2,
            self.variable_menu2,
            self.function_menu2,
        ]:
            if not any(
                query.lower() in action.text().lower() for action in menu.actions()
            ):
                menu.setEnabled(False)
                continue
            elif not menu.isEnabled():
                menu.setEnabled(True)
            for action in menu.actions():
                action.setVisible(query.lower() in action.text().lower())

    def append_variable(self, variable):
        """Used for the single actions of the context menu.

        Parameters
        ----------
        variable :


        Returns
        -------

        """
        self.setText(self.text() + f"{variable}")

    def insert_variable(self, variable):
        """Used for the single actions of the context menu.

        Parameters
        ----------
        variable :


        Returns
        -------

        """
        self.setText(f"{variable}")
