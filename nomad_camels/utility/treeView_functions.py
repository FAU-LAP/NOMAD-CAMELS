def getItemIndex(item_model, data: str, starts_with=False):
    """Iteration over the item_model to return the index of an item with
    given data.

    Parameters
    ----------
    item_model : QStandardItemModel
        the searched item_model
    data : str
        the data which the looked-for item has
    starts_with : bool, default False
        also return an item, if it only starts with the searched data (Default value = False)
    data:str :


    Returns
    -------


    """
    rows = item_model.rowCount()
    cols = item_model.columnCount()
    for r in range(rows):
        for c in range(cols):
            item = item_model.item(r, c)
            if item is None:
                continue
            tester = (
                item.data().startswith(data) if starts_with else item.data() == data
            )
            if tester:
                return item.index()
            if item.hasChildren():
                found, ind = iterItem(item, data, starts_with)
                if found:
                    return ind
    return None


def iterItem(item, data, startWith=False):
    """Iteration over the children of the given item to return the index
    of an item with given data. Called by getItemIndex.
    Runs recursively, if the children-items also have children.

    Parameters
    ----------
    item : QStandardItem
        item whose children are iterated over
    data : str
        the data which the looked-for item has
    startWith : bool, default False
        also return an item, if it only starts with the searched data (Default value = False)

    Returns
    -------


    """
    rows = item.rowCount()
    cols = item.columnCount()
    found = False
    ind = None
    for r in range(rows):
        if found:
            break
        for c in range(cols):
            if found:
                break
            child = item.child(r, c)
            if child is None:
                continue
            tester = (
                child.data().startswith(data) if startWith else child.data() == data
            )
            if tester:
                return True, child.index()
            if child.hasChildren():
                found, ind = iterItem(child, data)
    return found, ind


def get_substeps(parent):
    """Helper function, to get the substeps of loop_step with children.

    Parameters
    ----------
    parent :


    Returns
    -------

    """
    steps = []
    for i in range(parent.rowCount()):
        item = parent.child(i, 0)
        substeps = get_substeps(item)
        steps.append((item.data(), substeps))
    return steps
