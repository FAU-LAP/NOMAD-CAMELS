from PySide6.QtWidgets import QComboBox


class DynamicUploadComboBox(QComboBox):
    def showPopup(self):
        # Call your custom function to update items.
        self.refreshItems()
        # Now call the base class's showPopup() to display the drop-down.
        super().showPopup()

    def refreshItems(self):
        # Example: Clear the combo box and add dynamic items.
        self.clear()

        # Generate new items dynamically.
        # For example, this list could be the result of a query or other dynamic process.
        dynamic_items = self.getDynamicItems()

        for item in dynamic_items:
            self.addItem(item)

    def getDynamicItems(self):
        """This is a placeholder function that should be overridden in a subclass.
        Must return a iterable list of items to be displayed in the combo box.
        """
        raise NotImplementedError("Subclasses must implement this method.")
