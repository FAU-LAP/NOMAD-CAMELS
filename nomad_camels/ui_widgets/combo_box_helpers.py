SEMANTIC_NONE_LABEL = "None"
SEMANTIC_NONE_IRI = ""


def apply_table_cell_combobox_style(combo):
    """Style an embedded combo box using the active Qt/CAMELS palette."""
    combo.setStyleSheet(
        """
        QComboBox {
            background-color: palette(base);
            color: palette(text);
        }
        QComboBox QAbstractItemView {
            background-color: palette(base);
            color: palette(text);
            selection-background-color: palette(highlight);
            selection-color: palette(highlighted-text);
        }
        """
    )