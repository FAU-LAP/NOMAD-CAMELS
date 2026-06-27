SEMANTIC_NONE_LABEL = "None"
SEMANTIC_NONE_IRI = ""

SEMANTIC_COMBOBOX_STYLESHEET = """
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


def apply_semantic_combobox_style(combo):
    """Apply the standard style for semantic-mapping combo boxes."""
    combo.setStyleSheet(SEMANTIC_COMBOBOX_STYLESHEET)