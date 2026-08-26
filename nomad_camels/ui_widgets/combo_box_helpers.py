from PySide6.QtCore import Qt

SEMANTIC_NONE_LABEL = "None"
SEMANTIC_NONE_IRI = ""


def normalize_semantic_options(options):
    """Normalizes a list of semantic options - each a 3-tuple (label, iri,
    description), a 2-tuple (label, iri), or a bare label - into a list of
    (label, iri, description) tuples, with the "None" sentinel prepended so
    users can clear a selection."""
    normalized = [(SEMANTIC_NONE_LABEL, SEMANTIC_NONE_IRI, "")]
    for option in options:
        if isinstance(option, tuple):
            if len(option) == 3:
                label, iri, description = option
            else:
                label, iri = option
                description = ""
        else:
            label, iri, description = option, "", ""
        if label:
            normalized.append((label, iri, description))
    return normalized


def populate_semantic_combo(combo, options, selected_iri=""):
    """Fills `combo` with the normalized form of `options` (each item's
    description becomes its tooltip) and selects the item matching
    `selected_iri`, if any. Returns the normalized options list."""
    normalized = normalize_semantic_options(options)
    for label, iri, description in normalized:
        combo.addItem(label, iri)
        if description:
            combo.setItemData(combo.count() - 1, description, Qt.ToolTipRole)
    selected_index = 0
    if selected_iri:
        for index, (_label, iri, _description) in enumerate(normalized):
            if iri == selected_iri:
                selected_index = index
                break
    combo.setCurrentIndex(selected_index)
    return normalized


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